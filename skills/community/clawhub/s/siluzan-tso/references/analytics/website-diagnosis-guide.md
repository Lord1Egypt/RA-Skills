# 网站诊断（Website Diagnosis）

> 对齐 Aiagent-Server `agent/tso_agent`：`getWebsiteDiagnosisData`（`website_diagnosis_tools.py` + `data/website_guide.py`）。  
> **CLI 负责拉数**；**6 模块 × 29 子项评分**由 Agent 按规则 + 采集数据生成 JSON。  
> **最终交付**：与线上一致，为**一份可浏览器打开、含 ECharts 图表的单文件 HTML 报告**（雷达图、模块得分条形图、Lighthouse 对比图等）。**用户未指定格式时默认交付 HTML**；Skill/CLI **Agent 只写诊断 JSON，HTML 一律由 `website-diagnosis render` 生成**（禁止 Agent 手写 HTML，禁止仅 Markdown/JSON 充当终稿）。

> **硬约束（100% CLI）**：凡 P8（含「诊断网站 / 是否符合广告投放要求 / 能不能投」+ URL），**必须**执行 `siluzan-tso website-diagnosis collect`（及后续 prepare/render）。**禁止**仅用 WebFetch / 浏览器打开官网 / 通用搜索写「是否符合 Google 广告」结论当交付。

---

## CLI 命令

```bash
# 推荐：一次采集 Lighthouse + 首页 HTML（落盘含 signals / dataAvailability）
siluzan-tso website-diagnosis collect --url https://www.example.com --json-out ./snap-web
# --include-html 仅把完整 HTML 写入落盘；signals 已按完整 HTML 抽取

# 从 collect 生成脚手架：Lighthouse 缺失项已预填 Absent，其余 needsAgent=true
siluzan-tso website-diagnosis prepare --collect ./snap-web/<collect>.json --out ./snap-web/diagnosis.scaffold.json

# 仅 Lighthouse（失败不阻断，payload 含 warning）
siluzan-tso website-diagnosis performance --url https://www.example.com --json-out ./snap-web

# 按 diagnoseId 查 ARIT 得分（ID 来自 list-accounts 的 ma.diagnoseReports）
siluzan-tso website-diagnosis search --ids <id1,id2> --json-out ./snap-web

# 由诊断 JSON 生成带图表的 HTML 终稿
siluzan-tso website-diagnosis render --data ./diagnosis.json --collect ./snap-web/<collect>.json
```

| 子命令        | HTTP                                                  | 基址             |
| ------------- | ----------------------------------------------------- | ---------------- |
| `performance` | `GET /api/WebsiteDiagnosisReports/performance?url=`   | TSO `apiBaseUrl` |
| `collect`     | 上式 + `POST /download-assets` body `{ urls: [url] }` | TSO + Agent 网关 |
| `search`      | `GET /query/WebsiteDiagnoseReport/search?ids=`        | TSO              |

**Agent 网关**（与 `TSOWebsiteService` 一致）：

- 生产：`https://agent.mysiluzan.com`
- CI：`https://agent-ci.mysiluzan.com`
- 覆盖：`SILUZAN_AGENT_BASE`

请求头：`x-client-type: tso`，鉴权与 TSO 相同（JWT / API Key）。

---

## Agent 标准流程（P8）

1. 确认 `website_url`（须可访问，建议含 `https://`；CLI 可自动补全）。
2. `website-diagnosis collect --url <url> --json-out ./snap-web`（**必须** `--json-out`）。`--include-html` 仅把完整 HTML 写入 JSON，**不**影响 `signals`。
3. 读落盘 `signals` / `dataAvailability`（CLI 已抽好：HTTPS、表单、CTA、GTM、社媒、Lighthouse 分数等）。
4. `website-diagnosis prepare --collect <collect.json>` → `diagnosis.scaffold.json`（**推荐**）。
5. Read `assets/website-diagnosis-rules.md`；**只补全**脚手架里 `needsAgent=true` 的子项（依据 `signals` 写 issue/suggestion/score）；`needsAgent=false`（含 Lighthouse 不可用项）**禁止**改成虚构分。
6. 写 `priorityPlan`：按本站未满分项和 `coreIssuesIds` 分高/中/低（规则见 `website-diagnosis-rules.md`）。禁止套用固定行动清单，禁止留空。
7. 落盘完整 `diagnosis.json` 后：
   ```bash
   siluzan-tso website-diagnosis render --data ./diagnosis.json --collect ./snap-web/<collect>.json --out ./snap-web/website-diagnosis-report.html
   ```
   **禁止** Agent 手写/拼接 HTML；**禁止**只给 Markdown 或纯 JSON 充当终稿。`priorityPlan` 为空时 render 失败，先补再跑。
8. **禁止编造**未在 `signals` / HTML / Lighthouse 中出现的指标。见下节「数据缺失降级」。

**在 TSO Copilot 网页内**：工具返回 `rendered: true` 时，前端已渲染卡片 +「查看详情」全页 HTML，Agent 只需简短确认，**勿重复贴报告正文**（见 tso_agent `prompt.py`）。

---

## 数据缺失降级（Lighthouse 等）

**统一策略（P8 / P1 着陆页共用）**：打 TSO `WebsiteDiagnosisReports/performance`（失败自动重试，最多 3 次）。**不再**用 HTML 下载耗时冒充 Lighthouse。拿不到分则 `lighthouseSource` / `landingPageAnalysis.source` = `none`，`m2i1`/`m5i1` 标 Absent。**禁止**编造 score/FCP。表单/导航等结构信号来自 collect 的 `signals`（完整 HTML），与测速成败无关。

`collect` **不会**因 Lighthouse 失败而中止；落盘含 `lighthouseWarning` 与：

| 字段                                  | 含义                                   |
| ------------------------------------- | -------------------------------------- |
| `signals.lighthouseOk`                | 是否拿到桌面/移动 score                |
| `dataAvailability.lighthouse`         | `ok` / `missing` / `error` / `partial` |
| `dataAvailability.unavailableItemIds` | 默认含 `m2i1`、`m5i1`（依赖性能分）    |
| `dataAvailability.agentHint`          | 给 Agent 的硬约束文案                  |

**Agent 必遵**：

- `unavailableItemIds` 内子项：`status=Absent`、`score=0`，issue 写明未测到；**禁止**编造 FCP/score。
- **禁止**在无 Lighthouse 时勾选 `coreIssuesIds` 的 `ci4`（页面加载缓慢），除非有其它硬证据。
- HTML 失败时：依赖 DOM 的项须标明无法判定，禁止编造导航/表单/邮箱。
- 报告对用户说明「性能维度本次未测到」，不是「网站很快」。

`prepare` 会把上述不可用项预填好，降低 Agent 糊弄空间。

---

## 输出契约（对齐 `getWebsiteDiagnosisData`）

工具成功时 `data` 字段结构（Agent 生成或 Copilot `rendered: true` 时前端已渲染，对话侧勿重复贴全文）：

```json
{
  "url": "https://www.example.com",
  "ratingId": "s1",
  "coreIssuesIds": ["ci1", "ci2"],
  "priorityPlan": [
    {
      "priority": "高",
      "period": "1-2周",
      "impact": "本站这项对转化的影响",
      "items": [
        {
          "itemId": "m4i2",
          "direction": "本站现象的短标题",
          "task": "依据 signals 或第三节 issue 写的具体动作",
          "adImpact": "对这个站广告的影响"
        }
      ]
    }
  ],
  "modules": [
    {
      "id": "m1",
      "score": 0,
      "items": [
        {
          "id": "m1i1",
          "score": 0,
          "status": "Excellent",
          "issue": "…",
          "suggestion": "强烈建议：…"
        }
      ]
    }
  ],
  "analyzedAt": "2026-06-02T12:00:00+00:00"
}
```

| 字段                 | 说明                                                                           |
| -------------------- | ------------------------------------------------------------------------------ |
| `ratingId`           | `s1` 优秀 … `s5` 不建议投放（见规则文档评分等级）                              |
| `coreIssuesIds`      | 从 `ci1`–`ci10` 选取适用项                                                     |
| `priorityPlan`       | 第四节。按本站未满分项写，空数组时 render 失败                                 |
| `modules[].id`       | `m1`–`m6` 六板块均须出现                                                       |
| `items[].suggestion` | 较差/需优化/缺失类 status → **「强烈建议：」** 开头；其余 → **「推荐优化：」** |

---

## 六模块一览（29 子项，ID 与 tso_agent 一致）

| ID  | 名称                 | 子项 ID                           |
| --- | -------------------- | --------------------------------- |
| m1  | 网站内容及结构       | m1i1–m1i9                         |
| m2  | 网站性能             | m2i1–m2i5                         |
| m3  | 营销基础与广告落地页 | m3i1、m3i2、m3i4、m3i5（无 m3i3） |
| m4  | 用户体验与转化       | m4i1–m4i5                         |
| m5  | 媒体广告投放辅助     | m5i1、m5i2、m5i4（无 m5i3）       |
| m6  | 社交媒体辅助         | m6i1–m6i3                         |

子项满分、判断规则、评分细则见 **`assets/website-diagnosis-rules.md`**（摘自 `tso_agent/data/website_guide.py`）。

---

## Lighthouse 字段

```json
{
  "desktop": { "score", "firstContentfulPaint", "firstMeaningfulPaint", "speedIndex" },
  "mobile": { "score", "firstContentfulPaint", "firstMeaningfulPaint", "speedIndex" }
}
```

---

## 优化策略中的复用

`tso_agent` 的 `getOptimizationStrategy` 在 `device_2` 等维度会调用**同一** `WebsiteDiagnosisReports/performance`（需 Google 账户 `final-urls`）。与单次网站诊断独立；见 `references/operations/optimize.md` 与 Google 账户优化策略话术。

---

## 相关文档

- `report-templates/website-diagnosis-report.md` — 用户可见报告结构
- `assets/website-diagnosis-rules.md` — 规则与 Schema
- `references/accounts/accounts-list.md` — ARIT 与 `list-accounts`
- `references/core/playbooks.md` — **P8**
- `references/core/tips.md` — `--json-out` 处理顺序
