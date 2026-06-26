# CLAUDE.md

## 项目概述

weread-import：将微信读书划线与想法导出为 Markdown，支持 Obsidian。既是 npm CLI 工具，也是 clawhub skill。

## 模块结构

```
src/
  cli.mjs              ← CLI 入口（parseArgs + main）
  index.mjs            ← 编程接口导出
  api.mjs              ← 微信读书 API 请求（wereadFetchJson 等）
  cookie.mjs           ← Cookie 提取（浏览器 CDP / 手动）
  entries.mjs          ← 条目构建、比较、分组
  render.mjs           ← Markdown 渲染、frontmatter 生成、文件写入
  merge.mjs            ← 增量合并统计、已删除内容处理
  markdown-parser.mjs  ← 从现有 Markdown 提取结构化数据
  state.mjs            ← 同步状态文件读写
  errors.mjs           ← WereadAuthError / WereadApiError
  utils.mjs            ← sanitizeFileName / cleanText / yamlScalar
```

## 关键约定

- **ESM only**：`"type": "module"`，所有文件使用 `.mjs` 扩展名
- **唯一运行时依赖**：`playwright`（不使用 dotenv，环境变量由调用方负责）
- **错误分类**：`WereadAuthError`（登录/鉴权问题）和 `WereadApiError`（其他 API 错误）
- **测试**：使用 Node.js 内置 `node:test`，零额外依赖；运行 `npm test`
- **Skill 入口**：`scripts/run.sh`，首次运行自动 `npm install --production`

## 文案风格

- 文档和用户可见的错误提示使用中文
- 引用书名、按钮名等使用中文引号「」
- 错误提示简洁直接，如 `"HTTP 401 错误: ..."` 而非 `"请求失败 401: ..."`
- 代码注释只写必要的解释，不留 changelog 性质的内容

## 常用命令

```bash
npm test                          # 运行测试
node --check src/cli.mjs          # 语法检查
node src/cli.mjs --book "书名" --mode api --cookie-from browser --output "/path"
bash scripts/run.sh --all --mode api --cookie-from browser --output "/path"
```
