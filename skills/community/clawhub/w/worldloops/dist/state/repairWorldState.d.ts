export interface RepairAction {
    code: string;
    status: 'planned' | 'applied' | 'skipped' | 'non_repairable';
    file: string;
    referenceId?: string;
    message: string;
}
export interface RepairSummary {
    issuesObserved: number;
    repairableIssues: number;
    nonRepairableIssues: number;
    repairsPlanned: number;
    repairsApplied: number;
}
export interface RepairReceiptStub {
    id: string;
    createdAt: string;
    externalWrite: false;
}
export interface RepairResult {
    ok: boolean;
    mode: 'dry_run' | 'apply';
    summary: RepairSummary;
    repairs: RepairAction[];
    receipt: RepairReceiptStub;
    safety: {
        externalWrite: false;
    };
}
export interface RepairOptions {
    apply?: boolean;
    worldloopsDir?: string;
}
export declare function repairWorldState(options?: RepairOptions): RepairResult;
export declare function loadRepairReceipts(options?: {
    worldloopsDir?: string;
}): unknown[];
