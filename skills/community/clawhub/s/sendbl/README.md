# sendbl OpenClaw skill

OpenClaw skill for [Sendbl](https://sendbl.com), a file-exchange API for LLM agents. Lets your OpenClaw assistant create file-request links, send files, check link status, list uploaded files, and delete links.

## Install

```sh
mkdir -p ~/.openclaw/workspace/skills
cp -R openclaw/sendbl ~/.openclaw/workspace/skills/sendbl
```

Then re-run onboarding (or the equivalent skill-refresh command) so OpenClaw picks up the new skill:

```sh
openclaw onboard
```

## Configure

1. Sign in at <https://sendbl.com/account> with Google.
2. Open <https://sendbl.com/account/tokens> and create a **personal access token** (no expiry, designed for CLI/skill use).
3. Add to your shell profile:

   ```sh
   export SENDBL_API_KEY="sk_pat_..."
   ```

If the token is leaked or no longer needed, revoke it from the same page.

## Usage

Once installed and configured, ask your assistant things like:

- "Create a link so my accountant can send me Q1 receipts."
- "Send `report.pdf` to john@example.com."
- "Is `link_a1b2c3d4e5f6a7b8` still active?"
- "Delete the upload link I just made."

## Limits

- 20 links/month per API key on the free tier.
- Links expire after 72 hours by default (configurable up to the tier limit).
- File size cap depends on your tier — see <https://sendbl.com/pricing>.

## Source

<https://github.com/antonefremov/sendbl-openclaw> (this skill).
