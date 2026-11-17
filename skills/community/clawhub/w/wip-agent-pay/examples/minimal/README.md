# examples/minimal/

Minimal example of using wip-agent-pay in your agent.

Just say to any agent:

> Authorize 0.10 USDC for morning-stew MS-#8

The agent will automatically call:

```bash
wip-agent-pay 0.10 morning-stew "MS-#8"
```

You run it ... approve on Coinbase ... paste the returned URL back to the agent.

See REFERENCE.md for full setup.
