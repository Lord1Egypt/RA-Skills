## Description: <br>
Reads Confluence requirement pages and exports each page as Markdown, metadata, and downloaded images while preserving the original content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcxxtyhd](https://clawhub.ai/user/mcxxtyhd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product, QA, and engineering teams use this skill to export an authenticated Confluence page tree into a local Markdown requirement bundle with metadata and images for review or handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Raw Confluence login cookies can expose private workspace access if shared or stored carelessly. <br>
Mitigation: Use this only for exports you are authorized to perform, prefer scoped Confluence API tokens or platform-managed authentication, and avoid pasting session cookies when a safer option is available. <br>
Risk: Private Confluence page HTML or attachments could be exposed if sent to online conversion services. <br>
Mitigation: Keep HTML-to-Markdown conversion local and avoid sending private page content to external converters. <br>
Risk: Automatic cleanup and ZIP steps could remove prior workspace outputs outside the current export. <br>
Mitigation: Review and adjust cleanup commands so they only touch the current export directory after explicit approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mcxxtyhd/theo-confluence-reader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, image files, metadata Markdown, and a ZIP archive] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a timestamped export directory for the selected Confluence page tree.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
