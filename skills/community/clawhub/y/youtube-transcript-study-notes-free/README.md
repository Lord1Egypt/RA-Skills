# YouTube 字幕学习笔记

## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。

![YouTube 字幕学习笔记推广图](assets/promo-1600x900.png)

把 YouTube 页面中实际可见的字幕整理成可复核的学习笔记：你会获得摘要、术语表、时间锚点与明确的缺项说明，而不是未经证实的“转录结果”。适合语言学习、课程复盘和短视频知识整理。

输入是视频 URL、目标语言、学习目标和用户指定的 `browserId`；结果是基于可见字幕的 Markdown 草稿。若字幕不存在、关闭或语言不匹配，Skill 会交付限制报告，不会凭音频猜写内容。

## 安装

```bash
npx skills add xxjrq/youtube-transcript-study-notes-free
```

## 使用方式

示例请求：

```text
用 browserId <你选择的浏览器环境> 打开 https://www.youtube.com/watch?v=…，
目标语言为英语，学习目标是掌握产品讲解中的核心动词。
请只读取可见字幕，输出摘要、术语表和时间锚点；没有字幕时报告限制。
```

每次运行只选择一个用户指定的浏览器环境，并创建自己的标签组；不会广播操作到其他账号或环境。默认只读，若获授权填充草稿也绝不点击最终发布或发送。

## 运行前提

本 Skill 需要安装并连接 Easy WebBridge：主下载地址为 [GitHub](https://github.com/xxjrq/easy-webbridge)，备用为 [Gitee](https://gitee.com/xxjrq/easy-webbridge)。运行时调用已安装的 Easy WebBridge CLI，并由用户提供目标 `browserId`。

遇到登录、验证码或风控验证会暂停，绝不尝试绕过。公开资料不会包含实际 browserId、session、凭据或本机路径。

## 交付结构

- 来源 URL、页面可见字幕语言与覆盖范围
- 仅根据可见字幕归纳的摘要
- 术语、上下文与时间锚点
- 字幕缺失、关闭、语言不匹配或范围不足等限制

单次处理一个章节、场景或短文，表格最多 100 行。内容超过范围时会先列出未覆盖区段，并请你分批处理。

## 自检

```bash
node scripts/self-test.mjs
```

自检只验证本仓库元数据、图标与离线页面资料模拟夹具，不访问浏览器或 YouTube，夹具不是在线采集结果。

## 参考与许可证

业务用途参考：[OpenCLI](https://github.com/jackwener/OpenCLI) 及其 [YouTube 浏览器适配说明](https://github.com/jackwener/OpenCLI/blob/main/docs/adapters/browser/youtube.md)。本仓库的说明、流程与示例为原创，没有复制其源码或文档实现；本仓库采用 [MIT-0](LICENSE)。
