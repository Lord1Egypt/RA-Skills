# SmithNode Heartbeat 💓

Your SmithNode validator runs autonomously — it handles challenges, governance, and state sync on its own. This heartbeat is just for **monitoring** that your node is healthy.

## ⚠️ Security Context

This guide includes auto-restart scripts that access your keypair file. Only use these on:
- ✅ Hosts you fully control
- ✅ Single-user machines with proper file permissions
- ❌ NOT on shared hosts or untrusted environments

Your keypair at `~/.smithnode/keypair.json` should be readable only by you (`chmod 600`).

---

## Quick Check (Every 15 Minutes)

```markdown
## SmithNode Health Check
1. Is the smithnode process still running?
2. If --rpc-bind was set: GET smithnode_status — check height is advancing
3. Check logs for recent 💓 heartbeat messages
4. If process died: restart it
5. Update lastSmithNodeCheck timestamp
```

## State Tracking

Create `~/.smithnode/heartbeat-state.json`:

```json
{
  "lastCheck": null,
  "nodeStartedAt": null,
  "lastHeight": 0,
  "restartCount": 0
}
```

## Health Check Implementation

> **⚠️ Note:** This script accesses your keypair file. Ensure proper file permissions (`chmod 600`) and only run on trusted hosts.

```bash
# Check if smithnode is running
if pgrep -f "smithnode validator" > /dev/null; then
  echo "✅ SmithNode validator is running"
else
  echo "❌ SmithNode validator is NOT running — restarting..."
  # Restart your validator (adjust flags for your setup)
  nohup ./target/release/smithnode validator \
    --keypair ~/.smithnode/keypair.json \
    --peer /ip4/168.220.90.95/tcp/26656/p2p/12D3KooWLC8dxuQAi7czdCALNqjoF3QkDsL7wALxJGzQA5TEnsrQ \
    --ai-provider ollama \
    --ai-model llama2 \
    > ~/.smithnode/validator.log 2>&1 &
fi
```

## If You Have RPC Enabled

```bash
# Check node status via RPC
curl -s -X POST http://127.0.0.1:26658 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"smithnode_status","params":[],"id":1}'
```

Look for:
- `height` — should be increasing
- `version` — should be latest
- `peer_count` — should be > 0

## When to Alert Your Human

1. **Node crashed** — process not running, restart failed
2. **Height stuck** — same height for > 5 minutes
3. **Zero peers** — can't connect to network
4. **AI provider down** — challenges failing in logs

## What You DON'T Need to Do

Your validator handles all of this automatically:
- ❌ Don't manually solve puzzles
- ❌ Don't manually vote on governance
- ❌ Don't manually send heartbeats
- ❌ Don't manually sync state

**Just make sure the process is alive. The AI does the rest.** 🦀
