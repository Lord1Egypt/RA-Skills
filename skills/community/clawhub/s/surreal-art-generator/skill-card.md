## Description: <br>
Generate surreal AI art from text prompts using the Neta AI image generation API, with options for image size and reference-based style inheritance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate surreal or absurdist image concepts from text prompts for social posts, album covers, gallery prints, concept art, and similar creative work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference UUIDs, and the Neta/TalesOfAI token are sent to a remote image service. <br>
Mitigation: Use a limited token, avoid confidential prompts, and install only when that data sharing is acceptable. <br>
Risk: Passing a literal token on the command line can expose it through shared shells or logs. <br>
Mitigation: Prefer expanding the token from a protected environment variable such as $NETA_TOKEN. <br>


## Reference(s): <br>
- [Surreal Art Generator on ClawHub](https://clawhub.ai/omactiengartelle/surreal-art-generator) <br>
- [Neta AI token and service page](https://www.neta.art/open/) <br>
- [TalesOfAI image API host](https://api.talesofai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text image URL with Markdown command examples in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a direct image URL after the remote image job completes; requires a Neta/TalesOfAI token.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
