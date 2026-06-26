## Description: <br>
A command-line finance data tool for querying Xinhua Finance market quotes, K-line data, stock symbols, and finance news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jindongyi011039](https://clawhub.ai/user/jindongyi011039) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to query Xinhua Finance market data, K-line data, stock symbols, and categorized finance news from a CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential handling needs review before installation. <br>
Mitigation: Avoid passing secrets directly on the command line; prefer an environment variable or protected config file and review how the API key is provided. <br>
Risk: Dependency posture needs review before use. <br>
Mitigation: Update or pin dependencies with a lockfile before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jindongyi011039/xhcj-finance) <br>
- [README](artifact/README.md) <br>
- [Xinhua Finance OpenClaw API endpoint](https://xhcj-h5-zg.cnfin.com/xhcj-bun/func/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [CLI text with JSON-formatted API responses and Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Xinhua Finance API key supplied at runtime.] <br>

## Skill Version(s): <br>
1.0.8 (source: frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
