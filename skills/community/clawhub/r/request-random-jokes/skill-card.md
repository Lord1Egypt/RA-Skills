## Description: <br>
Gets random fun content, including jokes, funny stories, and dujitang quotes, from public APIs when a user asks for light entertainment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aolinlu](https://clawhub.ai/user/aolinlu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch a random joke, funny story, or dujitang quote from public APIs and return it as plain text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts api.pearktrue.cn and returns untrusted third-party text that may be inaccurate or inappropriate. <br>
Mitigation: Install only when outbound access to that domain is acceptable, and review or filter returned text before presenting it in sensitive contexts. <br>
Risk: The script depends on the Python requests library and public API availability. <br>
Mitigation: Ensure requests is installed and handle network or API failures in calling workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aolinlu/request-random-jokes) <br>
- [Pearktrue random joke API](https://api.pearktrue.cn/api/jdyl/xiaohua.php) <br>
- [Pearktrue random duanzi API](https://api.pearktrue.cn/api/random/duanzi/) <br>
- [Pearktrue dujitang API](https://api.pearktrue.cn/api/dujitang) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional command-line argument selects xiaohua, duanzi, or dujitang; invalid or missing arguments choose a random API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
