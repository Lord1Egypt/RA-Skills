---
name: vibe-remote
description: Vibe Remote 远程 AI Coding 工具。当用户提到 vibe-remote、vibe remote、远程 coding、iOS 远程控制 Mac 跑 AI 写代码、安装 vibe-remote、配置 vibe-remote、或提交 vibe-remote issue 时使用。
---

# Vibe Remote Skill

远程调用 AI Coding Agent 的工具，通过 iOS app 远程控制 Mac/Linux 机器上的 Claude Code / Codex 来写代码。

## 基本信息

- **Repo**: https://github.com/ymzuiku/vibe-remote
- **文档**: https://docs.vibe-remote.com
- **支持 Agent**: Claude Code（推荐）、Codex、OpenCode（实验性）

## 启动

```bash
export PATH="$HOME/bin:$PATH"
vibe-remote
```

启动后会显示 QR 二维码，用 iOS Vibe Remote app 扫码连接。

**Headless 模式（CI / 脚本）**：
```bash
vibe-remote --headless --account <用户名> --password <密码>
```

二进制文件路径：`~/bin/vibe-remote`

## GitHub Issue 提交流程

提交 issue 前需要：
1. 确保 `gh` CLI 已登录 GitHub：`gh auth status`
2. 确认 owner/repo：`ymzuiku/vibe-remote`
3. **Issue 提交完成后，必须将链接发送给用户**

### Bug Report 格式

```bash
gh issue create --repo ymzuiku/vibe-remote \
  --title "<标题>" \
  --body "## Bug Description
<描述>

## Steps to Reproduce
1. ...
2. ...

## Expected Behavior
<期望行为>

## Actual Behavior
<实际行为>

## Version
<版本号>
vibe-remote Version: <版本>" \
  --label "bug"
```

### Feature Request 格式

```bash
gh issue create --repo ymzuiku/vibe-remote \
  --title "<标题>" \
  --body "## Problem / Motivation
<问题背景>

## Proposed Solution
<建议方案>

## Alternatives Considered
<考虑过的替代方案>" \
  --label "enhancement"
```

### 图片/视频上传（嵌入 Issue）

GitHub Issue API 不支持直接上传二进制文件。规则：

| 文件类型 | 上传方式 |
|---|---|
| 图片（jpg/png/gif/webp） | 使用 `nodeimage-upload` Skill；如不可用则用 catbox |
| 视频（mp4/mov） | 上传到 catbox（见下方命令） |

**上传到 catbox**（图片或视频均可用）：
```bash
curl -F "reqtype=fileupload" -F "fileToUpload=@文件路径" https://catbox.moe/user/api.php
```
返回的 URL：
- 图片：用 `![描述](URL)` 嵌入 issue body
- 视频：直接贴 URL

### Issue 模板（参考）

| 字段 | 说明 |
|---|---|
| vibe-remote Version | 版本号，如 0.1.254 |
| Operating System | macOS (Apple Silicon) / macOS (Intel) / Linux / Windows |
| Bug Description | 描述问题 |
| Steps to Reproduce | 重现步骤 |
| Expected Behavior | 期望行为 |
| Actual Behavior | 实际行为 |

**Issue 链接格式**：`https://github.com/ymzuiku/vibe-remote/issues/<编号>`

## 常用命令

```bash
# 显示帮助
vibe-remote help

# 检查版本
vibe-remote --version

# 重新生成 QR 码（运行中按 r）
```
