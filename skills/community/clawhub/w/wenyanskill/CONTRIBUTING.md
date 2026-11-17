# Contributing to WenYan

Thank you for your interest in improving the WenYan classical Chinese style engine! 🏮

WenYan is a **general-purpose classical Chinese style engine** — it works with any LLM/agent (OpenClaw, Claude, ChatGPT, Gemini, Dify, Ollama, Cursor, …) through a pure system-prompt + Python engine design.

## Ways to Contribute

| Area | What you can add |
|------|-----------------|
| **New styles** | A new classical style as a JSON block in `assets/styles.json` (see `references/custom-styles.md`) |
| **Translations** | Localize `README.md` / `SPONSORS.md` into more languages |
| **Engine** | Improve `generate.py`, `validate.py`, `score.py` (Python, no external deps) |
| **Tests** | Add cases to `tests/test_styles.py` |
| **Docs** | Fix errors, improve the per-agent guide in `assets/agents.md` |
| **Bug reports** | Open an Issue with a minimal reproduction |

## Local Development

```bash
# 1. Clone
git clone https://github.com/Pondsi/wenyanskill.git
cd wenyanskill

# 2. Generate a prompt (any style / intensity)
python scripts/generate.py --style wangchao --intensity 3 --out prompt.md

# 3. Validate + score a candidate reply
python scripts/validate.py --style wangchao --text-file reply.txt
python scripts/score.py    --style wangchao --text-file reply.txt

# 4. Run the test suite
python -m pytest tests/ -q
```

The engine has **zero external Python dependencies** — it runs anywhere `python3` exists.

## Style Authoring Rules

- Style IDs must be **ASCII lowercase letters + digits** (e.g. `sanguo`, `zhanGuo` → `zhanguo`).
- Every style must define all five fields: `identity`, `language`, `forbidden_words`, `required_words`, `examples`.
- `examples` should cover at least: greeting, explanation, list, refusal.
- Keep `forbidden_words` free of modern/loan words and any style-specific anachronisms.

## Pull Request Checklist

- [ ] `python -m pytest tests/ -q` passes
- [ ] No local absolute paths or personal machine details in added files
- [ ] New style (if any) passes `validate.py` self-check
- [ ] README / agents.md updated if the change is user-facing
- [ ] Attribution preserved: `Made with ❤️ by Pondsi` + MIT license remain intact

## Code of Conduct

Be kind. This project exists because the author loves classical Chinese; contribute in that spirit. 🦞

## License

By contributing, you agree your contributions are licensed under the **MIT License** and may be used by `Pondsi` and downstream users.

---

WenYan — 古風語體引擎 · Made with ❤️ by [Pondsi](https://github.com/Pondsi)
