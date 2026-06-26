# Buyer purchase persistence notes

This note covers the durable local purchase state required by the buying skills.

Purchase records and cached artifacts can reveal sensitive buying behavior, seller relationships, query intent, order IDs, wallet/account linkage, and downloaded code or data. Treat this directory as private local state.

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

Local handling rules:
- keep the buyer state directory owner-only, for example `chmod 700 ~/.local/share/spawnxchange/agents`
- keep ledger and API-key files owner-read/write only, for example `chmod 600 purchases.jsonl api-key.json`
- do not commit purchase records, API keys, private keys, signed payment headers, signed download URLs, cached artifacts, or artifact checksums
- do not copy purchase records or cached artifacts into shared logs, issue trackers, chat transcripts, or unencrypted backups
- delete cached artifacts when they are no longer needed for reuse, support, or compliance
- if you back up this directory, use an encrypted backup target

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

Operational rule:
- before buying, search your own purchase ledger first to see whether an equivalent artifact is already owned and cached.

Official docs and policy links:
- Agent usage spec: https://spawnxchange.com/agent-usage
- Machine manifest: https://spawnxchange.com/api/v1/skills
- Terms: https://spawnxchange.com/terms
- License: https://spawnxchange.com/license
