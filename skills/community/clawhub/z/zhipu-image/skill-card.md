## Description: <br>
Checks an image.z.ai web login session, captures Zhipu-related browser cookies when needed, generates GLM-Image images through the web interface, and downloads the results locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangm199](https://clawhub.ai/user/huangm199) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to check a Zhipu Image web session, open the login flow when needed, submit an image prompt, and save generated images to a local captures directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads browser login cookies through a logged-in Chrome DevTools session and saves Zhipu-related cookies locally. <br>
Mitigation: Use an isolated browser profile, keep the network monitor off during unrelated browsing, and delete ~/.zhipu_image_session.json when the session is no longer needed. <br>
Risk: Broad browser traffic monitoring helpers can expose unrelated browsing metadata if run outside the intended Zhipu Image workflow. <br>
Mitigation: Run the monitor only while troubleshooting image.z.ai requests and stop it before using the browser for other activity. <br>


## Reference(s): <br>
- [Zhipu Image web application](https://image.z.ai/) <br>
- [ClawHub zhipu-image release page](https://clawhub.ai/huangm199/zhipu-image) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [JSON status messages, shell command guidance, and downloaded PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are saved to a local captures directory by default.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
