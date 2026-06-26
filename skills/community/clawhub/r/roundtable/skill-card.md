## Description: <br>
Multi-agent debate council that spawns Scholar, Engineer, and Muse sub-agents for parallel analysis, optional cross-examination, and a synthesized final answer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robbyczgw-cla](https://clawhub.ai/user/robbyczgw-cla) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and other agent users use Roundtable for complex questions that benefit from research, rigorous reasoning, creative alternatives, debate, and a final synthesized recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Council runs can use extra model calls and web searches, increasing cost and exposing prompts to external research workflows. <br>
Mitigation: Use quick mode, budget presets, or confirmation prompts for cost-sensitive tasks, and avoid including credentials, secrets, personal data, or proprietary material in prompts when web research is enabled. <br>
Risk: Prompts and outputs can be saved locally when session logging is enabled. <br>
Mitigation: Choose no logging for sensitive work, or review and delete files under memory/roundtable/ as needed. <br>


## Reference(s): <br>
- [Roundtable README](README.md) <br>
- [ClawHub Roundtable page](https://clawhub.ai/robbyczgw-cla/roundtable) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown answer with structured sections for confidence, agreement, dissent, sources, and round status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or read configuration for model presets and, when logging is enabled, save council session logs under memory/roundtable/.] <br>

## Skill Version(s): <br>
0.4.1 (source: frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
