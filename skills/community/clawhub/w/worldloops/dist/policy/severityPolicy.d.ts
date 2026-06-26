import type { MinSeverity } from '../types';
import type { SeverityAdjudication } from '../types/severityPolicy';
export declare function adjudicateSeverity(severity: MinSeverity | undefined): SeverityAdjudication;
