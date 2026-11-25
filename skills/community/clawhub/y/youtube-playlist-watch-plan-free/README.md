# YouTube 播放列表观看计划

## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。

![推广图](assets/promo.png)

把 YouTube 播放列表按你的每日可用时间整理成一份只读观看草稿：得到视频顺序、可见时长预算、每日建议、逐条来源和明确的缺失信息。列表受限或时长未知时，Skill 不会假装完整，也不会改动收藏或观看队列。

## 输入与结果

输入：一个播放列表 URL、每天可用分钟数，以及用户明确指定的 Easy WebBridge `browserId`。单次最多读取页面可见的 10 条视频。

结果：Markdown 表格，包含原始顺序、标题、可见时长、建议观看日、来源链接、已知总时长与待确认项。只把页面实际可见信息计入预算；私密、受限、登录验证或无时长项目会原样标记。

## 安装

```bash
npx skills add xxjrq/youtube-playlist-watch-plan-free
```

## 浏览器前置依赖

本 Skill 依赖可安装的 [Easy WebBridge（GitHub 主下载）](https://github.com/xxjrq/easy-webbridge)，GitHub 不可用时可用 [Gitee 备用地址](https://gitee.com/xxjrq/easy-webbridge)。先在目标浏览器加载其扩展并确认已连接；运行时必须由用户传入一个 `browserId`。

每次读取创建独立 session/标签组，只在该组内复用标签页，完成后仅关闭本 Skill 创建的组；不会广播到所有账号或接管既有页面。登录、验证码或风控页面会暂停，绝不绕过。

## 使用示例

```text
使用 browserId 读取 https://www.youtube.com/playlist?list=...，我每天有 30 分钟。
请生成最多 10 条的只读观看计划，保留每条来源和缺失信息；不要改动收藏或观看队列。
```

本仓库的 fixtures 是离线页面资料模拟，仅用于结构验证，不是在线采集结果。

## 本地验证

```bash
node scripts/self-test.mjs
```

## 来源与许可

业务用途参考：[OpenCLI](https://github.com/jackwener/OpenCLI) 及其 [YouTube adapter 文档](https://github.com/jackwener/OpenCLI/blob/main/docs/adapters/browser/youtube.md)。本 Skill 的说明、流程和 fixtures 为原创，未复制其实现；本仓库以 [MIT-0](LICENSE) 发布。
