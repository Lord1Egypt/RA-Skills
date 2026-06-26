## Description: <br>
Automates WPS Office tasks such as document creation, opening, format conversion, batch processing, and optional WPS 365 form, document, sheet, flowchart, and mind map operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilei0311](https://clawhub.ai/user/lilei0311) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and office automation users use this skill to let an agent create, open, list, convert, and batch process WPS Office documents. Users with WPS 365 credentials can also access cloud document, form, sheet, flowchart, and mind map operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generic document-related triggers can invoke desktop automation and type user-supplied text into the active window. <br>
Mitigation: Keep WPS Office focused during content entry, review requested actions before execution, and test first in a sandbox or virtual machine. <br>
Risk: The skill can create, open, convert, and batch process local files, including broad directory operations. <br>
Mitigation: Use trusted paths, avoid broad batch directories, and review or back up important documents before running conversions. <br>
Risk: WPS 365 operations use app_id and app_secret credentials when configured. <br>
Mitigation: Leave credentials blank unless cloud features are needed, avoid shared devices, store secrets securely, and rotate credentials periodically. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lilei0311/wps-office) <br>
- [WPS Open Platform documentation](https://open.wps.cn/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, API Calls, Configuration] <br>
**Output Format:** [JSON command results plus created, opened, converted, or exported WPS Office files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local features may operate on desktop windows and files; WPS 365 features require optional app_id and app_secret configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
