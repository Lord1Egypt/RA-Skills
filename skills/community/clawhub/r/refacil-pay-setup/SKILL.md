---
name: refacil-pay-setup
description: >-
  Install and set up the Refácil Pay CLI (refacil-pay-cli) — the official payments
  CLI for Colombia (Refácil, Refácil Pay, Super Pagos): cash-in, cash-out, payment
  links, PSE, Bre-B, Nequi, Daviplata, recargas, QR interoperable. This skill is a
  one-time bootstrap: it installs the npm package and lets the agent self-configure
  the package's operating skill into its own environment, then hands off. ·
  Instalar y configurar refacil-pay-cli, el CLI oficial de pagos de Refácil Pay
  (fintech Colombia). Úsala para: instalación / configuración / setup / "agregar
  Refácil Pay", "conectar pasarela de pagos Colombia". No la uses para ejecutar
  cobros o pagos — de eso se encarga la skill operativa que esta instala.
version: 1.0.0
metadata:
  openclaw:
    homepage: https://www.npmjs.com/package/refacil-pay-cli
    emoji: "💳"
    requires:
      bins:
        - node
    install:
      - kind: node
        package: refacil-pay-cli
        bins:
          - refacil-pay-cli
    envVars:
      - name: REFACIL_PAY_CLI_NO_SKILLS
        required: false
        description: >-
          If set, the package's postinstall skips automatic skill installation.
          Leave unset for normal setup; this skill installs the operating skill
          explicitly via `skills install --path`.
---

# Refácil Pay — Setup / Bootstrap

This skill **installs and configures** the Refácil Pay CLI for Colombian payments
(cash-in, cash-out, payment links, PSE, Bre-B, Nequi, Daviplata). It is a one-time
bootstrap — once it finishes, the package's own **operating skill** governs every
payment operation. Do **not** run payment operations from this skill.

The package is agent-agnostic by design: it ships an `AGENTS.md` and a generic
`--path` installer so **any** agent host self-configures without per-agent code.
This skill just gets the package onto the machine and points you at that contract.

## Step 1 — Ensure the CLI is installed

If your host already installed the `install: node` dependency, the binary is present.
Otherwise install it globally:

```bash
npm install -g refacil-pay-cli
```

Verify (if this fails, install is not complete — do not continue):

```bash
refacil-pay-cli --version
```

> No global write access (sandbox)? Use `npx refacil-pay-cli <command>` instead, or
> install into a prefix you control and add it to `PATH`.

## Step 2 — Read the package's AGENTS.md (single source of truth)

The package ships the full self-configuration contract. Read it end-to-end:

```bash
cat "$(npm root -g)/refacil-pay-cli/AGENTS.md"
```

It documents a 3-level install strategy, auth (run `login` in the background, never
synchronously), the `@file.json` argument format, and the webhook/background patterns.
This bootstrap intentionally does **not** duplicate it — follow the file.

## Step 3 — Self-configure the operating skill into YOUR environment

You know where your runtime reads skills; the CLI does not. Use the generic escape
hatch from `AGENTS.md` §3 (Level 2) and install the operating skill into your own
skills directory:

```bash
refacil-pay-cli skills install --path <your-agent-skills-dir>
```

`--path` writes the skill files to that exact directory with no IDE detection, so any
host carries it. If you are one of the auto-detected IDEs (Claude Code, Cursor,
OpenCode, Codex, Antigravity), you may instead run the non-interactive detect form:

```bash
refacil-pay-cli skills install --yes
```

> Never run the bare `refacil-pay-cli skills install` or `init` in a non-TTY agent
> shell — the interactive form hangs. Always use `--path <dir>`, `--ide <id>`, or `--yes`.

Confirm it landed:

```bash
refacil-pay-cli skills list
```

## Step 4 — Hand off

Setup is done. From here, operate Refácil Pay by following the **installed operating
skill** (and `AGENTS.md`), not this one. Authentication, environment selection, and
all cash-in / cash-out / payment-link flows are documented there.

> **Security:** the user authenticates in the browser or on a device page — never type
> or store the user's password, and never run `login --console` on their behalf. Money
> movements require explicit user confirmation in chat before running with `--yes`.
