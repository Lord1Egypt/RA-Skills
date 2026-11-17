# veida-image — a Claude Agent Skill for generating images with no API key

Drop `SKILL.md` into `.claude/skills/veida-image/` and your agent can make images without a
single credential. It calls the free anonymous tier of
[Veida](https://veida.ai/?utm_source=lobehub&utm_medium=skill), an [AI image generator](https://veida.ai/image?utm_source=lobehub&utm_medium=skill) that meters
its free allowance per client id instead of per account.

```bash
mkdir -p .claude/skills/veida-image
curl -o .claude/skills/veida-image/SKILL.md \
  https://raw.githubusercontent.com/hanshs474/veida-image-skill/main/SKILL.md
```

**What it gives an agent**: one image per generated client id, 1K and watermarked, roughly
7 a day from one machine. Enough for covers, mockups and placeholders during development.

**What it does not**: editing an existing image, which costs more than the anonymous grant
can pay — that needs an account, and the
[image editor](https://veida.ai/image/nano-banana-2-lite?utm_source=lobehub&utm_medium=skill) is where it lives.

Every number in `SKILL.md` was read out of the running service, not estimated. See the
[pricing page](https://veida.ai/pricing?utm_source=lobehub&utm_medium=skill) for what changes when you sign in.

MIT.
