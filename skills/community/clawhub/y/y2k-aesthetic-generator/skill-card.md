## Description: <br>
Generates nostalgic early-2000s and 2010s-style image prompts through the Neta AI image generation API, returning a direct image URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and developers use this skill to create Y2K and 2010s-inspired social media images, profile pictures, moodboards, party invites, and nostalgia-themed edits from text prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference image UUIDs, and the Neta API token are sent to the Neta/TalesOfAI service. <br>
Mitigation: Use non-sensitive prompts and reference images, and review the third-party service terms before sending private or regulated content. <br>
Risk: Passing the API token with the documented --token flag can expose it through shell history or process listings on shared systems. <br>
Mitigation: Run the command only in trusted local sessions, clear shell history when needed, and rotate the token if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/omactiengartelle/y2k-aesthetic-generator) <br>
- [Neta API token setup](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text image URL with Markdown usage guidance and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token; optional size and reference image UUID change the generated image request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
