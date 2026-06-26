## Description: <br>
Quick Capture helps an agent save user-provided notes into a local Inbox or Journal as structured knowledge notes or raw dated journal blocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daowuu](https://clawhub.ai/user/daowuu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to quickly capture notes into a local note vault, choosing between structured Inbox notes and unmodified Journal entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad capture phrases can cause notes to be saved when the user did not intend a durable record. <br>
Mitigation: Use explicit Inbox or Journal wording for captures and review the returned destination path after each write. <br>
Risk: The skill writes Markdown files into local Inbox and Journal folders, so mistakes can affect a user's note vault. <br>
Mitigation: Keep backups or version control for the note vault before routine use. <br>
Risk: Inbox mode may expand or restructure the user's source text. <br>
Mitigation: Use Journal mode when the note should remain raw and unmodified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daowuu/quick-capture) <br>
- [Project homepage](https://github.com/daowuu/elysia) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands] <br>
**Output Format:** [Markdown note files with a short text confirmation; the helper script returns JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes to local Inbox or Journal paths and requires python3.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
