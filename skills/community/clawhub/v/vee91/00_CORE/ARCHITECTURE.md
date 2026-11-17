# V90 Architecture

VEE is a control plane over a heterogeneous intelligence fabric, not a single model.

Planes:
1. Control Plane: goals, policy, routing, budgets, approvals.
2. Model Plane: commercial APIs, open-weight models, local models, specialist models.
3. Agent Plane: A2A workers, specialist agents, swarms, critics, verifiers.
4. Tool Plane: MCP tools, APIs, browsers, files, code, deterministic utilities.
5. Knowledge Plane: evidence graph, memory, caches, provenance.
6. Evaluation Plane: benchmarks, red-team, regression, drift, independent judges.
7. Evolution Plane: genetic search, mutation, recombination, curriculum, skill factory.
8. Compute Plane: local CPU/GPU, optional cloud, queues, schedulers.
9. Safety Plane: sandbox, permissions, secrets isolation, rollback, audit.

No plane may depend on a single vendor by design.
