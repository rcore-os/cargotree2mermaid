# cargotree2mermaid.py
Convert file created by 'cargo tree' to mermaid-format file.

# mermaid_level_nodes.py
Give the dependency info of the node in mermaid-format file.

# run
```
./cargotree2mermaid.py -h
usage: cargotree2mermaid.py [-h] [-i INPUT] [-b BLACKLIST] [-o OUTPUT] [-w WHITE] [--direction {TD,TB,LR,RL,BT}]
...

./cargotree2mermaid.py -i ./example/crates-dep.txt -b ./example/blacklist.txt -o ./example/crates-dep.mmd -w ./example/whitelist.txt
# You can check the mermaid file ./example/crates-dep.mmd and whitelist file ./example/whitelist.txt

./mermaid_level_nodes.py -i ./example/crates-dep.mmd -n 2 -u
# Output file defaults to ./example/crates-dep.up.level2.txt
# Each line format: crate  :   dep1, dep2

./mermaid_level_nodes.py -i ./example/crates-dep.mmd -n 2 -d
# Output file defaults to ./example/crates-dep.down.level2.txt
# Each line format: crate  :   dep1, dep2
```
# example
The crates-dep.txt is from https://github.com/Starry-OS/StarryOS

```
git clone git@github.com:Starry-OS/StarryOS.git
cd StarryOS
cargo tree >crates-dep.txt
```

The crates in black.list.txt are not from rcore-os, arceos-org, Starry-OS, arceos-hypervisor github repos.