# 公众号文章阅读简报

## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。

用你指定的浏览器读取 1–3 篇公开公众号文章，快速拿到可追溯的主结论、关键步骤、作者、日期、来源与未显示项。文章删除、需要登录、触发验证或正文不完整时，结果会明确保留限制，不会把摘要误写成全文。

![公众号文章阅读简报推广图](promo.png)

## 输入与结果

输入：1–3 个公开文章 URL、关注问题和用户指定的 `browserId`。单次仅限短文/单一章节/单一场景，表格最多 100 行；超出需分批。

结果：每篇文章的主结论、关键步骤、作者/日期/来源链接，以及“全文可见”“正文截断”“登录验证”“已删除”等可见范围与缺项。全部结论只基于网页可见资料。

## 安装

```bash
npx skills add xxjrq/wechat-article-reading-brief-free
```

这是浏览器类 Skill，需先安装 Easy WebBridge：GitHub <https://github.com/xxjrq/easy-webbridge>，Gitee 备用 <https://gitee.com/xxjrq/easy-webbridge>。启动 Bridge、连接浏览器后，在请求中提供目标 `browserId`。每次任务仅创建自己的 session 标签组，不操作其他账号或既有页面。

## 使用示例

```text
使用 browserId <我指定的环境> 读取以下两篇公开公众号文章：
<URL 1>
<URL 2>
关注：作者提出的行动步骤是什么？输出可溯源简报；遇到正文不全请标明。
```

默认只读。若明确授权填写草稿，也只停在最终发布/发送之前；登录、验证码和风控会暂停，不会绕过。

## 本地验证

```bash
node scripts/self-test.mjs
```

fixtures 中的成功与失败页面均为离线页面资料模拟，只验证输出边界和结构，并非在线采集。

## 来源与许可证

本 Skill 的流程为原创说明。业务行为仅参考 [OpenCLI](https://github.com/jackwener/OpenCLI) 及其 [微信浏览器适配说明](https://github.com/jackwener/OpenCLI/blob/main/docs/adapters/browser/weixin.md)，未复制其源码或文章内容。采用 MIT-0，见 [LICENSE](LICENSE)。
