# xhs-fav-export · xhs收藏夹导出

把自己xhs「收藏」tab 里的笔记**批量导出成本地 Markdown**，收藏不再吃灰——可检索、可跳转原文、博主删帖也不丢。

一句话：以前收藏了上千篇干货从来不看，现在一键导出成 Markdown 进 Obsidian / 语雀 / 本地目录，随时搜索、随时引用。

## 能干什么

- 打开自己主页「收藏」tab，按收藏时间倒序（最新在前）批量导出
- 每篇存成一个 Markdown：标题、原文链接（可跳转）、正文、图片/视频 URL
- `offset/count` 支持分批、断点续导，全量收藏也能覆盖
- **纯本地运行**：内容只落到你自己电脑上，图片/视频存 URL 不下载（CDN 地址裸请求可访问）

## 前提（必须装）

- **必须装 webclaw3**：本 skill 靠 webclaw3 打开你已登录的xhs收藏夹，不装跑不了。
  - 装好后先检查通道：`node <webclaw3安装路径>/scripts/webclaw3.mjs doctor`
  - 路径一般在 `~/.claude/skills/webclaw3` 或 `~/.workbuddy/skills/webclaw3`
- 浏览器里已登录xhs（导出的就是当前登录账号的收藏）。

## 怎么用

```bash
node skill.mjs <input.json>
```

input.json：

| 参数 | 说明 | 默认 |
|---|---|---|
| `offset` | 从第几篇开始（分批续导用） | 0 |
| `count` | 本次导出篇数上限 | 10 |
| `outputDir` | 输出目录 | 当前目录下 `xhs-fav-export-output/` |

输出：`<序号>_<笔记名>.md` 每篇一个 + `summary.json` 汇总。

## 常见问题

- **导出的不是收藏？** 大概率是旧版 bug，已修复（自动点击「收藏」tab + 过滤「笔记」tab 残留），升级后即正常。
- **一次没导完？** 收藏懒加载依赖真实滚动，一次运行可能加载不全；用 `offset/count` 分批、断点续导即可覆盖全部。
- **图片打不开？** 图片/视频是 CDN 签名 URL（有一定时效），导出后尽快查看；长期保存建议后续版本支持下载本地。
