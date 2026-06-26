## Description: <br>
Provides pre-call experience checks, error-driven learning, and layered per-skill experience storage so agents can avoid repeated mistakes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jilanfang](https://clawhub.ai/user/jilanfang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add per-skill experience memory, pre-call mistake checks, and error-driven updates to an agent's learning workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages broad automatic persistent memory updates, which can preserve stale, sensitive, or incorrect lessons. <br>
Mitigation: Use explicit rules for when experience files may be created or updated, require approval for long-term memory writes, and periodically review memory/experiences/ for stale or sensitive content. <br>
Risk: The skill may cause agents to treat past mistakes or best practices as authoritative in contexts where they no longer apply. <br>
Mitigation: Keep experience entries scoped with context, timestamps, and prevention notes, and prune or revise lessons during regular reviews. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jilanfang/skill-experience-layer) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/jilanfang) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, JSON] <br>
**Output Format:** [Markdown guidance with JSON experience-file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to create or update persistent per-skill experience files under memory/experiences/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
