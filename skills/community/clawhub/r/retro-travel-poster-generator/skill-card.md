## Description: <br>
Generate vintage-style travel posters inspired by the golden age of tourism advertising (1920s-1960s WPA, art deco, mid-century modern) featuring iconic destinations, national parks, beaches, cities, landmarks, and exotic locales. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and developers use this skill to generate retro travel poster images from text prompts for print-on-demand products, wall art, postcards, travel branding, and similar creative workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, optional reference identifiers, and the API token to api.talesofai.com while the provider disclosure is inconsistent. <br>
Mitigation: Use only non-sensitive prompts and credentials, and require publisher documentation to clearly identify the destination domain and data sent before broader deployment. <br>
Risk: The skill requires an external image-generation API token. <br>
Mitigation: Use a scoped or disposable token where available, avoid sharing secrets in prompts or logs, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [Retro Travel Poster Generator on ClawHub](https://clawhub.ai/blammectrappora/retro-travel-poster-generator) <br>
- [Neta API token setup](https://www.neta.art/open/) <br>
- [Neta image generation endpoint](https://api.talesofai.com/v3/make_image) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text image URL from a command-line workflow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token and optional image size or reference image UUID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
