import type { ProposalRiskLevel, ProposalTemplateId } from './proposalTemplate';

export type ExecutionContractStatus = 'draft';

export type DeniedCapability =
  | 'sendEmail'
  | 'createEmailDraft'
  | 'sendSlackMessage'
  | 'createCalendarEvent'
  | 'modifyGitHub'
  | 'writeExternalSystem';

export interface ExecutionBoundary {
  externalWrite: false;
  allowedBoundary: 'local_commit';
  deniedCapabilities: DeniedCapability[];
  reason: string;
}

export interface ExecutionPrecondition {
  id: string;
  description: string;
  satisfied: boolean;
  required: boolean;
}

export interface RequiredApproval {
  id: string;
  role: string;
  required: boolean;
  satisfied: boolean;
  reason: string;
}

export interface RollbackPlan {
  available: false;
  reason: 'Rollback execution is not implemented in v1.0.0';
}

export interface ContractAudit {
  proposalExists: boolean;
  proposalApproved: boolean;
  decisionReceiptExists: boolean;
  planExists: boolean;
  planStatus: string;
  externalWrite: false;
}

export interface ExecutionContract {
  id: string;
  planId: string;
  proposalId: string;
  templateId: ProposalTemplateId;
  title: string;
  status: ExecutionContractStatus;
  riskLevel: ProposalRiskLevel;
  executionBoundary: ExecutionBoundary;
  preconditions: ExecutionPrecondition[];
  requiredApprovals: RequiredApproval[];
  rollbackPlan: RollbackPlan;
  audit: ContractAudit;
  externalWrite: false;
  createdAt: string;
  updatedAt: string;
  source: 'worldloops.local';
}
