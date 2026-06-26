# Validation

## Must-pass checks

Run validation against at least two different agent maps, for example:

- a small map with 2 agents
- a larger map with 4+ agents

This catches hidden assumptions about fixed agent count or private naming.

### 1. Switching works

- send `切换到{agent}`
- expect direct confirmation
- send `当前是谁`
- expect the new agent

### 2. Session isolation works

- talk to agent A about one problem
- switch to agent B about another problem
- verify B does not inherit A's immediate working context
- switch back to A and verify A keeps its own thread

### 3. Timeout fallback works

- leave the conversation idle beyond the configured window
- send a normal message
- expect routing back to the default agent

### 4. Handoff works

- talk to agent A for several turns
- send `交给{agentB}`
- expect handoff confirmation
- next user message should be handled by agent B
- agent B should receive summary context, not blank context

### 5. Reset works

- talk to one agent
- reset only that agent
- verify summary/history for that agent is cleared or version-switched
- verify other agents are unaffected

## UX checks

- command matching should tolerate natural punctuation where appropriate
- silent handoff should not cause duplicate reply bursts
- summary view should not recurse into “summary of summary” nesting
- direct router replies should stay short and clear
