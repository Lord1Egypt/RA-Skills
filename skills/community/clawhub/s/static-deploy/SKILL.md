---
name: static-deploy
description: |
  静态站点部署助手。覆盖构建产物校验、以及多种部署目标的发布流程：CloudStudio 沙箱、EdgeOne Pages、Netlify、Vercel、GitHub Pages。当用户需要"部署网站""发布前端""上线这个页面""部署到云"时调用。
agent_created: true
visibility: "public"
---

# 静态站点部署助手

帮助用户把本地构建产物（含 index.html 的目录）可靠地发布到云上，并拿到可访问 URL。核心：**先校验产物，再选目标，最后发布并验证**。

## 适用场景
- 单页 HTML / 多页站点 / React·Vue·Vite 构建产物上线
- 想把生成物（报告、PPT、简历页）一键变成可分享链接
- 对比不同部署平台的成本与适用面

## 部署目标速查

| 目标 | 适合 | 入口 |
|------|------|------|
| CloudStudio 沙箱 | 任意静态目录，免配置，国内可达 | `workbuddy_cloudstudio_deploy` 工具 |
| EdgeOne Pages | 国内加速、绑定域名 | `edgeone-pages-deploy` 技能 |
| Netlify / Vercel | 海外、CI 友好、自动 HTTPS | CLI / Git 集成 |
| GitHub Pages | 开源项目页、文档站 | `github-pages-auto-deploy` 技能 |

> WorkBuddy 已内置 `workbuddy_cloudstudio_deploy` 工具，可直接把本地目录部署到 CloudStudio 沙箱并返回访问 URL——这是最省心的默认路径。

## 标准工作流

### 1. 校验构建产物
使用 `scripts/deploy_check.py` 确认目录可作为静态站发布：
```bash
python scripts/deploy_check.py /path/to/dist
```
输出：是否存在 index.html、入口文件列表、总体积、是否含明显错误文件。

### 2. 选择并发布
- **默认（最快）**：调用 `workbuddy_cloudstudio_deploy`，目录填构建输出目录（如 `dist/`）。
- **国内加速**：用 `edgeone-pages-deploy` 技能，支持自定义域名。
- **海外/CI**：Netlify/Vercel CLI（`npx netlify-cli deploy --prod --dir dist`）。
- **开源文档**：`github-pages-auto-deploy`。

### 3. 发布后验证
- 拿到 URL 后用 `web-fetch` 技能抓取首页，确认状态码 200 且关键内容存在。
- 记录本次部署 URL 到技能记忆，便于下次更新。

## 质量门禁
- [ ] 目录含 `index.html`（否则部署后无入口）
- [ ] 资源引用为相对路径（避免 404）
- [ ] 体积合理（过大考虑压缩/分包）
- [ ] 发布后实际可访问（curl/抓取验证）

## 自进化学习系统
```bash
python scripts/learner.py record . --capability "静态站部署" [--fail --error <类型> --note <说明>]
python scripts/learner.py insight .
python scripts/learner.py reflect .
```
- 某目标连续失败 → 记录 `error`，reflect 建议切换默认目标
- 用户偏好某平台 → `prefer` 记录

## 安全边界
- 不部署含密钥/私钥的目录；部署前检查 .env、credentials 是否被误打包
- 不修改用户的版本库主分支，除非明确要求
