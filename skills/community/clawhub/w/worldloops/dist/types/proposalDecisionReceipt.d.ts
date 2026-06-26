export type ProposalDecision = 'approved' | 'rejected' | 'snoozed' | 'escalated' | 'proposed';
export interface ProposalDecisionReceipt {
    id: string;
    proposalId: string;
    templateId: string;
    decision: string;
    previousStatus: string;
    newStatus: string;
    actor: 'worldloops.local';
    note: string | null;
    boundaryCrossed: 'local_commit';
    externalWrite: false;
    createdAt: string;
    source: 'worldloops.local';
}
