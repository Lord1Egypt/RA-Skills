---
name: wechat-draft-format-check-free
description: 在用户指定的 Easy WebBridge 浏览器环境中，只读检查本人指定的公众号草稿与目标阅读样式，交付标题层级、长段落、图片说明、断链和空白问题清单及可见来源。适合发布前短文或单章节复核；草稿归属不明、编辑器不可见、登录验证或内容超出单批范围时暂停并列出缺项，不修改草稿、不发送、不发布。
---


## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。
# 公众号草稿排版检查

读取你明确指定的公众号草稿，输出可执行的版面问题清单；默认全程只读，不改稿、不群发、不发布。

## 输入

- `browserId`：用户指定且当前在线的 Easy WebBridge 浏览器环境。
- 草稿定位：用户给出的草稿标题、编辑页链接或当前页面说明。
- 目标阅读样式：例如“二级标题清晰、段落不超过 4 行、图片有说明”。未提供时，报告中标为“目标样式缺失”，不臆测品牌规范。

单次只检查一篇短文、一个章节或一个场景；表格最多 100 行。超出时按可见边界分批，绝不声称已读完全文。

## 前置依赖

安装并启动 [Easy WebBridge](https://github.com/xxjrq/easy-webbridge)；GitHub 为主下载地址，Gitee 备用：[gitee.com/xxjrq/easy-webbridge](https://gitee.com/xxjrq/easy-webbridge)。仅使用用户明确提供的 `browserId`，绝不向全部账号广播。

## 执行流程

1. 先读取 CLI 帮助：`node /path/to/easy-webbridge/cli/easy-webbridge.mjs --help`。确认目标 `browserId` 在线；不明确草稿归属时暂停。
2. 仅当需要打开页面时，创建唯一 session：`wechat-draft-format-check-free-<run-id>`，并复用该组内标签页。不得接管或关闭用户既有页面；结束前核对本 session 的所有权，只关闭本任务创建的 session。
3. 使用可见页面内容检查。每次读取编辑器前执行 `snapshot <browserId> <tabId> --text-mode page`，页面变动后及时重新获取 refs。不能读取编辑器正文、遇到登录/验证码/风控时立即暂停，不绕过。
4. 逐项标记标题层级、过长段落、图片说明、断链与异常空白，并附上真实可见来源（页面标题/位置/摘录或 URL）和缺项。草稿内容不对外扩散。
5. 默认不点击编辑、保存、发布或发送。即使用户授权填充草稿，也仅填充并停在最终发布/发送按钮之前。

## 交付格式

```text
检查状态：完成 | 暂停
草稿来源：<可见页面标题或用户指定定位>
目标样式：<用户提供内容；未提供则写缺失>
已检查范围：<可见章节/段落范围>

问题清单：
1. [标题层级] 位置：…｜证据：…｜建议：…｜来源：…
2. [长段落] 位置：…｜证据：…｜建议：…｜来源：…

缺项/暂停原因：…
未执行：未改稿、未发送、未发布。
```

不得把离线 fixture、示例或用户提供的文本表述为在线采集结果。
