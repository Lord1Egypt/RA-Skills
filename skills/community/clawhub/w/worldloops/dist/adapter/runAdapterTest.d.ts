export interface AdapterTestResult {
    file: string;
    validate: 'passed' | 'failed';
    validateErrors?: string[];
    reconcile: 'passed' | 'failed';
    reconcileError?: string;
    openLoopPersisted: boolean;
    proposalPersisted: boolean;
    idempotency: 'passed' | 'failed';
    externalWrite: false;
    reconcileMode: 'local_heuristic';
}
export declare function runAdapterTest(filePath: string, opts?: {
    worldloopsDir?: string;
}): AdapterTestResult;
