# Edge Cases — Web Design Lead Qualifier

Reference file for the standalone lead qualifier. The agent should consult this when encountering unusual situations.

## Scenario → Action

| Scenario | Action |
|---|---|
| Company name only, no website found | Search for it. Still nothing → ask the user. Don't proceed without a URL or LinkedIn. |
| Site is down / unreachable | Note in report. Try cached version or social. Flag as data quality issue. `data_confidence=LOW`. |
| Multiple companies with similar names | Present options, ask user to confirm. Don't guess. |
| Clearly enterprise (500+ employees) | Still produce report. Note: likely has in-house team or agency — different approach needed. |
| Very small (micro-business) | Still produce report. Note: budget likely limited. |
| LOW data confidence | Heavy uncertainty flags. Recommend manual research before contact. Don't inflate score because of missing contrary evidence. |
| Different country | Note location, timezone, language, payment implications. Don't disqualify on location alone. |
| Playwright not installed | Use `web_fetch` as fallback. Note in report that JS-rendered content may be incomplete. |

## Principles

- Always produce the report, even for unlikely leads. The freelancer decides whether to pursue, not the skill.
- Never disqualify based on assumptions. Note concerns, let the human judge.
- When data quality is low, be explicit about what's missing and why it matters.
