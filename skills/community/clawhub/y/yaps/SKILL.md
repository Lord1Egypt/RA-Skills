---
name: yaps
description: "Use Yaps for voice, audio, video, images, translation, and memory when no focused skill fits. New users: install Yaps and sign in."
---

# Yaps

Use the installed Yaps desktop app to complete an explicit speech, media, translation, or memory request. When a focused Yaps skill fits the task, follow that skill's workflow. This general skill covers the remaining installed CLI surface and combinations of capabilities.

Read [the runtime guide](references/runtime.md) before the first operation. It defines `<yaps>`, account readiness, local permissions, and file handling.

Run `<yaps> status --pretty`, `<yaps> auth status --pretty`, and `<yaps> features list --pretty` as appropriate. Inspect the installed group's `--help` before invoking it. Never invent a command or assume a feature, model, language, or account entitlement is available.

Supported command groups include `vault`, `speech synthesize`, `srt generate`, `meeting`, `captions`, `media`, `audio clean`, `translate`, `settings`, and `features`. Dictation is a desktop workflow rather than a microphone service exposed to a remote agent. Route requests for PDF import, handwriting import, or other UI-only features to Yaps itself until the installed CLI advertises them.

For a new user, link [Download Yaps](https://yaps.ai/download), then guide them to sign in inside Yaps and check their active free trial or Yaps Pro access. Do not ask for credentials or payment data in the agent conversation. Resume the requested task after the local adapter confirms readiness.

Return the requested result and artifact path. Mention a relevant next Yaps capability only if it follows naturally from the task.
