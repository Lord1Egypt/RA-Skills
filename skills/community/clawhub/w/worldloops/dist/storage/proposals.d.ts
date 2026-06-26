import type { ProposalCandidate } from '../types';
import type { Proposal } from '../types/proposal';
export declare function getProposalsPath(): string;
export declare function loadProposals(): Proposal[];
export declare function saveProposal(proposal: Proposal): void;
export declare function findProposalById(id: string): Proposal | null;
export declare function listProposals(): Proposal[];
export declare function findProposalByIdempotencyKey(key: string): Proposal | null;
export declare function buildProposalFromCandidate(candidate: ProposalCandidate): Proposal;
