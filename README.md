# cargotree2mermaid.py
Convert file created by 'cargo tree' to mermaid-format file.

# mermaid_level_nodes.py
Give the dependency info of the node in mermaid-format file.

# run
```
./cargotree2mermaid.py -h
usage: cargotree2mermaid.py [-h] [-i INPUT] [-b BLACKLIST] [-o OUTPUT] [-w WHITE]
                            [--direction {TD,TB,LR,RL,BT}]

Convert cargo tree output to a Mermaid dependency graph

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path to cargo tree output file
  -b BLACKLIST, --blacklist BLACKLIST
                        Blacklist file path; crate names separated by commas or whitespace
  -o OUTPUT, --output OUTPUT
                        Mermaid output file path; print to screen if not provided
  -w WHITE, --white WHITE
                        Whitelist output file path; crates in cargo tree but not in blacklist
  --direction {TD,TB,LR,RL,BT}
                        Mermaid graph direction


./cargotree2mermaid.py -i ./example/crates-dep.txt -b ./example/blacklist.txt -o ./example/crates-dep.mmd -w ./example/whitelist.txt
# You can check the mermaid file ./example/crates-dep.mmd and whitelist file ./example/whitelist.txt
# If -o is not provided, mermaid output will be printed to screen

# build png from mmd
mmdc -s 4 -i crates-dep.mmd -o crates-dep.png
#if no mmdc, install it: npm install -g @mermaid-js/mermaid-cli

#show png file
feh crates-dep.png
#if no feh, install it: sudo apt install feh -y


./mermaid_level_nodes.py -h
usage: mermaid_level_nodes.py [-h] -i INPUT -n LEVEL (-u | -d) [-o OUTPUT]

Extract node list at a specific dependency level from Mermaid graph

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Mermaid dependency graph file path
  -n LEVEL, --level LEVEL
                        Dependency level (NUM >= 0)
  -u, --up              Upward dependency level (default direction)
  -d, --down            Downward dependency level (reversed direction)
  -o OUTPUT, --output OUTPUT
                        Output file path; print to screen if not provided

./mermaid_level_nodes.py -i ./example/crates-dep.mmd -n 2 -u
# Output file defaults to ./example/crates-dep.up.level2.txt
# Each line format: crate  :   dep1, dep2
# If -o is not provided, output will be printed to screen

./mermaid_level_nodes.py -i ./example/crates-dep.mmd -n 2 -d
# Output file defaults to ./example/crates-dep.down.level2.txt
# Each line format: crate  :   dep1, dep2
# If -o is not provided, output will be printed to screen
```
# example

```
# Produce crates-dep.txt is from https://github.com/Starry-OS/StarryOS
# setup rust/c development env for rust os, rust/c app...

git clone git@github.com:Starry-OS/StarryOS.git
cd StarryOS
cargo tree >crates-dep.txt

# use cargotree2mermaid.py -i SOME-PATH/crates-dep.txt ...
```

The crates-dep.txt is from https://github.com/arceos-org/arceos-apps

```
git clone git@github.com:arceos-org/arceos-apps.git
cd arceos-apps
# setup development env ...

# riscv64 helloworld
cargo tree -p arceos-helloworld --target riscv64gc-unknown-none-elf --features "axstd/defplat axstd/log-level-info" >crates-dep.txt

# aarch64 helloworld
cargo tree -p arceos-helloworld --target aarch64-unknown-none-softfloat --features "axstd/defplat axstd/log-level-info" >crates-dep.txt

#x86_64 helloworld
cargo tree -p arceos-helloworld --target x86_64-unknown-none --features "axstd/defplat axstd/log-level-info" >crates-dep.txt

#loongarch64 helloworld
cargo tree -p arceos-helloworld --target loongarch64-unknown-none-softfloat --features "axstd/defplat axstd/log-level-info" >crates-dep.txt

# use cargotree2mermaid.py -i SOME-PATH/crates-dep.txt ...
```

## NOTICE
The crates in blacklist.txt(as input file for cargotree2mermaid.py) are not from github repos: rcore-os, arceos-org, Starry-OS, arceos-hypervisor, etc.

The crates in output file(e.g. whitelist.txt) for cargotree2mermaid.py are from  github repos: rcore-os, arceos-org, Starry-OS, arceos-hypervisor, etc.