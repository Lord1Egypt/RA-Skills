## Description: <br>
Help users add icons to their projects using the Unicon icon library, including 19,000+ icons across Lucide, Phosphor, Hugeicons, Heroicons, Tabler, Feather, Remix, Simple Icons, and Iconoir. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlesrhoward](https://clawhub.ai/user/charlesrhoward) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to search, select, bundle, configure, and generate project-specific icons for React, Vue, Svelte, or web projects. It also guides use of the Unicon CLI, REST API, local cache, and assistant-skill installation workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs users to install and run the @webrenew/unicon npm package. <br>
Mitigation: Install only if the package and publisher are trusted, and use npx or a pinned dependency workflow when your environment requires package review. <br>
Risk: CLI commands can write generated icon files, configuration files, cache data, or assistant rule files to the current project. <br>
Mitigation: Run commands from the intended project directory, review generated changes before committing, and use dry-run or explicit output paths where available. <br>
Risk: Assistant-skill installation with --all or --force can add or overwrite persistent rules for multiple AI tools. <br>
Mitigation: Use targeted assistant installation commands unless broad persistent rule installation is intended, and inspect rule files after installation. <br>
Risk: Remote API SVG content can be unsafe if rendered blindly in sensitive applications. <br>
Mitigation: Sanitize or precompile SVG content before rendering it in sensitive contexts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlesrhoward/unicon) <br>
- [Publisher profile](https://clawhub.ai/user/charlesrhoward) <br>
- [Unicon website](https://unicon.sh) <br>
- [Unicon repository](https://github.com/WebRenew/unicon) <br>
- [CLI Commands Reference](references/cli-commands.md) <br>
- [Config File Reference](references/config-file.md) <br>
- [API Reference](references/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and framework code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may lead users to run CLI commands that write icon components, SVG files, JSON config, cache data, or assistant rule files in the current project.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
