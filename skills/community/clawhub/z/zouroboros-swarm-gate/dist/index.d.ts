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
declare const WEIGHTS: {
    readonly parallelism: 0.2;
    readonly scopeBreadth: 0.15;
    readonly qualityGates: 0.15;
    readonly crossDomain: 0.15;
    readonly deliverableComplexity: 0.15;
    readonly mutationRisk: 0.1;
    readonly durationSignal: 0.1;
};
declare const THRESHOLD_SWARM = 0.45;
declare const THRESHOLD_SUGGEST = 0.3;
type Decision = "SWARM" | "DIRECT" | "SUGGEST" | "FORCE_SWARM";
type Override = "force_swarm" | "bias_direct" | null;
interface SwarmDecision {
    decision: Decision;
    score: number;
    signals: Record<string, number>;
    weightedSignals: Record<string, number>;
    override: Override;
    reason: string;
    directive: string;
    performanceMs: number;
}
interface SwarmGateConfig {
    thresholdSwarm?: number;
    thresholdSuggest?: number;
    biasDirectPenalty?: number;
}
declare function evaluate(msg: string, config?: SwarmGateConfig): SwarmDecision;

export { type Decision, type Override, type SwarmDecision, type SwarmGateConfig, THRESHOLD_SUGGEST, THRESHOLD_SWARM, WEIGHTS, evaluate };
