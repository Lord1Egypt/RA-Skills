## Description: <br>
Turn app screenshots into structured UX, copywriting, and conversion audits with issue severity and recommended fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, product managers, developers, and growth teams use this skill to review app screenshots and turn UX, copywriting, accessibility, and conversion issues into prioritized fixes and shareable issue logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshots and product context may contain sensitive user, business, or interface information. <br>
Mitigation: Provide only screenshots and context that are appropriate to share with the reviewing agent. <br>
Risk: CSV issue-log generation can overwrite an existing output file if the same path is reused. <br>
Mitigation: Choose an explicit output path and review the destination before running the helper script. <br>
Risk: UX audit recommendations may be incomplete or based on assumptions when product goals, users, or funnel context are missing. <br>
Mitigation: Keep assumptions explicit and treat recommendations as reviewable drafts before using them for product decisions. <br>


## Reference(s): <br>
- [UX Heuristics Checklist](artifact/resources/heuristics-checklist.md) <br>
- [Example Prompt](artifact/examples/example-prompt.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/screenshot-ux-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown audit summaries, prioritized issue lists, CSV or Markdown issue logs, and before/after prompt suggestions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use the local Python helper to convert user-provided JSON issue data into a CSV issue log.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
