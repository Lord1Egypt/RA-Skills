## Description:

An OpenClaw skill for redesigning GitHub README pages and creating project-specific visual assets, with render-level visual checks and dark/light theme guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dtsola](https://clawhub.ai/user/dtsola)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to improve a repository's README story and visuals, create README-specific SVG or raster assets, or audit an existing README and its visuals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes executable scripts, including subprocess-backed rendering and auditing tools.

Mitigation: Review the bundled scripts and run them only for the README or assets you intend to inspect; check generated previews and findings before applying changes.

Risk: The PNG image was outside the static analyzer's scope.

Mitigation: Inspect the bundled PNG if its contents matter to your use of the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dtsola/skills/xiaoyaoclaw-beautify-github-readme)
- [Project repository](https://github.com/dtsola/xiaoyaoclaw-beautify-github-readme)
- [Upstream project](https://github.com/oil-oil/beautify-github-readme)
- [XiaoyaoClaw](https://www.xiaoyaosai.com/xiaoyaoclaw/)

## Skill Output:

**Output Type(s):** [Markdown, SVG, PNG/WebP, GIF, Guidance, Shell commands]

**Output Format:** [README content or audit guidance in Markdown, plus project-specific visual asset files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Visual assets may include SVG, PNG, WebP, or opt-in GIF; rendered checks can include preview images and audit findings.]

## Skill Version(s):

1.0.18 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
