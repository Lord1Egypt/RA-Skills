# Codex skill mechanics

A skill contains SKILL.md with a name and a concise description. Scripts,
references and assets are optional: add them when the workflow needs them.

Codex supports explicit skill selection and implicit matching by description.
For an explicit-only skill, use the native policy in agents/openai.yaml:

```yaml
policy:
  allow_implicit_invocation: false
```

The default is true. Do not assume another client's frontmatter flag controls
Codex, that explicit-only means zero prompt cost, or that a pointer cannot be
read merely because implicit invocation is disabled. Verify the target client's
semantics when packaging for multiple harnesses.

A router should select relevant guidance, not load every target in its catalog.
Use separate skills when independent invocation is useful; ordinary conditional
reference can remain a supporting document.

The operator's selected model and native permissions remain authoritative.
This authoring reference does not install skills, change configuration or grant
permission to publish. Invocation syntax and placement are client-specific.

Source checked 2026-09-12:
[OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills).
