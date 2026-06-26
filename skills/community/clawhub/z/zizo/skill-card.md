## Description: <br>
Search images and boards in zizo library. Use when user asks to search for images, photos, pictures, visual assets, or boards/collections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foobarhe](https://clawhub.ai/user/foobarhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to search Zizo for images, photos, visual assets, and boards from an agent workflow. It supports public searches by default and can search a user's own or all accessible image content when configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and the ZIZO_TOKEN are sent to the configured Zizo HTTPS server. <br>
Mitigation: Install only when Zizo is trusted for the intended searches, keep ZIZO_TOKEN private, and leave ZIZO_SERVER set to the official HTTPS endpoint unless another trusted server is intentionally used. <br>
Risk: Using the mine or all search scopes can include private or otherwise accessible Zizo content in results. <br>
Mitigation: Use the default public scope unless the workflow specifically requires private or all accessible content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/foobarhe/zizo) <br>
- [Zizo service](https://zizo.pro) <br>
- [Zizo token settings](https://zizo.pro/#/?settings=token) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown with inline bash commands and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search commands return formatted image or board result lists, including titles, IDs, URLs or counts when provided by Zizo.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
