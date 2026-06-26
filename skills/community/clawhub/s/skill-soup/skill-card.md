## Description: <br>
Autonomous skill generation agent that picks up community ideas, uses evolved builder tools to produce Agent Skills, and publishes them back to the Skill Soup ecosystem; it also supports submitting ideas, voting on ideas, and voting on skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BennettPhil](https://clawhub.ai/user/BennettPhil) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and community maintainers use this skill to authenticate to a Skill Soup API, submit or vote on ideas and skills, generate Agent Skills from community ideas, and publish generated skills back to the ecosystem. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Skill Soup or GitHub-linked identity to generate, mutate, and publish public skill content with weak approval boundaries. <br>
Mitigation: Use a dedicated test account, monitor autonomous runs, and review generated files before publication. <br>
Risk: Externally synced builder instructions can influence generated skills and may weaken review expectations. <br>
Mitigation: Treat synced builders as untrusted input, inspect builder changes, and scan generated skills before deployment. <br>
Risk: A saved authentication token may remain in .soup/auth.json after use. <br>
Mitigation: Protect the local workspace and delete .soup/auth.json when the token is no longer needed. <br>


## Reference(s): <br>
- [Mutation Guide](references/mutation-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, files, guidance] <br>
**Output Format:** [Markdown instructions, shell commands, JSON API payloads, configuration files, and generated skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local .soup workspace files and publish generated skills or builders through the configured Skill Soup API.] <br>

## Skill Version(s): <br>
0.5.0 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
