## Description: <br>
Read, edit, and write Notion pages as Markdown using the solid-notion CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentdchan](https://clawhub.ai/user/vincentdchan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to manage Notion pages through the solid-notion CLI, including pulling content, applying Markdown or JSON-patch edits, submitting changes with rollback support, restoring history, and configuring Notion API authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide commands that modify live Notion pages. <br>
Mitigation: Review target page IDs and planned diffs before write, submit, new, or restore operations, and use dry-run options where available. <br>
Risk: Notion tokens and local page copies may expose sensitive workspace content. <br>
Mitigation: Use a dedicated least-privilege Notion integration, prefer token stdin over command-line tokens, share only intended pages with the integration, and manage or delete SOLID_NOTION_HOME data according to content sensitivity. <br>


## Reference(s): <br>
- [solid-notion ClawHub page](https://clawhub.ai/vincentdchan/solid-notion) <br>
- [Notion integration setup](https://www.notion.so/profile/integrations/internal) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides CLI workflows that can read local Notion exports, write live Notion pages, and emit JSON command results when requested.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
