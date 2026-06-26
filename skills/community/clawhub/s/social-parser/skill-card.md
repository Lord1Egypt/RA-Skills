## Description: <br>
Parses Douyin video and Xiaohongshu note links with the gnomic CLI to extract titles, media URLs, descriptions, tags, author details, and related metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huyi9531](https://clawhub.ai/user/huyi9531) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content analysts use this skill to parse Douyin and Xiaohongshu links for content review, topic research, competitor analysis, and creator metadata extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The parser uses an external CLI and remote API, so submitted social links and retrieved content may leave the local environment. <br>
Mitigation: Use only Douyin or Xiaohongshu links that are intended for parser processing, and avoid private, restricted, or sensitive links unless remote processing is acceptable. <br>
Risk: The skill instructs users to install the gnomic-cli npm package globally when the command is unavailable. <br>
Mitigation: Verify the npm package and project source before installation, and install it only in environments where a global CLI dependency is acceptable. <br>
Risk: Platform limitations can affect completeness, including private Xiaohongshu notes and missing Xiaohongshu engagement or author fields. <br>
Mitigation: Present parsed results as best-effort data, call out missing fields, and avoid treating absent metrics as zero or definitive. <br>


## Reference(s): <br>
- [ClawHub social-parser release page](https://clawhub.ai/huyi9531/social-parser) <br>
- [gnomic-cli project](https://github.com/huyi9531/gnomic_cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and parsed JSON or text results from the CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include media URLs, cover images, title, description, tags, author information, and engagement metadata depending on the platform and source link.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
