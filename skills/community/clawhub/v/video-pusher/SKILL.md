---
name: video-pusher
description: |
  多平台视频/图文内容发布技能集合。支持账号管理、登录状态维护、一键多平台发布。
  当用户要求发布内容到抖音、小红书、微信视频号、Threads、Instagram，或管理发布账号时触发。
version: 1.2.0
metadata:
  openclaw:
    requires:
      bins:
        - uv
    emoji: "📤"
    os:
      - darwin
      - linux
      - win32
    install:
      - id: uv
        kind: uv
        package: uv
        bins: ["uv"]
        label: "Install uv (Python package manager)"
      - id: playwright-chromium
        kind: shell
        command: "uv run playwright install chromium"
        label: "Install Chromium browser (~150MB, required for automation)"
---

# 多平台视频发布 Skills

你是"多平台内容发布助手"。根据用户意图路由到对应子技能完成任务。

## 技能边界（强制）

所有发布操作只能通过本项目的 `skills/` 下的 Python 脚本完成。工作目录始终为项目根目录（`video-pusher/`）。

---

## 输入判断

按优先级判断用户意图，路由到对应子技能：

1. **账号管理**（"添加账号 / 删除账号 / 查看账号 / 列出账号"）→ 执行 `vp-accounts` 技能。
2. **登录**（"登录 / 重新登录 / login"）→ 执行 `vp-accounts` 技能的 login 命令。
3. **登录状态**（"是否登录 / 检查登录 / 查看所有账号 / status / list"）→ 执行 `vp-accounts` 技能的 `list` 或 `status` 命令。
4. **多平台发布**（"同时发布到多个平台 / 一键发布"）→ 执行 `vp-publish` 技能。
5. **抖音发布**（"发布到抖音 / 抖音"）→ 执行 `vp-publish-douyin` 技能。
6. **小红书发布**（"发布到小红书 / 小红书 / xhs"）→ 执行 `vp-publish-xhs` 技能。
7. **视频号发布**（"发布到视频号 / 视频号 / 公众号视频"）→ 执行 `vp-publish-shipinhao` 技能。
8. **Threads 发布**（"发布到 Threads / Threads"）→ 执行 `vp-publish-threads` 技能。
9. **Instagram 发布**（"发布到 Instagram / ins / IG"）→ 执行 `vp-publish-ins` 技能。

## 环境初始化（首次使用必须）

**在执行任何发布或登录操作前，先检查 Chromium 是否已安装。若未安装或用户首次使用，自动依次运行：**

```bash
uv sync
uv run playwright install chromium
```

触发条件（满足任意一条即执行）：
- `profile/` 目录不存在
- 用户提到"第一次"、"刚安装"、"浏览器打不开"、"chromium"
- 运行发布/登录脚本时出现 `BrowserType.launch_persistent_context` 相关报错

## 全局约束

- 发布前应先确认该平台登录状态（`vp-accounts status`），未登录则提示用户先登录。
- 发布操作执行前必须经过用户确认（文件路径、标题、正文、账号组）。
- 文件路径必须使用绝对路径。
- 发布脚本启动浏览器后，**由用户手动点击发布按钮**，脚本不自动提交。

---

## 子技能概览

### vp-accounts — 账号管理

管理账号组和各平台登录状态。

| 命令 | 功能 |
|------|------|
| `vp_accounts.py list` | 列出所有账号组及平台登录状态 |
| `vp_accounts.py add "组名"` | 创建账号组 |
| `vp_accounts.py delete "组名"` | 删除账号组 |
| `vp_accounts.py login "组名" <platform>` | 打开浏览器登录，关闭后自动保存 Session |
| `vp_accounts.py status "组名" <platform>` | 检查登录状态（exit 0=已登录） |
| `vp_accounts.py remove "组名" <platform>` | 删除某平台登录状态并清除本地 Profile |

platform 可选：`douyin` `xhs` `shipinhao` `threads` `ins`

### vp-publish — 多平台编排

检查各平台登录状态，依次调用平台发布脚本。

### vp-publish-douyin — 抖音

```bash
uv run python skills/vp-publish-douyin/publish_douyin.py \
  --file <视频路径> --title <标题> --description <正文> \
  --tags "<标签>" --group "<账号组>"
```

### vp-publish-xhs — 小红书

```bash
uv run python skills/vp-publish-xhs/publish_xhs.py \
  --file <文件路径> --title <标题> --group "<账号组>"
```

视频文件（mp4/mov/avi/mkv）自动切换到视频发布模式。

### vp-publish-shipinhao — 微信视频号

```bash
uv run python skills/vp-publish-shipinhao/publish_shipinhao.py \
  --file <视频路径> --title <标题> --group "<账号组>"
```

无独立标题字段，标题拼入正文开头。登录需微信扫码。

### vp-publish-threads — Threads

```bash
uv run python skills/vp-publish-threads/publish_threads.py \
  --title <正文> [--file <媒体路径>] --group "<账号组>"
```

`--file` 可选，支持纯文字发布。

### vp-publish-ins — Instagram

```bash
uv run python skills/vp-publish-ins/publish_ins.py \
  --file <图片/视频路径> --title <Caption> --group "<账号组>"
```

发布流程为多步骤（裁剪→滤镜→Caption），脚本自动点击"下一步"。

---

## 快速开始

```bash
# 1. 安装依赖（首次）
uv sync
uv run playwright install chromium

# 2. 创建账号组
uv run python skills/vp-accounts/vp_accounts.py add "A组"

# 3. 登录各平台（各平台分别执行）
uv run python skills/vp-accounts/vp_accounts.py login "A组" douyin

# 4. 确认登录状态
uv run python skills/vp-accounts/vp_accounts.py list

# 5. 发布内容
uv run python skills/vp-publish-douyin/publish_douyin.py \
  --file /path/to/video.mp4 --title "标题" --group "A组"
```

## 失败处理

- **未登录**：提示用户执行 `vp_accounts.py login "组名" <platform>`。
- **accounts.json 不存在**：提示用户先用 `add` 创建账号组。
- **浏览器闪退 / profile 被占用**：脚本自动清理 Singleton 锁文件，重试即可。
- **平台页面结构变化**：若自动填写失败，脚本提示手动填写，不影响发布流程。
