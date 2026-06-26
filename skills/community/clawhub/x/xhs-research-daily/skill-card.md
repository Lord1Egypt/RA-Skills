## Description: <br>
Collect Xiaohongshu posts/comments for a research topic, synthesize a daily roundup, and optionally publish it back to Xiaohongshu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhrli324](https://clawhub.ai/user/zhrli324) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to collect Xiaohongshu research posts for configured topics, rank and summarize them, review a daily draft, and optionally publish the final post from a logged-in Xiaohongshu account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing mode can post to a real Xiaohongshu account. <br>
Mitigation: Run with --dry-run first, inspect the generated post_draft.json, and enable --publish only after confirming the draft and target account. <br>
Risk: Scheduled publishing can repeat public account actions without timely review. <br>
Mitigation: Start scheduled runs in dry-run mode and add operational controls before using the cron publish example. <br>
Risk: Command errors or logs may expose xsec_token values from Xiaohongshu requests. <br>
Mitigation: Redact command errors and logs before sharing them outside the operational environment. <br>


## Reference(s): <br>
- [XHS Research Daily Operations](references/operations.md) <br>
- [ClawHub skill page](https://clawhub.ai/zhrli324/xhs-research-daily) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown digest files, JSON data files, JSON post drafts, shell command examples, and optional published Xiaohongshu content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes dated data under data/<topic>/<date>/ and can publish when run with --publish.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
