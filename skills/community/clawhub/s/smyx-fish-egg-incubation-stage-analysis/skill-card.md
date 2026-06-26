## Description: <br>
Analyzes fish egg images or videos from breeding tanks to classify incubation stage, estimate hatching timing, and return stage-specific handling suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Ornamental fish breeders, aquaculture hatcheries, laboratories, and developers use this skill to send authorized fish egg media to an analysis service and receive incubation-stage reports with timing estimates and recommended next actions. It supports routine monitoring from fixed breeding-tank cameras, macro lenses, or uploaded media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided fish tank images, videos, media URLs, and an open-id to a configured remote LifeEmergence analysis service. <br>
Mitigation: Use only media the user is authorized to submit, avoid sensitive personal identifiers when a non-sensitive open-id is acceptable, and confirm the configured service endpoint before use. <br>
Risk: The skill may keep local service tokens in the workspace so future report queries can work. <br>
Mitigation: Protect the workspace, avoid sharing token-bearing configuration files, and rotate or remove tokens when access is no longer needed. <br>


## Reference(s): <br>
- [Fish egg incubation API documentation](artifact/references/api_doc.md) <br>
- [Shared analysis API documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-fish-egg-incubation-stage-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown tables and structured JSON-style analysis reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include incubation stage, egg color distribution, eye-spot ratio, estimated hatching window, alert level, recommended actions, and a disclaimer.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
