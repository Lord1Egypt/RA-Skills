#!/usr/bin/env node

// src/index.ts
var WEIGHTS = {
  parallelism: 0.2,
  scopeBreadth: 0.15,
  qualityGates: 0.15,
  crossDomain: 0.15,
  deliverableComplexity: 0.15,
  mutationRisk: 0.1,
  durationSignal: 0.1
};
var THRESHOLD_SWARM = 0.45;
var THRESHOLD_SUGGEST = 0.3;
var BIAS_DIRECT_PENALTY = 0.15;
var FORCE_SWARM_PATTERNS = [
  /\buse\s+swarm\s+orchestrat/i,
  /\buse\s+swarm\b(?!\s+(bench|decision|gate|orchestrator|system))/i,
  /\bswarm\s+this\b/i,
  /\brun\s+(it\s+)?through\s+(the\s+)?swarm\b/i,
  /\bengage\s+(the\s+)?swarm\b/i,
  /\bfull\s+swarm\s+pipeline\b/i,
  /\bswarm\s+execution\b/i,
  /\bthrough\s+(the\s+)?swarm\s+pipeline\b/i
];
var SWARM_QUESTION_PATTERNS = [
  /\bhow\s+(has|did|does|do|will|would|can|could|should)\b.*\bswarm\b/i,
  /\bwhat\s+(is|are|was|were|does|did)\b.*\bswarm\b/i,
  /\bswarm.*(changed|work|function|operate|look|mean)/i,
  /\b(run|test|bench|validate|verify)\s+(a\s+)?swarm.?bench\b/i
];
var BIAS_DIRECT_PATTERNS = [
  /\bjust\s+(quickly?\s+)?/i,
  /\bquick(ly)?\b/i,
  /\bsimple\b/i,
  /\breal\s+quick\b/i,
  /\bjust\s+do\b/i
];
function detectOverride(msg) {
  for (const p of SWARM_QUESTION_PATTERNS) {
    if (p.test(msg)) return null;
  }
  for (const p of FORCE_SWARM_PATTERNS) {
    if (p.test(msg)) return "force_swarm";
  }
  for (const p of BIAS_DIRECT_PATTERNS) {
    if (p.test(msg)) return "bias_direct";
  }
  return null;
}
function scoreParallelism(msg) {
  const lower = msg.toLowerCase();
  let score = 0;
  const actionVerbs = lower.match(/\b(implement|build|create|deploy|analyze|research|test|write|fix|update|migrate|refactor|evaluate|audit|review|generate|design|integrate|configure|setup|install|digest|catalogue|catalog|compare|compile|identify|scan|index|map|extract|aggregate|prioritize|cross.?reference|transform|produce|deliver|send|compose|assess|profile|optimize|draft|publish|merge|document|benchmark|consolidate|reconfigure|ingest)\b/g);
  const uniqueVerbs = new Set(actionVerbs || []);
  if (uniqueVerbs.size >= 5) score += 0.5;
  else if (uniqueVerbs.size >= 4) score += 0.4;
  else if (uniqueVerbs.size >= 3) score += 0.3;
  else if (uniqueVerbs.size >= 2) score += 0.15;
  const conjunctions = (lower.match(/\b(and then|and also|as well as|plus|along with|additionally|meanwhile|in parallel|concurrently|simultaneously)\b/g) || []).length;
  if (conjunctions >= 2) score += 0.3;
  else if (conjunctions >= 1) score += 0.15;
  if (/\b(each|every)\s+\w+/i.test(lower) && uniqueVerbs.size >= 2) score += 0.15;
  if (/(?:\d+[\.\)]\s|\-\s|\*\s).*(?:\d+[\.\)]\s|\-\s|\*\s)/s.test(msg)) score += 0.2;
  if (/\b(phase|wave|stage|step)\s*\d/i.test(msg)) score += 0.1;
  const numericItems = lower.match(/\b(\d+)\s+(component|route|page|test|endpoint|feature|strateg|module|package|service|worker|agent|skill|step|task|item|asset|model|transport|adapter|check|function|method|hook|rule|seed|wave|domain)s?\b/g) || [];
  const totalNumericItems = numericItems.reduce((sum, m) => {
    const n = parseInt(m);
    return sum + (isNaN(n) ? 0 : n);
  }, 0);
  if (totalNumericItems >= 10) score += 0.5;
  else if (totalNumericItems >= 5) score += 0.4;
  else if (totalNumericItems >= 3) score += 0.3;
  else if (totalNumericItems >= 2) score += 0.2;
  const commaSeparated = msg.match(/(?:[A-Z][\w]+(?:Transport|Layer|Module|Service|Strategy|Gate|Client|Provider|Manager|Handler|Worker|Adapter|Bridge|Plugin|Hook|System)?(?:\s+\w+)?\s*,\s*){2,}[A-Z][\w]+/g) || [];
  if (commaSeparated.length > 0) score += 0.3;
  const commaFeatures = lower.match(/(?:[\w\s-]+,\s+){2,}(?:and\s+)?[\w\s-]+/g) || [];
  const featureCount = commaFeatures.reduce((sum, m) => sum + m.split(/,/).length, 0);
  if (featureCount >= 4) score += 0.3;
  else if (featureCount >= 3) score += 0.2;
  return Math.min(score, 1);
}
function scoreScopeBreadth(msg) {
  const lower = msg.toLowerCase();
  let score = 0;
  const fileRefs = (msg.match(/(?:\/[\w\-\.]+){2,}|[\w\-]+\.(ts|js|py|yaml|json|md|sh|tsx|jsx|css|html)/g) || []).length;
  if (fileRefs >= 5) score += 0.4;
  else if (fileRefs >= 3) score += 0.25;
  else if (fileRefs >= 1) score += 0.1;
  const domains = [
    /\b(database|db|sql|postgres|sqlite|duckdb|schema|migration)\b/,
    /\b(api|endpoint|route|server|backend|handler)\b/,
    /\b(ui|frontend|component|page|dashboard|react)\b/,
    /\b(deploy|hosting|service|docker|ci|cd|pipeline|production)\b/,
    /\b(memory|recall|episodic|procedural)\b/,
    /\b(test|spec|benchmark|eval|coverage)\b/,
    /\b(email|sms|notification|alert|report|pdf)\b/,
    /\b(auth|security|token|credential)\b/,
    /\b(swarm|orchestrat|executor|agent)\b/,
    /\b(git|repo|repository|codebase|branch|pr|commit)\b/,
    /\b(skill|plugin|hook|pattern|architecture)\b/,
    /\b(ecosystem|system|platform|framework)\b/,
    /\b(blog|social|content|marketing|post|article|media)\b/,
    /\b(npm|package|publish|release|changelog|version)\b/
  ];
  const domainHits = domains.filter((d) => d.test(lower)).length;
  if (domainHits >= 4) score += 0.4;
  else if (domainHits >= 3) score += 0.3;
  else if (domainHits >= 2) score += 0.15;
  if (/\b(across|entire|whole|all|every|full|comprehensive|end.to.end)\b/i.test(lower)) score += 0.2;
  if (/\b(migrat|abstract|transport|layer|adapter)\b/i.test(lower)) score += 0.15;
  const namedEntities = msg.match(/[A-Z][\w-]*(?:\s+[A-Z][\w-]*)*/g) || [];
  const uniqueEntities = new Set(namedEntities.filter((e) => e.length > 2));
  if (uniqueEntities.size >= 4) score += 0.3;
  else if (uniqueEntities.size >= 3) score += 0.2;
  return Math.min(score, 1);
}
function scoreQualityGates(msg) {
  const lower = msg.toLowerCase();
  let score = 0;
  const qualityTerms = [
    /\b(test|tests|testing|tsc|typecheck|lint|build)\b/,
    /\b(acceptance\s+criteria|ac\b|criteria)\b/,
    /\b(verify|validate|confirm|check|ensure|assert)\b/,
    /\b(eval|evaluat|benchmark|score|metric)\b/,
    /\b(review|audit|inspect|post.?flight)\b/,
    /\b(ci|cd|pipeline|green|passing)\b/
  ];
  const qualityHits = qualityTerms.filter((t) => t.test(lower)).length;
  if (qualityHits >= 3) score += 0.5;
  else if (qualityHits >= 2) score += 0.3;
  else if (qualityHits >= 1) score += 0.15;
  if (/\b(report|pdf|document|summary|matrix|roadmap|checklist)\b/i.test(lower)) score += 0.25;
  if (/\b(email|send|deliver)\b/i.test(lower) && /\b(report|pdf|document)\b/i.test(lower)) score += 0.25;
  return Math.min(score, 1);
}
function scoreCrossDomain(msg) {
  const lower = msg.toLowerCase();
  let score = 0;
  const executorSignals = [
    /\b(research|investigate|explore|deep\s+dive|analyze|compare)\b/,
    /\b(implement|code|build|refactor|fix|write\s+code|migrate|abstract)\b/,
    /\b(design|ui|ux|visual|layout|wireframe|dashboard)\b/,
    /\b(deploy|publish|host|service|production|release)\b/,
    /\b(test|benchmark|eval|validate|verify)\b/,
    /\b(document|report|write.up|summarize|blog|pr\b|readme)\b/,
    /\b(social|marketing|content|campaign|newsletter|announce)\b/,
    /\b(configur|setup|provision|register|bootstrap|architect)\b/
  ];
  const executorHits = executorSignals.filter((s) => s.test(lower)).length;
  if (executorHits >= 4) score += 0.5;
  else if (executorHits >= 3) score += 0.35;
  else if (executorHits >= 2) score += 0.2;
  if (/\b(subagent|delegate|parallel\s+agent|multi.?agent|specialist)\b/i.test(lower)) score += 0.3;
  if (/\b(integrate|integration|connect|bridge|sync)\b/i.test(lower)) score += 0.2;
  return Math.min(score, 1);
}
function scoreDeliverableComplexity(msg) {
  const lower = msg.toLowerCase();
  let score = 0;
  const artifacts = [
    /\b(report|pdf)\b/,
    /\b(email|send)\b/,
    /\b(code|implement|script)\b/,
    /\b(deploy|publish|site|page)\b/,
    /\b(diagram|chart|visual)\b/,
    /\b(database|schema|migration)\b/,
    /\b(config|configuration|setup)\b/,
    /\b(test|spec|benchmark)\b/,
    /\b(seed|yaml|spec)\b/,
    /\b(pr|pull\s+request|commit)\b/,
    /\b(blog\s+post|article|post|readme|documentation|guide)\b/,
    /\b(social|assets|media|banner|image)\b/,
    /\b(announcement|newsletter|campaign)\b/
  ];
  const artifactHits = artifacts.filter((a) => a.test(lower)).length;
  if (artifactHits >= 4) score += 0.5;
  else if (artifactHits >= 3) score += 0.35;
  else if (artifactHits >= 2) score += 0.2;
  if (/\b(matrix|roadmap|checklist|plan|inventory|catalogue|catalog)\b/i.test(lower)) score += 0.25;
  if (/\b(then|after|finally|once\s+done|when\s+complete|followed\s+by)\b/i.test(lower)) score += 0.25;
  return Math.min(score, 1);
}
function scoreMutationRisk(msg) {
  const lower = msg.toLowerCase();
  let score = 0;
  if (/\b(production|prod|live|deploy|publish|release)\b/i.test(lower)) score += 0.3;
  if (/\b(refactor|migrate|rename|restructure|rewrite|overhaul)\b/i.test(lower)) score += 0.3;
  if (/\b(service|server|database|schema|migration|config)\b/i.test(lower) && /\b(update|change|modify|create|delete|remove)\b/i.test(lower)) score += 0.2;
  if (/\b(shared|cross.?boundary|multi.?process|env\s+var|global)\b/i.test(lower)) score += 0.2;
  return Math.min(score, 1);
}
function scoreDuration(msg) {
  const lower = msg.toLowerCase();
  let score = 0;
  const wordCount = msg.split(/\s+/).length;
  if (wordCount > 150) score += 0.3;
  else if (wordCount > 80) score += 0.2;
  else if (wordCount > 40) score += 0.1;
  if (/\b(comprehensive|thorough|deep|exhaustive|complete|full|three.stage|end.to.end)\b/i.test(lower)) score += 0.25;
  if (/\b(migrat|pipeline|architecture|abstraction|transport|dashboard|framework)\b/i.test(lower)) score += 0.15;
  if (/\b(phase|iteration|sprint|cycle|round|pass)\b/i.test(lower)) score += 0.25;
  if (/\b(all|every|each)\b/i.test(lower) && wordCount > 20) score += 0.2;
  return Math.min(score, 1);
}
function scoreArchetypes(msg) {
  const lower = msg.toLowerCase();
  let bonus = 0;
  if (/\b(implement|build|create|develop|add)\b.*\b(with|including|featuring)\b.*,.*,/i.test(lower)) {
    const commaCount = (lower.match(/,/g) || []).length;
    bonus += commaCount >= 3 ? 0.4 : 0.3;
  }
  const numericMatches = lower.match(/\b\d+\s+\w+/g) || [];
  const numericValues = numericMatches.map((m) => parseInt(m)).filter((n) => !isNaN(n) && n >= 2);
  const totalNumericScale = numericValues.reduce((a, b) => a + b, 0);
  if (numericValues.length >= 2 && totalNumericScale >= 10) bonus += 0.35;
  else if (numericValues.length >= 2 || totalNumericScale >= 8) bonus += 0.3;
  else if (totalNumericScale >= 5) bonus += 0.25;
  else if (totalNumericScale >= 3) bonus += 0.15;
  if (/\b(migrat|abstract)/i.test(lower) && /\b(from\b.*\bto\b|layer|client|model|system)\b/i.test(lower)) bonus += 0.25;
  if (/\b(compare|versus|vs\.?|evaluate|research)\b/i.test(lower)) {
    const entities = lower.split(/,|\band\b/).length;
    if (entities >= 4) bonus += 0.3;
    else if (entities >= 3) bonus += 0.25;
    else if (entities >= 2) bonus += 0.15;
  }
  if (/\b(dashboard|page|site|app)\b/i.test(lower) && /\b(route|component|endpoint|api|widget|panel|section)\b/i.test(lower)) bonus += 0.2;
  if (/\b(email|send|deliver)\b/i.test(lower) && /\b(pdf|report|summary)\b/i.test(lower) && /\b(analyz|research|evaluat|audit|review|implement|build|deploy|test)\b/i.test(lower)) bonus += 0.2;
  if (/\b(publish|release)\b/i.test(lower) && /\b(all|every|multiple|packages?)\b/i.test(lower)) bonus += 0.2;
  if (/\b(pr|pull\s+request)\b/i.test(lower) && /\b(skill|plugin|tool|package)\b/i.test(lower) && /\b(communit|registr|upstream|open.?source)\b/i.test(lower)) bonus += 0.2;
  if (/\b(three.stage|full|comprehensive)\b/i.test(lower) && /\b(eval|audit|review|assessment)\b/i.test(lower)) bonus += 0.2;
  if (/\b(set\s*up|configure|architect)\b/i.test(lower) && /\b(bridge|architecture|pattern|framework|bot)\b/i.test(lower)) bonus += 0.15;
  if (/\b(blog\s+post|write\s+a\s+blog|create\s+a?\s*blog|draft\s+a?\s*blog|publish\s+a?\s*blog)\b/i.test(lower)) bonus += 0.45;
  return Math.min(bonus, 0.45);
}
function buildDirective(mode, score, signals) {
  const topSignal = Object.entries(signals).sort((a, b) => b[1] - a[1])[0]?.[0] || "unknown";
  if (mode === "SWARM") {
    return [
      `[Swarm Decision Gate: SWARM \u2014 score ${score.toFixed(2)}]`,
      "This task warrants formal swarm orchestration. Engage the full pipeline:",
      "1. Spec Interview \u2192 produce seed YAML with tasks, ACs, DAG, exit conditions",
      "2. Seed Eval Gate \u2192 validate paths, schemas, DAG conflicts",
      "3. User Approval \u2192 present seed for sign-off before execution",
      "4. DAG Execution \u2192 dispatch through swarm orchestrator",
      "5. Post-Flight Eval \u2192 3-stage evaluation (mechanical, AC, consensus)",
      "6. Gap Audit \u2192 reachability, data prereqs, cross-boundary, eval-production parity",
      `Primary driver: ${topSignal}`
    ].join("\n");
  }
  return [
    `[Swarm Decision Gate: SUGGEST \u2014 score ${score.toFixed(2)}]`,
    "This task could benefit from swarm orchestration but doesn't strictly require it.",
    `Primary signal: ${topSignal}. Consider whether the task has independent workstreams`,
    "that would benefit from parallel execution and structured quality gates.",
    "Proceeding with direct execution. User can override with 'use swarm orchestration'."
  ].join("\n");
}
function evaluate(msg, config) {
  const start = performance.now();
  const threshSwarm = config?.thresholdSwarm ?? THRESHOLD_SWARM;
  const threshSuggest = config?.thresholdSuggest ?? THRESHOLD_SUGGEST;
  const biasPenalty = config?.biasDirectPenalty ?? BIAS_DIRECT_PENALTY;
  const override = detectOverride(msg);
  const signals = {
    parallelism: scoreParallelism(msg),
    scopeBreadth: scoreScopeBreadth(msg),
    qualityGates: scoreQualityGates(msg),
    crossDomain: scoreCrossDomain(msg),
    deliverableComplexity: scoreDeliverableComplexity(msg),
    mutationRisk: scoreMutationRisk(msg),
    durationSignal: scoreDuration(msg)
  };
  const weightedSignals = {};
  let totalScore = 0;
  for (const [key, value] of Object.entries(signals)) {
    const weight = WEIGHTS[key];
    const weighted = value * weight;
    weightedSignals[key] = Number(weighted.toFixed(4));
    totalScore += weighted;
  }
  const wordCount = msg.split(/\s+/).length;
  const activeSignals = Object.values(signals).filter((v) => v > 0).length;
  if (wordCount <= 25 && activeSignals >= 3) totalScore *= 1.5;
  else if (wordCount <= 40 && activeSignals >= 4) totalScore *= 1.4;
  else if (wordCount <= 40 && activeSignals >= 3) totalScore *= 1.3;
  totalScore += scoreArchetypes(msg);
  if (override === "bias_direct") {
    totalScore = Math.max(0, totalScore - biasPenalty);
  }
  totalScore = Number(totalScore.toFixed(4));
  let decision;
  let reason;
  let directive;
  if (override === "force_swarm") {
    decision = "FORCE_SWARM";
    reason = "User explicitly requested swarm orchestration \u2014 override engaged.";
    directive = buildDirective("SWARM", totalScore, signals);
  } else if (totalScore >= threshSwarm) {
    decision = "SWARM";
    const topSignals = Object.entries(weightedSignals).sort((a, b) => b[1] - a[1]).slice(0, 3).map(([k]) => k);
    reason = `Score ${totalScore.toFixed(2)} exceeds SWARM threshold (${threshSwarm}). Top signals: ${topSignals.join(", ")}.`;
    directive = buildDirective("SWARM", totalScore, signals);
  } else if (totalScore >= threshSuggest) {
    decision = "SUGGEST";
    reason = `Score ${totalScore.toFixed(2)} in SUGGEST range (${threshSuggest}\u2013${threshSwarm}). Swarm may add value but isn't required.`;
    directive = buildDirective("SUGGEST", totalScore, signals);
  } else {
    decision = "DIRECT";
    reason = `Score ${totalScore.toFixed(2)} below DIRECT threshold (${threshSuggest}). Direct execution is appropriate.`;
    directive = "";
  }
  return { decision, score: totalScore, signals, weightedSignals, override, reason, directive, performanceMs: Number((performance.now() - start).toFixed(1)) };
}

// src/cli.ts
function main() {
  const args = process.argv.slice(2);
  if (args[0] === "--help" || args[0] === "-h") {
    console.log(`@zouroboros/swarm-gate \u2014 Zero-cost task complexity classifier

Usage:
  npx @zouroboros/swarm-gate "<task description>"
  npx @zouroboros/swarm-gate --json "<task description>"

Exit codes:
  0  SWARM or FORCE_SWARM \u2014 task warrants multi-agent orchestration
  2  DIRECT \u2014 execute directly, no orchestration needed
  3  SUGGEST \u2014 orchestration recommended but not required
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
  > 0.45     SWARM    \u2014 full orchestration pipeline
  0.30\u20130.45  SUGGEST  \u2014 recommended, proceed direct
  < 0.30     DIRECT   \u2014 direct execution

Overrides:
  "use swarm" / "swarm this"  \u2192 FORCE_SWARM (bypass scoring)
  "just" / "quick" / "simple" \u2192 BIAS_DIRECT (penalty -0.15)

Part of the Zouroboros ecosystem. https://github.com/AlariqHQ/zouroboros`);
    process.exit(0);
  }
  const jsonMode = args.includes("--json");
  const flagIndices = /* @__PURE__ */ new Set();
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
      console.log(`
[gate] decision=${result.decision} score=${result.score} override=${result.override || "none"} ${result.performanceMs}ms`);
    } else {
      console.log(`[Swarm Decision Gate: ${result.decision} \u2014 score ${result.score.toFixed(2)}]`);
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
/**
 * @zouroboros/swarm-gate — Zero-cost task complexity classifier
 *
 * Pure TypeScript heuristic (~2ms, zero API cost). Evaluates 7 weighted signals
 * to score whether a task warrants multi-agent swarm orchestration.
 *
 * Part of the Zouroboros ecosystem. https://github.com/AlariqHQ/zouroboros
 *
 * @license MIT
 */
