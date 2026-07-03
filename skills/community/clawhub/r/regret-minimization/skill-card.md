## Description: <br>
Guides agents through a Regret Audit for major, hard-to-reverse life decisions where joy, meaning, identity, or autonomy matter more than expected-value math. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to structure coaching for major life decisions such as career pivots, founding a company, relocation, relationship exits, or family decisions. It helps define the decision fork, compare realistic path regrets from an age-80 perspective, name the real unit being optimized, and set a commitment date. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill could be over-applied to routine, reversible, or primarily financial decisions where regret minimization is the wrong tool. <br>
Mitigation: Use the documented fit check before running the audit and redirect routine, reversible, or expected-value decisions to a more appropriate framework. <br>
Risk: The skill influences high-stakes personal choices and may produce misleading guidance if it projects values for the user. <br>
Mitigation: Have the user define their own age-80 evaluator, compare realistic versions of each path, name the optimized unit, and set a concrete re-open trigger. <br>
Risk: Security evidence notes that the package may include powerful ClawHub or Convex maintainer workflows. <br>
Mitigation: Install only when those maintainer workflows are intended, review proposed commands before approval, keep credentials scoped, and use documented dry-run and confirmation steps. <br>


## Reference(s): <br>
- [Regret Minimization skill listing](https://clawhub.ai/deciqai/skills/regret-minimization) <br>
- [Sources for Regret Minimization](references/sources.md) <br>
- [Jeff Bezos, D.E. Shaw to Amazon example](examples/jeff-bezos-de-shaw-amazon-1994.md) <br>
- [Jeff Bezos 1997 Letter to Shareholders](https://www.sec.gov/Archives/edgar/data/1018724/000119312513151836/d511111dex991.htm) <br>
- [Jeff Bezos 2010 Princeton Baccalaureate Remarks](https://www.princeton.edu/news/2010/05/30/2010-baccalaureate-remarks) <br>
- [Loomes and Sugden, Regret Theory](https://www.jstor.org/stable/2232669) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown text with stepwise coaching prompts and a structured Regret Audit template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May pause at explicit wait checkpoints so the user can supply decision-specific inputs before the audit proceeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
