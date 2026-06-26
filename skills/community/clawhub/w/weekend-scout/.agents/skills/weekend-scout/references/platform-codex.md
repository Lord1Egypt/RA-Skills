# Codex Platform Rules

This reference contains Codex-only behavior that is still genuinely platform-specific.
Shared JSON transport rules live in `references/platform-transport.md`.

<approval-retry-rule>
- Only request Codex approval / outside-sandbox execution when a stage reference explicitly authorizes it.
- For Telegram resend fallback, rerun the exact same `python -m weekend_scout send ...` command once with approval-gated outside-sandbox execution.
- Do not change arguments, do not rerun `format-message`, and do not broaden this to any other command or failure class.
- If approval is denied, or the retried command still returns `{"sent": false, ...}`, stop retrying and treat that result as final.
</approval-retry-rule>
