## Description: <br>
Analyzes gecko and lizard tail images or video URLs to detect abnormal tail shortening, tail-tip wounds, scabs, regenerated-tail baselines, and tail-loss event alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External keepers, vivarium operators, and breeding-farm staff use this skill to analyze reptile tail imagery, compare tail length against baseline signals, and produce event reports or history tables for suspected autotomy or injury. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send supplied reptile images, video URLs, user open-id values, and analysis history to the configured LifeEmergence/Open API service. <br>
Mitigation: Use only with appropriate authorization and privacy review; avoid submitting media or identifiers that are not acceptable for the configured service. <br>
Risk: Service tokens or open-id configuration may be cached locally in the OpenClaw workspace, which can be sensitive on shared machines. <br>
Mitigation: Review local workspace configuration and token storage before installation or use, especially in shared or managed environments. <br>
Risk: Low-quality or incomplete images can produce unreliable tail-loss findings. <br>
Mitigation: Require clear imagery with the full tail visible, adequate lighting, sufficient resolution, and SVL or baseline reference data; return an unreliable-signal result when those inputs are missing. <br>
Risk: Health-related visual findings may be mistaken for veterinary diagnosis or treatment instructions. <br>
Mitigation: Keep outputs limited to visual observations and conservative actions, avoid drug names, doses, brands, and surgical guidance, and direct infection-risk cases to a qualified reptile veterinarian. <br>


## Reference(s): <br>
- [API Interface Documentation](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON analysis report with optional shell commands for local invocation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include event IDs, timestamps, enclosure and individual identifiers, tail-length measurements, morphology signals, alert levels, recommended non-prescription actions, disclaimers, and optional saved output files.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
