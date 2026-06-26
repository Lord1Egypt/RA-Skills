## Description: <br>
Coach and generate Xiaohongshu (小红书/RedNote/XHS) note writing for titles, body copy, tags, comment prompts, cover text, engagement optimization, and AI-content labeling reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[herve-clawd](https://clawhub.ai/user/herve-clawd) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators, marketers, and writing assistants use this skill to turn raw ideas into publish-ready Xiaohongshu/RedNote post drafts with title options, structured body copy, tags, CTAs, cover text, and review notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI-content labeling guidance is internally inconsistent between the artifact and security review. <br>
Mitigation: Check the target platform and publication context before posting, and override any stale instruction that conflicts with required AI-content labeling. <br>
Risk: Hot-topic grounding can expose private draft details if external search queries include sensitive user context. <br>
Mitigation: Keep private details out of search queries and use generalized topic searches when gathering references. <br>
Risk: The skill relies on living reference notes that can change the writing strategy over time. <br>
Mitigation: Review and approve updates to reference notes before relying on them for recurring publication workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/herve-clawd/xhs-writing-coach) <br>
- [Source notes](references/source-notes.md) <br>
- [Strategy notes](references/strategy-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON object containing title, content, tags, cta, cover_text, and notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are constrained for XHS-style drafting: title length guidance, 300-600 character body guidance, 5-8 tags, structured CTA, and review notes.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
