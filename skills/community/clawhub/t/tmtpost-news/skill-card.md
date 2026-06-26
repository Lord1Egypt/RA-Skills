## Description: <br>
Fetches TMTPost 7x24 finance, technology, business, and venture-capital news, including hot articles, latest articles, and brief updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taimeiti](https://clawhub.ai/user/taimeiti) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve and format TMTPost finance, technology, business, and startup news through the tmtpost-news-cli. It also guides setup, update, and API-key checks before making news requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download, install, update, and execute an external TMTPost CLI on the user's machine. <br>
Mitigation: Install only when the publisher's CLI distribution is trusted, review installer and update behavior before execution, and stop on download, checksum, version, or execution errors. <br>
Risk: The skill manages an API key through CLI commands, so accidental disclosure in logs or screenshots is possible. <br>
Mitigation: Treat the API key as a secret, avoid exposing apikey-get output, and clear or rotate the key if it may have been revealed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/taimeiti/tmtpost-news) <br>
- [API Key setup guide](references/env-setup-guide.md) <br>
- [CLI update guide](references/update-guide.md) <br>
- [TMTPost API key page](https://www.tmtpost.com/exchange) <br>
- [TMTPost CLI distribution](https://pack.tmtpost.net/tmtpost-news) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown news summaries with inline shell commands and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses current CLI help output to choose subcommands and stops on CLI failure rather than falling back to other news sources.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
