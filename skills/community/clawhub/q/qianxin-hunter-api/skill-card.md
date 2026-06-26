## Description: <br>
Qianxin Hunter API helper for running asset search queries and managing batch export tasks with a configured QIANXIN_HUNTER_API_KEY. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PiggyHurry](https://clawhub.ai/user/PiggyHurry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security analysts use this skill to query Qianxin Hunter for asset search results, submit batch export jobs from search syntax or CSV input, check job status, and download CSV outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Hunter API access through QIANXIN_HUNTER_API_KEY. <br>
Mitigation: Configure the API key through OpenClaw settings or configuration rather than chat, and rotate the key promptly if exposure is suspected. <br>
Risk: Batch mode can upload local CSV target files to the external Hunter API. <br>
Mitigation: Review CSV contents before submission and only upload files intended for Qianxin Hunter processing. <br>
Risk: Download mode writes CSV output to a user-selected local path. <br>
Mitigation: Choose output paths deliberately to avoid overwriting existing files. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/PiggyHurry/qianxin-hunter-api) <br>
- [Hunter search API reference](references/api.md) <br>
- [Hunter batch query API reference](references/api_batch.md) <br>
- [API key configuration guidance](references/apikey_config.md) <br>
- [Batch file template](references/batch_file_template.csv) <br>
- [Hunter batch template download](https://hunter.qianxin.com/api/search/batch/template?type=api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON API responses, and CSV downloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the requests package, and QIANXIN_HUNTER_API_KEY; batch downloads write CSV files to the selected output path.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
