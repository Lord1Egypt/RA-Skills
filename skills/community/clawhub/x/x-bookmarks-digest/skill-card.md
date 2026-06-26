## Description: <br>
Automatically review X/Twitter bookmarks for useful tools, projects, repos, products, and ideas. Fetches via xurl, analyses for value, and outputs an actionable digest with proposed next steps, including ClawHub installs or new skill scaffolding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BEARLY-HODLING](https://clawhub.ai/user/BEARLY-HODLING) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to turn their authenticated X/Twitter bookmarks into a concise digest of useful tools, projects, products, resources, and next actions. It helps triage high-value bookmarks into proposed installs, repository evaluations, skill scaffolds, Obsidian saves, or memory saves. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads bookmarks from the X/Twitter account currently authenticated in xurl. <br>
Mitigation: Install and run it only for an account you intend to analyze, verify the active xurl identity before fetching, and use the documented dry-run flag when testing. <br>
Risk: Digest recommendations can include installs, repository clones, ClawHub installs, skill scaffolds, Obsidian saves, or memory saves. <br>
Mitigation: Review each proposed action before approving execution; the skill instructs the agent to ask before carrying out actions. <br>
Risk: The skill updates local run-tracking state after successful fetches. <br>
Mitigation: Use dry-run mode for tests that should not update state, and inspect state.json when validating a run. <br>


## Reference(s): <br>
- [Bookmark Analysis Criteria](references/analysis_criteria.md) <br>
- [ClawHub Release Page](https://clawhub.ai/BEARLY-HODLING/x-bookmarks-digest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown digest with proposed actions, plus JSON analysis from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and xurl; fetches bookmarks from the currently authenticated xurl account and maintains local run-tracking state.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release evidence, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
