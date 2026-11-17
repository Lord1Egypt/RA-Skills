---
name: xhs-fav-export
slug: xhs-fav-export-v2
displayName: xhs 收藏导出 · 收藏夹笔记批量备份为本地 Markdown 知识库
version: 1.0.6
summary: 把你收藏的笔记一键备份为本地 Markdown 知识库（bookmark export）——标题、原文链接、正文、图片/视频链接全保留，支持分批断点续导、可重跑不重复。不需要任何第三方 API key 或付费额度，用你 Chrome 里已登录的账号跑。当用户需要导出/备份/检索自己的收藏内容、想离线保存收藏笔记、建个人知识库时唤起。
description: 把你收藏的笔记一键备份为本地 Markdown 知识库——标题、原文链接、正文、图片/视频链接全保留，支持分批断点续导、可重跑不重复。不需要任何第三方 API key 或付费额度，用你 Chrome 里已登录的账号跑。当用户需要导出/备份/检索自己的收藏内容、想离线保存收藏笔记、建个人知识库时唤起。
license: MIT
---

# xhs-fav-export

把 Web 端**当前登录用户**自己主页「收藏」tab 里的收藏笔记，批量导出为本地 Markdown 文件。每篇一个 md，包含标题、原文链接（可跳转原文）、正文文字、图片/视频 URL（只存 URL 不下载），最后生成 `summary.json` 汇总。

## 前置条件

- wc3-chrome 扩展 + Relay（`http://127.0.0.1:3459`）已启动（`extensionConnected` 为 true）
- 已在 Chrome 中登录（收藏 tab 依赖登录态；未登录会明确报错）
- 本 skill 全程确定性代码（Extension Relay 操作），**不依赖**本地 pipeline 子会话服务
- 需要 Node.js 22+

## 使用方式

```bash
node skill.mjs [input.json]
```

`input.json`：

```json
{
  "offset": 0,
  "count": 10,
  "outputDir": "/absolute/path/to/output"
}
```

| 参数 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `outputDir` | string | `/tmp/xhs-fav-export-output` | 输出目录（也接受 `output_dir`） |
