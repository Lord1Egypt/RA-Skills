## Description: <br>
ZenStudio CLI helps agents use zencli to generate images and videos, manage projects, upload and download assets, manage materials and canvases, and interact with the ZenStudio platform from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoda](https://clawhub.ai/user/zhaoda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, developers, and agent operators use this skill to manage ZenStudio content workflows through zencli, including AI image and video generation, project operations, asset handling, and canvas updates. The artifact states that ZenStudio CLI has been upgraded to WorkRally and that new features will be released there. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad ZenStudio account-changing authority, including project, upload, download, canvas delete or overwrite, and generic tool passthrough operations. <br>
Mitigation: Install only when the operator intends to delegate ZenStudio content management, prefer named commands, and confirm before uploads, downloads, canvas delete or overwrite actions, or tools call usage. <br>
Risk: The CLI uses sensitive ZenStudio credentials that may be stored in ~/.zencli/config.json or a directory selected with ZENCLI_CONFIG_DIR. <br>
Mitigation: Protect the saved credential file, use scoped API keys where available, and avoid exposing ZENSTUDIO_API_KEY or the config directory to untrusted processes. <br>


## Reference(s): <br>
- [ZenStudio CLI Skill Page](https://clawhub.ai/zhaoda/zenstudio) <br>
- [ZenStudio Homepage](https://ai.tvi.v.qq.com/zenstudio) <br>
- [ZenStudio Open API Key Setup](https://ai.tvi.v.qq.com/zenstudio/open-api) <br>
- [WorkRally Migration Skill](https://clawhub.ai/tencent-adm/workrally) <br>
- [WorkRally npm Package](https://www.npmjs.com/package/workrally) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI options] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent guidance should prefer named zencli commands and JSON output where available.] <br>

## Skill Version(s): <br>
1.3.7 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
