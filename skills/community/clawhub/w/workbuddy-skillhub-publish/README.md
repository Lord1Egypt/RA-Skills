# workbuddy SkillHub skill 自动发布

## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。

通过 Easy WebBridge 复用已登录浏览器，把本地 Skill 校验、打包、上传图标和资料并提交到 SkillHub。免费使用，不需要第三方 API Key。

## 需要什么

- Node.js 20+
- 已安装并运行 [Easy WebBridge](https://github.com/xxjrq/easy-webbridge)，备用地址：[Gitee](https://gitee.com/xxjrq/easy-webbridge)
- SkillHub 已登录并完成实名认证的浏览器环境
- Bridge 仅允许本机 loopback HTTP 地址；投稿目标仅允许 `https://skillhub.cn` 页面，Bridge 请求不跟随重定向。
- 页面就绪、文件上传前和提交前都会核验实际域名；导航到其他站点时停止并清理本次任务标签组。

## 用法

```bash
node scripts/skillhub-publish.mjs validate /绝对路径/skill-dir
node scripts/skillhub-publish.mjs plan /绝对路径/skill-dir
node scripts/skillhub-publish.mjs preflight
node scripts/skillhub-publish.mjs publish /绝对路径/skill-dir --browser-id <browserId>
node scripts/skillhub-publish.mjs publish /绝对路径/skill-dir --display-name "自媒体"
node scripts/skillhub-publish.mjs publish /绝对路径/skill-dir --display-name "自媒体" --update
node scripts/skillhub-publish.mjs publish /绝对路径/skill-dir --display-name "自媒体" --fill-only
node scripts/skillhub-publish.mjs readback /绝对路径/skill-dir --browser-id <browserId>
```

`--display-name` 指浏览器环境显示名；表单名称和更新说明可分别用 `--skill-name`、`--changelog` 覆盖。

`publish` 默认点击“提交审核”或“更新 Skill”，并回到列表核对版本和审核状态。只有明确要先预览时才使用 `--fill-only` 停在提交前。遇到登录、实名、验证码、风控或平台拒绝会明确停下，不伪报成功。
`readback` 是只读核对命令；仅在确认所有分页已完整读取后才报告 `absent`，证据不足时返回 `unknown`。
脚本复用指定 EasyBR 浏览器的登录态，每次运行创建独立 UUID 标签组，正常结束时只清理本次自有标签组并保留用户原有标签。`--fill-only` 预览默认保留本次标签供检查；需要清理时追加 `--close-tab`。
