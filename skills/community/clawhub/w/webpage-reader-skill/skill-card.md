## Description: <br>
Downloads webpage content with Google Chrome in headless mode and returns the HTML content with a basic summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[24K-handsomer](https://clawhub.ai/user/24K-handsomer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users can use this skill to fetch a webpage through headless Chrome, inspect the returned HTML, and get a simple title, length, and paragraph-count summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may attempt to install Google Chrome, which can modify the host environment. <br>
Mitigation: Install Chrome manually before use and run the skill without elevated privileges. <br>
Risk: The skill runs user-supplied URLs in headless Chrome and can contact external, local, or internal network services. <br>
Mitigation: Use trusted public URLs only; avoid localhost, internal services, cloud metadata addresses, signed-in pages, and untrusted URLs. <br>
Risk: Downloaded HTML may contain sensitive page content if the supplied URL points to private or authenticated material. <br>
Mitigation: Do not use the skill on sensitive pages, and review outputs before sharing or storing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/24K-handsomer/webpage-reader-skill) <br>
- [Google Chrome](https://www.google.com/chrome/) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [JSON-like Python dictionary with success, message, content, and summary fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a URL input and Google Chrome; returns full HTML content plus a basic summary.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
