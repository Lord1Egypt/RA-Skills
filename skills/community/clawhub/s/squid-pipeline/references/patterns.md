# Workflow Patterns

## Plan -> Gate -> Execute

Always gate before side effects.

```yaml
steps:
  - id: plan
    type: spawn
    spawn: { task: "Plan: ${args.task}", thinking: high, timeout: 300 }
  - id: review
    type: gate
    gate: { prompt: "Review plan. Approve?", preview: $plan.json }
  - id: execute
    type: spawn
    spawn: { task: "Execute: ${plan.json}", timeout: 300 }
    when: $review.approved
```

## Parallel Agents -> Review

Fan out to specialists, aggregate results.

```yaml
steps:
  - id: work
    type: parallel
    parallel:
      maxConcurrent: 3
      merge: object
      branches:
        research: [{ id: r, type: spawn, spawn: "Research: ${args.topic}" }]
        code: [{ id: c, type: spawn, spawn: "Implement: ${args.topic}" }]
        test: [{ id: t, type: spawn, spawn: "Test: ${args.topic}" }]
  - id: review
    type: spawn
    spawn:
      task: "Review: research=${r.json}, code=${c.json}, tests=${t.json}"
      thinking: high
```

## Iterative Refinement (restart)

Loop until quality threshold. Agent gets feedback from previous iteration.

```yaml
steps:
  - id: write
    type: spawn
    spawn:
      task: "Implement: ${args.task}\nFeedback: ${review.json.feedback}"
      timeout: 300
  - id: review
    type: spawn
    spawn: { task: "Score 0-100: ${write.json.code}", thinking: high, timeout: 180 }
  - id: decide
    type: transform
    transform: "$review.json.score"
    restart:
      step: write
      when: $review.json.score < 80
      maxRestarts: 3
```

Flow: write -> review -> score=60 -> restart -> write(+feedback) -> review -> score=85 -> continue.

## Sub-Pipeline Orchestration

Break large workflows into reusable YAML files.

```
pipelines/
  release.yaml          <- orchestrator
  stages/
    build.yaml          <- standalone sub-pipeline
    test.yaml
    deploy.yaml
```

```yaml
# release.yaml
steps:
  - id: build
    type: pipeline
    pipeline: { file: ./stages/build.yaml, args: { target: $args.env } }
  - id: test
    type: pipeline
    pipeline: { file: ./stages/test.yaml }
    when: "!$args.skip_tests"
  - id: deploy
    type: pipeline
    pipeline:
      file: ./stages/deploy.yaml
      args: { artifact: $build.json.artifact, env: $args.env }
```

Each stage standalone: `squid run stages/build.yaml --args-json '{"target":"prod"}'`. Gates propagate up.

## Batch Processing (Loop + Parallel)

```yaml
steps:
  - id: discover
    type: run
    run: find /data -name "*.json" | jq -Rs 'split("\n")[:-1]'
  - id: process
    type: loop
    loop:
      over: $discover.json
      maxConcurrent: 8
      maxIterations: 500
      collect: results
      steps:
        - id: analyze
          type: spawn
          spawn: { task: "Analyze: ${item}", timeout: 60 }
```

## Error Handling + Rollback

```yaml
steps:
  - id: deploy
    type: run
    run: kubectl apply -f deploy.yaml
    retry: { maxAttempts: 3, backoff: exponential }
  - id: handle
    type: branch
    branch:
      conditions:
        - when: $deploy.status == "failed"
          steps:
            - id: rollback
              type: run
              run: kubectl rollout undo deployment/app
            - id: alert
              type: spawn
              spawn: "Diagnose deployment failure"
      default:
        - id: verify
          type: run
          run: kubectl rollout status deployment/app
```

## Retry with Escalation

```yaml
steps:
  - id: deploy
    type: run
    run: kubectl apply -f deploy.yaml
    retry: { maxAttempts: 3, backoff: exponential, retryOn: ["timeout"] }
  - id: check
    type: branch
    branch:
      conditions:
        - when: $deploy.status == "failed"
          steps:
            - id: rollback
              type: run
              run: kubectl rollout undo deployment/app
            - id: diagnose
              type: spawn
              spawn: "Deployment failed after 3 retries. Diagnose."
            - id: escalate
              type: gate
              gate: "Deploy failed and rolled back. Review diagnosis."
```

## Environment-Specific Routing

```yaml
- id: deploy
  type: branch
  branch:
    conditions:
      - when: $args.env == "prod"
        steps:
          - id: gate
            type: gate
            gate: { prompt: "Deploy to PRODUCTION?", requiredApprovers: ["lead"] }
          - id: prod
            type: run
            run: kubectl apply -f k8s/prod/
            when: $gate.approved
      - when: $args.env == "staging"
        steps:
          - id: staging
            type: run
            run: kubectl apply -f k8s/staging/
    default:
      - id: dev
        type: run
        run: docker compose up -d
```

## Anti-Patterns

1. **No spawn output format** — always tell the agent what JSON shape to return
2. **No timeout** on spawn/run — agents can hang forever
3. **No gate before side effects** — gate destructive operations
4. **Deep nesting** — use `type: pipeline` sub-pipelines instead
5. **No maxIterations on loops** — prevent runaway execution
6. **autoApprove in production** — only for dev/CI, use `--test` flag
7. **Loops without maxIterations** — always set a safety limit
