# Scenario Forecaster Skill - Expert-Level Decision Support

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.3.0-blue)]()

> **Stop guessing. Start forecasting.** Let AI systematically map every possible future path and give you a tailored action checklist.

**Struggling with uncertainty?**
- "The Fed might cut rates" - should you **buy or sell**?
- Policy changes ahead - **how to prepare** with minimal risk?
- Major life decision - what does **5 years ahead** look like?

Regular AI gives vague disclaimers. **Scenario Forecaster** gives you structured reports: **probability-weighted paths + trigger milestones + do/don't lists**.

---

## Why This Skill?

| Regular AI Chat | Scenario Forecaster |
| :--- | :--- |
| Opinions without evidence | **Multi-source cross-validation** (news + academia + social + gov reports) |
| Only one possibility | **3-5 self-consistent future paths** with probability estimates |
| No clear action | **Role-specific recommendations** for investors, managers, policymakers |
| No way to track | **Explicit trigger milestones** for easy review and correction |

---

## Get Started in 30 Seconds

### Option 1: Copy the Prompt (Any AI Platform)
Copy [`skill/prompt.md`](./skill/prompt.md) into ChatGPT, Claude, Kimi, or DeepSeek.

### Option 2: Import to Specialized Platforms
- **ClawHub / Dify / Coze**: Upload [`skill/scenario_forecaster.yaml`](./skill/scenario_forecaster.yaml).
- **OpenAI GPTs**: Copy `prompt.md` into Instructions.

### Option 3: One-Click Install
```bash
npx clawhub install scenario-forecaster
```

### Try It Now
```
Forecast: Impact of escalating Middle East tensions on crude oil prices over 6 months.
Focus: Economic and Political dimensions.
```

---

## Configuration

| Parameter | Effect | Example |
| :--- | :--- | :--- |
| `time_horizon` | Forecast duration | `1 year`, `3 months` |
| `focus_dimensions` | Narrow the scope | `["Economic", "Technology"]` |
| `num_paths` | Number of paths | `3` (focused) / `5` (include tail risks) |
| `confidence_threshold` | Filter low-probability noise | `0.2` |

---

## File Structure

```
.
├── skill/
│   ├── scenario_forecaster.yaml   # Structured workflow definition
│   └── prompt.md                  # Plain-text prompt (works everywhere)
├── examples/                      # Input/output examples
└── docs/                          # API reference and customization guide
```

---

## Community

- **Bug reports**: [Open an Issue](https://github.com/Onecore-me/scenario-forecaster-skill/issues)
- **PRs welcome**: Improve the forecasting logic
- **Share your results**: Post in Discussions if this helped your investment or strategy work!

---

## Disclaimer
This skill performs logical scenario analysis based on publicly available information. **It does not constitute financial or policy advice.** Probability figures are for risk assessment only. Use your own judgment.

MIT License - 2026
