# cargotree2mermaid
Convert file created by 'cargo tree' to mermaid-format file.

# run
```
./cargotree2mermaid.py -h
usage: cargotree2mermaid.py [-h] [-i INPUT] [-b BLACKLIST] [-o OUTPUT] [--direction {TD,TB,LR,RL,BT}]
...

./cargotree2mermaid.py -i ./example/crates-dep.txt -b  ./example/blacklist.txt -o ./example/crates-dep.mmd
# You can check the mermaid file ./example/crates-dep.mmd