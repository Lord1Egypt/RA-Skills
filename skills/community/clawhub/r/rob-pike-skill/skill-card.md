## Description:

A Chinese-language advisory persona skill that applies Rob Pike's documented software design principles, expression style, and decision heuristics to Go, Unix, concurrency, API design, debugging, and engineering tradeoff questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallnest](https://clawhub.ai/user/smallnest)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to get Pike-style software design guidance for Go, Unix philosophy, concurrency, interfaces, error handling, debugging, and API tradeoffs. For fact-sensitive questions, the skill directs the agent to research current information before applying the Pike-style analysis frame.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require web research for fact-sensitive questions, which can expose prompts to external search or browsing tools depending on the host agent configuration.

Mitigation: Use the skill in an agent environment with approved browsing tools and review citations or source summaries before relying on current factual claims.

Risk: The README documents npx-based installation, which can execute package manager behavior outside the Markdown artifact itself.

Mitigation: Prefer pinned, reviewed, or otherwise verified installation commands before running npx in a production environment.

Risk: Persona-style answers can overstate what Rob Pike actually said when applying principles to new topics.

Mitigation: Keep the skill's documented boundary: distinguish direct Pike evidence from Pike-style inference and state uncertainty when Pike has not publicly addressed a topic.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/smallnest/skills/rob-pike-skill)
- [README](README.md)
- [Skill definition](SKILL.md)
- [Research: writings](references/research/01-writings.md)
- [Research: conversations](references/research/02-conversations.md)
- [Research: expression DNA](references/research/03-expression-dna.md)
- [Research: external views](references/research/04-external-views.md)
- [Research: decisions](references/research/05-decisions.md)
- [Research: timeline](references/research/06-timeline.md)
- [Go at Google: Language Design in the Service of Software Engineering](https://talks.golang.org/2012/splash.article)
- [Less is exponentially more](https://commandcenter.blogspot.com/2012/06/less-is-exponentially-more.html)
- [Go Proverbs](https://go-proverbs.github.io/)
- [Concurrency is not Parallelism](https://www.youtube.com/watch?v=cN_DpYBzKso)
- [The Unix Programming Environment](https://www.informit.com/store/unix-programming-environment-9780139376818)
- [The Practice of Programming](https://www.informit.com/store/practice-of-programming-9780201615869)
- [Evrone interview with Rob Pike](https://evrone.com/rob-pike-interview)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands]

**Output Format:** [Chinese-language Markdown prose, optionally including code or shell command snippets when the user's engineering question calls for them]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require web research for fact-sensitive questions; asks the agent to distinguish documented Pike statements from Pike-style inference.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
