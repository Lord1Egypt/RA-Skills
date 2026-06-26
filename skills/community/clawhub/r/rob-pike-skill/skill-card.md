## Description: <br>
Rob Pike Skill gives agents a Chinese-language Rob Pike-style programming perspective grounded in research notes, mental models, and decision heuristics for Go, Unix philosophy, concurrency, interfaces, and software design. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallnest](https://clawhub.ai/user/smallnest) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to analyze programming, API, concurrency, tooling, and software-design questions through Rob Pike-inspired principles. It is especially suited to Go and Unix-adjacent design discussions where concise guidance and explicit uncertainty boundaries are useful. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may encourage web research for factual or current programming questions, which can expose sensitive prompt details if the user includes private code or confidential context. <br>
Mitigation: Avoid including secrets, private source, customer data, or confidential internal details in prompts where external search or research may be used. <br>
Risk: The skill imitates a public figure's perspective and may overfit advice to a specific style rather than the user's engineering constraints. <br>
Mitigation: Treat responses as design guidance to review, and verify technical claims or tradeoffs against project requirements before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smallnest/rob-pike-skill) <br>
- [Publisher profile](https://clawhub.ai/user/smallnest) <br>
- [README](artifact/README.md) <br>
- [Writings research notes](artifact/references/research/01-writings.md) <br>
- [Conversations research notes](artifact/references/research/02-conversations.md) <br>
- [Expression DNA research notes](artifact/references/research/03-expression-dna.md) <br>
- [External views research notes](artifact/references/research/04-external-views.md) <br>
- [Decisions research notes](artifact/references/research/05-decisions.md) <br>
- [Timeline research notes](artifact/references/research/06-timeline.md) <br>
- [Language Design in the Service of Software Engineering](https://talks.golang.org/2012/splash.article) <br>
- [Less is Exponentially More](https://commandcenter.blogspot.com/2012/06/less-is-exponentially-more.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Concise Markdown or plain-text programming advice in a Rob Pike-inspired voice] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prompt the agent to research factual or current technical questions before answering; does not contain executable code.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
