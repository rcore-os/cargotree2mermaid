#!/usr/bin/env python3
import argparse
import re


TREE_LINE_RE = re.compile(
    r'^(?P<prefix>(?:│   |    )*)(?:(?:├──|└──)\s)(?P<rest>.+)$'
)
SECTION_LINE_RE = re.compile(
    r'^(?P<prefix>(?:│   |    )*)(?P<section>\[[^\]]+\])\s*$'
)


def _sanitize_node_id(label):
    node_id = re.sub(r'[^0-9A-Za-z_]', '_', label)
    if node_id and node_id[0].isdigit():
        node_id = f"n_{node_id}"
    return node_id


def _parse_line(line):
    raw = line.rstrip("\n")
    if not raw.strip():
        return None
    match = TREE_LINE_RE.match(raw)
    if match:
        depth = len(match.group("prefix")) // 4 + 1
        payload = match.group("rest").strip()
        return depth, payload

    match = SECTION_LINE_RE.match(raw)
    if match:
        depth = len(match.group("prefix")) // 4 + 1
        payload = match.group("section").strip()
        return depth, payload

    if raw.lstrip().startswith(("│", "├", "└")):
        return None

    else:
        depth = 0
        payload = raw.strip()
        return depth, payload


def _parse_node(payload):
    if payload.startswith("["):
        return {
            "id": _sanitize_node_id(payload),
            "label": payload,
            "is_crate": False,
        }
    tokens = payload.split()
    if not tokens:
        return None
    name = tokens[0]
    version = tokens[1] if len(tokens) > 1 and tokens[1].startswith("v") else None
    label = f"{name} {version}" if version else name
    return {
        "id": _sanitize_node_id(label),
        "label": label,
        "is_crate": True,
    }


def parse_cargo_tree(lines, blacklist):
    """解析Cargo依赖树，提取依赖关系"""
    stack = []  # 每一层的节点信息
    dependencies = []
    seen = set()
    nodes = {}
    crates = set()

    for line in lines:
        parsed = _parse_line(line)
        if parsed is None:
            continue
        depth, payload = parsed
        node = _parse_node(payload)
        if node is None:
            continue

        if depth <= len(stack):
            stack = stack[:depth]

        if node["is_crate"]:
            crate_name = node["label"].split()[0]
            crates.add(crate_name)
            if crate_name in blacklist:
                stack.append(node)
                continue
            parent = None
            for ancestor in reversed(stack):
                if ancestor["is_crate"]:
                    if ancestor["label"].split()[0] in blacklist:
                        continue
                    parent = ancestor
                    break
            if parent is not None:
                edge = (parent["id"], node["id"])
                if edge not in seen:
                    seen.add(edge)
                    dependencies.append(edge)

        nodes.setdefault(node["id"], node["label"])
        stack.append(node)

    return dependencies, nodes, crates

def main():
    parser = argparse.ArgumentParser(
        description="将 cargo tree 输出转换为 Mermaid 依赖图"
    )
    parser.add_argument(
        "-i",
        "--input",
        default="crates-dep.txt",
        help="cargo tree 输出文件路径",
    )
    parser.add_argument(
        "-b",
        "--blacklist",
        default=None,
        help="黑名单列表文件路径，文件内用逗号分隔 crate 名",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="dependencies.mmd",
        help="Mermaid 输出文件路径",
    )
    parser.add_argument(
        "-w",
        "--white",
        default=None,
        help="白名单输出文件路径，输出 cargo tree 中不在黑名单的 crate 名",
    )
    parser.add_argument(
        "--direction",
        default="TD",
        choices=["TD", "TB", "LR", "RL", "BT"],
        help="Mermaid 图方向",
    )
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        lines = f.readlines()

    blacklist = set()
    if args.blacklist:
        with open(args.blacklist, "r", encoding="utf-8") as f:
            content = f.read()
        items = re.split(r"[,\s]+", content.strip())
        blacklist = {item for item in items if item}

    dependencies, nodes, crates = parse_cargo_tree(lines, blacklist)

    mermaid_lines = [f"graph {args.direction}"]
    for parent, child in dependencies:
        mermaid_lines.append(
            f"    {parent}[{nodes[parent]}] --> {child}[{nodes[child]}]"
        )

    with open(args.output, "w", encoding="utf-8") as f:
        f.write("\n".join(mermaid_lines) + "\n")

    if args.white:
        whitelist = sorted(crate for crate in crates if crate not in blacklist)
        with open(args.white, "w", encoding="utf-8") as f:
            f.write("\n".join(whitelist) + "\n")

    print(f"转换完成！依赖关系图已保存为 {args.output}")

if __name__ == "__main__":
    main()
