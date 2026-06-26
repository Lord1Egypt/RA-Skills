import type { OpenLoopState, OpenLoopStatus } from './types/openLoopState';
export type ObservationIntent = 'new_loop' | 'state_transition' | 'noise' | 'related_context' | 'evidence';
export interface OpenClawObservation {
    id: string;
    source: string;
    sourceId: string;
    observedBy: 'openclaw';
    userQuery?: string;
    observationIntent?: ObservationIntent;
    title: string;
    text: string;
    timestamp: string;
    actor?: string | null;
    dueAt?: string;
    evidence: Record<string, unknown>;
    confidence?: number;
    relatedContext?: Record<string, unknown> | null;
}
export type AdjudicationVerdict = 'accepted' | 'suppressed' | 'attached_context' | 'needs_review' | 'state_transition';
export type SuppressionReason = 'promotional_or_informational' | 'negative_intent_no_action' | 'duplicate_signal' | 'weak_evidence' | 'context_only';
export interface StateTransitionInfo {
    loopId: string;
    loopTitle: string;
    canonicalKey: string;
    fromStatus: OpenLoopStatus;
    toStatus: OpenLoopStatus | 'still_open';
    transitionApplied: boolean;
    note: string;
}
export interface AdjudicationResult {
    observation: OpenClawObservation;
    verdict: AdjudicationVerdict;
    suppressionReason?: SuppressionReason;
    openLoopId?: string;
    openLoopTitle?: string;
    stateTransition?: StateTransitionInfo;
}
export interface SuppressionReceipt {
    id: string;
    observationId: string;
    source: string;
    title: string;
    verdict: AdjudicationVerdict;
    suppressionReason?: SuppressionReason;
    stateTransition?: StateTransitionInfo;
    adjudicatedAt: string;
    safety: {
        externalWrite: false;
    };
}
export interface IntakeSummary {
    total: number;
    accepted: number;
    suppressed: number;
    attached_context: number;
    needs_review: number;
    state_transition: number;
    results: AdjudicationResult[];
    receipts: SuppressionReceipt[];
    morningBriefLines: string[];
    safety: {
        externalWrite: false;
    };
}
export declare function canonicalKeyForObservation(obs: OpenClawObservation): string;
export declare function adjudicateObservation(obs: OpenClawObservation, acceptedKeysInBatch: Set<string>, existingLoopKeys: Set<string>, createdLoopsInBatch: Map<string, OpenLoopState>, existingLoops: OpenLoopState[]): {
    verdict: AdjudicationVerdict;
    suppressionReason?: SuppressionReason;
    stateTransition?: StateTransitionInfo;
};
export declare function runIntake(observations: OpenClawObservation[]): IntakeSummary;
export declare function loadObservations(filePath: string): OpenClawObservation[];
