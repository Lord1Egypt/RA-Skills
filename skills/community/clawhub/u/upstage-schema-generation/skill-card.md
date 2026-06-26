## Description: <br>
Generate a JSON schema for structured document information extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[upstage-deployment](https://clawhub.ai/user/upstage-deployment) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document automation teams use this skill to generate reusable JSON schemas for structured information extraction from sample documents, either through the Upstage schema-generation API or a more careful VLM workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Upstage API key. <br>
Mitigation: Store the key in the UPSTAGE_API_KEY environment variable and avoid exposing it in prompts, files, logs, or shared output. <br>
Risk: Sample documents may be sent to external AI or API services for schema generation. <br>
Mitigation: Use only documents approved for external processing, prefer narrow file selections over broad folders, and set file or page limits when needed. <br>
Risk: Generated schemas may omit important fields or encode ambiguous extraction rules. <br>
Mitigation: Review generated schemas against representative documents before using them in production extraction workflows. <br>


## Reference(s): <br>
- [Upstage Console](https://console.upstage.ai) <br>
- [Upstage Information Extraction Schema Generation API](https://api.upstage.ai/v1/information-extraction/schema-generation) <br>
- [Schema Design Guidelines](references/schema-design.md) <br>
- [VLM-Based Schema Generation Workflow](references/vlm-workflow.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/upstage-deployment/upstage-schema-generation) <br>
- [Publisher Profile](https://clawhub.ai/user/upstage-deployment) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [JSON schema file with a Markdown response that reports the resolved output path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is a schema JSON file under the system temp directory unless the user provides an output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
