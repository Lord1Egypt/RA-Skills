## Description: <br>
Willhaben CLI for searching Austria's largest classifieds marketplace. Search listings, view details, check seller profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pasogott](https://clawhub.ai/user/pasogott) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and command-line users use this skill to install and run whcli for searching willhaben.at listings, viewing listing details, and checking seller profiles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs an external whcli package from a Homebrew tap or source repository. <br>
Mitigation: Review the package source or formula before installing in sensitive environments, and install only when you trust the publisher. <br>
Risk: The artifact notes known CLI limitations, including a bug in the show command and location filters that may include nearby regions. <br>
Mitigation: Validate important listing details in willhaben.at directly before relying on CLI output for decisions. <br>


## Reference(s): <br>
- [Willhaben](https://willhaben.at) <br>
- [whcli repository](https://github.com/pasogott/whcli) <br>
- [whcli issues](https://github.com/pasogott/whcli/issues) <br>
- [Homebrew tap](https://github.com/pasogott/homebrew-tap) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may produce table, JSON, or CSV output when run through whcli.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
