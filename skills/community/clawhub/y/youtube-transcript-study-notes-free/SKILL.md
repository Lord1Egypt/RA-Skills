---
name: youtube-transcript-study-notes-free
description: 使用用户指定的浏览器环境读取 YouTube 视频页面中实际可见的字幕，按目标语言与学习目标交付摘要、术语表和时间锚点。适用于单个章节、场景或短文学习；字幕关闭、缺失或语言不匹配时保留来源并报告限制，不根据音频或猜测补写内容。
---


## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。
# YouTube 字幕学习笔记

把网页上**可见的** YouTube 字幕变成可复核的学习笔记：摘要、术语表、时间锚点和缺项说明。它不下载视频、不调用转录 API，也不把推测的音频内容写成字幕。

## 输入

用户提供：视频 URL、目标语言、学习目标和 `browserId`。单次仅处理一个章节、场景或短文；表格最多 100 行，超过时先说明范围并请求分批。

## 结果

输出 Markdown 草稿，包含：来源 URL 与页面可见语言、范围说明、要点摘要、术语表、时间锚点、限制与缺项。没有可见字幕、字幕已关闭或语言不匹配时，输出限制报告，不能补写音频内容。

## 运行前提：Easy WebBridge

这是浏览器 Skill。先安装并连接 [Easy WebBridge（GitHub）](https://github.com/xxjrq/easy-webbridge)；GitHub 不可用时使用 [Gitee 备用地址](https://gitee.com/xxjrq/easy-webbridge)。在目标浏览器扩展中确认已连接后，用户提供一个明确的 `browserId`。

运行时使用 CLI：`node /path/to/easy-webbridge/cli/easy-webbridge.mjs`。先阅读本机 CLI 的 `--help`；本 Skill 不内置、不复制浏览器 API，也不公开本机路径、实际 browserId 或 session。

## 工作流

1. 确认输入完整：URL、目标语言、学习目标、明确的 `browserId`。默认只读。
2. 执行 CLI `--help`，再为本次运行创建唯一 `youtube-transcript-study-notes-free-<run-id>` session 和“字幕学习笔记”标签组。只在用户指定的 `browserId` 内打开 URL，复用该组的标签页，绝不广播到其他环境。
3. 使用 `snapshot <browserId> <tabId> --text-mode page` 读取网页可见文本；导航、展开字幕或滚动后立即刷新快照和 refs。仅依据快照中可见的字幕、章节与时间信息记录笔记。
4. 核对字幕是否存在、是否开启及目标语言是否匹配。遇到登录、验证码、风控或账户安全验证，停止并报告；不绕过。
5. 生成草稿时逐项保留来源 URL 和可见范围。字幕内容上限为 100 行；超出时标记未覆盖范围并请用户分批。
6. 若用户明确授权“草稿填充”，只填入草稿字段并停在最终发布/发送前；绝不点击发布或发送。结束时仅关闭本次创建且确认归属的 session，不接管或关闭已有页面。

## 输出模板

```markdown
# 学习笔记草稿

- 来源：<视频 URL>
- 页面可见字幕语言：<语言或“未确认”>
- 学习目标：<用户目标>
- 覆盖范围：<可见时间/章节；最多 100 行>

## 摘要
- <仅基于可见字幕的要点>

## 术语表
| 术语 | 页面可见释义/上下文 | 时间锚点 |
| --- | --- | --- |

## 时间锚点
| 时间 | 可见内容摘要 |
| --- | --- |

## 限制与缺项
- <字幕不存在、关闭、语言不匹配、可见范围不足等实际情况>
```

## 失败分支

- 字幕不存在或关闭：说明页面未提供可见字幕/字幕未开启，交付限制报告。
- 语言不匹配：说明可见语言与目标语言，并请求用户选择可用语言或提供对应字幕。
- 登录、验证码或风控：暂停，等待用户完成验证；不得规避。
- 页面内容超过边界：只交付已见范围，列出未覆盖部分并请求分批。

## 本地验证

运行 `node scripts/self-test.mjs`。它只检查仓库结构和离线页面资料模拟夹具，不连接浏览器，也不把样例宣称为在线采集。
