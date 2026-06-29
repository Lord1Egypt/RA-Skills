## Description: <br>
Analyzes tomato or chili flower and young-fruit images or videos to count open flowers and set fruits, compute fruit-set rate, and return a structured report with cultivation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External growers, greenhouse operators, and developers use this skill to analyze tomato or chili flower-cluster media, estimate fruit-set rate, review report history, and decide whether pollination or water/fertilizer management should be adjusted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends plant images, videos, or URLs to a vendor cloud service for analysis and report retrieval. <br>
Mitigation: Use only with media that is appropriate to share with the vendor service, and avoid sensitive or private imagery unless that sharing is intended. <br>
Risk: The skill automatically creates or reuses an internal identity and stores or reuses tokens locally. <br>
Mitigation: Run it in a workspace where local account-linking and token persistence are expected, and review workspace data files before use in sensitive environments. <br>
Risk: The server security verdict is suspicious because account-linking and token behavior have limited user control. <br>
Mitigation: Review before installing and restrict use to trusted workspaces and trusted release channels. <br>


## Reference(s): <br>
- [API 接口文档](references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-flowering-fruit-set-rate-analysis-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON-like structured report text, with optional Markdown tables for history queries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include flower and young-fruit counts, fruit-set percentage, report links, and cultivation guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
