## Description: <br>
Aggregates SMZDM deal-search results and formats discount summaries for shopping queries, with fallback demo results when live requests fail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[275254cl-hash](https://clawhub.ai/user/275254cl-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping-focused agents use this skill to search public SMZDM deal listings and summarize current-looking offers, prices, merchants, heat scores, and links. Users should treat the output as deal-discovery assistance rather than verified price intelligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopping search terms are sent to SMZDM during live searches. <br>
Mitigation: Avoid entering sensitive or private purchase intent when using live search. <br>
Risk: Some results may be demo or mock data when live requests fail. <br>
Mitigation: Verify prices, merchant details, and availability directly with the linked retailer or SMZDM before acting. <br>
Risk: The documentation describes real-time alerts, historical-low checks, and BUG-price monitoring that are not fully implemented by the artifact. <br>
Mitigation: Use the skill as a lightweight search and summary helper, not as an automated monitoring or pricing assurance system. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/275254cl-hash/smzdm-deals) <br>
- [SMZDM](https://www.smzdm.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-formatted deal summaries with links and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to 10 deals per search and may fall back to demo data if outbound SMZDM requests fail.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
