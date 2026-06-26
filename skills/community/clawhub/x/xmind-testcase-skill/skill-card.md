## Description: <br>
Generate structured XMind test cases from functional requirement descriptions for login, registration, checkout, search, and related features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manman1104](https://clawhub.ai/user/manman1104) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers, test engineers, and developers use this skill to turn functional requirement text into structured test case outlines and an XMind mind-map file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact declares an entry command that does not match the provided Python file, so the packaged skill may need cleanup before it runs correctly. <br>
Mitigation: Verify the release wiring before automation use, or invoke the provided generator through the declared workflow after packaging is corrected. <br>
Risk: The generator writes testcase.xmind in the working directory, which can overwrite an existing file with the same name. <br>
Mitigation: Run it in a dedicated workspace or adjust the output path before using it with existing files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/manman1104/xmind-testcase-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, file] <br>
**Output Format:** [Structured test case data and a generated .xmind file reference] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes testcase.xmind in the working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
