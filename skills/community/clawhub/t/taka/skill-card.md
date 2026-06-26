## Description: <br>
Taka creative tools CLI generates AI images, videos, emails, and flyers for small businesses from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielokaninm](https://clawhub.ai/user/danielokaninm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and AI agents use Taka to create and manage small-business marketing content such as Instagram posts, emails, flyers, logos, blog posts, images, and videos from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to run shell commands that create, update, or delete creative projects and may call the Taka service. <br>
Mitigation: Review generated commands before execution, authenticate with the intended Taka account, and use listing or retrieval commands to confirm affected creative IDs before update or delete operations. <br>
Risk: Generated marketing assets can be inaccurate, off-brand, or unsuitable for publication. <br>
Mitigation: Have a human review generated images, videos, emails, and flyer content before publishing or sending it to customers. <br>
Risk: The CLI stores local access and refresh tokens in the user's Taka config file. <br>
Mitigation: Use the documented logout command when access should be removed and protect the local account environment where the token file is stored. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danielokaninm/taka) <br>
- [Publisher profile](https://clawhub.ai/user/danielokaninm) <br>
- [Taka website](https://taka.ai) <br>
- [Taka CLI npm package](https://www.npmjs.com/package/taka-cli) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [HOW_TO_RUN.md](artifact/HOW_TO_RUN.md) <br>
- [QUICK_START.md](artifact/QUICK_START.md) <br>
- [Examples](artifact/examples/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown] <br>
**Output Format:** [Markdown instructions with bash command examples and JSON-oriented CLI workflows.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The Taka CLI commands described by the skill generally return JSON for agent parsing.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
