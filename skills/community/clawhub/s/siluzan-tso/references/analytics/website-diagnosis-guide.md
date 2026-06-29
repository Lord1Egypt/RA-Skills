# 网站诊断（Website Diagnosis）

> 对齐 Aiagent-Server `agent/tso_agent`：`getWebsiteDiagnosisData`（`website_diagnosis_tools.py` + `data/website_guide.py`）。  
> **CLI 负责拉数**；**6 模块 × 29 子项评分**由 Agent 按规则 + 采集数据生成 JSON。  
> **最终交付**：与线上一致，为**一份可浏览器打开、含 ECharts 图表的单文件 HTML 报告**（雷达图、模块得分条形图、Lighthouse 对比图等）。**用户未指定格式时默认交付 HTML**；Skill/CLI **Agent 只写诊断 JSON，HTML 一律由 `website-diagnosis render` 生成**（禁止 Agent 手写 HTML，禁止仅 Markdown/JSON 充当终稿）。

---

## CLI 命令

```bash
# 推荐：一次采集 Lighthouse + 首页 HTML（供 Agent 写报告）
siluzan-tso website-diagnosis collect --url https://www.example.com --json-out ./snap-web

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
2. `website-diagnosis collect --url <url> --json-out ./snap-web`（**必须** `--json-out`）。
3. Read `assets/website-diagnosis-rules.md`（评分规则与 JSON Schema）。
4. 用脚本读 `writtenFiles[0]` 的 `lighthouse`、`htmlPreview`（或 `--include-html` 时的 `htmlContent`）生成结构化 `data`（见下节输出契约）。
5. 将诊断 JSON 落盘为 `diagnosis.json`（脚本写文件，勿在对话里贴全文），再执行：
   ```bash
   siluzan-tso website-diagnosis render --data ./diagnosis.json --collect ./snap-web/<collect>.json --out ./snap-web/website-diagnosis-report.html
   ```
   **禁止** Agent 手写/拼接 HTML；**禁止**只给 Markdown 或纯 JSON 充当终稿。
6. **禁止编造**未在采集 HTML/Lighthouse 中出现的指标。Lighthouse 缺失时须在 HTML 中醒目说明。

**在 TSO Copilot 网页内**：工具返回 `rendered: true` 时，前端已渲染卡片 +「查看详情」全页 HTML，Agent 只需简短确认，**勿重复贴报告正文**（见 tso_agent `prompt.py`）。

---

## 输出契约（对齐 `getWebsiteDiagnosisData`）

工具成功时 `data` 字段结构（Agent 生成或 Copilot `rendered: true` 时前端已渲染，对话侧勿重复贴全文）：

```json
{
  "url": "https://www.example.com",
  "ratingId": "s1",
  "coreIssuesIds": ["ci1", "ci2"],
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
- `references/accounts/accounts.md` — ARIT 与 `list-accounts`
- `references/core/playbooks.md` — **P8**
- `references/core/tips.md` — `--json-out` 处理顺序
