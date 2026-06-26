## Description: <br>
Generate stunning AI tarot card art and mystical oracle deck illustrations with custom arcana, divination, spiritual, occult, and fortune-card imagery via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative users use this skill to ask an agent to generate tarot or oracle card artwork from text prompts, choose image dimensions, and optionally provide a reference image UUID for style inheritance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference image UUIDs, and the Neta API token are sent to api.talesofai.com for image generation. <br>
Mitigation: Use only prompts and references that are appropriate to share with that service, and avoid confidential or personal data. <br>
Risk: Passing the API token on the command line can expose it through shell history or process listings. <br>
Mitigation: Prefer a limited token, avoid use on shared systems, and clear shell history or use a safer local wrapper when needed. <br>


## Reference(s): <br>
- [Neta AI Open Platform](https://www.neta.art/open/) <br>
- [ClawHub Skill Page](https://clawhub.ai/omactiengartelle/tarot-card-art-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text image URL with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token passed with --token; supports portrait, landscape, square, and tall sizes plus an optional reference image UUID.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
