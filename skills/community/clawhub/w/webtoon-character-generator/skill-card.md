## Description: <br>
AI webtoon character generator - create manhwa-style portraits, Korean comic characters, and webtoon OCs with clean line art, expressive eyes, and vibrant colors via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, comic artists, and developers use this skill to generate webtoon-style character image URLs from text prompts, with optional size selection and reference-image UUID style inheritance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts, optional reference UUIDs, and the Neta API token are sent to api.talesofai.com. <br>
Mitigation: Avoid private, confidential, or regulated information in prompts or reference identifiers, and install only if that third-party API use is acceptable. <br>
Risk: Passing the token directly on the command line can expose it in shell history or process listings. <br>
Mitigation: Prefer environment variable expansion for the token and rotate credentials if accidental exposure is suspected. <br>


## Reference(s): <br>
- [Webtoon Character Generator on ClawHub](https://clawhub.ai/omactiengartelle/webtoon-character-generator) <br>
- [Neta API token signup](https://www.neta.art/open/) <br>
- [Neta image generation endpoint](https://api.talesofai.com/v3/make_image) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Plain text image URL, with command-line usage examples in Markdown documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token; supports portrait, landscape, square, and tall image dimensions plus an optional reference UUID.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
