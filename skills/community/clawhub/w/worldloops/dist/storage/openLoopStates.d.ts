import type { ProposalCandidate, Signal } from '../types';
import type { OpenLoopState, OpenLoopStatus } from '../types/openLoopState';
export declare function getOpenLoopStatesPath(): string;
export declare function loadOpenLoopStates(): OpenLoopState[];
export declare function saveOpenLoopStates(states: OpenLoopState[]): void;
export declare function saveOpenLoopState(state: OpenLoopState): void;
export declare function findOpenLoopStateById(id: string): OpenLoopState | null;
export declare function transitionOpenLoopState(id: string, to: OpenLoopStatus, opts?: {
    actor?: string | null;
    note?: string | null;
}): OpenLoopState;
export declare function selectRelevantSignalsForProposal(candidate: ProposalCandidate, signals: Signal[]): Signal[];
export declare function buildOpenLoopStateFromProposal(candidate: ProposalCandidate, signals: Signal[]): OpenLoopState;
