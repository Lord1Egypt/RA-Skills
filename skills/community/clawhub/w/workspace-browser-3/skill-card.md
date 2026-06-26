## Description: <br>
Browse and search workspace files with syntax-highlighted code and AI-generated explanations saved persistently in SQLite. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coopeter](https://clawhub.ai/user/coopeter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to inspect, search, download, and explain files in a workspace through a local browser interface. It is useful for quickly understanding project structure and preserving AI-generated or manually written code explanations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace files may be exposed too broadly over the network. <br>
Mitigation: Run only in a trusted environment, bind the service to localhost, add authentication or a local-only token, and restrict CORS before deployment. <br>
Risk: The AI explanation feature may send selected file contents to DeepSeek. <br>
Mitigation: Use AI explanations only for files that are acceptable to share with that external service, or disable the feature for sensitive projects. <br>
Risk: Stored explanations may retain sensitive project information in SQLite. <br>
Mitigation: Clear or disable the explanation database when working with confidential code or data. <br>
Risk: Path containment behavior needs review before relying on it for access control. <br>
Mitigation: Use resolved-path containment checks and restrict allowed workspace roots before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/coopeter/workspace-browser-3) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill description](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Local web UI and JSON API responses with file contents, search results, downloads, and code explanations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist AI-generated or manual explanations in a local SQLite database and may send selected file contents to DeepSeek when configured.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and artifact manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
