## Description: <br>
Write reliable Ruby avoiding mutable string traps, block pitfalls, and metaprogramming bugs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill as a Ruby and Rails reference for avoiding common language, collection, block, method visibility, metaprogramming, and ActiveRecord pitfalls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ruby and Rails reference guidance can become inaccurate across language or framework versions. <br>
Mitigation: Verify recommendations against the Ruby and Rails versions used in the target project before applying them. <br>
Risk: Metaprogramming patterns such as eval, const_get, send, and method_missing can introduce security or maintainability issues when used without care. <br>
Mitigation: Prefer safer alternatives such as public_send, avoid evaluating user input, and pair method_missing with respond_to_missing?. <br>


## Reference(s): <br>
- [Ruby skill page](https://clawhub.ai/ivangdavila/ruby) <br>
- [Publisher profile: ivangdavila](https://clawhub.ai/user/ivangdavila) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Object Traps](artifact/objects.md) <br>
- [Block/Proc/Lambda Traps](artifact/blocks.md) <br>
- [Collection Traps](artifact/collections.md) <br>
- [Method Traps](artifact/methods.md) <br>
- [Metaprogramming Traps](artifact/metaprogramming.md) <br>
- [Rails/ActiveRecord Traps](artifact/rails.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code] <br>
**Output Format:** [Markdown guidance with inline Ruby and Rails code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires users to verify Ruby and Rails guidance against the versions used in their project.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
