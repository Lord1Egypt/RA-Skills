## Description: <br>
Generate clean PNG table images from JSON data for messaging platforms where ASCII tables render poorly, with dark and light modes, custom styling, emoji support, RTL support, and auto-sizing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dannyshmueli](https://clawhub.ai/user/dannyshmueli) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, engineers, and agents use this skill to convert structured JSON row data into readable PNG table images for Discord, Telegram, WhatsApp, and other messaging surfaces where monospaced ASCII tables are unreliable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the skill's script dependencies pulls the Sharp image library and platform packages from npm. <br>
Mitigation: Install dependencies in a controlled environment, use trusted registries, and review the provided package lock and scan results before deployment. <br>
Risk: Tables containing emoji may contact jsDelivr/Twemoji and cache SVG files under the skill directory. <br>
Mitigation: Use plain text or avoid emoji for fully offline rendering, or pre-review the CDN and local cache behavior before enabling emoji-heavy inputs. <br>
Risk: Inline JSON passed through a shell can fail or be misread when values contain quotes or special characters. <br>
Mitigation: Prefer the documented --data-file option or stdin input pattern for generated or user-provided table data. <br>


## Reference(s): <br>
- [Artifact README](README.md) <br>
- [ClawHub skill page](https://clawhub.ai/dannyshmueli/table-image-generator) <br>
- [Twemoji SVG assets used for emoji rendering](https://cdn.jsdelivr.net/gh/twitter/twemoji@latest/assets/svg/) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PNG image files generated from JSON data, with Markdown usage guidance and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports dark mode, custom columns and headers, alignment, RTL layout, word wrapping, emoji rendering, and configurable output paths.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata; artifact frontmatter reports 1.3.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
