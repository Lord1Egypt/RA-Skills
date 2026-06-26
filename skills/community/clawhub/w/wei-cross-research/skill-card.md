## Description: <br>
Cross-validate research answers by querying multiple LLMs in parallel with judge-based synthesis, reducing hallucination risk and surfacing model disagreements for higher-stakes questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikehankk](https://clawhub.ai/user/mikehankk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill when a complex research question benefits from multiple model perspectives, consensus checks, and a synthesized final answer. It is especially relevant for financial, technical, scientific, current-events, social, creative, and general analysis workflows where disagreement should be visible. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries are sent to configured external LLM providers and may include sensitive or confidential user content. <br>
Mitigation: Use only approved providers for the data being submitted, and avoid sending secrets, regulated data, or confidential business information unless those providers are approved for that classification. <br>
Risk: The skill can make multiple model calls per request, which can increase token usage and provider costs. <br>
Mitigation: Use the skill for questions where cross-validation is worth the added cost, and configure model count, routing, and provider settings before deployment. <br>
Risk: Generated reports and intermediate model outputs may persist locally and contain sensitive query content or responses. <br>
Mitigation: Review and delete files under reports/ and intermediate/ when they contain sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mikehankk/wei-cross-research) <br>
- [Publisher profile](https://clawhub.ai/user/mikehankk) <br>
- [Project homepage from ClawHub metadata](https://github.com/MikeHanKK/wei-skills/tree/main/skills/wei-cross-research) <br>
- [Bun runtime](https://bun.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Structured JSON response plus local text report files and intermediate model response files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include models used, failed models, individual answers, synthesized final answer, confidence score, warnings, or error details. Runs can save reports/ and intermediate/ files identified by timestamp.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
