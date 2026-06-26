## Description: <br>
Generate yearbook-style portrait image URLs from text prompts via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate yearbook-style portraits from prompts, with optional output sizing and reference-image UUID inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and API tokens are sent to a remote TalesOfAI endpoint that is not consistently disclosed as the actual recipient. <br>
Mitigation: Review the service endpoint before use and use only a low-scope token intended for the talesofai.cn/Neta service. <br>
Risk: Prompts or reference-image identifiers can include personal or sensitive information. <br>
Mitigation: Avoid sensitive personal details in prompts or reference images, and obtain appropriate consent for any identifiable portrait generation. <br>
Risk: Passing long-lived tokens on the command line can expose them through shell history or process inspection. <br>
Mitigation: Use short-lived or low-scope tokens, avoid persistent shell history for token-bearing commands, and rotate tokens after use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/omactiengartelle/yearbook-photo-skill) <br>
- [Neta API Token Signup](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text image URL on stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token; supports optional size and reference image UUID inputs.] <br>

## Skill Version(s): <br>
1.6.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
