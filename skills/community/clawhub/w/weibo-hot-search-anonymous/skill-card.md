## Description: <br>
Fetches public Weibo real-time hot search trends anonymously through Chrome or Edge CDP and saves the results as a Markdown table. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kazeMace](https://clawhub.ai/user/kazeMace) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can ask an agent to collect the current public Weibo hot search list without a Weibo login and save ranked results, heat values, tags, and search links in a local Markdown file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill launches and controls a local Chrome or Edge browser through a debugging port. <br>
Mitigation: Install and run it only in environments where local browser automation is acceptable, and review the browser profile and debug-port settings before use. <br>
Risk: The browser profile may retain session state if a user logs into Weibo during automation. <br>
Mitigation: Use a dedicated empty browser profile and avoid logging into Weibo unless persistent session data is intentional. <br>
Risk: The skill can terminate browser debugging processes associated with its profile. <br>
Mitigation: Check that the configured profile is not used for other work before allowing automatic browser-process cleanup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kazeMace/weibo-hot-search-anonymous) <br>
- [Weibo public hot search page](https://weibo.com/newlogin?tabtype=search) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown table file with console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bun or npx and a local Chrome, Chromium, or Microsoft Edge installation; writes to a dated Markdown file by default or to the path passed with --output.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
