## Description: <br>
Standalone lightweight router for a personal second-brain loop. Use when the user asks knowledge, judgment, writing, reflection, decision, AI-agent, product, learning, or long-term thinking questions. It maps the question to cognitive anchors, recalls local knowledge and experience context, answers, and optionally writes back to the right wiki layer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route knowledge, writing, judgment, reflection, and long-term thinking prompts through a lightweight personal second-brain workflow. It helps select cognitive anchors, recall limited local wiki context, answer from that context, and write back only when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording and local recall can cause an agent to inspect personal notes more often than a user expects. <br>
Mitigation: Review or change the hardcoded vault paths before use, and require confirmation before reading sensitive local notes or performing wiki writebacks. <br>


## Reference(s): <br>
- [Second Brain Router on ClawHub](https://clawhub.ai/harrylabsj/second-brain-router) <br>
- [Publisher profile: harrylabsj](https://clawhub.ai/user/harrylabsj) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with concise routing receipts and optional shell command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose small, auditable wiki writebacks only when the user explicitly asks to save or update content.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
