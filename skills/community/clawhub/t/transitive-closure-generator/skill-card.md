## Description: <br>
Compute transitive closure on graphs to infer implicit relationships and expand graphs with logically implied connections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fisa712](https://clawhub.ai/user/fisa712) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to analyze graph relationships, expand knowledge graphs, infer dependency chains, compute reachability, and materialize transitive relations from supplied edge data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Advertised cycle-detection behavior is not implemented in the included helper, so cycle reports may be absent or misleading. <br>
Mitigation: Use it as a local transitive-closure helper; validate cycle-sensitive results independently and avoid relying on cycle detection until the behavior is implemented and tested. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fisa712/transitive-closure-generator) <br>
- [Publisher profile](https://clawhub.ai/user/fisa712) <br>
- [ClawHub homepage](https://clawhub.com) <br>
- [Transitive Closure Algorithms & Patterns](references/closure-patterns.md) <br>
- [Transitive Closure Examples](examples/closure-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and optional local script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The included helper can produce closure edges, reachability sets, path lists, and graph statistics from local edge data.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
