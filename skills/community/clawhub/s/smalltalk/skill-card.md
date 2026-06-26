## Description: <br>
Interact with live Smalltalk image (Cuis or Squeak). Use for evaluating Smalltalk code, browsing classes, viewing method source, defining classes/methods, querying hierarchy and categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnmci](https://clawhub.ai/user/johnmci) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to inspect, execute, and modify code in live Squeak or Cuis Smalltalk images. It supports exploratory playground work as well as persistent development workflows with user-supplied image and changes files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can define or delete classes and methods, and dev mode can persist changes to a user's Smalltalk image. <br>
Mitigation: Use playground mode for experiments, back up dev images before use, and review proposed image-modifying commands before execution. <br>
Risk: LLM-powered explain, audit, and test-generation commands can send source code to configured external providers. <br>
Mitigation: Use those commands only with code that may be shared with the selected provider, and configure API keys intentionally. <br>
Risk: The background daemon keeps local VM state available through a Unix socket while it is running. <br>
Mitigation: Stop the daemon when finished and run it in an isolated local environment appropriate for the code being inspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/johnmci/smalltalk) <br>
- [Publisher Profile](https://clawhub.ai/user/johnmci) <br>
- [Squeak Setup](https://github.com/CorporateSmalltalkConsultingLtd/ClaudeSmalltalk/blob/main/SQUEAK-SETUP.md) <br>
- [Clawdbot Setup](https://github.com/CorporateSmalltalkConsultingLtd/ClaudeSmalltalk/blob/main/CLAWDBOT-SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown with Smalltalk code snippets, command output, and setup commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some commands can start a local daemon, modify a live Smalltalk image, or file generated SUnit tests into the image.] <br>

## Skill Version(s): <br>
1.7.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
