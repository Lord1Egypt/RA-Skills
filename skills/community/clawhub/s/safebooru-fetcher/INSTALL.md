# Installation / 安装说明

## Dependencies / 依赖

- **Python 3.9+**
- Install python deps:
  ```bash
  pip3 install -r requirements.txt
  ```

## Usage

This version uses the **DAPI**:
- Makes HTTPS requests to `https://safebooru.org`
- Writes image files to `./downloads`

## Quick test

```bash
python3 safebooru.py "cat_girl" 2 --sort random
python3 safebooru.py --suggest genshin
```
