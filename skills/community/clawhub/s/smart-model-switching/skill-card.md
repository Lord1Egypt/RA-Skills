## Description: <br>
Guides agents to route Claude tasks across Haiku, Sonnet, and Opus based on task complexity to reduce cost while preserving capability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[millibus](https://clawhub.ai/user/millibus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to choose an economical Claude model tier for each task and escalate when complexity requires stronger reasoning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The routing heuristics could under-select model capability for high-stakes security, production, legal, medical, or financial tasks. <br>
Mitigation: Review and adjust the escalation rules for high-stakes workflows, including rules that require a higher-capability model when conservative routing is needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/millibus/smart-model-switching) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/millibus) <br>
- [Skill homepage](https://clawhub.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown with routing rules, decision trees, and inline code/configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides heuristic model-selection guidance; no tool calls, credentials, persistence, or data collection are indicated by the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
