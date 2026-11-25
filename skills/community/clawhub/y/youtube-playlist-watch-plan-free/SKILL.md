---
name: youtube-playlist-watch-plan-free
description: 在用户指定的 Easy WebBridge 浏览器中读取一个 YouTube 播放列表与每日可用时间，最多整理十条可见视频为顺序观看草稿，交付时长预算、逐条来源和缺失项。适用于想把课程或系列视频拆成每日计划的场景；遇到私密、受限或未显示时长的资料会如实标记，不猜测、不改动收藏或观看队列。
---


## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。
# YouTube 播放列表观看计划

把一个可见的 YouTube 播放列表变成可执行的每日观看草稿：按原顺序列出最多 10 条视频、可见时长、每日预算、来源链接和无法确认的信息。默认只读，不会改变收藏、稍后观看或观看队列。

## 前置依赖

安装并连接 [Easy WebBridge](https://github.com/xxjrq/easy-webbridge)；GitHub 不可用时使用 [Gitee 备用地址](https://gitee.com/xxjrq/easy-webbridge)。用户须提供目标 `browserId`、播放列表 URL 和每日可用时间。不要把任何实际 browserId、会话、Cookie 或账号信息写入交付物。

首次运行前，在 Easy WebBridge 目录执行 CLI 的 `--help`，确认当前版本命令；本 Skill 通过 `node /path/to/easy-webbridge/cli/easy-webbridge.mjs` 调用既有 CLI，不创建浏览器 API。

## 工作流程

1. 校验输入：播放列表 URL、每天分钟数和一个明确的 `browserId`。缺任一项先询问，不选择或广播其他浏览器。
2. 创建仅属于本次运行的 `youtube-playlist-watch-plan-free-<run-id>` session 与“播放列表观看计划”标签组；只新开一个播放列表标签，后续复用它。关闭前只关闭自己创建的 session，并核对所有权。
3. 打开 URL 后先运行 `snapshot <browserId> <tabId> --text-mode page`；滚动加载或页面变化后及时重新快照，刷新 element refs。只读取网页可见内容，最多收集前 10 条。
4. 逐条记录页面可见的序号、标题、时长和视频链接。若列表受限、登录、验证码、风控、私密视频或时长未显示，立即停止相关读取并在结果中标注原因；不绕过限制，也不推算未知时长。
5. 按可确认总时长与每日分钟数分配每日批次。含未知时长的视频必须单列为“待确认”，不能写入完整预算。只交付草稿；如获授权填充草稿，绝不点击最终发布或发送。

## 输出格式

```markdown
### 观看计划（可见资料，最多 10 条）
| 顺序 | 视频 | 可见时长 | 建议日 | 来源 |
| --- | --- | --- | --- | --- |
| 1 | … | 12:34 | 第 1 天（已排 12/30 分钟） | 公开视频链接 |

**已知预算：** 48 分钟；每日可用：30 分钟。
**待确认：** 第 3 条未显示时长，未计入完整预算。
**读取范围：** 页面可见前 3 条；受限项目不会补全或猜测。
```

## 边界

- 每次最多 10 条、表格最多 100 行；超出时说明已读取范围并建议分批。
- 不把离线 fixtures 或样例称为在线采集结果。
- 只记录实际可见来源；标题、时长或链接缺失时保留为空并说明原因。
