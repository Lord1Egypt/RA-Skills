## Description: <br>
Super Agent Knowledge helps agents capture, organize, search, and maintain local Markdown knowledge entries from URLs, extracts, social posts, and research outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to maintain a persistent local knowledge store for useful source material and research notes, then search, validate, clean up, and reindex that store when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local storage can retain secrets, private customer data, copyrighted material, or proprietary content if users add it. <br>
Mitigation: Store only material you are authorized to retain, and avoid adding secrets, private customer data, or restricted content. <br>
Risk: Cleanup automation such as `know tidy --fix` or cron-based maintenance can modify local knowledge files without close review. <br>
Mitigation: Run `know tidy` in audit mode first and review the results before using `--fix` or unattended automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/super-agent-knowledge) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown, configuration] <br>
**Output Format:** [Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes a local Markdown knowledge store with YAML frontmatter and command-driven indexing, search, validation, and cleanup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
