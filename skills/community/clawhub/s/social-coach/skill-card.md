## Description: <br>
Social Coach is an anti-PUA dating and social-growth coach that helps users record social interactions, practice conversations, review outcomes, and receive data-driven communication and mindset guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wnzzer](https://clawhub.ai/user/wnzzer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to track dating and social outreach attempts, rehearse low-pressure conversations, review outcomes, and identify patterns over time. The skill is intended to support respectful social growth rather than manipulative pickup tactics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive dating, relationship, and emotional-history records long term in local files. <br>
Mitigation: Use aliases instead of real names, avoid screenshots or identifying details, set SOCIAL_COACH_DATA to a private folder, and delete stored JSONL, profile, and backup files when no longer needed. <br>
Risk: Error handling may reveal full saved records while reporting damaged JSONL lines. <br>
Mitigation: Review error output before sharing transcripts or logs, and remove identifying details from records before continuing analysis. <br>
Risk: Backup files created during repair or deletion workflows can retain sensitive historical data. <br>
Mitigation: Manually review and delete backup files after confirming the repaired records are correct. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wnzzer/social-coach) <br>
- [Analytics reference](references/analytics.md) <br>
- [Field guide](references/field-guide.md) <br>
- [Mindset reference](references/mindset.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown conversational responses with inline shell commands and JSON or JSONL records when saving user-approved data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and update local profile, invitation, interaction, conversation, review, and backup files in a user-configured data directory.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
