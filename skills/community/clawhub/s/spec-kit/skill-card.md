## Description: <br>
Use GitHub Spec Kit for Spec-Driven Development. Initialize projects, create specifications, and build software using the /speckit.* slash commands. Supports Claude Code, GitHub Copilot, Gemini CLI, and Codebuddy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AungMyoKyaw](https://clawhub.ai/user/AungMyoKyaw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to initialize Spec Kit projects, create executable specifications, clarify requirements, plan implementation, and build software through the /speckit.* workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spec Kit can automate project setup and development, which may change files, configuration, tests, and commits in a working project. <br>
Mitigation: Use it on a clean branch or disposable project when possible, review generated diffs and test results, and inspect commits before pushing or sharing them. <br>
Risk: The documented setup runs Spec Kit through uvx from a GitHub source, which may matter for supply-chain controls. <br>
Mitigation: Pin or review the GitHub source used by uvx when supply-chain control is required. <br>


## Reference(s): <br>
- [Spec Kit Skill Page](https://clawhub.ai/AungMyoKyaw/spec-kit) <br>
- [Spec Kit Documentation](https://github.github.com/spec-kit/) <br>
- [Spec Kit Repository](https://github.com/github/spec-kit) <br>
- [uv Documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with slash-command examples and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify project files, configuration, specifications, implementation code, tests, and Git commits when used with Spec Kit commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
