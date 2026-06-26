## Description: <br>
Walmart Review Checker analyzes Walmart product reviews for suspicious patterns, rating manipulation, incentivized-review indicators, and WFS or verification signals without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phheng](https://clawhub.ai/user/phheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce sellers, marketplace analysts, and developers use this skill to review product-review text or structured review data for authenticity signals and suspicious-review patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the Walmart-specific claims do not match the implementation, so results may reflect generic or Amazon-style review heuristics. <br>
Mitigation: Treat scores and flags as directional review-assistance signals, not proof of fraud, and verify any suspicious findings against the original review data and marketplace context. <br>
Risk: The security guidance says generated HTML reports can render untrusted review text unsafely. <br>
Mitigation: Prefer plain text output for untrusted input, and only open generated HTML after the report renderer is fixed to escape user-controlled text or render it via textContent. <br>
Risk: The security verdict is suspicious. <br>
Mitigation: Review the package source and scanner evidence before installing or deploying the skill. <br>


## Reference(s): <br>
- [Walmart Review Checker on ClawHub](https://clawhub.ai/phheng/walmart-review-checker) <br>
- [Nexscope AI](https://www.nexscope.ai/) <br>
- [Chart.js CDN used by HTML report generator](https://cdn.jsdelivr.net/npm/chart.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown and plain text analysis reports, with optional JSON input and generated HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an authenticity score, risk level, detection results, suspicious-review indicators, and follow-up guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
