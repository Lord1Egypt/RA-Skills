## Description: <br>
Reviews Wish SSH server code for proper middleware, session handling, and security patterns. Use when reviewing SSH server code using charmbracelet/wish. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Go SSH server code built with charmbracelet/wish for middleware ordering, host key management, graceful shutdown, session handling, PTY behavior, and related security patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled Go snippets are simplified review examples and may be unsafe if copied directly into production services. <br>
Mitigation: Treat snippets as review guidance and validate production SSH services for public key authentication, PTY checks, rate limiting, logging, and graceful shutdown. <br>
Risk: A documentation-only review skill can miss context-specific security issues outside the Wish SSH patterns it covers. <br>
Mitigation: Use it as one review aid alongside normal code review, testing, security scanning, and operational safeguards. <br>


## Reference(s): <br>
- [Server Setup](references/server.md) <br>
- [Sessions & Security](references/sessions.md) <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/wish-ssh-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown code review findings with file and line citations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings use [FILE:LINE] ISSUE_TITLE formatting when defects are reported.] <br>

## Skill Version(s): <br>
2.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
