## Description: <br>
Weekly AI tool mini-review — Sol reviews a tool she actually uses, with rating, verdict, and context from dev.to community discussion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amrree](https://clawhub.ai/user/amrree) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and site maintainers use this skill to automate weekly AI tool mini-reviews by gathering dev.to context, drafting with MiniMax, and creating Jekyll blog posts for a local site. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled automatic publication and git pushes may publish generated content without adequate review. <br>
Mitigation: Run the workflow manually before enabling launchd and require a separate review step before any git push. <br>
Risk: Use of a local MiniMax API key and local Jekyll repository can expose credentials or write to the wrong publishing target. <br>
Mitigation: Keep the MiniMax key narrowly scoped and confirm the local site path and permissions before installation. <br>
Risk: The referenced external source script controls the actual publication behavior. <br>
Mitigation: Review the source script before enabling scheduled execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amrree/skills/sol-tool-spotlight) <br>
- [sol-skills-bundle source link referenced by artifact](https://github.com/TheSolAI/sol-skills-bundle) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands] <br>
**Output Format:** [Markdown Jekyll post with scheduled file-write and git commit/push actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates 350-500 word mini-reviews and is intended to run weekly on Fridays at 9am UK time.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
