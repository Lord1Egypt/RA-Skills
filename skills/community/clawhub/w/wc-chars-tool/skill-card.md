## Description: <br>
Count characters in text input - total, non-whitespace, CJK, and Unicode-aware character counts for text analysis, content length limits, and i18n validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content engineers use this skill to count text characters, bytes, whitespace-filtered characters, CJK characters, and grapheme clusters when checking content limits or internationalized text handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The authoritative security summary marks the release suspicious due to a review helper that can run nested Codex review with broad filesystem and approval-bypass privileges by default. <br>
Mitigation: Install only in a trusted maintainer environment, review helper behavior before use, and run without full-access nested review unless explicitly intended. <br>
Risk: The artifact's executable script only counts stdin length, while the skill description advertises broader CLI modes such as file input, grapheme counting, CJK-only counts, and JSON detail. <br>
Mitigation: Validate the installed command behavior against expected counting modes before depending on it for production content checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/wc-chars-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe JSON output for script integration when requested by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
