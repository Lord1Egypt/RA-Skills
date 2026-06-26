# Security Policy

## Private Key Safety

wallet-mcp stores private keys in **plaintext** in `~/.wallet-mcp/wallets.csv`.

**You are responsible for securing this file.**

```bash
# Restrict access immediately after setup
chmod 700 ~/.wallet-mcp
chmod 600 ~/.wallet-mcp/wallets.csv
```

Additional recommendations:
- Use **disk encryption** (LUKS on Linux, FileVault on macOS, BitLocker on Windows)
- Never commit `wallets.csv` or `.env` to git — `.gitignore` covers this, but double-check
- Never expose `wallets.csv` over any network share or API
- Use **dedicated wallets** for automation — never import your main wallet

---

## Docker Security

The Docker image runs as non-root user `mcpuser`. The wallet data volume is mounted at `/data` inside the container.

```bash
# Ensure the host volume is restricted
chmod 700 /path/to/wallet-data-volume
```

Never publish the container port (8000) publicly without a reverse proxy + authentication (nginx + basic auth or mTLS).

---

## Reporting a Vulnerability

If you discover a security vulnerability, **do not open a public GitHub issue**.

Instead, open a [GitHub Security Advisory](https://github.com/genoshide/wallet-mcp/security/advisories/new) (private disclosure).

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

You will receive a response within **72 hours**.

---

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x (latest) | Yes |
| < 1.0 | No |
