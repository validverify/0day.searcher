# 0day.searcher

Simple and comfortable to use search from [0day today](https://0day.today/) website.

## Installation

1. Install python
2. Install modules(pip):
```bash
pip install -r request.txt
```

## Usage

```bash
python 0day-searcher.py -flag1 -flag2=something YOUR QUERY HERE
```
### Flags

**-h** - Show help message and exit.
**-c** - Print results WITHOUT colors.
**-CVE=CVE-Year-Number** - Filter with CVE.
**-O=FILE_NAME.extension** - Write all output to file.

## Results structure

> **date** / **name** / **link** / **platform** / **risk** / **download** INFO: **CVE** / **verify** / **author**

date - Date of creation.

name - Name and small description of exploit.

link - Link to exploit(Need to add befor: https://0day.today/).

platform - For which platform exploit created.

risk - Risk level for victim system.

download - Link to download exploit(Need to add befor: https://0day.today/).

CVE - CVE id(If able).

verify - Exploit's status of verification.

author - Just author of exploit.

> [!WARNING]
> First step P.S. Specifically:
> 
> \[INFO\](0day.today) Creating session and making request...~~~.
>
> Can take a while, it's all depends on you internet speed!

                      2023 year
## Changelog
### Version 1.5
#### Bug Fix
### Version 1.0 Alpha
