#!/usr/bin/env node
/**
 * @zouroboros/swarm-gate CLI
 *
 * Usage:
 *   npx @zouroboros/swarm-gate "build a REST API with auth and tests"
 *   npx @zouroboros/swarm-gate --json "fix the typo on line 42"
 *
 * Exit codes:
 *   0  SWARM or FORCE_SWARM
 *   2  DIRECT
 *   3  SUGGEST
 *   1  Error
 */

import { evaluate } from "./index.js";

function main() {
  const args = process.argv.slice(2);

  if (args[0] === "--help" || args[0] === "-h") {
    console.log(`@zouroboros/swarm-gate — Zero-cost task complexity classifier

Usage:
  npx @zouroboros/swarm-gate "<task description>"
  npx @zouroboros/swarm-gate --json "<task description>"

Exit codes:
  0  SWARM or FORCE_SWARM — task warrants multi-agent orchestration
  2  DIRECT — execute directly, no orchestration needed
  3  SUGGEST — orchestration recommended but not required
  1  Error

Signals (7, weighted):
  parallelism           (20%)  Multiple independent workstreams
  scopeBreadth          (15%)  Files/systems/domains touched
  qualityGates          (15%)  Structured validation needed
  crossDomain           (15%)  Multiple executor types required
  deliverableComplexity (15%)  Multiple output artifacts
  mutationRisk          (10%)  Production/shared state changes
  durationSignal        (10%)  Estimated effort/complexity

Thresholds:
  > 0.45     SWARM    — full orchestration pipeline
  0.30–0.45  SUGGEST  — recommended, proceed direct
  < 0.30     DIRECT   — direct execution

Overrides:
  "use swarm" / "swarm this"  → FORCE_SWARM (bypass scoring)
  "just" / "quick" / "simple" → BIAS_DIRECT (penalty -0.15)

Part of the Zouroboros ecosystem. https://github.com/AlariqHQ/zouroboros`);
    process.exit(0);
  }

  const jsonMode = args.includes("--json");
  const flagIndices = new Set<number>();
  const jsonIdx = args.indexOf("--json");
  if (jsonIdx !== -1) flagIndices.add(jsonIdx);

  const message = args.filter((_, idx) => !flagIndices.has(idx)).join(" ");

  if (!message) {
    console.error("No message provided. Use --help for usage.");
    process.exit(1);
  }

  const result = evaluate(message);

  if (jsonMode) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    if (result.directive) {
      console.log(result.directive);
      console.log(`\n[gate] decision=${result.decision} score=${result.score} override=${result.override || "none"} ${result.performanceMs}ms`);
    } else {
      console.log(`[Swarm Decision Gate: ${result.decision} — score ${result.score.toFixed(2)}]`);
      console.log(result.reason);
      console.log(`[gate] ${result.performanceMs}ms`);
    }
  }

  switch (result.decision) {
    case "SWARM":
    case "FORCE_SWARM":
      process.exit(0);
    case "DIRECT":
      process.exit(2);
    case "SUGGEST":
      process.exit(3);
  }
}

main();
