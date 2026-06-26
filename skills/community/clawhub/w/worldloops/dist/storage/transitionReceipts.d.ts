import type { TransitionReceipt, BoundaryCrossed } from '../types/transitionReceipt';
import type { ProposalCandidate, Signal } from '../types';
export declare function getTransitionReceiptsPath(): string;
export declare function loadTransitionReceipts(): TransitionReceipt[];
export declare function saveTransitionReceipt(receipt: TransitionReceipt): void;
export declare function saveTransitionReceipts(receipts: TransitionReceipt[]): void;
export declare function buildTransitionReceipt(candidate: ProposalCandidate, signals: Signal[], opts: {
    proposalId?: string | null;
    adjudicationResult: string | null;
    decision: string | null;
    boundaryCrossed: BoundaryCrossed;
}): TransitionReceipt;
