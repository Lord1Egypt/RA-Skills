## Description: <br>
AI steampunk art generator that creates Victorian steampunk portraits, cyberpunk Victorian characters, brass-and-gears illustrations, cosplay reference art, and industrial fantasy scenes through the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate steampunk-themed artwork from text prompts, optionally selecting image size and a reference image UUID for style inheritance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference image UUIDs, and the user-supplied Neta API token are sent to the TalesOfAI/Neta service. <br>
Mitigation: Avoid sensitive prompts or reference IDs, and use short-lived or low-scope tokens where available. <br>
Risk: Passing the Neta token on the command line can expose it through local process listings, shell history, or logs. <br>
Mitigation: Run the command only in trusted environments and rotate the token if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/blammectrappora/steampunk-art-generator) <br>
- [Neta token and API access](https://www.neta.art/open/) <br>
- [TalesOfAI image generation API endpoint](https://api.talesofai.com/v3/make_image) <br>
- [TalesOfAI task polling API endpoint](https://api.talesofai.com/v1/artifact/task/${taskUuid}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; runtime output is a direct image URL.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-supplied Neta API token; supports portrait, landscape, square, and tall image dimensions plus an optional reference image UUID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
