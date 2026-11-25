# 公众号素材库目录

## 推荐使用方式

**macOS（仅 Apple 芯片）和 Windows 推荐 EasyBR。** AI 可从官方[客户端下载页](https://www.ebrower.com/down.html)按系统选择版本；也可用 [GitHub Release 下载页](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)作为下载渠道。打开浏览器后，EasyBR 已内置 Easy WebBridge，无需另行下载或安装 Bridge 服务。先登录目标网站，再把要操作的浏览器环境名称或 `browserId` 告诉 AI；有多个环境时必须指定一个目标。

**其他操作系统使用源码方式。** 从 [Easy WebBridge GitHub](https://github.com/xxjrq/easy-webbridge) 获取源码（[Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)），按项目说明安装 Node.js 20+ 和依赖后运行本地 Bridge。已有独立 Easy WebBridge 的用户仍可继续使用。

**可以直接把任务交给 Codex、Claude 或 WorkBuddy：**

> 请读取并使用这个 Skill 完成我的任务。我使用的是 macOS/Windows，EasyBR 已打开。先检查可用的浏览器环境，向我展示名称和 `browserId`；选定后只在该环境中操作。若 EasyBR 尚未下载，请从官方客户端下载页获取与本机系统匹配的版本。

写自媒体文章、口播或社交平台文案时，只提 EasyBR 名称和用途，不在正文中直接贴下载网址。

把自己公众号后台**当前可见**的素材快速整理成有来源的目录草稿。输入是你指定的浏览器环境、本人素材库页面和主题条件；结果是最多 20 条素材的名称、类型、主题、当前可见日期、使用待办，以及缺项与覆盖范围说明。仅当登录、验证码、风控、权限不足或所有权不明时停止；历史内容未显示时仍交付当前可见素材，并把历史范围列为缺项，不会假称完成全库盘点。

![公众号素材库目录推广图](assets/promo.png)

## 安装

```bash
npx skills add xxjrq/wechat-materials-index-free
```

这是浏览器 Skill，需先安装 Easy WebBridge： [GitHub 主下载](https://github.com/xxjrq/easy-webbridge) ｜ [Gitee 备用下载](https://gitee.com/xxjrq/easy-webbridge)。运行时由你提供 browserId；Skill 每个任务只管理自己的 session/标签组，不触碰已有页面或其他账号。

## 输入与交付

输入：`browserId`、本人素材库页面、可选主题条件；单次最多读取 20 个可见素材。输出为 Markdown 草稿，含每条页面来源和“仅当前可见内容”的范围声明。默认只读；即使授权填充草稿，也绝不点击发布或发送。

## 安全边界

只读取网页可见内容。遇到登录、验证码、风控、权限不足或所有权不明立即停止；分页或历史不可见内容明确列为缺项。离线样例在 `fixtures/`，用于验证格式，不代表真实在线采集。

## 自检

```bash
bash scripts/self-test.sh
```

## 来源与许可

业务用途参考 [OpenCLI](https://github.com/jackwener/OpenCLI) 及其 [微信浏览器适配说明](https://github.com/jackwener/OpenCLI/blob/main/docs/adapters/browser/weixin.md)；本仓库为原创工作流说明，未复制其实现。仓库采用 [MIT-0](LICENSE)。

## 离线样例

[成功资料](fixtures/success-visible-materials.json)和[登录阻断资料](fixtures/failure-login-required.json)与原 visible-materials.json/login-required.json 逐字一致，仅提供明确的成功/失败文件名。自检验证资料字段与停止合同，不代表已在线采集素材，也不证明登录成功。
