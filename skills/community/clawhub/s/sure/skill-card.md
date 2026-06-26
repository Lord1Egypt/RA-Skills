## Description: <br>
Get report from Sure personal financial board. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bt0r](https://clawhub.ai/user/bt0r) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to configure a Sure API key and base URL, then retrieve account amounts from a Sure personal financial board. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a configured Sure API key to read account amounts, which are sensitive financial data. <br>
Mitigation: Use a least-privilege or read-only API key if available, keep the key in environment variables, and treat returned account amounts as private information. <br>
Risk: A misconfigured SURE_BASE_URL could send the API key or request to the wrong Sure instance. <br>
Mitigation: Verify SURE_BASE_URL before running the command and install the skill only for Sure instances you trust. <br>


## Reference(s): <br>
- [Sure homepage](https://sure.am) <br>
- [ClawHub skill page](https://clawhub.ai/bt0r/sure) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl plus SURE_API_KEY and SURE_BASE_URL; retrieved account amounts may contain private financial information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
