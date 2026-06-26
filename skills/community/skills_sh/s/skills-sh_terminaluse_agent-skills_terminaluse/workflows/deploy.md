# Deploying an Agent

**Trigger**: User wants to deploy, push, go live, ship.

**Full docs**: https://docs.terminaluse.com/introduction/deploying.md

## Steps

1. `tu ls` to see if they have been past deployments of the agent

2. If yes:
   1. Check agent code (src/agent.py) for required env vars
   2. List env vars to confirm required vars set
   3. If some missing, ask users to put values in .env file and then import it
   4. `tu deploy`
3. If no:
   1. `tu deploy` will deploy agent and create prod and preview environments
   2. If succeeds, check and set env vars as above

4. If **fails**:
   - `tu ls <branch>` — find FAILED event
   - Analyze error, suggest fix
   - `tu deploy` again
