## Description: <br>
Read, search, send, and manage Zoho Mail from the terminal with JSON output for scripting and agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robsannaa](https://clawhub.ai/user/robsannaa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agents use this skill to inspect, search, send, organize, and download Zoho Mail content through the zoho CLI after local OAuth setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Zoho credentials, keyring entries, config files, debug logs, downloaded attachments, and email bodies are sensitive. <br>
Mitigation: Treat those materials as confidential, avoid exposing local config or keyring data, and review debug logs before sharing them. <br>
Risk: The skill can send email, attach files, permanently delete mail, and delete folders through the external zoho CLI. <br>
Mitigation: Require explicit user review before sending messages, attaching files, deleting mail permanently, or deleting folders. <br>
Risk: The skill depends on an external zoho CLI and local OAuth setup. <br>
Mitigation: Install only from a trusted zoho CLI source and complete authentication on the user's local machine. <br>


## Reference(s): <br>
- [Zoho CLI GitHub repository](https://github.com/robsannaa/zoho-cli) <br>
- [Zoho CLI setup guide](https://github.com/robsannaa/zoho-cli#setup) <br>
- [ClawHub skill page](https://clawhub.ai/robsannaa/zoho-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The underlying zoho CLI writes JSON to stdout by default, can emit Markdown tables with --md, and writes errors, prompts, and debug logs to stderr.] <br>

## Skill Version(s): <br>
0.1.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
