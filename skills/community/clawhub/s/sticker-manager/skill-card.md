## Description:

Sticker Manager helps agents save, search, tag, rename, clean up, collect, import, recommend, and prepare media-sending workflows for local sticker and reaction-image libraries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuwenzhuang](https://clawhub.ai/user/zhuwenzhuang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage local sticker and reaction-image libraries, including saving inbound media, finding matching stickers, adding semantic metadata, importing batches, collecting candidate sources, and preparing recommendations for an outer agent or model layer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplied names or paths may reach outside the intended sticker library during rename or delete operations.

Mitigation: Constrain file operations to the configured sticker library, normalize and validate paths before mutation, and review rename/delete behavior before deployment.

Risk: Remote URL fetching can access unsafe or unintended destinations when source discovery or collection is enabled.

Mitigation: Restrict fetching to safe public destinations, require explicit fetch actions, and enforce network, size, and content validation limits.

Risk: Sticker collection and image processing can consume excessive resources or save invalid media without bounded validation.

Mitigation: Apply download size limits, image validation, deduplication, low-quality filtering, and animated-file checks before importing or sending media.

Risk: Context-based recommendation can process sensitive chat histories.

Mitigation: Use the feature only on chat histories appropriate for processing and avoid passing private or sensitive conversation content unless approved.

Risk: Unpinned dependencies reduce reproducibility across installs.

Mitigation: Pin dependency versions before production use and rerun the security review after dependency changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuwenzhuang/skills/sticker-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, resolved file paths, JSON-like handoff markers, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return model-planning markers for semantic tagging, recommendation, history analysis, and vision fallback flows.]

## Skill Version(s):

0.3.0 (source: evidence.release.version and CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
