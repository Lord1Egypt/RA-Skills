# Workflows (OpenClaw / shell / REST)

Working rules for agents using shell, REST, or browser—consistent and traceable.

## Always first: fresh data

- **Stale-data protection:** Before any write, fetch current state (e.g. `wp post get <id>`, REST `GET` on the resource, or re-read the file).
- **Single source of truth:** Answers about IDs, titles, status only from **latest command output / API JSON**—do not fill in from chat memory.

## Read → Plan → Write → Verify

1. **Read:** Load existing posts/plugins/options/files.
2. **Plan:** For multi-step or risky changes, state the plan briefly; for simple reads, execute directly.
3. **Write:** Apply the change (WP-CLI, `curl` PATCH/POST, or controlled browser step).
4. **Verify (read-after-write):**  
   - After file edits: re-read the file or `wp plugin verify` / syntax check if available.  
   - After REST writes: `GET` the same resource.  
   - Check the site’s PHP error log if you have access.  
   - Only then report “done”.

## Complexity

- Simple (1–2 steps): execute directly.
- Complex (many files/systems): show the plan; checkpoint every 2–3 steps.
- Do **not** add features that were not requested.

## Debugging (minimal)

1. Read error log / `wp option` / relevant file.  
2. Name the cause.  
3. Apply the **smallest** fix—do not rewrite everything without reason.

## Posts vs pages

Always distinguish based on the **current user request**—never confuse them.
