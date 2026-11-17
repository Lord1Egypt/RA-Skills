# Operating Protocol

For every mission:
1. Compile the user's objective into a machine-checkable task contract.
2. Identify success metrics and forbidden side effects.
3. Probe available models, agents, tools, memory, compute, and network.
4. Route each subtask to the least expensive capable worker; escalate only when evidence requires it.
5. Run independent candidates when uncertainty or quality gain justifies parallelism.
6. Verify outputs with deterministic tests or independent evaluators.
7. Attack the solution with adversarial cases.
8. Record evidence, failures, costs, latency, and provenance.
9. Generate improvement candidates.
10. Test candidates in isolation.
11. Promote only if the candidate beats the incumbent on the relevant Pareto frontier and passes safety/regression gates.
12. Save a checkpoint and update the capability lineage.
