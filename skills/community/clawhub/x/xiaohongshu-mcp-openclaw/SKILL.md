---
name: xiaohongshu-mcp-openclaw
description: 当用户提到小红书/XHS/Rednote 并需要关键词搜笔记、看笔记详情、抓评论、统计点赞与评论数时使用。通过 xpzouying/xiaohongshu-mcp + mcporter 提供统一查询流程。
metadata: {"openclaw":{"emoji":"📕","requires":{"bins":["bash","mcporter","python3","jq"]},"install":[{"id":"node","kind":"node","package":"mcporter","bins":["mcporter"],"label":"Install mcporter (node)"}]}}
---

# xiaohongshu-mcp-openclaw

通过本 skill 可统一完成：
- 关键词搜索笔记
- 获取笔记详情和评论
- 输出点赞数/评论数等归一化指标
- 多笔记抓取并自动汇总

## Quick Start

初始化（安装服务端 + 启动 + 注册 + 冒烟 + 登录守卫）：
```bash
bash {baseDir}/scripts/quickstart.sh
```

分发前环境预检：
```bash
bash {baseDir}/scripts/preflight.sh
```

已安装到 OpenClaw 后可用：
```bash
bash {baseDir}/scripts/install_to_openclaw.sh
openclaw skills info xiaohongshu-mcp-openclaw
```
默认会同步到 `~/.agents/skills/xiaohongshu-mcp-openclaw-1.0.0`；如不需要可加 `XHS_SYNC_AGENTS_SKILL=0`。

## Agent Rules (Critical)

- 用户提到“登录/扫码/看不到二维码/fail to login/未登录”时，必须先执行：
```bash
bash {baseDir}/scripts/login_qr.sh xiaohongshu-mcp
```
- 回复用户时必须带上脚本输出中的 `qr_file` 和 `open_command`（若存在）。
- 若返回 `status=qr_url_ready`，必须返回 `qr_url_hint`（和 `open_command` 若存在），不要只说“请扫码”。
- 禁止直接调用 `mcporter call xiaohongshu-mcp.get_login_qrcode --output raw` 后只给文字提示。

## Core Commands

登录守卫（已登录则直接返回）：
```bash
python3 {baseDir}/scripts/xhs_mcp_client.py --server xiaohongshu-mcp ensure-login
```

二维码登录（推荐，落盘 PNG 并返回可打开路径）：
```bash
bash {baseDir}/scripts/login_qr.sh xiaohongshu-mcp
```

仅生成二维码文件，不自动打开：
```bash
XHS_QR_AUTO_OPEN=0 bash {baseDir}/scripts/login_qr.sh xiaohongshu-mcp
```

登录守卫精简模式（不返回完整二维码 base64）：
```bash
python3 {baseDir}/scripts/xhs_mcp_client.py --server xiaohongshu-mcp ensure-login --strip-qr-image
```

登录专用流程（临时 headful，成功后自动切回 headless）：
```bash
bash {baseDir}/scripts/login_flow.sh xiaohongshu-mcp 120
```

关键词搜索：
```bash
python3 {baseDir}/scripts/xhs_mcp_client.py --server xiaohongshu-mcp search --keyword 防晒 --limit 5
```

详情 + 评论报告：
```bash
python3 {baseDir}/scripts/xhs_mcp_client.py --server xiaohongshu-mcp report --keyword 防晒 --search-limit 5 --comment-limit 3
```

多笔记总结：
```bash
bash {baseDir}/scripts/multi_summary.sh 防晒 5 2
```

登录诊断：
```bash
bash {baseDir}/scripts/login_doctor.sh xiaohongshu-mcp
```

生成可分享分发包：
```bash
bash {baseDir}/scripts/build_distribution.sh
```

可选：安装系统级常驻服务（防止隔天 offline）：
```bash
bash {baseDir}/scripts/service_install.sh xiaohongshu-mcp
bash {baseDir}/scripts/service_status.sh xiaohongshu-mcp
```

## Notes

- 默认 `headless=true`，避免频繁弹浏览器页面。
- 脚本主要面向 Linux/macOS shell；Windows 建议用 WSL/Git Bash。
- 常驻服务支持：macOS `launchd`、Linux `systemd --user`。
- 查询命令默认带登录预检（未登录会直接返回并提示 `ensure-login`）。
- `ensure-login` 默认包含二维码图片数据，便于上层代理直接展示扫码图。
- 登录场景优先使用 `scripts/login_qr.sh`，该脚本会把二维码保存到本地 PNG（默认 `~/.openclaw/workspace/xhs-login-qrcode.png`），避免“有扫码提示但看不到二维码图片”。
- `xhs_mcp_client.py/login_qr.sh` 已兼容 `mcporter` 的非标准对象输出（JS object literal），不依赖 `PyYAML` 也可解析二维码。
- 禁止直接调用 `mcporter call xiaohongshu-mcp.get_login_qrcode --output raw` 并只回复文字；必须返回 `qr_file`（或 `open_command`）给用户。
- 若服务未启动，`xhs_mcp_client.py` 会返回 `error_type=server_offline` 和可直接执行的 `next_commands`（先启动再重试），不要只回复“离线”。
- `detail/comments` 建议传 `xsec_token`（可从 `search` 结果中取）。
- 出现登录/验证码时，需用户手动完成校验后重试。
- 返回 “Sorry, This Page Isn't Available Right Now.” 多为目标笔记当前账号不可见。
- 新会话如果没有加载该 skill，可先执行 `openclaw skills info xiaohongshu-mcp-openclaw`；找不到时执行 `bash {baseDir}/scripts/install_to_openclaw.sh` 后再新开会话。

## Full Docs

详细使用说明见：
- `README.md`
- `references/field-mapping.md`
