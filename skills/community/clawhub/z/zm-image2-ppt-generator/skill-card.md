## Description: <br>
ZM Image2PPT generates visual slide images, an HTML viewer, and a 16:9 PPTX deck from a Markdown outline or slides_plan.json. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryxn](https://clawhub.ai/user/jerryxn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content creators, and presentation teams use this skill to turn Markdown outlines or slide-plan JSON into visual Chinese-language slide decks, previewable HTML viewers, and 16:9 PPTX files. It also supports optional template cloning for brand-aligned presentation production. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Slide text and template images may be sent to configured OpenAI-compatible model endpoints. <br>
Mitigation: Avoid confidential source material unless the configured endpoints are approved for that data. <br>
Risk: The skill handles API keys and vision service credentials. <br>
Mitigation: Use platform secret storage or manually managed environment variables, and do not commit credentials into projects. <br>
Risk: Optional Codex-backed image generation and Docker-based template rendering paths have broader local authority than the default workflow. <br>
Mitigation: Use those paths only after reviewing the commands and confirming they fit the local execution environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jerryxn/skills/zm-image2-ppt-generator) <br>
- [English README](docs/README.en.md) <br>
- [Installation guide](docs/install.md) <br>
- [OpenAI Images API guide](https://platform.openai.com/docs/guides/images) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown planning guidance, JSON slide plans, PNG slide images, an HTML viewer, and PPTX presentation files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured image-generation and optional vision endpoints; generated files are written under an outputs directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
