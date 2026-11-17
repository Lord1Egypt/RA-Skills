# Durable polling and recovery

Read this reference whenever an API returns a task ID or a previous command was interrupted. The mandatory terminal-state rule remains in `SKILL.md`.

## Invariants

- Persist the task before the first status request and after every response.
- Treat queued, pending, waiting, processing, running, and unknown nonterminal values as waiting—not success.
- Poll every 2 seconds initially for 3D/image tools and every 5 seconds for video/music; increase gradually and cap at 15 seconds.
- Print a heartbeat every 30 seconds without exposing secrets.
- By default, use no wall-clock timeout. `--max-wait` is an explicit user override.
- Stop only on terminal failure, terminal success with result URLs, or an explicit maximum wait.
- A success state without a downloadable result is an error, not completion.
- Download all result URLs and save their local paths back to the journal.

## Recovery

```bash
python3 scripts/showmeai.py tasks list
python3 scripts/showmeai.py tasks resume
python3 scripts/showmeai.py tasks resume --max-wait 1800
```

The journal directory is platform-neutral and can be overridden with `SHOWMEAI_STATE_DIR`. Interrupted records remain pending; successful and failed records remain as an audit trail.
