## Description: <br>
seedream5 helps agents generate text-to-image and reference-image outputs through the Seedream5.0 API with prompt, size, watermark, and image parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runninghcm](https://clawhub.ai/user/runninghcm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate images, covers, posters, and illustrations from prompts or reference-image URLs through the Seedream5.0 API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference-image URLs are sent to an external Seedream/API provider. <br>
Mitigation: Do not submit confidential prompts or private reference-image URLs unless sharing them with the provider is acceptable. <br>
Risk: The skill can persist an API key in ~/.config/seedream5.0/.env for reuse. <br>
Mitigation: Use a dedicated revocable API key, keep the local key file protected, and rotate the key if exposure is suspected. <br>


## Reference(s): <br>
- [Seedream5.0 API Guide](references/api-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/runninghcm/seedream5-official) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text summaries with optional shell command output and image URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API response summaries, image URLs, and error hints; requires an x-api-key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
