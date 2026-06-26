---
name: quake-search-use
description: 用于调用 Quake CLI 进行资产检索、自动翻页导出 CSV/RAW。用户提到 Quake、quake.exe、quake_for_Linux、quake_for_Apple、资产测绘、批量查询、自动翻页导出等需求时优先加载本 skill。
---

# Quake Search Use

## First

- 目标是让用户输入 key 和查询参数后，自动翻页并导出结果。
- 脚本支持 `search/domain/host/info/honeypot` 五种模式。
- 自动识别系统并选择二进制：
  - Windows: `quake.exe`
  - macOS: `quake_for_Apple`
  - Linux: `quake_for_Linux`
- 可用 `--quake-bin` 手动覆盖二进制路径。
- 本 skill 可移植：整个目录复制到任意项目即可使用。

## 入口脚本

- 主脚本：`scripts/quake_batch_cli.py`
- 运行方式：
  - AI 无交互推荐：
    - `python3 scripts/quake_batch_cli.py --no-interactive --mode search --key "$QUAKE_API_KEY" --query 'app:"exchange 2010"' --fields "ip,port,title" --page-size 100 --max-records 1000 --output-csv search.csv --output-raw search_raw.txt`
  - 兼容交互：
    - `python3 scripts/quake_batch_cli.py`

## 可移植要求

- 将 Quake 官方二进制放到 `scripts/` 目录同级（至少一个）：
  - `quake.exe`
  - `quake_for_Apple`
  - `quake_for_Linux`
- 或者运行时通过 `--quake-bin` 指定绝对/相对路径。

## 参数说明

- `--mode`：`search/domain/host/info/honeypot`
- `--key`：可选，提供后先执行 `quake init <key>`
- `--quake-bin`：可选，手动指定 Quake 二进制路径
- `--query`：仅 `search` 模式需要
- `--domain`：仅 `domain` 模式需要
- `--ip`：仅 `host/honeypot` 模式需要
- `--fields`：`search/domain` 返回字段
- `--filter`：`search` 模式正则过滤（映射 quake `-f`）
- `--page-size`：每页数量（1~100）
- `--max-records`：最大导出条数
- `--output-csv`：CSV 输出文件
- `--output-raw`：RAW 输出文件
- `--no-interactive`：禁止交互输入，缺参即报错

## CSV 导出帮助

- 自定义导出字段：`search/domain` 模式使用 `--fields` 指定，字段顺序即 CSV 列顺序。
- `search` 常用字段：
  - `ip,port,title,country,province,city,owner,time,domain,ssldomain`
- `domain` 常用字段：
  - `domain,ip,port,title`
- 无交互导出示例（search）：
  - `python3 scripts/quake_batch_cli.py --no-interactive --mode search --key "$QUAKE_API_KEY" --query 'ip: "118.1XX.XX.191" AND port: "21008"' --fields "ip,port,title,country,province,city,time" --page-size 10 --max-records 50 --output-csv quake_custom.csv --output-raw quake_custom_raw.txt`
- 无交互导出示例（domain）：
  - `python3 scripts/quake_batch_cli.py --no-interactive --mode domain --key "$QUAKE_API_KEY" --domain "360.cn" --fields "ip,port,domain,title" --page-size 100 --max-records 1000 --output-csv quake_domain.csv --output-raw quake_domain_raw.txt`
- 结果为空时，CSV 仅保留表头；如需排查请查看 `--output-raw` 文件中的原始返回。

## 安全注意事项

- 不要把真实 API key 写进仓库。
- 推荐通过环境变量注入（如 `QUAKE_API_KEY`）。
- 对外分发时只提供脚本和说明，不包含你的 key。
