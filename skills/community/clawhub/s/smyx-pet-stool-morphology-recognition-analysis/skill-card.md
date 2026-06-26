## Description: <br>
Analyzes dog toilet or outdoor dog-walking image and video inputs to report pet stool color, shape, and visible blood or mucus as observation features without diagnosing disease. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and pet-health monitoring workflows use this skill to submit dog stool-area images or videos and receive structured observation reports for stool morphology and abnormal feature screening. The skill is for observation support only and does not provide veterinary diagnosis or treatment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet images, videos, URLs, account-linked identifiers, and report history may be sent to the publisher's remote services. <br>
Mitigation: Use only when that data sharing is acceptable, confirm privacy and retention terms before deployment, and avoid sensitive media or URLs. <br>
Risk: The skill silently creates or reuses a persistent local identity and token store for report history access. <br>
Mitigation: Use isolated workspaces for different users, avoid shared environments unless identity isolation is guaranteed, and know how to delete the local data/smyx-common-claw.db store. <br>
Risk: Stool morphology output can be mistaken for medical diagnosis or treatment advice. <br>
Mitigation: Treat results as observation support only and escalate concerning findings to a qualified veterinarian. <br>


## Reference(s): <br>
- [Pet stool morphology API documentation](references/api_doc.md) <br>
- [Skill usage guide](https://lifeemergence.com/guide.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON analysis report, with optional saved text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured observation fields, risk prompts, recommendations, report links, and remote history-list results.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
