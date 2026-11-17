# wx-huitu — 公众号数据绘图专家

[![ClawHub](https://img.shields.io/badge/ClawHub-wx--huitu-blue)](https://clawhub.ai/skills/wx-huitu)
[![SkillHub](https://img.shields.io/badge/SkillHub-wx--huitu-green)](https://skillhub.cn/skills/wx-huitu)
[![版本](https://img.shields.io/badge/版本-2.2.0-brightgreen)](https://github.com/EdwardWason/wx-huitu)
[![协议](https://img.shields.io/badge/协议-MIT--0-lightgrey)](LICENSE)

输入文章或数据描述，输出公众号内嵌图表 PNG 包。

## 核心特性

- **18 种版式** (C01-C18)：柱状/折线/饼图/面积/雷达/散点/漏斗/热力/仪表盘/混合图表等
- **三轴决策框架**：变量类型 × 论证意图 × 数据形态 → 自动推荐最适图型
- **8 条拦截规则**：主动拦截不当选择（2 点折线/7+类别饼图/单值做图等）
- **色盲安全**：Okabe-Ito 8 色色板 + 冗余编码
- **三套财经配色**：麦肯锡/经济学人/财新
- **Puppeteer 截图交付**：HTML → PNG → 桌面文件夹 → 飞书云盘同步

## 工作流

```
输入 → Step 1: 数据剖析(静默) → Step 2: 版式推荐(确认) → Step 3: 风格+生成HTML → Step 4: 截图交付+云盘同步
```

## 使用方式

在 TRAE IDE 中说：
- "文章绘图"
- "绘图图表"
- "画个图表"
- "数据图"
- "公众号图表"

## 不适用范围

- 封面/封底 → 用 wx-peitu
- 金句图/宣言卡/转场卡 → 用 wx-peitu
- 全文配图方案 → 用 wx-peitu
- 代码编辑 → 用代码工具
- 交互式图表 → 用 plotly/echarts 独立部署

## ⚠️ 用户须知

本技能运行时会：
1. **自动写入本地文件**：PNG 图片保存到桌面文件夹
2. **调用 subprocess**：运行 Puppeteer-core 进行浏览器截图（需要系统安装 Chrome 或 Edge）
3. **网络请求**：加载 Google Fonts（Inter / Noto Sans SC）

**可选操作（默认关闭，需用户明确确认）**：
4. **飞书云盘上传**：仅当用户明确说"同步飞书"或"上传云盘"时执行。生成的图表（可能含文章源数据）会上传到外部飞书云存储。用户可随时说"不同步"跳过。

## 文件结构

```
wx-huitu/
├── SKILL.md              # 技能定义（frontmatter + 工作流 + 版式 + CSS + 规则）
├── README.md             # 本文件
├── CHANGELOG.md          # 变更日志
├── LICENSE               # MIT-0
├── .gitignore
├── .claude-plugin/
│   └── plugin.json
└── references/
    ├── workflow.md       # 完整4步工作流
    ├── chart-system.md   # 18种版式+三轴决策树+拦截规则+HTML骨架
    └── design-tokens.md  # 设计令牌：配色+字号+间距+画幅
```

## 协议

MIT-0 — 自由使用、修改和分发，无需署名。

---

# wx-huitu — WeChat Article Chart Expert

[![ClawHub](https://img.shields.io/badge/ClawHub-wx--huitu-blue)](https://clawhub.ai/skills/wx-huitu)
[![SkillHub](https://img.shields.io/badge/SkillHub-wx--huitu-green)](https://skillhub.cn/skills/wx-huitu)
[![Version](https://img.shields.io/badge/version-2.2.0-brightgreen)](https://github.com/EdwardWason/wx-huitu)
[![License](https://img.shields.io/badge/license-MIT--0-lightgrey)](LICENSE)

Input an article or data description, output a WeChat article chart PNG package.

## Key Features

- **18 Chart Types** (C01-C18): bar/line/donut/area/radar/scatter/funnel/heatmap/dashboard/mixed charts, etc.
- **Three-Axis Decision Framework**: Variable type × Argument intent × Data shape → Auto-recommend best chart
- **8 Interception Rules**: Proactively block inappropriate choices (2-point line / 7+ category pie / single-value chart, etc.)
- **Colorblind-Safe**: Okabe-Ito 8-color palette + redundant encoding
- **Three Financial Color Schemes**: McKinsey / The Economist / Caixin
- **Puppeteer Screenshot Delivery**: HTML → PNG → Desktop folder (Feishu cloud sync is optional, requires user confirmation)

## Workflow

```
Input → Step 1: Data Profiling (silent) → Step 2: Chart Recommendation (confirm) → Step 3: Style + Generate HTML → Step 4: Screenshot & Deliver
```

## Usage

Say in TRAE IDE:
- "文章绘图" / "绘图图表" / "画个图表" / "数据图" / "公众号图表"

## Out of Scope

- Cover/back cover → use wx-peitu
- Quote cards / transition cards → use wx-peitu
- Full article illustration → use wx-peitu
- Code editing → use code tools
- Interactive charts → use plotly/echarts standalone

## ⚠️ User Notice

This skill will:
1. **Write local files**: PNG images saved to desktop folder
2. **Call subprocess**: Run Puppeteer-core for browser screenshots (Chrome required)
3. **Network requests**: Load Google Fonts (Inter / Noto Sans SC)

**Optional actions (off by default, require explicit user confirmation)**:
4. **Feishu cloud upload**: Only executed when user explicitly says "同步飞书" or "上传云盘". Generated charts (may contain article source data) will be uploaded to external Feishu cloud storage. User can say "不同步" to skip at any time.

## License

MIT-0 — Free to use, modify, and redistribute. No attribution required.
