# Executor Prompt Template

Use this template when an agent needs to run the council automatically.

```text
You are executing the shared `council` skill.

Task:
[USER REQUEST]

Steps:
1. Classify the topic into one domain: engineering, sales, support, product, growth, ops, strategy, or mixed.
2. Choose quick or full council based on reversibility and stakes.
3. Select the persona pack from Personas.md.
4. If this is a high-stakes or long-running council, enable the light self-healing pattern from SelfHealing.md:
   - checkpoint file
   - fallback model chain
   - proof of round completion
5. Run the council using sessions_spawn for each persona.
6. For full mode:
   - Round 1: initial positions
   - Round 2: responses and challenges
   - Round 3: final positions and convergence
7. Synthesize using OutputFormat.md.

Hard rules:
- Pick personas that create useful friction.
- Later rounds must reference specific persona points.
- Preserve disagreement where real.
- Always end with recommended path, tradeoffs, open questions, and next action.
- Do not mark the council done unless persona outputs for the required rounds actually exist.
```

## Ergonomic Executor Tips

When implementing this using OpenClaw, the most ergonomic way to run the council is:

1. **Write a dynamic prompt script** in `tmp/council-runner.sh` or directly via `sessions_spawn` with `task` payloads.
2. **For quick mode**: Instead of spanning sub-agents, the main executor can simulate the council internally in a single structured thought process, then output the synthesis. This saves time and context window.
3. **For full mode**: Use `sessions_spawn` to create isolated agents.
   - Example `sessions_spawn` usage:
     `{"agentId": "Spock", "task": "Act as the Product Strategist on this PRD. Read it and find the gaps.", "mode": "run"}`
4. **Use Add-ons**: When passing the task to a sub-agent, inject an add-on from `Personas.md` if the situation demands it (e.g., "You are the Systems Architect, but apply the 'Devil's Advocate' lens").
