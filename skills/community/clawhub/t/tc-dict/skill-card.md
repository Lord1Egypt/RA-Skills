## Description: <br>
Queries Taiwan Ministry of Education Traditional Chinese dictionary data for word definitions, examples, and optional dictionary update management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kai-tw](https://clawhub.ai/user/kai-tw) <br>

### License/Terms of Use: <br>
MIT License; dictionary data CC BY 3.0 TW <br>


## Use Case: <br>
External users, developers, and agents use this skill to look up Traditional Chinese word meanings, examples, and related dictionary details from Taiwan MOE dictionary data. They can also use it to download, refresh, and check local dictionary data versions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts MOE servers and downloads ZIP/XLSX dictionary data during setup or updates. <br>
Mitigation: Install it in an isolated Python environment and run updates only when network access to MOE and local dictionary changes are acceptable. <br>
Risk: Automatic cron updates can periodically change local dictionary data without an interactive review step. <br>
Mitigation: Enable cron updates only when scheduled network checks are desired, and monitor update logs or run manual update checks for tighter control. <br>
Risk: Downloaded dictionary files are stored locally under the default user directory. <br>
Mitigation: Use the documented storage configuration if a different local path, retention policy, or backup boundary is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kai-tw/tc-dict) <br>
- [MOE Dictionary Data Sources](artifact/references/DICTIONARY_SOURCES.md) <br>
- [Dictionary Data Schema](artifact/references/SCHEMA.md) <br>
- [Taiwan MOE dictionary site](https://language.moe.gov.tw/) <br>
- [Concised Mandarin Dictionary download page](https://language.moe.gov.tw/001/Upload/Files/site_content/M0001/respub/dict_concised_download.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text responses with optional shell commands and JSON status from update checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local dictionary files and may download public MOE ZIP/XLSX data when updating dictionaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
