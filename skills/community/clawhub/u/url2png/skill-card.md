## Description: <br>
Convert URL to PNG suitable for mobile reading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoqiao](https://clawhub.ai/user/guoqiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and users can ask an agent to capture a webpage URL as a PNG optimized for mobile reading, then receive the generated image file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs shot-scraper and Chromium through uvx. <br>
Mitigation: Install only when you are comfortable with uvx downloading those dependencies in the execution environment. <br>
Risk: Rendering a URL from the local environment may load internal or sensitive pages if the agent is given those URLs. <br>
Mitigation: Use URLs you intentionally want rendered and avoid internal or sensitive URLs unless that access is deliberate. <br>
Risk: The output directory argument is passed through the shell script without quoting. <br>
Mitigation: Use simple trusted directory names, or review and adjust the script before passing paths with spaces or shell metacharacters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guoqiao/url2png) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PNG image file with brief delivery guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Captures a mobile-width, retina webpage screenshot and saves it under the requested output directory or ~/Pictures by default.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
