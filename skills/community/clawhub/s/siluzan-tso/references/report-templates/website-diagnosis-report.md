# 网站诊断报告

> **最终交付物：一份可打开的、带图表的 HTML 文件**（如 `website-diagnosis-report.html`），不是仅 Markdown 摘要。须含：综合得分环、模块雷达图、风险/模块条形图、Lighthouse 对比图（有数据时）。  
> 数据：`website-diagnosis collect` 落盘 JSON + Agent 按 `assets/website-diagnosis-rules.md` 生成的诊断 JSON

---

**siluzan-tso Skill / 纯 CLI 场景**：**Agent 只负责产出诊断 JSON**；终稿 HTML **必须**由 CLI 的 `render` 命令读取该 JSON 生成。**严禁** Agent 现场手写、拼接、或直接输出 HTML 作为交付物。

必须严格按以下三步顺序执行，**不得跳过任何一步**：

1. **采集原料**（拿到 Lighthouse + 首页 HTML，落盘 JSON）：

```bash
siluzan-tso website-diagnosis collect --url <网站URL> --json-out ./out
```

2. **生成诊断 JSON**：Agent 依据上一步原料 + `assets/website-diagnosis-rules.md` 规则，产出 **诊断结果 JSON**（落盘为 `./out/diagnosis.json`，结构见下文「数据字段速查」）。**此步只能输出 JSON，不能输出 HTML。**

3. **用 JSON 调用 render 生成 HTML**（唯一允许产出 HTML 的方式）：

```bash
siluzan-tso website-diagnosis render --data ./out/diagnosis.json [--collect ./out/collect.json] --out ./website-diagnosis-report.html
```

> 口诀：**没有诊断 JSON，就不能 render；不经过 render，就没有 HTML 交付物。**

模板源码：

- `report-templates/website-diagnosis-report.html` — 结构与样式
  `render` 会向输出目录写入 HTML + runtime.js，并注入 `window.__WEBSITE_DIAGNOSIS__`。

---

## HTML 章节清单（须全部出现）

| 区块 ID / 组件   | 内容                                                                   |
| ---------------- | ---------------------------------------------------------------------- |
| `ReportHeader`   | 标题「网站诊断报告」、URL、`analyzedAt`、综合得分与等级色              |
| `HealthOverview` | 总分、行业对比文案、`ratingId` 说明、**ECharts 雷达图** + 得分环       |
| `RiskMap`        | `coreIssuesIds` 列表 + **模块得分横向条形图**（对齐前端 RiskMap）      |
| `ModuleDetail`   | 6 模块 × 子项：得分、status、issue、suggestion（表格或卡片）           |
| `PriorityPlan`   | 高/中/低优先级改进计划（来自核心问题 + 低分子项）                      |
| `LoadingSpeed`   | **Lighthouse 柱状对比图** + desktop/mobile 指标表；缺失时 callout 说明 |
| `LongtermValue`  | 投放建议、长期优化价值（与 s1–s5 评级一致）                            |

生成前可对 JSON 做与前端相同的聚合逻辑：各模块 `score` = 子项得分之和

---

## 样式与文件约定

- 单文件 HTML，`lang` 与用户语言一致（默认 `zh-CN`）。
- ECharts 统一引用：`https://staticpn.siluzan.com/assets/slz/homeCDN/echarts.js`（与 `report-template.html` 相同）。
- 落盘建议与 `--json-out` 同目录：`website-diagnosis-report.html`。
- **唯一生成方式**：先产出诊断 JSON，再 `siluzan-tso website-diagnosis render --data <diagnosis.json> [--collect <collect.json>]`（详见顶部「强制流程」）。
- **禁止**只交付 Markdown 或纯 JSON 当作最终报告（JSON 仅为 render 的输入/中间产物）。
- **禁止**绕过 render 直接手写或拼接 HTML。

---

## 数据字段速查

| 字段                              | HTML 中的用法                                      |
| --------------------------------- | -------------------------------------------------- |
| `url`                             | 报告头、页脚                                       |
| `analyzedAt`                      | 诊断时间                                           |
| `ratingId`                        | 等级徽章（s1–s5 → 优秀…不建议投放）                |
| `score`                           | 总分（可由 modules 汇总）                          |
| `coreIssuesIds`                   | RiskMap / 优先改进                                 |
| `modules[].id`                    | m1–m6 分节标题                                     |
| `modules[].items[]`               | 子项行：诊断项名、得分/满分、issue、suggestion     |
| `lighthouse` / `lighthouseResult` | LoadingSpeed 节（collect payload 为 `lighthouse`） |

---

## 可选附录（非必须单独成章）

- 与 Google 账户衔接：引导 `google-analysis` / 广告诊断页（勿混淆两种「诊断」）。
