## Description: <br>
Extracts high-speed direct download and stream links from TeraBox URLs using the XAPIverse protocol without requiring a browser session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abdul-karim-mia](https://clawhub.ai/user/abdul-karim-mia) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to extract direct download and streaming links from TeraBox URLs through the XAPIverse service after user consent. It is useful when an agent needs to return a text report of file names, sizes, stream URLs, download URLs, and remaining service credits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TeraBox URLs and the configured XAPIverse API key are sent to xapiverse.com for processing. <br>
Mitigation: Ask for informed user consent before extraction and use a dedicated API key with appropriate access controls. <br>
Risk: The optional CLI download mode may write outside the promised Downloads folder according to the authoritative security summary. <br>
Mitigation: Prefer link extraction only, and avoid `--download` until provider file names are sanitized and the final resolved download path is validated. <br>
Risk: The release has a suspicious security verdict because third-party data sharing is not disclosed consistently. <br>
Mitigation: Disclose the xapiverse.com data transfer before use and review the skill before deployment in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abdul-karim-mia/terabox-link-extractor) <br>
- [API reference](references/api-reference.md) <br>
- [Version history](references/changelog.md) <br>
- [XAPIverse TeraBox Pro API](https://xapiverse.com/apis/terabox-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown text report and optional JSON or pipe-delimited CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and TERABOX_API_KEY; extraction sends the target TeraBox URL and API key to xapiverse.com.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence, package.json, _meta.json, handler.js, references/changelog.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
