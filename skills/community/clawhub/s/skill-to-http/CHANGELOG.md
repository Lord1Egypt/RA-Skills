# Changelog

## v1.0.2 (2026-07-28)

Documentation-only update (no code change):

- **README Security Notice** extended with an explicit note that the optional `llm` executor / param-extraction path sends `SKILL.md` to an external chat-completions endpoint. Clarifies it is **off by default** (only active when `llm.base_url` + `llm.api_key` are configured) and advises trusting the endpoint / keeping SKILL.md free of secrets. This matches the safety note already in SKILL.md and addresses review findings about undocumented data egress.

## v1.0.1 (2026-07-28)

Security hardening in response to clawhub SkillSpector review (no functional change):

- **Directory permissions**: `ensure_dirs()` created the HTTP root at `0o755` despite the docstring stating `0o700`. Tightened to `0o700` in both `tls_auth.py` and `gen_cert.py` (the latter re-set the parent to `0o755`), preventing directory traversal/metadata exposure on multi-user hosts. Service runs as a single user, so no functional impact.
- **Prominent Security Notice** added to the top of `SKILL.md` and `README.md`: explains that exposing installed Skills over HTTP widens the attack surface, that `expose_skills: ["*"]` / `--expose-skill "*"` opens every Skill, that default HTTP is cleartext, and that execution is immediate without confirmation — so operators deploy with informed consent.

## v1.0.0 (open-source first release)

- Persistent FastAPI server exposing installed agent Skills as REST API endpoints (one endpoint per Skill)
- Sync / async execution with webhook callbacks (HMAC-signed, SSRF-guarded)
- Multi-engine executor with graceful fallback: OpenClaw → Claude Code SDK → Claude CLI → Codex CLI → LLM API
- Bilingual (EN/ZH) web management console: skill on/off, test runs, job history, logs, metrics, doctor
- HTTP by default, optional HTTPS with self-signed SAN certificates (`upgrade-to-https` one-liner)
- API Key auth (constant-time compare), expose whitelist + deny blacklist, `--no-docs` hardening
- Init wizard (8 steps) + non-interactive mode for agent environments
- Doctor self-check with `--fix` (TLS expiry, SAN mismatch, config drift)
