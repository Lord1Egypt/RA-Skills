# Roadmap / 路线图

Future plans for OpenClaw Smartness Eval.

---

## v0.3 — Enhanced Reporting / 增强报告 (Q2 2026)

| Feature | Description | 说明 |
|---------|-------------|------|
| Normalized benchmark export | JSON Schema–validated output for cross-tool comparison | 标准化输出，便于跨工具对比 |
| Richer trend explanations | Auto-generated natural language explaining score changes | 自然语言趋势解释 |
| Calibration diagnostics | Detailed breakdown of confidence accuracy per dimension | 置信度准确性诊断 |
| HTML summary card | Single-page HTML score card for embedding / sharing | 可嵌入的 HTML 评分卡 |

---

## v0.4 — Visualization & Customization / 可视化与定制 (Q3 2026)

| Feature | Description | 说明 |
|---------|-------------|------|
| Chart generation | SVG/PNG score trend charts (matplotlib optional dep) | 趋势图表生成 |
| HTML report renderer | Full interactive HTML report with dimension drill-down | 交互式 HTML 报告 |
| Custom anti-gaming strategies | Configurable probe templates and difficulty levels | 可配置反作弊策略 |
| Dimension grouping | Allow users to define custom dimension groups and weights | 自定义维度分组 |

---

## v0.5 — Integration / 集成 (Q4 2026)

| Feature | Description | 说明 |
|---------|-------------|------|
| GitHub Actions integration | Pre-built workflow to auto-eval on push/PR | GitHub Actions 自动评估 |
| Slack/Feishu notification | Post score summary to team channels | 评分推送到团队频道 |
| Multi-workspace comparison | Compare scores across different OpenClaw instances | 多工作区横向对比 |
| CI/CD gate | Block deployment if score drops below threshold | 部署门控 |

---

## v1.0 — Stable Release / 正式版 (2027 H1)

| Feature | Description | 说明 |
|---------|-------------|------|
| Plugin API for custom dimensions | Register new dimensions with custom scoring functions | 自定义维度插件 API |
| Cross-workspace profiles | Shareable evaluation profiles for benchmarking | 可分享的评估配置 |
| Long-term drift analytics | Statistical analysis of score trends over months | 长期趋势统计分析 |
| Localization | Full i18n support (EN, CN, JP) | 多语言支持 |
| Stable JSON Schema | Versioned, backward-compatible output schema | 稳定的输出格式 |

---

## How to contribute to the roadmap / 如何参与

1. Open an issue with the `roadmap` label to suggest a feature
2. Vote on existing roadmap issues with 👍
3. Submit a PR for any planned feature — see [CONTRIBUTING.md](../CONTRIBUTING.md)

欢迎通过 Issue（标签 `roadmap`）提出建议，或直接提交 PR。
