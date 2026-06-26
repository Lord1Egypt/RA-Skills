## Description: <br>
Skill Evolver helps agents evolve skills and extract patterns from execution data by collecting feedback, generating AI improvement suggestions, tracking impact, and supporting A/B testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pagoda111king](https://clawhub.ai/user/pagoda111king) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, skill authors, and platform operators use Skill Evolver to evaluate skill performance, collect feedback, extract reusable patterns, generate optimization suggestions, compare versions, and plan or validate skill changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for broad skill-data collection, which may capture sensitive prompts, outputs, ratings, or operational details. <br>
Mitigation: Use it only in a test or tightly scoped workspace unless collection settings, retention, and redaction are configured and reviewed. <br>
Risk: Generated skill edits, evolution proposals, hooks, or A/B tests could introduce incorrect guidance or unwanted behavior. <br>
Mitigation: Require human approval, scan changes before deployment, keep rollback paths available, and disable hooks unless they are explicitly needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pagoda111king/skill-evolver-v2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance, Configuration] <br>
**Output Format:** [Markdown reports with optional code snippets and structured recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include prioritized recommendations, A/B test plans, version comparisons, confidence estimates, and impact summaries.] <br>

## Skill Version(s): <br>
0.3.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
