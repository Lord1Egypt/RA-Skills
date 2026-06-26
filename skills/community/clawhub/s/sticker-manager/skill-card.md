## Description: <br>
Sticker Manager helps an OpenClaw agent save, search, tag, rename, clean up, collect, import, and recommend local stickers or reaction images across JPG, JPEG, PNG, WEBP, and GIF files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuwenzhuang](https://clawhub.ai/user/zhuwenzhuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to manage a local sticker library, resolve matching media files, and prepare model-oriented tagging or recommendation payloads for chat workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says some file and data-handling paths are not safely scoped. <br>
Mitigation: Install and run with supervision, keep sticker directories dedicated to non-sensitive media, and avoid path-like names when deleting or renaming. <br>
Risk: Remote discovery and collection can involve untrusted or internal URLs. <br>
Mitigation: Review source lists before collection, avoid untrusted or internal URLs, and use active URL fetching only when the source is expected and safe. <br>
Risk: Auto-tagging and context recommendation may expose local paths or message text. <br>
Mitigation: Do not pass sensitive files or chat histories, and review generated recommendations or tagging payloads before sharing or storing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhuwenzhuang/sticker-manager) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands, file paths, and JSON or structured marker payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return resolved local media paths, import or collection summaries, semantic tagging plans, and context recommendation candidates.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata and CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
