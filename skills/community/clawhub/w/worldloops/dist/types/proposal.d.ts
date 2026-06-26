import type { ProposalTemplateId, ProposalRiskLevel, ProposalTemplateCategory } from './proposalTemplate';
export type ProposalStatus = 'proposed' | 'approved' | 'rejected' | 'snoozed' | 'escalated';
export interface Proposal {
    id: string;
    templateId: ProposalTemplateId;
    title: string;
    intent: string;
    category: ProposalTemplateCategory;
    riskLevel: ProposalRiskLevel;
    requiredReview: true;
    externalWrite: false;
    checks: string[];
    status: ProposalStatus;
    createdAt: string;
    updatedAt: string;
    source: 'worldloops.local';
    idempotencyKey?: string;
}
