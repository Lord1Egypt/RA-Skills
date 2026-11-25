# 公众号草稿排版检查

## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。

发布前，用你指定的浏览器只读检查本人公众号草稿，交付带可见来源的标题层级、长段落、图片说明、断链与异常空白修改清单。不会替你改稿、发送或发布；正文不可见、草稿归属不明或出现登录验证时会明确暂停和列出缺项。

![公众号草稿排版检查推广图](assets/promo-1600x900.png)

## 输入与结果

输入为：你指定的 `browserId`、本人草稿的标题/编辑页链接/当前页面说明，以及目标阅读样式。单次适用于一篇短文、一个章节或一个场景；表格最多 100 行，超出会分批检查。

结果为：每条问题的类别、位置、可见证据、修改建议与来源，以及已检查范围、缺项和未执行动作。离线样例仅用于自检，绝不冒充在线采集结果。

```text
检查状态：完成
草稿来源：编辑器可见正文，第 1—6 段
问题：[长段落] 第 4 段｜连续 7 行｜建议按转折拆段｜来源：编辑器可见正文，第 4 段
未执行：未改稿、未发送、未发布
```

## 安装

```bash
npx skills add xxjrq/wechat-draft-format-check-free
```

这是浏览器类 Skill。先安装 [Easy WebBridge（GitHub）](https://github.com/xxjrq/easy-webbridge)，GitHub 不可用时使用 [Gitee 备用地址](https://gitee.com/xxjrq/easy-webbridge)。运行时只能使用你明确指定的 `browserId`；一个任务一个 session 分组，绝不广播到全部账号，也不接管既有页面。

## 使用边界

- 只读取网页可见内容；每次检查编辑器前使用 `snapshot --text-mode page`，页面变动后刷新 refs。
- 登录、验证码、风控、草稿归属不清或编辑器内容不可见时暂停，不绕过。
- 默认只读。即使获得草稿填充授权，也停在最终发布/发送前。
- 仅关闭本任务创建的 session；完成前核对其所有权。

## 本地验证

```bash
node scripts/self-test.mjs
```

自检只验证仓库元数据、离线成功/失败 fixture 和图标尺寸，不访问浏览器或网络。业务执行与自检相互独立。

## 来源与许可

业务用途仅参考 [OpenCLI](https://github.com/jackwener/OpenCLI) 及其 [微信浏览器适配说明](https://github.com/jackwener/OpenCLI/blob/main/docs/adapters/browser/weixin.md)；本仓库的说明、流程与样例均为原创，未复制其实现或源码。许可见 [MIT-0](LICENSE)。
