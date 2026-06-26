## Description: <br>
Batch submits websites to AI tool and SEO directories to earn backlinks, using Playwright automation to check whether directories accept free submissions and fill submission forms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kennyzir](https://clawhub.ai/user/kennyzir) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and site operators use this skill to prepare and run backlink directory submissions for a website while recording which directories are free, paid, login-gated, or failed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live runs can automatically submit website details and a contact email to external directory websites with limited user review. <br>
Mitigation: Start with check-only behavior, manually limit the directory list, review target policies, and use a non-personal contact email before enabling submissions. <br>
Risk: The quick-submit script has mismatched behavior and does not reliably require explicit user-provided target and data. <br>
Mitigation: Do not run quick_submit.py unless it is fixed to accept explicit target and data inputs, then review those inputs before execution. <br>


## Reference(s): <br>
- [Directory list](references/directories.txt) <br>
- [Targets directory guide](targets/README.md) <br>
- [ClawHub release page](https://clawhub.ai/kennyzir/seo-backlink-submitter) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Batch runs save timestamped JSON results that include check results, submission results, statuses, URLs, and errors.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
