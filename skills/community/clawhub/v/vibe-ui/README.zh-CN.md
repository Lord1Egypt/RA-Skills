# Vibe UI

<p align="center">
  <a href="README.md">English</a>
  ·
  <a href="README.zh-CN.md"><strong>简体中文</strong></a>
</p>

<p align="center">
  <img alt="版本 1.1.0" src="https://img.shields.io/badge/version-1.1.0-2563eb?style=for-the-badge">
  <img alt="测试通过" src="https://img.shields.io/badge/tests-passing-22c55e?style=for-the-badge">
  <img alt="Node.js" src="https://img.shields.io/badge/runtime-Node.js-475569?style=for-the-badge">
  <img alt="本地优先" src="https://img.shields.io/badge/local--first-DESIGN.md-7c3aed?style=for-the-badge">
</p>

一个本地优先的 `DESIGN.md` 工作流 Skill，用于 Web UI 生成、风格选择、Design Read、提示词生成和设计一致性检查。

Vibe UI 帮助 AI 编程助手选择视觉风格、写入设计上下文、生成页面提示词、执行实现前质量门禁，并检查生成后的 UI 代码。Vibe UI 自有工作流能力统一使用 **Vibe Gate**、**Vibe UI template recipes** 等命名。上游项目名称只用于来源筛选、资源 id、溯源和归因，避免和 Open Design / Kami 出现同名。

## 功能

- 18 个精选内置风格，适合高置信默认推荐。
- 150 个上游 `DESIGN.md` 系统，离线打包在 `resource/open-design-systems.json`。
- 从 `Liuwei1125/vibe-ui-resources` 索引的 111 个上游 `design-templates`。
- 从上游模式提炼的 Vibe UI 模板配方，包括购物、电商、产品发布、定价、等待名单、文档、后台、看板、移动端、引导、作品集和 SaaS。
- Vibe Gate 2.0 执行链路：`read`、`workflow`、`invariants`、`brief-check`、`generate`、`report`、`critique` 和 `polish`。
- Design Read 会输出 audience、buyer anxiety、register、density/variance/motion 三拨盘、proof strategy 和 section strategy。
- 可生成本地静态风格浏览器，支持筛选和复制命令。
- 设计一致性检查，包含评分、阻塞项、综合判断和 Bad/Fix/Evidence 指导。
- 发布包模式：`minimal`、`standard`、`offline-full`。

## 快速开始

```bash
cd skills/vibe-ui
npm test
node scripts/design.mjs list
node scripts/design.mjs recommend "面向前端工程师的 AI SaaS 落地页"
```

在任意项目根目录应用设计：

```bash
node /absolute/path/to/skills/vibe-ui/scripts/design.mjs use linear
node /absolute/path/to/skills/vibe-ui/scripts/design.mjs read "面向前端工程师的 AI SaaS 落地页" --page landing --design linear
node /absolute/path/to/skills/vibe-ui/scripts/design.mjs workflow landing --design linear --target src/app/page.tsx
node /absolute/path/to/skills/vibe-ui/scripts/design.mjs brief-check landing --design linear
node /absolute/path/to/skills/vibe-ui/scripts/design.mjs generate landing
node /absolute/path/to/skills/vibe-ui/scripts/design.mjs report src/app/page.tsx
node /absolute/path/to/skills/vibe-ui/scripts/design.mjs critique src/app/page.tsx
node /absolute/path/to/skills/vibe-ui/scripts/design.mjs polish src/app/page.tsx
```

需要更大的离线上游参考库时：

```bash
node scripts/design.mjs list --source open-design
node scripts/design.mjs use open-design:linear-app
node scripts/design.mjs template vibe:commerce-home
node scripts/design.mjs generate landing --template vibe:commerce-home
```

执行 `use` 后会写入：

- `DESIGN.md`
- `DESIGN.generated.md`
- `.vibe-ui/current-design.json`

执行 `read` 后会写入：

- `.vibe-ui/brief-read.json`
- `.vibe-ui/product-context.json`

## 命令

```bash
node scripts/design.mjs list [--source built-in|open-design|all]
node scripts/design.mjs search <keyword> [--source built-in|open-design|all]
node scripts/design.mjs recommend "<user goal>" [--source built-in|open-design|all]
node scripts/design.mjs read "<brief>" [--page page_type] [--design design_id] [--template template_id] [--source built-in|open-design|all]
node scripts/design.mjs use <design_id>
node scripts/design.mjs like <design_id> [page_type] [--strength light|medium|bold]
node scripts/design.mjs remix <primary_design_id> <secondary_design_id> [goal]
node scripts/design.mjs workflow <page_type> [--design design_id] [--template template_id] [--target file_or_directory]
node scripts/design.mjs template <template_id>
node scripts/design.mjs generate <page_type> [--template template_id]
node scripts/design.mjs invariants <design_id>
node scripts/design.mjs brief-check <page_type> [--design design_id] [--template template_id]
node scripts/design.mjs check <file_or_directory>
node scripts/design.mjs report <file_or_directory> [--out DESIGN-REPORT.md]
node scripts/design.mjs browse [--source built-in|open-design|all] [--out directory]
node scripts/design.mjs preview [--source built-in|open-design|all] [--out directory]
node scripts/design.mjs submit <design_id> <DESIGN.md> [--name display_name]
node scripts/design.mjs extract-url <url_or_html_file> [--out DESIGN.md]
node scripts/design.mjs import <figma_or_screenshot_notes> [--kind figma|screenshot] [--out DESIGN.md]
node scripts/design.mjs critique <file_or_directory> [--out directory]
node scripts/design.mjs polish <file_or_directory>
node scripts/sync-open-design.mjs
node scripts/publish-kit.mjs --platform all --package minimal|standard|offline-full [--dry-run|--check]
```

资源同步优先使用 companion 资源镜像库：

```bash
node scripts/sync-open-design.mjs --resources-repo /path/to/vibe-ui-resources
```

只有维护者需要直接从上游同步时才使用：

```bash
node scripts/sync-open-design.mjs --upstream-open-design
```

## Vibe Gate

视觉或用户可见页面实现前，建议先运行 Vibe Gate 2.0：

```bash
node scripts/design.mjs read "面向医疗合规团队的 AI 发布治理落地页" --page landing --design cursor --template open-design:saas-landing
node scripts/design.mjs workflow landing --design open-design:linear-app --template open-design:saas-landing --target src/app/page.tsx
node scripts/design.mjs invariants open-design:linear-app
node scripts/design.mjs brief-check landing --design open-design:linear-app --template open-design:saas-landing
node scripts/design.mjs generate landing --template open-design:saas-landing
```

`read` 会写入隐藏的 Design Read 和轻量 PRODUCT.md 式上下文。`brief-check` 会写入 `.vibe-ui/vibe-gate-contract.json`，其中包含三拨盘、proof strategy、页面级 preflight 和根据 brief 生成的 anti-pattern watchlist。Design Read、dials 和内部脚手架文字不应该渲染到真实页面里。

实现完成后运行：

```bash
node scripts/design.mjs report src/app/page.tsx
node scripts/design.mjs critique src/app/page.tsx
node scripts/design.mjs polish src/app/page.tsx
```

## 来源模式

- `built-in`：Vibe UI 精选内置风格，默认模式。
- `open-design`：150 个本地上游系统，使用 `open-design:<slug>` 形式引用。
- `all`：内置风格加上离线上游资源库。

## 发布包

```bash
node scripts/publish-kit.mjs --platform all --package minimal --dry-run
node scripts/publish-kit.mjs --platform all --package standard --dry-run
node scripts/publish-kit.mjs --platform all --package offline-full --dry-run
node scripts/publish-kit.mjs --platform all --package offline-full --check
```

- `minimal`：核心 Skill 文件、registry、CLI、prompts、icon 和 Vibe Gate watchlist。
- `standard`：在 `minimal` 基础上加入 attribution、模板索引、模板配方、资源 manifest 和精选源设计文件。
- `offline-full`：在 `standard` 基础上加入 150 个系统的离线资源包和完整模板 source bundle。

## 市场更新

更新到 Skill 市场时，建议先发布新的 GitHub tag 和 Release，再把推荐包上传到市场表单。

1. 更新 `package.json`、`registry.json` 和 `CHANGELOG.md` 到新版本。
2. 运行 `npm run release:check`、`npm run release:dry-run`、`npm run release:smoke` 和 `npm run release:zip`。
3. 推送 `main`，创建新的 `vX.Y.Z` tag，并在 GitHub Release 中上传三个 zip。
4. 默认上传 `vibe-ui-standard-skill.zip` 到市场，除非平台明确要求最小包。
5. 只有市场或审核方需要完整离线 150 系统资源和完整模板 source bundle 时，才上传 `vibe-ui-offline-full-skill.zip`。
6. 市场更新说明直接复制 `CHANGELOG.md` 中对应版本的摘要。

## 仓库说明

如果发布到公开 GitHub 仓库，建议不要把 `dist/` 等生成产物提交到 git。需要发布 zip 时，使用 GitHub Releases 更合适。

## 归因

Vibe UI 为离线搜索和应用打包了上游设计资源。来源和许可证说明见 `resource/open-design-attribution.md`。

## 免责声明

内置和上游风格都只是基于公开可见 UI 模式的灵感参考，不是官方品牌系统。不要复制真实 Logo、商标、专有素材、截图或官方品牌声明。
