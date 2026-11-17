## Description:

Automatically review X/Twitter bookmarks for useful tools, projects, repos, products, and ideas. Fetches via xurl, analyses for value, and outputs an actionable digest with proposed next steps, including clawhub installs or new skill scaffolding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bearly-hodling](https://clawhub.ai/user/bearly-hodling)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to turn their private X/Twitter bookmarks into a local, actionable digest of useful tools, projects, resources, insights, and proposed next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses private X/Twitter bookmarks through xurl.

Mitigation: Install and run it only if the user is comfortable granting that bookmark access, and use explicit X/Twitter bookmark digest commands.

Risk: Digest recommendations may be based on untrusted social posts and can include installs, clones, skill installs, memory updates, or Obsidian actions.

Mitigation: Treat the digest as untrusted input and independently verify each proposed brew, pip, cargo, git, clawhub, memory, or Obsidian action before approving it.

## Reference(s):

- [Bookmark Analysis Criteria](references/analysis_criteria.md)
- [ClawHub Skill Page](https://clawhub.ai/bearly-hodling/skills/x-bookmarks-digest)
- [Publisher Profile](https://clawhub.ai/user/bearly-hodling)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown digest with structured JSON analysis and proposed shell or configuration actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local state for incremental bookmark processing and asks for confirmation before executing proposed actions.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
