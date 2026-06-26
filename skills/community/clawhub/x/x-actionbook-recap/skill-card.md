## Description: <br>
Collect, scroll, extract, and summarize recent X (Twitter) posts for any handle, optionally filtered by keyword search, using the Actionbook Rust CLI workflow and produce Chinese working notes plus neutral English recap copy for publication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jack4world](https://clawhub.ai/user/jack4world) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and operators use this skill to collect public X posts for a requested handle and time window, summarize observed themes, and draft neutral English recap copy. It can also guide optional image-card creation and publication after confirming the target account and final text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a logged-in X account through browser automation and may publish externally. <br>
Mitigation: Use it only with accounts intended for this workflow, and confirm the target account, final post text, and image choice before publication. <br>
Risk: Infinite scroll collection may miss posts or provide incomplete coverage for the requested time window. <br>
Mitigation: State the requested time window, scroll depth or cutoff, and that the results may be incomplete. <br>
Risk: Recaps can misattribute claims if interview quotes or external statements are used without exact source links or timestamps. <br>
Mitigation: Only attribute quoted material when exact links or timestamps are available, and separate public-post observations from interpretation. <br>


## Reference(s): <br>
- [Extraction checklist](references/checklist.md) <br>
- [Image card without Python](references/image-card.md) <br>
- [Templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown notes, recap drafts, and inline shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes coverage caveats, source-link notes, and confirmation steps before publishing.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
