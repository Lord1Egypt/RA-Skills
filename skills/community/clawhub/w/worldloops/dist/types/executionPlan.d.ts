import type { ProposalRiskLevel, ProposalTemplateId } from './proposalTemplate';
export type ExecutionPlanStatus = 'planned';
export type ExecutionPlanStepType = 'review' | 'boundary_check' | 'prepare' | 'dry_run' | 'receipt_ready';
export interface ExecutionPlanStep {
    id: string;
    title: string;
    type: ExecutionPlanStepType;
    description: string;
    externalWrite: false;
}
export interface ExecutionPlan {
    id: string;
    proposalId: string;
    templateId: ProposalTemplateId;
    title: string;
    status: ExecutionPlanStatus;
    riskLevel: ProposalRiskLevel;
    steps: ExecutionPlanStep[];
    externalWrite: false;
    createdAt: string;
    updatedAt: string;
    source: 'worldloops.local';
}
