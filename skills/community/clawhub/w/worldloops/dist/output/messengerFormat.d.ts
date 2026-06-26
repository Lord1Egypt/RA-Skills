import type { ProposalCandidate } from '../types';
export interface MessengerOutputData {
    ok: boolean;
    candidates: ProposalCandidate[];
    openLoopCount: number;
    receiptsGenerated: number;
    proposalsPersisted: number;
    proposalsAlreadyTracked: number;
}
export interface CompactOutputData {
    ok: boolean;
    candidates: ProposalCandidate[];
}
export declare function printMessengerOutput(data: MessengerOutputData): void;
export declare function printCompactOutput(data: CompactOutputData): void;
