## Description: <br>
AI watercolor art generator that creates watercolor paintings, portraits, and illustrations from text prompts using the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate watercolor-style images from prompts for portraits, illustrations, social posts, gifts, commissions, and printable wall art. The skill supports portrait, landscape, square, and tall image sizes plus an optional reference image UUID for style inheritance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference image UUIDs, and the Neta API token are sent to api.talesofai.com. <br>
Mitigation: Use a revocable token, avoid sensitive prompt or reference content, and review the external service before use. <br>
Risk: Passing the token with --token can expose it through shell history or local process listings. <br>
Mitigation: Prefer short-lived or revocable tokens, avoid shared shells, and rotate the token if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blammectrappora/watercolor-art-generator) <br>
- [Publisher profile](https://clawhub.ai/user/blammectrappora) <br>
- [Neta API token page](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls] <br>
**Output Format:** [Plain text URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a direct image URL after polling the Neta API; requires a Neta API token.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
