---
name: kuanshu-tiku
description: 宽数题库项目入口，涵盖五套量化题库来源、仓库结构、常用命令、公式渲染约束与当前公网部署信息。
---

# 宽数题库

## 用途

当你需要查看、运行、扩展或部署“宽数题库”这个多来源量化题库项目时，使用这个技能。

适合这些场景：

- 需要快速理解项目是什么、当前公开站点是什么
- 需要确认仓库中已经接入了哪些题库来源
- 需要知道原始抓取、标准化数据和页面代码分别放在哪里
- 需要重新抓取、构建或检查部署前置条件

## 项目资源

- GitHub 仓库：https://github.com/aznikline/Quantics-Bank
- 当前公开站点：https://quantics-bank.vercel.app

## 当前接入的题库来源

- OpenQuant：`openquant.co/questions`
- Brainstellar：`brainstellar.com/puzzles`
- QuantQuestion：`quantquestion.com`
- Jane Street：`janestreet.com/puzzles`
- MyntBit：`myntbit.com`

当前总题量：1454 道。

## 目录结构

- `data/raw/`
  说明：五套来源的原始索引与详情数据
- `data/translations/`
  说明：中文翻译与分批翻译产物
- `src/data/questions.json`
  说明：OpenQuant 标准化数据
- `src/data/brainstellar-questions.json`
  说明：Brainstellar 标准化数据
- `src/data/quantquestion-questions.json`
  说明：QuantQuestion 标准化数据
- `src/data/janestreet-questions.json`
  说明：Jane Street 标准化数据
- `src/data/myntbit-questions.json`
  说明：MyntBit 标准化数据
- `src/pages/index.astro`
  说明：首页
- `src/pages/questions/[slug].astro`
  说明：统一详情页
- `scripts/`
  说明：抓取、构建、翻译和部署检查脚本

## 常用命令

安装依赖：

```bash
npm install
```

抓取与构建：

```bash
npm run data:index
npm run data:details
npm run data:brainstellar:index
npm run data:brainstellar:details
npm run data:brainstellar:build
npm run data:quantquestion:fetch
npm run data:quantquestion:build
npm run data:janestreet:index
npm run data:janestreet:details
npm run data:janestreet:translate
npm run data:janestreet:build
npm run data:myntbit
npm run data:validate
npm run data:build
```

本地开发与验证：

```bash
npm run dev
npm run test
npm run check
npm run build
```

## 托管与发布

- GitHub 仓库保持 private
- 公网托管走 Vercel
- 生产域名为 `https://quantics-bank.vercel.app`

Vercel 常用命令：

```bash
npx vercel whoami
npx vercel deploy dist --prod --yes
```

## 工作建议

如果你是第一次接手这个项目，建议按这个顺序：

1. 读 `README.md`
2. 跑 `npm run data:validate`
3. 跑 `npm run build`
4. 看 `src/pages/index.astro` 与 `src/pages/questions/[slug].astro`
5. 如果改抓取链，再读 `scripts/`

## 公式渲染约束

OpenQuant 原题和中文翻译中的 TeX source 必须保持原样。渲染器只做安全分隔符归一化，不做语义改写；不要把 `\operatorname`、`\textrm`、`\mod`、`\dbinom` 或 `equation` 环境改成其他命令来“修正”显示。若页面显示 KaTeX 错误，应先检查源数据本身，而不是在渲染层做猜测性替换。

## 什么时候用这个技能

- 想快速知道这个项目现在有哪些题库来源
- 想确认某道题属于哪个来源
- 想重新拉取 Brainstellar / Jane Street / MyntBit 等来源
- 想把本地最新内容重新部署到 Vercel
