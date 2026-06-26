## Description: <br>
Use when the user wants to collect tweets, search Twitter/X, get tweet details, set up site-use, or browse cached posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williampenrose](https://clawhub.ai/user/williampenrose) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect Twitter/X timeline, search, tweet detail, and reply data through site-use, then query cached posts for analysis or briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access account-scoped Twitter/X content, including private or personalized timeline and feed material. <br>
Mitigation: Use it only when the user intentionally wants Twitter/X content collected, and require explicit confirmation before collecting private or personalized feed content. <br>
Risk: Collected tweets are automatically retained in a local knowledge base. <br>
Mitigation: Confirm where site-use stores collected tweets and how retained data can be deleted before using the collection commands. <br>
Risk: Repeated Twitter/X commands can hit rate limits or extend cooldowns. <br>
Mitigation: Stop Twitter/X commands during rate-limit cooldowns and use local cache queries until the reset time has passed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/williampenrose/site-use-x) <br>
- [site-use Homepage](https://github.com/WilliamPenrose/site-use) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides command selection and output-size control for site-use Twitter/X collection and local cache queries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
