## Description: <br>
Analyzes fixed-camera reptile images or videos to classify shedding phase, identify dysecdysis warning signs, and provide care-oriented report guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External keepers, enclosure operators, and developers use this skill to analyze reptile enclosure media for shedding progress, stuck-shed risk signals, and historical shedding reports. It supports care recommendations while limiting outputs to visual assessment rather than veterinary diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media, URLs, and report-history requests may be sent to a remote provider service and associated with an account identity. <br>
Mitigation: Install and use the skill only when the provider is trusted and users accept remote processing and account-linked report history. <br>
Risk: The skill may silently create or reuse local identity and token state in the workspace. <br>
Mitigation: Review the workspace storage model before deployment and clear local identity or token files according to the deployment's data-retention policy. <br>
Risk: Visual shedding analysis can be incorrect or incomplete when images are low resolution, poorly lit, missing required angles, or when animal health issues require professional care. <br>
Mitigation: Require clear full-body media, treat outputs as visual guidance only, and direct users to a reptile veterinarian for persistent or severe stuck-shed concerns. <br>


## Reference(s): <br>
- [Reptile shedding progress API documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON report content with command-line invocation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write analysis output to a file when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
