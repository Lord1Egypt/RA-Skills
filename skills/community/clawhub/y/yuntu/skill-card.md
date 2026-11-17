## Description:

Downloads the latest NSMC FY-4B satellite cloud image, derives a readable capture time, and returns the image for an agent response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuliao8](https://clawhub.ai/user/wuliao8)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch the latest satellite cloud map when weather or cloud imagery is requested. It helps compose a response that includes a formatted capture time and the downloaded image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads a public satellite image from an external source, so availability and freshness depend on that source and network access.

Mitigation: Handle download failures clearly and verify the returned image source and timestamp before relying on it operationally.

Risk: Dependency setup includes system package installation and unpinned Python packages.

Mitigation: Install dependencies in a dedicated virtual environment, pin package versions, and review system package commands before execution.

Risk: OCR can fail and the skill may fall back to a local current timestamp, which can make the displayed capture time inaccurate.

Mitigation: Install the Tesseract Chinese language pack and treat fallback timestamps as lower confidence unless the image timestamp is verified.

Risk: The skill caches downloaded images in the user's home directory.

Mitigation: Review cache contents periodically and apply local data retention or storage policies as needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuliao8/skills/yuntu)
- [National Satellite Meteorological Center](https://www.nsmc.org.cn/)
- [FY-4B satellite cloud image source](https://img.nsmc.org.cn/CLOUDIMAGE/FY4B/AGRI/GCLR/FY4B_REGC_GCLR.JPG)
- [Tesseract Chinese language data](https://github.com/tesseract-ocr/tessdata/raw/main/chi_sim.traineddata)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files]

**Output Format:** [Markdown text with a local JPEG path in a qqmedia tag]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads and caches up to five JPEG files under ~/.openclaw/satellite_cache; images are compressed toward a 10 MB limit.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
