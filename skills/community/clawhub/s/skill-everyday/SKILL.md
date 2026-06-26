---
name: skill-everyday
description: 每天抓取 Clawhub 热门技能，深入分析并生成报告。每次执行获取一个未分析过的热门技能，避免重复。
metadata:
  {
    "openclaw": {
      "emoji": "📊",
      "requires": { "modules": ["playwright"] }
    }
  }
---

# 技能分析日报 (skill-everyday)

每天执行一次，抓取 Clawhub 热门技能，深入分析并生成报告。

## 特性

- **无需平台账号或 API Key**：榜单与详情来自公开页面；运行期状态只写在本地 `data/`。
- **去重**：按 `data/analyzed.json` 记录已分析 slug，每次只取「当前榜单中、未分析过的第一个」热门技能。
- **依赖需先行安装**：本技能依赖 **Node.js**、**Playwright** 与 **Chromium**（见下方「依赖」）。装好后再执行脚本即可，无需编辑配置文件。

## 目录结构

```
skill-everyday/
├── SKILL.md              # 本文件
├── README.md             # 安装与运行（给人看的简要说明）
├── package.json          # 可选：声明 playwright 依赖，便于 npm install
├── data/
│   ├── analyzed.json     # 已分析技能列表（自动管理）
│   └── reports/          # 每日报告
│       └── YYYY-MM-DD-<slug>.md
└── scripts/
    └── runner.mjs        # 执行脚本
```

首次运行 `scripts/runner.mjs` 时会自动创建 `data/`、`data/reports/`（若不存在），并初始化 `data/analyzed.json`。

## 使用方法

在**本技能根目录**（`SKILL.md` 所在目录）执行：

```bash
node scripts/runner.mjs
```

或在 OpenClaw 中按触发语调用本技能后，由 Agent 执行上述命令。

## 工作流程

### 1. 获取热门技能列表

使用 Playwright 访问 `clawhub.ai/skills` 并拦截页面请求的 Convex `api/query` 响应以取得榜单数据：

```javascript
import { chromium } from 'playwright';

let apiData = null;
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();

await page.route('https://wry-manatee-359.convex.cloud/api/query', async route => {
  const response = await route.fetch();
  const data = await response.json();
  apiData = data;
  route.continue();
});

await page.goto('https://clawhub.ai/skills', { waitUntil: 'networkidle' });
await page.waitForTimeout(3000);

const result = apiData?.status === 'success' ? apiData.value : apiData;
const skills = result?.page || [];
// 按下载量排序
skills.sort((a, b) => (b.skill?.stats?.downloads || 0) - (a.skill?.stats?.downloads || 0));
```

### 2. 避免重复分析

从技能根目录下的 `data/analyzed.json` 读取已分析列表（路径以 `SKILL.md` 为锚：`path.join(skillRoot, 'data', 'analyzed.json')`）。

```javascript
// 与 scripts/runner.mjs 一致：SKILL_DIR = dirname(scripts)，再拼 data/analyzed.json
const analyzedFile = path.join(SKILL_DIR, 'data', 'analyzed.json');
if (!analyzedData.analyzed.includes(skillSlug)) {
  // 分析该技能
}
```

### 3. 获取技能详情

打开技能详情页 `https://clawhub.ai/skill/{slug}`，读取标题、描述与页面正文（与榜单接口分离，非单独「完整信息」REST 文档）。

### 4. 尝试读取本地技能源码

在常见 OpenClaw 布局下，技能根目录的上一级为 `skills/`，据此拼接目标技能目录：

```javascript
const skillsRoot = path.join(SKILL_DIR, '..');
const targetSkillDir = path.join(skillsRoot, skillSlug);
```

### 5. 生成报告

按模板生成报告，保存到 `data/reports/YYYY-MM-DD-<slug>.md`（同日多次运行不会互相覆盖）。

### 6. 更新状态

自动更新 `data/analyzed.json` 添加新技能。

## 报告模板

- **内置深度模板的技能**（如 `self-improving-agent`）：标题行 + **核心原理** + Clawhub 简介 + 元数据表 + **一、核心工作原理（OpenClaw 主流实现）**（1～4 小节）+ **二、为什么受欢迎** + 可选榜单数据补充；不插入通用「技术/设计亮点」占位段落。
- **其他技能**：排名/名称/标识/分类/下载与点赞 + Clawhub 功能介绍 + **核心流程与特点**（默认模板）+ 可选榜单数据补充。

报告保存到 `data/reports/YYYY-MM-DD-<slug>.md`。

## 依赖

- **Node.js**：执行 `scripts/runner.mjs`（ESM）。
- **Playwright + Chromium**：若目录内有 `package.json`，可在技能根目录执行 `npm install`，再 `npx playwright install chromium`；否则全局或上级环境已安装 `playwright` 亦可。仅声明 `metadata.openclaw.requires` 不会自动安装浏览器。

## 触发方式

用户发送 "分析一个 Clawhub 技能" 或 "skill-everyday" 时执行。