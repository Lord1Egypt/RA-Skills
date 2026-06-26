# Buyer purchase persistence notes

This note covers the durable local purchase state required by the direct-buying skill.

Purchase records and cached artifacts can reveal what the agent bought, when it bought it, which seller it paid, and where proprietary downloads live. Treat this directory as private local state.

Suggested local layout:

```text
~/.local/share/spawnxchange/
	agents/
		<agent-name>/
			purchases.jsonl
			downloads/
				<order-id>.zip
```

A buyer should treat purchases as durable inventory.

Recommended append-only record fields:
- `purchased_at`
- `query`
- `item_id`
- `title`
- `seller_username`
- `chain`
- `currency`
- `amount_smallest_unit`
- `payment_scheme`
- `order_id`
- `local_cache_path`
- `artifact_sha256`
- `feedback_status`

Do not treat the signed download URL as durable state. It is a short-lived bearer credential; persist the cached artifact path and order ID instead.

Local handling rules:
- keep the state directory owner-only, for example `chmod 700 ~/.local/share/spawnxchange`
- keep ledger files owner-read/write only, for example `chmod 600 purchases.jsonl`
- do not commit purchase records, private keys, payment headers, signed download URLs, cached artifacts, or API keys
- do not copy purchase records or cached artifacts into shared logs, issue trackers, chat transcripts, or unencrypted backups
- delete cached artifacts and old purchase metadata when they are no longer needed for reuse, audit, or license compliance
- if you back up this directory, use an encrypted backup target

Operational rule:
- before buying, search your own purchase ledger first to see whether an equivalent artifact is already owned and cached.
- before executing a new purchase, compare the current quote against your budget, expected chain, expected currency, and any matching purchase record.

Official docs and policy links:
- Agent usage spec: https://spawnxchange.com/agent-usage
- Machine manifest: https://spawnxchange.com/api/v1/skills
- Terms: https://spawnxchange.com/terms
- License: https://spawnxchange.com/license