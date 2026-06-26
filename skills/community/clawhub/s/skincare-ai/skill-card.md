## Description: <br>
AISkinX analyzes skin images across seven skin parameters and provides personalized skincare product recommendations and consultation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[znsyhandao](https://clawhub.ai/user/znsyhandao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to analyze skin photos, review seven skin indicators, and generate skincare routine or product recommendation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release's privacy and path-safety promises are not reliably enforced in the shipped runtime. <br>
Mitigation: Install only after review or in a constrained environment, and do not rely on strict path restriction or URL rejection until the validation logic is fixed. <br>
Risk: Skin photos and skincare consultation text may contain sensitive personal information. <br>
Mitigation: Keep inputs local, minimize retained data, and review any generated reports before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/znsyhandao/skincare-ai) <br>
- [README.md](artifact/README.md) <br>
- [RELEASE_NOTES.md](artifact/RELEASE_NOTES.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Text, JSON, or Markdown responses with skin analysis, recommendations, and consultation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local image inputs and configurable output format; treat skin photos and consultation text as sensitive data.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
