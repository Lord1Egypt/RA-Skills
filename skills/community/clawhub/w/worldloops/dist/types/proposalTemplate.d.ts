export type ProposalTemplateId = 'file-write' | 'api-call' | 'state-transition' | 'human-review' | 'notification-draft' | 'escalation';
export type ProposalRiskLevel = 'low' | 'medium' | 'high' | 'critical';
export type ProposalTemplateCategory = 'file_system' | 'external_api' | 'state_management' | 'review' | 'communication' | 'escalation';
export interface ProposalTemplate {
    id: ProposalTemplateId;
    title: string;
    description: string;
    category: ProposalTemplateCategory;
    riskLevel: ProposalRiskLevel;
    externalWrite: false;
    requiredReview: true;
    suggestedChecks: string[];
    exampleUseCases: string[];
}
