## Description:

Write reliable Ruby avoiding mutable string traps, block pitfalls, and metaprogramming bugs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers use this skill for concise Ruby and Rails guidance on common language, collection, block, metaprogramming, and ActiveRecord pitfalls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect Ruby or Rails guidance could introduce application bugs or misleading fixes.

Mitigation: Review generated guidance and test resulting code before applying it to production systems.

Risk: Metaprogramming topics such as eval, const_get, and send can create security issues when used with untrusted input.

Mitigation: Prefer safer Ruby APIs such as public_send, avoid eval with user input, and validate constants or method names before use.

## Reference(s):

- [Ruby skill on ClawHub](https://clawhub.ai/ivangdavila/skills/ruby)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)
- [objects.md](artifact/objects.md)
- [blocks.md](artifact/blocks.md)
- [methods.md](artifact/methods.md)
- [collections.md](artifact/collections.md)
- [metaprogramming.md](artifact/metaprogramming.md)
- [rails.md](artifact/rails.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline Ruby, Rails, shell, and configuration examples when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Ruby executable when the agent needs to run or verify Ruby examples.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
