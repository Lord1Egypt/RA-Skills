## Description: <br>
Searches the Tongxin UOS driver center for printer drivers and downloads matching .deb driver packages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ykjack2005](https://clawhub.ai/user/ykjack2005) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, IT support staff, and UOS users use this skill to search for printer models, compare available driver packages, and download selected .deb installers for offline or local installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downloaded .deb packages are installable system software from the upstream driver provider. <br>
Mitigation: Verify the printer model, package source, and package suitability before installing downloaded drivers. <br>
Risk: Downloads may write driver packages into a default or user-specified local directory. <br>
Mitigation: Use a user-controlled download directory and inspect downloaded files before moving them into managed system locations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ykjack2005/uos-printer-driver-downloader) <br>
- [Publisher profile](https://clawhub.ai/user/ykjack2005) <br>
- [Tongxin UOS driver downloads](https://www.chinauos.com/resource/download-drivers) <br>
- [UOS driver search API](https://www.chinauos.com/driver-api/v1/driver/query/list) <br>
- [UOS driver download API](https://www.chinauos.com/driver-api/v1/driver/download?deb_id={deb_id}&driver_id={driver_id}) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, configuration] <br>
**Output Format:** [Console text plus downloaded .deb files and JSON search cache] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads are saved under printer_driver_YYYYMMDD/model-specific directories; separated search flow writes driver_list.json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
