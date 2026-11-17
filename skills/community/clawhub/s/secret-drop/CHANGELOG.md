# Changelog

All notable changes to this project are documented here.

## Unreleased

## [0.2.0] - 2026-09-19

- Add `secret-drop share` command to create short-lived Password Pusher links from local `.env`, `~/.openclaw/.env`, or raw secret files without exposing plaintext.
- Rewrite `SKILL.md` into a concise decision matrix for AI agents covering inbound drops, chat masking recovery, and outbound sharing.
- Require Password Pusher retrieval-step handovers to preserve the API-returned
  `html_url` ending in `/r`; bare `/p/<token>` links can be consumed by messenger
  link previews even when `retrieval_step` was enabled at creation.
- Recheck destination files with `lstat` immediately before atomic replacement.
- Reject mixed public/private DNS answers and normalize IPv4-mapped IPv6 addresses.
- Redact provider tokens embedded in `/p/` and `/g/` URL paths.
- Support bare `python -m unittest discover` from the repository root.
- Add optional `--restart-gateway` using OpenClaw's safe restart command.

## 0.1.0 - 2026-09-18

- Add the public `secret-drop` OpenClaw skill.
- Add native Password Pusher retrieval for hosted and self-hosted instances.
- Add native SnapPwd AES-GCM decryption.
- Add atomic `openclaw-env`, `dotenv`, raw-file, and OpenClaw-store destinations.
- Add HTTPS-only fetches, redirect checks, private-address rejection, bounded responses, and secret-free errors.
- Add unit tests, CI, security documentation, and OpenClaw `extraDirs` installation guidance.
