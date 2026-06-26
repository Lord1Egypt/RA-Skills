## Description: <br>
Zotero Manager helps agents search Zotero libraries, import references by DOI, inspect categories, export references, and route legacy Zotero requests through the knowledge entry point. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and external users use this skill to work with Zotero bibliographic libraries from an agent workflow, including searching references, importing DOI metadata, checking local API setup, and producing reference exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Zotero API credentials and may read tokens from local files or environment variables. <br>
Mitigation: Use a least-privilege Zotero token, prefer read-only permissions unless importing is required, and store tokens in a protected secret store or tightly permissioned file. <br>
Risk: Import commands can modify a Zotero library by creating items from DOI metadata. <br>
Mitigation: Run import actions only with intentional write permissions and review target collections before bulk DOI imports. <br>
Risk: The local API URL is configurable and could be pointed away from the expected local Zotero service. <br>
Mitigation: Use the default local Zotero endpoint or another trusted local endpoint, and do not pass non-local URLs to --api-url. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jirboy/zotero-manager) <br>
- [Zotero API key settings](https://www.zotero.org/settings/keys) <br>
- [Zotero Web API v3 documentation](https://www.zotero.org/support/dev/web_api/v3/start) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call local or remote Zotero APIs and may create or modify Zotero library items when import commands are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
