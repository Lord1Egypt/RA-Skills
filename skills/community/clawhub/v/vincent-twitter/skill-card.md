## Description: <br>
Twitter/X.com data access for agents to search tweets, look up user profiles, and retrieve recent tweets through the Vincent credit system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[glitch003](https://clawhub.ai/user/glitch003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent retrieve recent Twitter/X content, user profiles, tweet details, and user timelines through a paid Vincent proxy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable an agent to spend money through Vincent credits, including an autonomous USDC top-up flow. <br>
Mitigation: Prefer manual top-ups; require explicit approval for each purchase, set a hard budget, and use a wallet funded only for this purpose. <br>
Risk: The skill invokes an unpinned external npm CLI through npx, so executed code can change between runs. <br>
Mitigation: Pin and review the @vincentai/cli version before use, especially in production or shared environments. <br>
Risk: A local Vincent DATA_SOURCES key may be stored in the configured credentials directory. <br>
Mitigation: Restrict access to credential files, revoke the key when it is no longer needed, and re-link only with owner approval. <br>


## Reference(s): <br>
- [Vincent homepage](https://heyvincent.ai) <br>
- [ClawHub listing](https://clawhub.ai/glitch003/vincent-twitter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Twitter/X responses may include tweet or profile fields plus Vincent cost and remaining-credit metadata.] <br>

## Skill Version(s): <br>
1.0.69 (source: server release metadata; submitted SKILL.md frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
