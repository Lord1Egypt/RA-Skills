# SearXNG Search CLI Onboarding

> 本文档指导 AI Agent 完成首次环境配置。按顺序执行，遇到问题时参考 Troubleshooting。

## Prerequisites | 前置条件

- Python 3.x（运行 `python3 --version` 确认）
- 网络（需克隆 SearXNG 仓库，搜索时需访问外部搜索引擎）
- 可用端口（默认 8888）

## Step 1: 检查 Python 环境

### 检测
```bash
python3 --version
```
期望输出：`Python 3.x.x`

如果不存在，尝试：
```bash
python --version
which python3 || which python
```

如果完全没有 Python，告知用户需要安装 Python 3。

## Step 2: 安装 uv

### 检测
```bash
command -v uv && uv --version
```

如果已安装，跳到 Step 3。

### 安装
```bash
# 尝试 1: curl
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# 尝试 2: wget
wget -qO- https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# 尝试 3: 如果 PATH 未生效
export PATH="$HOME/.local/bin:$PATH"
```

### 验证
```bash
uv --version
```

## Step 3: 一键安装 SearXNG

### 检测
```bash
searxng-search status
```

如果显示 `✓ 服务运行中`，跳到 Step 5。

### 安装
```bash
# 确保脚本可执行
chmod +x <skill_dir>/scripts/searxng_cli.py

# 创建 symlink（如果不存在）
which searxng-search || sudo ln -sf <skill_dir>/scripts/searxng_cli.py /usr/local/bin/searxng-search

# 设置 secret（安装时会自动生成，也可预设置）
export SEARXNG_SECRET="your-secret-key"

# 一键安装（自动完成：克隆、venv、依赖、JSON启用、limiter配置、启动）
searxng-search install
```

> **install 自动执行以下操作：**
> 1. 克隆 SearXNG 到 `~/projects/searxng`
> 2. `uv venv --clear` 创建虚拟环境
> 3. `uv pip install -r requirements.txt` 安装依赖
> 4. 启用 JSON API（修改 `settings.yml`）
> 5. 复制 `limiter.toml` 到 `/etc/searxng/`（需要 sudo 或目录已存在）
> 6. 生成 secret 并启动服务

### 验证
```bash
searxng-search status
```
期望输出：`✓ 服务运行中: http://127.0.0.1:8888`

## Step 4: 验证搜索功能

### 验证
```bash
searxng-search search "test"
```
期望输出：搜索结果列表（标题 + URL + 摘要）

```bash
curl -s -H "X-Forwarded-For: 127.0.0.1" "http://127.0.0.1:8888/search?q=test&format=json" | python3 -m json.tool | head -10
```
期望输出：有效 JSON（`"query": "test"` + `"results": [...]`）

## Onboarding 完成

以上步骤全部通过后，onboarding 完成。后续可直接使用 `searxng-search` 命令。

## Known Limitations | 已知限制

- **部分引擎不稳定**：DuckDuckGo 可能触发 CAPTCHA、Brave 可能返回 403、Startpage 可能 JSON 解析失败。这是 SearXNG 上游和各搜索引擎的外部限制，非 CLI 问题
- **首次搜索较慢**：首次请求可能需要 5-30 秒（引擎初始化、DNS 解析），后续请求会加速
- **容器环境**：在资源受限的容器中可能启动超时，推荐部署在有稳定网络出口的宿主机上

## Troubleshooting | 故障排除

| 错误 | 原因 | 解决 |
|------|------|------|
| `command not found: searxng-search` | symlink 未创建 | `sudo ln -sf <skill_dir>/scripts/searxng_cli.py /usr/local/bin/searxng-search` |
| `command not found: uv` | uv 未安装或 PATH 未生效 | Step 2 重新安装，`export PATH="$HOME/.local/bin:$PATH"` |
| `TypeError: schema of limiter.toml is invalid` | `/etc/searxng/limiter.toml` 格式错误或为空 | `sudo cp ~/projects/searxng/searx/limiter.toml /etc/searxng/limiter.toml` |
| `403 Forbidden` (API 请求) | Bot detection 拦截（缺少 `X-Forwarded-For` header） | 确保 limiter.toml 存在且格式正确（使用源码默认文件）；CLI 已内置 header 处理 |
| JSON API 返回 HTML 而非 JSON | `settings.yml` 未启用 json format | 手动检查 `~/projects/searxng/searx/settings.yml` 的 `formats` 是否包含 `- json`，或重新运行 `searxng-search install` |
| `connection refused` | 服务未启动 | `searxng-search start` |
| `启动失败` (install/start 超时) | 服务启动慢或端口被占用 | 等待 20-30s 后重试 `searxng-search status`；检查端口：`ss -tlnp | grep 8888` |
| 搜索返回空结果 | 所有引擎被封/超时 | 部分引擎被封属正常现象，尝试换关键词或指定引擎 `--engine brave` |
| `No module named 'xxx'` | venv 依赖缺失 | `rm -rf ~/projects/searxng/.venv && searxng-search install` |
| `Permission denied: /home/node/projects` | 目录无写入权限 | `sudo mkdir -p ~/projects && sudo chown $(whoami) ~/projects` |
| `pip: not found` (旧版 install) | uv venv 不自带 pip | 确保使用最新版 CLI 脚本（v1.2.0+，已改用 `uv pip install`） |
| 端口 8888 被占用 | 其他服务占用 | `SEARXNG_PORT=9999 searxng-search start` |
