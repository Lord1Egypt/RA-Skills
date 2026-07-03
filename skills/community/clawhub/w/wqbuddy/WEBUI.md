---
name: wq-buddy-webui
description: "Local Web UI for browsing the WQBuddy SQLite database (alphas / field tests / data fields / batches). Auto-shares login with the CLI. Read-only viewing and light interaction only — heavy work goes through CLI/agent."
---

# WQ-Buddy Web UI

本地数据库可视化查看器。**仅供本地使用，请勿暴露在公网**。

## 启动

```bash
# 源码方式（推荐开发/测试用）
npm run db-viewer

# 全局安装后（需要 wq-buddy 全局安装）
node "$(npm root -g)/wq-buddy/dist/db-viewer/server.js"
```

服务启动后访问 http://localhost:9876。`Ctrl+C` 停止。

## 登录

与 CLI 凭证打通，**任意一边登录后另一边自动免密**：

- CLI 登录会把 token 缓存到 `~/.wq-buddy/.wq_token.json`
- WebUI 启动时自动读取该文件，token 有效直接进入主界面
- WebUI 登录后也会写回同一份文件
- 两边都没登录时，在 WebUI 登录页输入 BRAIN 账号密码即可

Token 有效期约 4 小时。

## 功能

| 入口 | 作用 |
|------|------|
| 仪表盘 | 6 张统计卡 + 时间进度 + 最近活动 |
| Alpha 列表 | 浏览/搜索/排序/分页/详情/批量操作 |
| 批次记录 | 批量回测的批次元信息 |
| 字段测试运行 | 手动输入 1~10 个字段 + 选预设，结果写入 `field_tests` 表（"字段测试历史"页面查看全部记录） |
| 字段测试历史 | `field_tests` 表的全部历史记录 |
| 数据字段缓存 | 搜索过的 BRAIN 数据字段 |
| 操作日志 | 系统日志（最近 10 条） |

### Alpha 列表批量操作

- 单选时显示"查看详情"
- 多选时可：提交、复制 ID、在 BRAIN 打开、导出 CSV、删除

## 设计原则

WebUI 是**查看 + 轻交互**工具。**重活仍交给 CLI/Agent**：

- 批量回测 → CLI/Agent
- 批量字段测试 → CLI/Agent
- 数据集爬取 → CLI/Agent
- 复杂筛选/分析 → CLI/Agent

WebUI 上能做的："看一眼结果"、"手动跑一两个字段测试"、"导出选中的几个 alpha"。
