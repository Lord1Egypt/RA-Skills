# QuakeSearchskill Scripts

## 1. Files

- `quake_batch_cli.py`: Quake 批量查询与导出脚本（交互 + 无交互）

## 2. Binary placement

将 Quake 官方二进制放到本目录（至少一个）：

- `quake.exe`（Windows）
- `quake_for_Apple`（macOS）
- `quake_for_Linux`（Linux）

脚本会自动按系统选择；也可以 `--quake-bin` 手动指定。

## 3. Quick start

```bash
python3 quake_batch_cli.py
```

无交互示例：

```bash
python3 quake_batch_cli.py --no-interactive --mode search --key "$QUAKE_API_KEY" --query 'ip: "118.114.241.191" AND port: "21008"' --fields "ip,port,title,country,province,city,time" --page-size 10 --max-records 50 --output-csv result.csv --output-raw result_raw.txt
```
