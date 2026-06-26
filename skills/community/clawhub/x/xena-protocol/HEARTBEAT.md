# OpenClaw Phishing Detection — Heartbeat

Runs every N seconds via OpenClaw's heartbeat scheduler. Keep short and
deterministic — long reasoning belongs in the `phishing-detection` skill,
not here.

## Every Cycle

- [ ] Run `python -m bin.setup check-config`.
      If `setup_required: true`, stop the cycle and activate the
      `phishing-detection` skill's interactive setup flow in the next user
      interaction (setup is user-mediated, not autonomous).

- [ ] Run `python -m bin.pipeline --poll`. This lists unread Gmail messages
      via `gog gmail messages search "in:inbox is:unread"`, fetches each
      via `gog gmail get --format raw`, runs stages 1+2 of the detection
      pipeline, and emits one JSON record per message.

- [ ] For each record where `needs_llm: true`: run the LLM classification
      from the `phishing-detection` skill, combine scores via
      `pipeline.combine_final`, and take the alert/report action per the
      skill's "Alert & Report Decisions" section.

- [ ] For each record where the final verdict is `spoof` or confidence
      `>= 70`: alert the user; in Reporter mode, offer on-chain submission.

- [ ] After each message is handled, call `gog gmail messages modify <id>
      --remove-label UNREAD` so repeat cycles don't re-process it. (This
      happens automatically inside `pipeline --poll`.)

- [ ] **Reporter mode only**: check the agent wallet balance via
      `python -c "from bin.registry_client import RegistryClient; ..."`
      (or the `bin.setup wait-balance` helper with a short timeout). If
      below `0.0001 ETH`, alert the user to top up and pause reporting.

- [ ] Retry any on-chain submissions that failed in previous cycles
      (they're queued in the local SQLite `scan_events` table with
      status `reported_pending`).
