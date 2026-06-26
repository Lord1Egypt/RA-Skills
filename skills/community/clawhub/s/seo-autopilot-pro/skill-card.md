## Description: <br>
Fully automated SEO content freshness engine that monitors keyword research reports, generates landing pages and blog posts, runs SEO audits, and pushes updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kennyzir](https://clawhub.ai/user/kennyzir) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to convert recurring keyword research reports into deployed SEO landing pages or blog posts for web projects. It is intended for projects where automated content generation, SEO checks, git commits, and deployment-triggering pushes are an accepted workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify a website repository and push changes that may deploy to production without a clear human approval step. <br>
Mitigation: Use a staging branch or pull requests, review generated diffs and SEO content before deployment, restrict git credentials or bot accounts, and document how to disable the hook and undo changes. <br>


## Reference(s): <br>
- [Setup Checklist](references/setup-checklist.md) <br>
- [Steering Template](references/steering-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with JSON configuration snippets, generated website files, git commands, and SEO audit guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces up to three new pages per keyword report and updates project state tracking.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
