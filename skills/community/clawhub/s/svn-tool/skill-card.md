## Description: <br>
Helps agents guide Subversion (SVN) version-control workflows using the svn CLI, including checkout, update, commit, status, log, diff, branch operations, and conflict resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bjbook](https://clawhub.ai/user/bjbook) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when they need an agent to propose or explain SVN CLI commands for repository checkout, synchronization, commits, history review, branch management, diff inspection, and conflict handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SVN commits, deletes, reverts, cleanup with removal flags, branch changes, and credential-cache deletion can alter repository or local working-copy state. <br>
Mitigation: Review the exact target with svn status and svn diff, then confirm the action before running state-changing commands. <br>
Risk: Credentials and server trust options can expose secrets or weaken repository transport security. <br>
Mitigation: Avoid passing passwords on the command line, and avoid --trust-server-cert unless the server certificate has been verified. <br>


## Reference(s): <br>
- [SVN Tool Configuration](config/README.md) <br>
- [SVN Tool Examples](examples/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces SVN command guidance and examples; users should review commands before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
