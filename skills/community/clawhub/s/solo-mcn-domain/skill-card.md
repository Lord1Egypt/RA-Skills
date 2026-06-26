## Description: <br>
A Chinese self-media and solo MCN operations reference skill that helps agents structure topic planning, content creation, visual design, platform operations, data analysis, and commercial monetization workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, operators, and agent users use this skill as a structured reference library for solo MCN and self-media operations. It guides agents through topic selection, article and video content planning, SEO, cover design, platform adaptation, analytics, scheduling, and monetization outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to automatically install and load universal-task-os when activated. <br>
Mitigation: Require user confirmation or a policy review before allowing dependency installation during normal content requests. <br>
Risk: Broad activation terms for self-media, MCN, content creation, SEO, video, cover design, community operations, analytics, pricing, and scheduling can cause the skill to engage in many content workflows. <br>
Mitigation: Confirm the user wants this domain reference applied before delegating content generation, analytics, or monetization planning. <br>
Risk: Without Universal Task OS, the artifact says the skill should only provide reference lookup and should not execute content production, pipeline orchestration, or data-driven tasks. <br>
Mitigation: Keep the skill in read-only reference mode when the dependency is unavailable or not approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjiaocheng/solo-mcn-domain) <br>
- [MCN task catalog](references/mcn-catalog.md) <br>
- [MCN requirements](references/mcn-requirements.md) <br>
- [Exemplars](references/exemplars.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown plans, tables, checklists, scripts, prompts, and operating guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on Universal Task OS for executable workflow orchestration; without that dependency the skill operates as read-only reference guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
