## Description: <br>
AI vintage poster generator - create retro art prints, old-school travel posters, 1950s-1970s style illustrations, antique advertising art, and nostalgic wall art from any text prompt using the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, designers, and sellers use this skill to generate vintage-style poster images from text prompts, with optional size and reference-image controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts and the Neta API token are sent to the Neta/TalesofAI service. <br>
Mitigation: Use the skill only when that remote processing is acceptable, and do not include secrets, personal data, or confidential business content in prompts. <br>
Risk: The artifact accepts the API token through a command-line flag. <br>
Mitigation: Prefer safer token handling where possible and avoid exposing tokens through shared shells, logs, or command history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blammectrappora/vintage-poster-generator) <br>
- [Neta API access](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text] <br>
**Output Format:** [Plain text image URL from a Node.js CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token and sends prompts to the Neta/TalesofAI service.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence.release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
