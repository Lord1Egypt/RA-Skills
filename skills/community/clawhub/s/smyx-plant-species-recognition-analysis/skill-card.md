## Description: <br>
Identifies plant species from images or videos and returns structured details such as species name, family, growth habits, maintenance tips, analysis results, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to identify plants from local files or public URLs and receive structured plant knowledge for gardening, ecological field work, and natural education. It also supports querying prior cloud-generated analysis reports linked to the current account identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends uploaded plant images or videos, account-linked identifiers, and report queries to external lifeemergence/open.lifeemergence services. <br>
Mitigation: Install only where that external processing is acceptable, and review the service data handling expectations before use. <br>
Risk: The skill may create local workspace data containing reusable service tokens or identity state. <br>
Mitigation: Review or clear the workspace data directory when persistent identity reuse is not desired. <br>


## Reference(s): <br>
- [API Documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-plant-species-recognition-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON] <br>
**Output Format:** [Structured plant-recognition analysis reports, Markdown report lists, or JSON detail output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include species classification, family/genus details, growth and care guidance, analysis status, and report links.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata; artifact frontmatter version: 1.0.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
