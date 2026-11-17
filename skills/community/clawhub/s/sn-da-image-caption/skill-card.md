## Description:

Analyzes images and extracts text or data from charts, tables, screenshots, and diagrams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use the skill to understand image content and extract information from charts, tables, screenshots, and diagrams for further analysis or export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch mode ignores the cache-disabling option, so text extracted from sensitive images may remain in the local cache.

Mitigation: Review before processing private images, confirm the external API destination, and use a directory containing only intended inputs. For uncached processing, use individual-image mode with --no-cache; batch mode does not honor this option. Delete existing cached captions separately. A SenseNova API key is required despite the skill text's no-setup claim.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sensenova-skills/skills/sn-da-image-caption)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV/Excel files, Analysis guidance]

**Output Format:** [Image descriptions and extracted content as text, Markdown tables, or JSON; downstream structured data may be exported to CSV or Excel.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on image legibility and vision model interpretation; review extracted values before relying on them.]

## Skill Version(s):

2026.10.29 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
