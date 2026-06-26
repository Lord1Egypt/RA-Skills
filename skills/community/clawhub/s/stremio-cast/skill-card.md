## Description: <br>
Busca conteúdo no Stremio Web e transmite para dispositivos Chromecast usando CATT e Playwright. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pedro-valentim](https://clawhub.ai/user/pedro-valentim) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to search for films or series in Stremio Web and cast the selected stream to a named Chromecast device. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the code uses a hard-coded Stremio server address that does not match the documented local setup. <br>
Mitigation: Review and edit the script to point to the user's own Stremio service before installing or running it. <br>
Risk: The security guidance calls out disabled browser protections and the need to confirm the target device and stream. <br>
Mitigation: Remove or justify disabled browser protections, then confirm the exact Chromecast device and selected stream before casting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pedro-valentim/stremio-cast) <br>
- [Stremio Web](https://app.strem.io/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Console text with command-line execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs browser automation and starts a Chromecast cast through CATT when dependencies and local services are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
