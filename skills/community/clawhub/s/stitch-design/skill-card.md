## Description:

Stitch Design lets agents use the official Google Stitch SDK to generate UI screens from text, edit existing screens, create variants, export HTML/images, and track screen aliases plus design lineage with local artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rasimme](https://clawhub.ai/user/rasimme)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and agents use this skill to turn product briefs into Google Stitch UI screens, review generated screenshots, iterate with edits or variants, and export HTML or images for downstream design work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI does not sufficiently constrain local state paths.

Mitigation: Use trusted project IDs and avoid automation that can choose --project values until the path handling is patched.

Risk: Remote artifact downloads depend on trusted Stitch API response paths.

Mitigation: Treat generated HTML, screenshots, and result metadata as external artifacts and review them before reuse.

Risk: The skill requires a Google Stitch API key.

Mitigation: Install only where STITCH_API_KEY can be scoped and managed appropriately.

## Reference(s):

- [Stitch Design homepage](https://github.com/rasimme/stitch-design)
- [@google/stitch-sdk package](https://www.npmjs.com/package/@google/stitch-sdk)
- [Google Stitch](https://stitch.withgoogle.com)
- [Prompt guide](references/prompt-guide.md)
- [SDK / CLI API reference](references/sdk-api.md)
- [Design system registry](design-systems/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI output; generated artifacts include HTML files, PNG screenshots, and result metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+ and STITCH_API_KEY; writes local runs/, state/, and latest-screen.json artifacts.]

## Skill Version(s):

1.2.3 (source: release evidence, package.json, CHANGELOG released 2026-03-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
