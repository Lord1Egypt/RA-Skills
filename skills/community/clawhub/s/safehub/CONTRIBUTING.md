# Contributing to SafeHub

Thank you for contributing. The most impactful way to help is **adding or improving Semgrep rules** that detect malicious or risky patterns in OpenClaw skills.

---

## Adding New Semgrep Rules

Rules live in the **`/rules`** directory. Each file is a YAML file that Semgrep runs against skill source code.

### Rule file structure

Create or edit a `.yml` file under `rules/`. Each rule must include:

- **`id`** — Unique identifier (e.g. `safehub-network-fetch`)
- **`message`** — Short explanation of what was found and why it matters
- **`severity`** — One of `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`
- **`languages`** — e.g. `["js"]`, `["ts"]`, `["python"]`
- **Pattern** — One of `pattern`, `patterns`, `pattern-either`, or `pattern-regex`

Example:

```yaml
rules:
  - id: safehub-example-eval
    message: "eval() can execute arbitrary code and is often used in malware"
    severity: CRITICAL
    languages:
      - js
    pattern: eval(...)
```

### Testing your rules locally

1. Install Semgrep (see [semgrep.dev](https://semgrep.dev)):
   ```bash
   npm install -g semgrep
   # or: brew install semgrep
   ```

2. Run Semgrep against a test skill directory:
   ```bash
   semgrep scan --config ./rules --config auto --json rules/
   ```

3. Try your rule on a real skill:
   ```bash
   semgrep scan --config ./rules /path/to/some-skill
   ```

4. Add a small test file in the skill repo that triggers your rule and run the scan again to confirm it fires.

### Pull request process

1. Fork the repo and create a branch (e.g. `rules/add-obfuscation-patterns`).
2. Add or edit rules in `rules/*.yml`. Keep one logical category per file (e.g. network, filesystem, execution).
3. Document in the rule `message` what the pattern detects and why it’s a risk.
4. Run `semgrep scan --config ./rules` from the SafeHub repo to ensure no syntax errors.
5. Open a PR with a short description of the new/updated rules and, if possible, an example of code they match.
6. Maintainers will review and may ask for severity or message tweaks.

---

## Code style

- Use async/await; avoid callbacks.
- Add a comment above each function describing what it does.
- Keep files under ~150 lines; split into smaller modules if needed.
- Do not hardcode credentials or environment-specific paths.

---

## Security

- Do not log or store the contents of scanned skills.
- Sandbox execution must stay isolated (no network, read-only FS except `/tmp`).
- Containers must be removed after each scan.

Thank you for helping make OpenClaw skills safer.
