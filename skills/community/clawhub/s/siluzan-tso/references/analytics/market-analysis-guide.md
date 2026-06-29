# 战略市场分析（Market Analysis）

> 对齐 TSO Copilot `getMarketReport` 业务目标；**Skill/CLI 场景**与网页版分工不同：
>
> - **TSO 网页**：Copilot 工具内调 `aisearch` 一次生成 HTML
> - **siluzan-tso Skill**：`collect` 只落盘上下文 → **宿主 Agent** WebSearch/WebFetch 调研 → 写 `market-report.json` → `render` 出 HTML

**质量门禁**（见 `assets/market-analysis-rules.md`）：`render` 按 **原始业务维度清单** 校验必含内容，缺项失败（非文件大小）。

与「网站诊断」模式一致：**CLI 拉原料，Agent 写报告，CLI 渲染终稿**。

> **常见入口（仅指定行业）**：用户说「帮我生成一份**电商行业**的行业分析报告」且未给公司名/官网时，**仍须走本流程**——不要改用 WebSearch 直接在聊天里写报告。
>
> ```bash
> siluzan-tso market-analysis collect --industry "电商" --json-out ./snap-market
> ```
>
> 缺目标市场/时间范围时用默认并在 HTML 中写明（全球 / 近12个月）；有客户名或官网时再补 `--customer-name` / `--website`。

---

## 与相近能力区分

| 能力             | 入口                                           | 说明                                 |
| ---------------- | ---------------------------------------------- | ------------------------------------ |
| **战略市场分析** | `market-analysis collect` + Agent + `render`   | KA 战略报告（公开数据 + Agent 归纳） |
| **网站诊断**     | `website-diagnosis collect` + Agent + `render` | 落地页 6 模块评分                    |
| **账户周期报告** | `google-analysis`                              | 广告投放数据                         |
| **拓词市场指标** | `keyword suggest`                              | Keyword Planner 搜索量/CPC           |

---

## CLI 命令

```bash
# 1. 采集原料（须 --json-out）
siluzan-tso market-analysis collect \
  --customer-name "示例公司" \
  --website https://www.example.com \
  --industry "工业设备" \
  --target-market "北美" \
  --json-out ./snap-market

# 2. Agent 读 rules → WebSearch → 写 market-report.json（见下节）

# 3. 渲染终稿
siluzan-tso market-analysis render \
  --data ./snap-market/market-report.json \
  --out ./snap-market/market-analysis-report.html
```

| 子命令    | 网络请求                                                | 说明                  |
| --------- | ------------------------------------------------------- | --------------------- |
| `collect` | 可选 `POST Agent /download-assets`（有 `--website` 时） | 不调用 aisearch       |
| `render`  | 无                                                      | 读取本地 JSON 写 HTML |

有 `--website` 时走 Agent 网关（与 `website-diagnosis collect` 相同）：`SILUZAN_AGENT_BASE` / `agent.mysiluzan.com`。

---

## 输入参数

| 参数         | CLI 选项              | 必填     | 默认                      |
| ------------ | --------------------- | -------- | ------------------------- |
| 客户名称     | `--customer-name`     | 四选一\* | —                         |
| 客户网站     | `--website`           | 四选一\* | —                         |
| 所属行业     | `--industry`          | 四选一\* | —                         |
| 核心产品     | `--core-products`     | 四选一\* | —                         |
| 商业定位     | `--business-position` | 否       | —                         |
| 目标市场     | `--target-market`     | 否       | 全球                      |
| 时间范围     | `--time-range`        | 否       | 近12个月                  |
| 跳过官网抓取 | `--skip-website`      | 否       | 有 website 时默认抓取预览 |

\* 客户名称、网站、行业、核心产品**至少提供一项**。

---

## Agent 标准流程（P9）

1. 确认客户信息（上表至少一项；默认目标市场/时间范围须写明）。
2. `market-analysis collect … --json-out ./snap-market`（**必须** `--json-out`）。
3. Read `assets/market-analysis-rules.md` + `report-templates/market-analysis-report.md`。
4. 用 **WebSearch / WebFetch** 补充行业、竞品、区域市场公开数据；结合 collect 的 `websitePreview`（若有）。
5. 按 rules 生成完整 HTML，**脚本落盘**为 `./snap-market/market-report.json`（字段 `htmlContent`；勿在对话贴全文）。
6. 执行：
   ```bash
   siluzan-tso market-analysis render --data ./snap-market/market-report.json --out ./snap-market/market-analysis-report.html
   ```
7. 向用户交付 HTML 路径；说明需联网加载 Bootstrap / ECharts CDN（`homeCDN/echarts.js`）。

**禁止**跳过 `render` 直接把聊天里的 HTML 当终稿；**禁止**编造无来源的具体数据。

---

## 输出契约

### collect（`market-analysis-collect.json`）

```json
{
  "customerInfo": {
    "customerName": "…",
    "website": "…",
    "targetMarket": "北美",
    "timeRange": "近12个月"
  },
  "targetMarket": "北美",
  "timeRange": "近12个月",
  "collectedAt": "2026-06-05T12:00:00.000Z",
  "websitePreview": "…前 8KB…",
  "agentHint": "…"
}
```

### Agent 产出（`market-report.json`）

```json
{
  "customerInfo": { "…": "与 collect 一致" },
  "targetMarket": "北美",
  "generatedAt": "2026-06-05T12:30:00.000Z",
  "htmlContent": "<!DOCTYPE html>…"
}
```

---

## 相关文档

- `assets/market-analysis-rules.md` — 章节、数据口径、HTML 版式（**Agent 必读**）
- `report-templates/market-analysis-report.md` — 交付检查清单
- `references/core/playbooks.md` — **P9**
