---
name: unione-email-templates
description: "Use when writing or fixing the HTML of an email for UniOne — welcome, password reset, OTP, receipts, notifications, newsletters — making it render in Gmail, Outlook and Apple Mail, adding substitutions and logic with the UniOne template engines (simple, Velocity, Liquid), storing it with template/set, or opening it in the UniOne visual editor for the user to edit."
license: MIT
metadata:
  author: "UniOne"
  version: "1.1.8"
  homepage: https://docs.unione.io/en/web-api-ref
  source: https://github.com/unione-repo/unione-skills
compatibility: "Requires UNIONE_API_KEY: the UniOne API key (the account key, or a project key for project data) from https://cp.unione.io/en/, server-side only."
---

# UniOne email templates

## Workflow

1. Ask what the email is for and what data it shows; pick the engine: flat merge tags → `simple`, objects / lists /
   conditions → `liquid` ([references/engines.md](references/engines.md)).
2. Write the HTML by the mail-client rules ([references/html-email.md](references/html-email.md)) and a plaintext
   version with the same content.
3. Store it with `template/set` (`editor_type: "html"`, `template_engine`, `subject`, `from_email`, `from_name`,
   `body.html`, `body.plaintext`); keep the returned `id` in config, not the HTML in code.
4. Show it to the user in the visual editor: `https://cp.unione.io/en/templates/edit-body-html/<template_id>` (the returned `id`). In a coding agent offer to
   open the link in the browser; the user must be signed in to the control panel of the same account. After the user
   edits it, read it back with `template/get`.
5. Test: send with `template_id` and real substitutions to the user's own (or sandbox-confirmed) address; check
   Gmail, Outlook and a phone. Then use `template_id` in the code.

## template/set

```json
{
  "template": {
    "name": "Password reset",
    "editor_type": "html",
    "template_engine": "liquid",
    "subject": "Reset your password",
    "from_email": "noreply@example.com",
    "from_name": "Example",
    "body": {"html": "<!DOCTYPE html>…{{ reset_url }}…", "plaintext": "Reset your password: {{ reset_url }}"}
  }
}
```

Send it: `email/send` with `template_id` and `recipients[].substitutions` (`{"reset_url": "https://…"}`); fields
passed in the call override the template's.

## Rules that matter most

- Tables and inline CSS, 600 px wide, no JavaScript / forms / external CSS; under ~100 KB (Gmail clips).
- Absolute `https://` image URLs with `alt`, `width`, `height`; essential text never only in images.
- Always a plaintext part; `lang`, headings, contrast ≥ 4.5:1, buttons as styled links.
- The syntax of the body must match `template_engine` (default `simple`): a Liquid body under `simple` goes out with
  raw `{%` tags; use `none` for literal braces.
- Do not remove the unsubscribe link of marketing emails; transactional ones may set `options.unsubscribe_url`.
- Substitution names: Latin letters, digits, `_`, starting with a letter; case-sensitive.

Related: the `unione` skill (sending, webhooks), `unione-email-best-practices` (content,
compliance).
