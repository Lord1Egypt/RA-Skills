## Description: <br>
A shared stock-skill cache utility module that supports A-share trading-time detection, automatic caching, and cache expiration management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georgetao730](https://clawhub.ai/user/georgetao730) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this utility to add local JSON caching to stock trading skills, including deciding when to use cached data outside A-share trading hours. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Data passed to save() is written to cache.json in the configured local cache directory. <br>
Mitigation: Avoid storing sensitive information unless the chosen local storage location and access controls are appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/georgetao730/shared) <br>


## Skill Output: <br>
**Output Type(s):** [code, configuration, guidance] <br>
**Output Format:** [Python module and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes cache data to cache.json in the configured local cache directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
