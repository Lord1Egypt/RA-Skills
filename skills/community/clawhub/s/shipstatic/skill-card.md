## Description: <br>
Static hosting via ShipStatic. Use when the user wants to deploy a website, upload files, manage deployments, set up domains, or publish static files to shipstatic.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shipstatic-com](https://clawhub.ai/user/shipstatic-com) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to deploy static sites and manage ShipStatic deployments, domains, tokens, and account checks from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses API keys and deploy tokens for authenticated hosting operations. <br>
Mitigation: Use environment variables or a protected config file, and avoid committing or logging API keys or token creation output. <br>
Risk: Deployment commands upload local files to ShipStatic. <br>
Mitigation: Use a dedicated build output directory and review the contents before upload. <br>
Risk: Domain, token, deployment removal, and account commands can make live account changes. <br>
Mitigation: Treat remove, token, and domain commands as live changes and review targets before execution. <br>
Risk: Automatic SPA detection may inspect index.html content. <br>
Mitigation: Use --no-spa-detect when index.html content is sensitive. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shipstatic-com/shipstatic) <br>
- [Publisher Profile](https://clawhub.ai/user/shipstatic-com) <br>
- [ShipStatic Homepage](https://github.com/shipstatic/ship) <br>
- [ShipStatic Platform](https://shipstatic.com) <br>
- [API Key Settings](https://my.shipstatic.com/settings) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash, TypeScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce machine-readable JSON command variants when the ShipStatic CLI supports --json.] <br>

## Skill Version(s): <br>
0.7.20 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
