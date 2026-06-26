# xiaohongshu-mcp-openclaw

![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-0ea5e9)
![Status](https://img.shields.io/badge/status-ready-22c55e)
![MCP](https://img.shields.io/badge/MCP-HTTP-8b5cf6)
![Tested](https://img.shields.io/badge/tested-2026--03--16-64748b)

一个可复用的 OpenClaw Skill：基于 `xpzouying/xiaohongshu-mcp`，用于小红书关键词搜索、笔记详情、评论抓取和互动指标统计。

- Repo: `https://gitea.leapinfra.cn/GlitterCCCC/xiaohongshu-mcp-openclaw`
- Skill Name: `xiaohongshu-mcp-openclaw`
- Runtime: `mcporter` + HTTP MCP (`http://127.0.0.1:18060/mcp`)

## Compatibility

- Shell scripts: Linux / macOS
- Windows: 建议使用 WSL 或 Git Bash 运行
- 必需依赖：`bash` `python3` `mcporter` `jq`
- 可选依赖：`go` `lsof` `curl` `zip`

## Install

### Option A: 直接克隆（推荐）

```bash
git clone https://gitea.leapinfra.cn/GlitterCCCC/xiaohongshu-mcp-openclaw.git
cd xiaohongshu-mcp-openclaw
bash scripts/install_to_openclaw.sh
```

### Option B: 已有目录直接安装到 OpenClaw

```bash
bash scripts/install_to_openclaw.sh
openclaw skills info xiaohongshu-mcp-openclaw
```

默认会同时同步一份到 `~/.agents/skills/xiaohongshu-mcp-openclaw-1.0.0`（便于新会话/其他 claw 复用）。  
如需关闭该同步：`XHS_SYNC_AGENTS_SKILL=0 bash scripts/install_to_openclaw.sh`

## Quick Start

```bash
# 先做环境预检
bash scripts/preflight.sh

# 一键初始化：setup -> start -> register -> smoke -> ensure-login
bash scripts/quickstart.sh

# 试跑搜索
python3 scripts/xhs_mcp_client.py --server xiaohongshu-mcp --timeout 120000 search --keyword 防晒 --limit 3
```

`quickstart.sh` 现在只做无二维码登录检测；未登录时会明确提示下一步执行 `login_flow.sh`。

登录疑难建议先跑：

```bash
bash scripts/login_doctor.sh xiaohongshu-mcp
```

## Commands

```bash
# 环境预检（分发给新机器时强烈建议先跑）
bash scripts/preflight.sh

# 登录状态
python3 scripts/xhs_mcp_client.py --server xiaohongshu-mcp login-status

# 登录守卫（已登录直接返回，未登录给二维码信息）
python3 scripts/xhs_mcp_client.py --server xiaohongshu-mcp ensure-login

# 推荐登录入口（保存二维码 PNG 到本地并给出打开命令）
bash scripts/login_qr.sh xiaohongshu-mcp

# 不自动打开二维码窗口（仅保存文件并输出路径）
XHS_QR_AUTO_OPEN=0 bash scripts/login_qr.sh xiaohongshu-mcp

# 登录守卫精简模式（不返回完整二维码 base64）
python3 scripts/xhs_mcp_client.py --server xiaohongshu-mcp ensure-login --strip-qr-image

# 登录守卫 + 扫码后自动轮询等待（90秒）
python3 scripts/xhs_mcp_client.py --server xiaohongshu-mcp ensure-login --wait-seconds 90 --poll-interval 3

# 登录专用流程（临时 headful，登录成功后自动切回 headless）
bash scripts/login_flow.sh xiaohongshu-mcp 120

# 搜索笔记
python3 scripts/xhs_mcp_client.py --server xiaohongshu-mcp search --keyword 防晒 --limit 5

# 笔记详情
python3 scripts/xhs_mcp_client.py --server xiaohongshu-mcp detail --note-id <note_id> --xsec-token <xsec_token>

# 评论
python3 scripts/xhs_mcp_client.py --server xiaohongshu-mcp comments --note-id <note_id> --xsec-token <xsec_token> --limit 10

# 一键报告（搜索 + 详情 + 评论）
python3 scripts/xhs_mcp_client.py --server xiaohongshu-mcp report --keyword 防晒 --search-limit 5 --comment-limit 2

# 多笔记汇总
bash scripts/multi_summary.sh 防晒 5 2

# 构建分发包（默认 tar.gz + sha256）
bash scripts/build_distribution.sh

# 如需 zip 包
XHS_BUILD_ZIP=1 bash scripts/build_distribution.sh

# 安装系统级常驻（推荐，避免隔天 offline）
bash scripts/service_install.sh xiaohongshu-mcp
bash scripts/service_status.sh xiaohongshu-mcp
bash scripts/service_uninstall.sh xiaohongshu-mcp
```

## FAQ

### Q1: 需要每次都扫码登录吗？
不需要。登录态通常可复用。并且 `search/detail/comments/report` 默认会先做登录预检，未登录会直接提示先登录。

### Q2: 为什么有时返回 `fail to login`？
通常是平台风控或登录态过期。请在官方页面/APP完成人机校验后，执行：

```bash
bash scripts/login_flow.sh xiaohongshu-mcp 120
```

### Q3: 为什么链接打开是 `Sorry, This Page Isn't Available Right Now.`？
常见原因是目标笔记对当前账号不可见或临时风控，并非脚本崩溃。

### Q4: 已登录但还是会弹浏览器页面？
把服务切回无头模式：

```bash
XHS_MCP_FORCE_RESTART=1 XHS_MCP_HEADLESS=true bash scripts/start_server.sh
```

或者直接使用登录专用流程，结束后会自动切回无头模式：

```bash
bash scripts/login_flow.sh xiaohongshu-mcp 120
```

### Q5: 能一次抓多个笔记并给总结吗？
可以，直接用：

```bash
bash scripts/multi_summary.sh 防晒 5 2
```

### Q6: 为什么提示 `another login_flow is running`？
这是并发登录保护。避免多个登录流程同时改写会话。可等待当前流程结束，或确认进程不存在后手动清理锁文件再重试。

### Q7: 为什么提示 `server_offline`？我希望看到启动指引
新版 `xhs_mcp_client.py` 在服务未启动时会返回 `next_commands`，可直接执行：

```bash
bash scripts/start_server.sh
bash scripts/register.sh xiaohongshu-mcp
python3 scripts/xhs_mcp_client.py --server xiaohongshu-mcp ensure-login --wait-seconds 90
```

### Q8: Windows 能直接运行吗？
脚本默认按 Linux/macOS shell 设计。Windows 推荐 WSL/Git Bash，或直接用打包后的文件在 WSL 中运行。

### Q9: 为什么服务经常“昨天能用，今天 offline”？
这是进程未常驻或被系统回收。先按 `next_commands` 启动，再考虑做系统级守护（如 launchd/systemd）。

### Q10: 常驻服务怎么装？

```bash
# macOS: launchd
bash scripts/service_install.sh xiaohongshu-mcp
bash scripts/service_status.sh xiaohongshu-mcp

# Linux: systemd --user
bash scripts/service_install.sh xiaohongshu-mcp
bash scripts/service_status.sh xiaohongshu-mcp
```

卸载：

```bash
bash scripts/service_uninstall.sh xiaohongshu-mcp
```

### Q11: 为什么有时只看到“请扫码登录”文字看不到二维码图？
这是上层代理展示链路问题，不一定是 MCP 没有生成二维码。优先使用：

```bash
bash scripts/login_qr.sh xiaohongshu-mcp
```

它会把二维码保存到本地（默认 `~/.openclaw/workspace/xhs-login-qrcode.png`）并输出 `open_command`。  
在 skill 编排里，建议禁止直接用 `mcporter call xiaohongshu-mcp.get_login_qrcode --output raw` 后只回复文本。

补充：如果脚本返回 `status=qr_url_ready`，说明当前返回没有内嵌图片，但有可扫码链接。此时应返回 `qr_url_hint`（及 `open_command`）给用户，不要只说“请扫码”。

### Q12: 为什么同样的问题昨天能触发 skill，今天却跑到浏览器/别的能力？
常见原因是新会话的 skill 上下文快照没有包含本 skill。先检查：

```bash
openclaw skills info xiaohongshu-mcp-openclaw
```

若找不到，重新安装：

```bash
bash scripts/install_to_openclaw.sh
```

然后新开一个会话再提问（避免旧会话沿用错误路由历史）。

### Q13: 没装 PyYAML 会影响二维码解析吗？
不会。当前版本已兼容 `mcporter` 的非标准对象输出（JS object literal），即使 `python3` 环境没有 `PyYAML` 也可解析二维码并输出 `qr_file`。

### Q14: 某些环境明明服务在跑，却偶尔报 `server_offline`？
这通常是执行环境隔离（sandbox）导致的本地端口可见性问题。建议先在同一执行环境里跑：

```bash
STRICT=1 bash scripts/smoke_test.sh xiaohongshu-mcp
bash scripts/login_doctor.sh xiaohongshu-mcp
```

若 `smoke_test` 通过，优先按返回的 `next_commands` 继续，而不是切换到浏览器抓取路径。

## Distribution

给其他 OpenClaw 分享建议流程：

```bash
# 1) 打包
bash scripts/build_distribution.sh

# 2) 对方解压后执行
bash scripts/preflight.sh
bash scripts/install_to_openclaw.sh
bash scripts/quickstart.sh
```

如果要减少“进程丢失”问题，建议对方在初始化后再执行：

```bash
bash scripts/service_install.sh xiaohongshu-mcp
```

## Output Schema (Normalized)

`xhs_mcp_client.py` 输出包含：

- `raw_response`: 原始 MCP 返回
- `normalized`: 归一化结构（常见字段）

```json
{
  "note_id": "...",
  "title": "...",
  "author": "...",
  "like_count": 0,
  "comment_count": 0,
  "content": "...",
  "xsec_token": "...",
  "url": "https://www.xiaohongshu.com/explore/...",
  "top_comments": [
    {
      "comment_id": "...",
      "author": "...",
      "content": "...",
      "like_count": 0
    }
  ]
}
```

## Project Layout

```text
.
├── SKILL.md
├── README.md
├── references/
│   └── field-mapping.md
└── scripts/
    ├── install_to_openclaw.sh
    ├── preflight.sh
    ├── build_distribution.sh
    ├── service_install.sh
    ├── service_status.sh
    ├── service_uninstall.sh
    ├── quickstart.sh
    ├── multi_summary.sh
    ├── login_doctor.sh
    ├── login_flow.sh
    ├── login_qr.sh
    ├── setup.sh
    ├── start_server.sh
    ├── register.sh
    ├── smoke_test.sh
    └── xhs_mcp_client.py
```

## Notes

- `SKILL.md` 保持精简，面向 OpenClaw 触发与执行。
- 详细说明放在 `README.md` 与 `references/`。
