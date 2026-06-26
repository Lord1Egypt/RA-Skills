## Description: <br>
Convert URL to PDF suitable for mobile reading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoqiao](https://clawhub.ai/user/guoqiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to render a web page as a mobile-oriented PDF and receive the resulting local PDF file path for sharing through the agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens user-provided URLs from the local machine in a Playwright browser and saves rendered page content as a PDF. <br>
Mitigation: Avoid using it on localhost, private-network, admin, or credential-bearing pages unless that content is intentionally being rendered into a PDF and shared back through the agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guoqiao/url2pdf) <br>
- [Usage examples](https://github.com/guoqiao/skills/tree/main/url2pdf/examples) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text] <br>
**Output Format:** [PDF file with stdout path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script saves the PDF under the configured output path, defaulting to the user's Documents directory.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
