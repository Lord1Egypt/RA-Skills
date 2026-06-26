## Description: <br>
Publishes Markdown, HTML, or JSX content to saved.md and returns a public shareable URL, with template scaffolds for common page types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anboias](https://clawhub.ai/user/anboias) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn supplied content into public saved.md pages, including reports, dashboards, resumes, invitations, and interactive JSX pages. It supports one-shot publishing, interactive draft review, local-only output, and remixing immutable saved.md pages into new URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected content is published to a public saved.md URL. <br>
Mitigation: Use interactive draft review before publishing sensitive material, resumes, or user-facing pages. <br>
Risk: Publishing history and deletion phrases may be stored locally in entries.json. <br>
Mitigation: Decide before use whether to allow local logging; instruct the agent not to log entries or clear entries.json after publishing when needed. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/anboias/saved-markdown) <br>
- [Publisher Profile](https://clawhub.ai/user/anboias) <br>
- [saved.md](https://saved.md) <br>
- [saved.md Pages API](https://saved.md/api/pages) <br>
- [Templates Index](artifact/templates/INDEX.md) <br>
- [Validation Guide](artifact/templates/validation.md) <br>
- [Charts Guide](artifact/templates/charts.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown, HTML, or JSX content plus a public saved.md URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Pages are immutable, content is limited to 100 KB, and publishing history with deletion phrases may be stored in entries.json.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
