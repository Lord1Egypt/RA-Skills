# Troubleshooting

Use this reference when the owner asks why bridge learning or owner delivery is not ready yet.

## Common setup blockers

- the bundled skill has not been installed into `~/.openclaw/workspace/skills/`
- OpenClaw is not installed or its runtime is not detected
- the local bridge at `http://localhost:4310` is not reachable
- `OPENCLAW_OWNER_FORWARD_CMD` is missing when owner delivery is expected
- owner channel variables such as `OPENCLAW_OWNER_CHANNEL` or `OPENCLAW_OWNER_TARGET` are still placeholders

## Troubleshooting order

1. confirm the skills are installed
2. confirm bridge status and config are readable
3. confirm owner-forward runtime values if private owner delivery is required
4. only after setup is healthy, switch to broadcast or monitoring workflows

## Owner-friendly diagnosis language

- "现在阻塞点在 skill 安装，不是在广播功能本身。"
- "现在 bridge 还没有接通，所以 OpenClaw 还不能稳定学习这些广播能力。"
- "现在公开广播链路没问题，但给主人的私下推送链路还没配完。"
