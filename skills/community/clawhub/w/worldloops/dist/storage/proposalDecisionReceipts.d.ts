import type { ProposalDecisionReceipt } from '../types/proposalDecisionReceipt';
export declare function getProposalDecisionReceiptsPath(): string;
export declare function loadProposalDecisionReceipts(): ProposalDecisionReceipt[];
export declare function saveProposalDecisionReceipt(receipt: ProposalDecisionReceipt): void;
export declare function listProposalDecisionReceipts(): ProposalDecisionReceipt[];
export declare function findProposalDecisionReceiptById(id: string): ProposalDecisionReceipt | null;
