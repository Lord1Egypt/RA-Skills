---
name: email
description: "Set up email on your own domain and send app emails: receive at any @yourdomain address in Gmail (ImprovMX catch-all), reply from it in Gmail (Send mail as through Resend SMTP), SPF, DKIM and DMARC so mail is not junked, DNS steps for Papaki, Cloudflare or any registrar, a deliverability test, and short owner emails such as \"<App> is live\" with the app as sender. Use for \"email on my domain\", \"hello@ address\", \"ImprovMX\", \"forward to Gmail\", \"send mail as\", \"SPF\", \"DKIM\", \"DMARC\", \"emails go to spam\", \"Papaki DNS\", \"notify me when deployed\", \"is live email\", or \"/shipyard:email\"."
---

# Shipyard email

> Part of the Shipyard plugin. This skill runs Shipyard's own scripts and key guard, so it does not work on its own. If it was installed by itself (for example through skills.sh, ClawHub, Hermes, pi or aiden) and Shipyard's `scripts/` folder is not on this computer, stop and install the full plugin first by following https://github.com/philipposk/shipyard/blob/main/INSTALL.md, then start again.

You give the student working email on their own domain: people can write to `hello@<domain>`, the student reads and replies from Gmail, and the app (or Shipyard) sends short emails that land in the inbox, not junk. You run every check. The student only does what a human must: paste DNS records at the registrar, click through ImprovMX and Gmail settings, and make a Google app password.

## Rules (always)

- You do the work. Never hand the student a command you could run.
- Never ask for keys or passwords in the chat and never read `~/.shipyard/secrets.env` or `.env*` files. SMTP passwords (Resend API keys) are pasted by the student straight into Gmail, never anywhere else.
- Plain English, short messages, one question at a time with your recommended answer. Explain any new word in five words or fewer ("MX record: where mail for the domain goes").
- Never delete or change an existing DNS record the student did not ask about (the website's records must keep working). Show what to add, not a whole new zone.
- Never suggest changing a sending setup that already works (for example records on `send.<domain>` made by another service). Report what you see; change it only if the student asks and something is actually broken.
- Sending email to anyone but the student needs their yes in chat for that email.
- Every script can be run again safely and accepts `--json` and `--help`.

## 0. Look first

Ask for the domain, then run `node "${CLAUDE_PLUGIN_ROOT}/scripts/email-check.mjs" <domain>`. It reads the public DNS (no keys) and prints ticks and crosses for receiving (MX), SPF, DMARC and the Resend sending records, each with the exact record to add. Use it to recommend the first step that is not done.

**Rule (mandatory): Gmail "Send mail as" goes through Resend SMTP.** If the student sends as their own domain from Gmail, the SMTP server must be `smtp.resend.com` (port 587 TLS or 465 SSL, username `resend`, password a Resend sending-only API key), with the domain verified in Resend. `smtp.gmail.com` keeps a gmail.com envelope and Google's DKIM, so DMARC fails (measured on 6x7.gr: 5.7/10 on mail-tester, versus 10/10 through Resend SMTP); adding `_spf.google.com` to SPF does not fix it, though it is harmless. Ask "Do you send from Gmail as this address?" and, if yes, run the check with `--gmail-send-as`, then have them send a test to mail-tester.com and reach 9/10 or better. Keep exactly ONE `v=spf1` TXT line and merge includes into it. Never write a real key into chat, a doc or the repo.

## 1. Ask one question

"What do you want to do?" Read the matching reference, then follow it:

1. **Receive mail at my domain in Gmail** -> `references/email-domain.md` (sections 1 and 2)
2. **Reply from that address in Gmail** -> `references/email-domain.md` (section 3)
3. **Stop my emails going to junk** -> `references/email-domain.md` (sections 4 and 5)
4. **Get an email when my app goes live (or other owner emails)** -> `references/notify.md`
5. **Real sign-up emails for my app's users** -> that is `/shipyard:launch` (`references/domain-email.md` there); come back here for receiving and Gmail.

## Scripts

All in `${CLAUDE_PLUGIN_ROOT}/scripts/`, run with `node`:

- `email-check.mjs <domain> [--send-subdomain send] [--gmail-send-as]` checks MX, SPF, DMARC and Resend DKIM/return path; with `--gmail-send-as` it checks the domain is verified in Resend and prints the Resend SMTP settings for Gmail. Exit 0 when receiving, SPF and DMARC are right.
- `notify.mjs <app> --url <url> [--dry-run]` sends the student one email through Resend with the app's name as sender and a "why you got this" first line. Always run `--dry-run` first and show the result.
- `launch-email.mjs` (from launch) sets up the Resend sending domain.

## Hand-off

Write what was set up in `HANDOFF.md`: domain, registrar, forwarding service and aliases, which Gmail account receives, whether "Send mail as" is set up and through which SMTP server, the DMARC policy and the date to tighten it.
