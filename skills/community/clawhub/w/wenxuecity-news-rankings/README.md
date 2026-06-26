# Wenxuecity News Rankings Skill

[中文](#中文) | [English](#english)

---

## 中文

抓取并整理文学城新闻频道 https://www.wenxuecity.com/news/ 的两个 24 小时榜单：

- `24小时热点排行`
- `24小时讨论排行`

### 本地运行

```bash
# Linux/macOS
python3 scripts/fetch_rankings.py --format md
```

Windows (PowerShell):

```powershell
py scripts\fetch_rankings.py --format md
```

### 参数（常用）

- `--top N`（默认 15；`--top 0` 输出页面实际全部）
- `--format md|json`
- `--pretty`（JSON）
- `--output FILE`

---

## English

Fetch and format Wenxuecity News 24-hour rankings from https://www.wenxuecity.com/news/:

- `24小时热点排行` (24-hour hot ranking)
- `24小时讨论排行` (24-hour discussion ranking)

### Local Run

```bash
# Linux/macOS
python3 scripts/fetch_rankings.py --format md
```

Windows (PowerShell):

```powershell
py scripts\fetch_rankings.py --format md
```

### Options (common)

- `--top N` (default: 15; use `--top 0` for all available)
- `--format md|json`
- `--pretty` (JSON)
- `--output FILE`
