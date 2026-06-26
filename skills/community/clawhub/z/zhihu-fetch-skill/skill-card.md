## Description: <br>
Fetches Zhihu collection lists, articles, images, and profile activity into Markdown, with resumable batch jobs and optional Obsidian import. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[handsomestwei](https://clawhub.ai/user/handsomestwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide an agent through authenticated Zhihu collection, article, and profile-activity capture workflows, then save the results as Markdown, images, JSON progress files, or Obsidian notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated Zhihu automation and stealth browsing may trigger verification or create account-policy risk. <br>
Mitigation: Use only accounts and content you are authorized to access, preferably with a low-privilege Zhihu account, and stop if Zhihu presents verification or access warnings. <br>
Risk: The skill stores Zhihu session cookies and browser user data locally. <br>
Mitigation: Run it in a dedicated workspace, restrict access to `zhihu_cookies.json` and `chrome_user_data`, and do not share or commit those files. <br>
Risk: Obsidian import behavior can move or delete local export files. <br>
Mitigation: Back up the vault and review the generated Markdown and image directories before importing or running write-to-Obsidian scripts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/handsomestwei/zhihu-fetch-skill) <br>
- [Skill Entry and Command Reference](SKILL.md) <br>
- [Script Dependencies](scripts/requirements.txt) <br>
- [Playwright](https://playwright.dev/) <br>
- [AgentSkills](https://agentskills.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; scripts produce JSON lists, Markdown article files, local images, progress files, and Obsidian notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist Zhihu cookies and browser user data in the configured workspace; batch jobs use progress files for resume and retry behavior.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
