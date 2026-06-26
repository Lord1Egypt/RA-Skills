## Description: <br>
Version tracking for Agent Skills bundles and their associated files across sessions, surfaces, and platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snapsynapse](https://clawhub.ai/user/snapsynapse) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to keep agent skill bundles traceable as they move across chat, CLI, IDE, API, registry, and local filesystem workflows. It guides creation and maintenance of manifests, changelogs, hashes, frontmatter modes, package variants, and handoff notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional shell scripts act on the files listed in MANIFEST.yaml and can package or validate the wrong files if that manifest is stale or overbroad. <br>
Mitigation: Review MANIFEST.yaml before running package.sh or validate.sh, and confirm that it lists only the intended bundle files. <br>
Risk: Generated manifests, changelogs, or handoff notes can carry private or stale information into a shared bundle. <br>
Mitigation: Review generated MANIFEST.yaml, CHANGELOG.md, and handoff notes before publishing or sharing a package. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/snapsynapse/skill-provenance) <br>
- [Publisher Profile](https://clawhub.ai/user/snapsynapse) <br>
- [README](README.md) <br>
- [MANIFEST](MANIFEST.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with YAML, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or update MANIFEST.yaml, CHANGELOG.md, package metadata, validation commands, and handoff notes when the user asks the agent to modify a skill bundle.] <br>

## Skill Version(s): <br>
4.9.0 (source: server release, MANIFEST.yaml, CHANGELOG.md; released 2026-04-08) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
