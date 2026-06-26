## Description: <br>
Reddit content creation assistant for indie developers and product builders that creates community-appropriate posts, researches subreddits, logs published links, and analyzes Reddit performance data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EdisonChenAI](https://clawhub.ai/user/EdisonChenAI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers, indie builders, and product teams use this skill to draft Reddit posts, research suitable communities, record published post URLs, and summarize post performance for future content decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs the agent to run local startup and workflow scripts that were not included in the reviewed package. <br>
Mitigation: Inspect or supply the referenced scripts before allowing automatic startup commands, and run the skill only in a controlled directory. <br>
Risk: Local memory files may retain launch plans, internal URLs, product strategy, post drafts, and performance history. <br>
Mitigation: Avoid storing confidential material unless local retention is acceptable, and review memory files before sharing or exporting the workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EdisonChenAI/reddit-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text guidance with inline shell commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local memory files for configuration, drafts, subreddit profiles, post logs, and monthly performance reports when the referenced helper scripts are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter states 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
