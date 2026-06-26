import type { MinSeverity } from '../types';
export type AdjudicationAction = 'track' | 'propose' | 'require_approval' | 'escalate';
export interface SeverityAdjudication {
    severity: MinSeverity;
    action: AdjudicationAction;
    approvalRequired: boolean;
    shouldEscalate: boolean;
    reason: string;
    safety: {
        externalWrite: false;
    };
}
