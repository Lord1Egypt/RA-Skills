# RollingGo Flight UVX 参考

## 目录
- [运行方式](#运行方式)
- [版本新鲜度](#版本新鲜度)
- [API Key 设置](#api-key-设置)
- [命令说明](#命令说明)
- [工作流教程](flight-workflows.md)
- [故障排查](#故障排查)

---

## 运行方式

### 临时执行（uvx，无需安装）
```bash
uvx --refresh --from rollinggo-flight@latest rollinggo-flight --help
uvx --refresh --from rollinggo-flight@latest rollinggo-flight search-airports --keyword "Hangzhou"
```

### 安装为工具（适合重复使用）
```bash
uv tool install rollinggo-flight@latest
uv tool upgrade rollinggo-flight@latest
rollinggo-flight --help

# 如果安装后 shell 找不到命令：
uv tool update-shell
```

### 独立二进制（无需 Node.js 或 Python）

**Linux / macOS：**
```bash
curl -fsSL https://raw.githubusercontent.com/RollingGo-AI/rollinggo-flight-cli/main/scripts/install.sh | sh
rollinggo-flight --help
```

**Windows PowerShell：**
```powershell
irm https://raw.githubusercontent.com/RollingGo-AI/rollinggo-flight-cli/main/scripts/install.ps1 | iex
rollinggo-flight --help
```

安装到 `~/.local/bin`（Linux/macOS）或 `%LOCALAPPDATA%\Programs\rollinggo-flight`（Windows）。该二进制为自包含包（约 40 MB），无需额外运行时依赖。

---

## 版本新鲜度
默认策略：每次执行都确保使用 PyPI 最新版本。

```bash
uvx --refresh --from rollinggo-flight@latest rollinggo-flight <subcommand> ...
```

如果使用已安装工具，先升级：
```bash
uv tool upgrade rollinggo-flight@latest
```

---

## API Key 设置
解析顺序：`--api-key` 参数 → `ROLLINGGO_API_KEY` 环境变量。

```bash
# Bash / zsh
export ROLLINGGO_API_KEY="YOUR_API_KEY"

# PowerShell
$env:ROLLINGGO_API_KEY="YOUR_API_KEY"

# 单次命令覆盖
rollinggo-flight search-airports --api-key YOUR_API_KEY --keyword "Beijing"
```

---

## 命令说明
以下示例为了易读，统一使用已安装的 `rollinggo-flight` 命令。若要强制走最新版，对应前缀为 `uvx --refresh --from rollinggo-flight@latest rollinggo-flight`。

### `search-airports`
必填：`--keyword`

```bash
# 最小示例
rollinggo-flight search-airports --keyword "Hangzhou"

# 表格输出
rollinggo-flight search-airports --keyword "Beijing" --format table
```

可选参数：`--format json|table`

### `search-flights`
必填：`--from-date`、`--trip-type`、`--adult-number`、`--child-number`、`--cabin-grade`  
二选一必填：`--from-city` 或 `--from-airport`  
二选一必填：`--to-city` 或 `--to-airport`

```bash
# 单程，按城市代码
rollinggo-flight search-flights \
  --from-city HGH --to-city CTU \
  --from-date 2026-06-01 \
  --trip-type ONE_WAY \
  --adult-number 1 --child-number 0 \
  --cabin-grade ECONOMY

# 往返，按机场代码
rollinggo-flight search-flights \
  --from-airport PEK --to-airport PVG \
  --from-date 2026-06-01 --ret-date 2026-06-05 \
  --trip-type ROUND_TRIP \
  --adult-number 2 --child-number 0 \
  --cabin-grade BUSINESS

# 表格输出
rollinggo-flight search-flights \
  --from-city SHA --to-city BJS \
  --from-date 2026-06-01 \
  --trip-type ONE_WAY \
  --adult-number 1 --child-number 0 \
  --cabin-grade ECONOMY \
  --format table
```

可选参数：`--ret-date`、`--format json|table`

---

## 工作流教程
更完整的分步场景教程见 [flight-workflows.md](flight-workflows.md)。

---

## 故障排查
- **401 Unauthorized** → API key 缺失或无效。检查 `ROLLINGGO_API_KEY` 或显式传入 `--api-key`。
- **参数校验失败（exit 2）** → 检查必填参数，运行 `rollinggo-flight search-flights --help` 查看完整选项。
- **`flightInformationList` 为空** → 尝试放宽条件：换日期、改用城市代码、调整舱位。
- **缺少 `--ret-date` 报错** → 当 `--trip-type ROUND_TRIP` 时必须提供。
