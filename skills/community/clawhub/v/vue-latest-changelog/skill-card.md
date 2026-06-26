## Description: <br>
Guides an agent to fetch the latest Vue changelog section and save it locally for review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aliangtech](https://clawhub.ai/user/aliangtech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release reviewers use this skill to retrieve the newest Vue changelog entry and organize it as a local markdown file for inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes an outbound request to GitHub for Vue changelog content. <br>
Mitigation: Confirm the environment permits the GitHub request and that the upstream changelog source is acceptable before running the script. <br>
Risk: The script writes or overwrites assets/latest_changelog.md in the current project. <br>
Mitigation: Review the target path before execution and preserve any existing changelog file that should not be replaced. <br>
Risk: The write can fail if the expected assets directory is missing. <br>
Mitigation: Create or verify the assets directory before running node scripts/changelog.js. <br>


## Reference(s): <br>
- [Vue core changelog](https://raw.githubusercontent.com/vuejs/core/refs/heads/main/CHANGELOG.md) <br>
- [ClawHub skill page](https://clawhub.ai/aliangtech/vue-latest-changelog) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown file with concise execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches Vue's public changelog from GitHub and writes the first changelog section to assets/latest_changelog.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
