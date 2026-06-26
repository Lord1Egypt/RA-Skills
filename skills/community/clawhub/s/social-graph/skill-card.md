## Description: <br>
Social Graph helps agents maintain per-person social context, sharing boundaries, and sharing history so they can decide what to share, when to listen, and avoid repeating themselves. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mculp](https://clawhub.ai/user/mculp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to give agents a local social-memory framework for relationship-management tasks, including tracking per-person preferences, sensitive topics, trust levels, and previously shared information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent notes about real people can capture sensitive personal context without clear privacy, consent, or deletion boundaries. <br>
Mitigation: Use aliases where possible, avoid storing contact details or sensitive personal inferences, get consent where appropriate, and regularly review and delete stale entries. <br>
Risk: The skill can be invoked outside explicit relationship-management tasks, increasing unnecessary collection or use of social context. <br>
Mitigation: Invoke the skill only for explicit relationship-management tasks and keep stored notes limited to what is needed for that task. <br>


## Reference(s): <br>
- [Social Network Graph Template](references/network-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with suggested local Markdown files for rules, network notes, and sharing logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code hooks or API calls; the skill guides agent reasoning and local note updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
