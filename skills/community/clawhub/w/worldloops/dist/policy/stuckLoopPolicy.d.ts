import type { OpenLoopState } from '../types/openLoopState';
import type { StuckLoopEvaluation, StuckLoopPolicyConfig } from '../types/stuckLoopPolicy';
export declare function evaluateStuckLoop(loop: OpenLoopState, nowIso?: string, config?: StuckLoopPolicyConfig): StuckLoopEvaluation;
export declare function getDefaultStuckLoopPolicyConfig(): StuckLoopPolicyConfig;
