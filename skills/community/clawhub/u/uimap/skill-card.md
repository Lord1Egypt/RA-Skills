## Description: <br>
Provides the accurate URL and step-by-step click operation path for completing tasks on websites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[delai](https://clawhub.ai/user/delai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use Uimap to identify the correct URL and click path for completing tasks in web applications before navigating the site. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an external CLI and browser OAuth login for website-navigation searches. <br>
Mitigation: Review the OAuth consent screen before granting access and avoid submitting passwords, tokens, private customer data, or sensitive internal domains. <br>
Risk: The artifact documents a curl-to-shell installer fallback. <br>
Mitigation: Prefer npm install -g @refore-ai/uimap and review any installer script before use. <br>


## Reference(s): <br>
- [ClawHub Uimap listing](https://clawhub.ai/delai/uimap) <br>
- [@refore-ai/uimap on npm](https://www.npmjs.com/package/@refore-ai/uimap) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with bash command examples and plain-text operation instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May depend on UIMap CLI search results and an authenticated OAuth session.] <br>

## Skill Version(s): <br>
0.1.9 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
