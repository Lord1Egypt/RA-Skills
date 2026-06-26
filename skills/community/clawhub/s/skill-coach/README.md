

## Skill Coach (OpenClaw)

This skill is a **coaching assistant** that helps you package your expertise into an **OpenClaw Skill**.
It guides you step-by-step so the resulting Skill is structured, concise, and reusable.

### Author

- `mars2003` (GitHub)

### What it does

- Helps you identify a good, repeatable scenario to build as a Skill
- Chooses an adaptive workflow depth: **3 / 4 / 5 steps**
- Enforces a **step-by-step confirmation** mechanism at key stages
- Produces a high-quality `SKILL.md` (and optionally supporting files) for the final Skill

### Triggers

Invoke the Skill by saying one of the following phrases:

- 「创建skill」
- 「封装skill」
- 「skill教练」
- 「帮我写skill」
- `create skill`
- `build skill`

### Quick start

Try one of these prompts in OpenClaw:

```text
create skill for unit conversion (kg to lb)
```

```text
build a skill that generates a weekly sales report from a CSV file
```

```text
create skill for a compliance audit workflow (with approval and boundary cases)
```

After you answer, the coach infers complexity and walks you through drafting the resulting Skill.

### What the final generated Skill should include

At minimum:

- `SKILL.md` with correct frontmatter (`name`, `description`, `version`)
- Clear sections: applicable scenarios, core abilities, inputs, key rules, and boundary validation
- Processing steps and output format
- 2-3 examples (normal + boundary + error/exception cases)

### License

MIT-0 (MIT No Attribution).
