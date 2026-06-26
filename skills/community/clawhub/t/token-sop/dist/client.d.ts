import type { TraceEvent } from "./interceptor";
export interface ClawMindConfig {
    apiUrl: string;
    nodeId: string;
    timeout?: number;
}
export declare class ClawMindClient {
    private config;
    constructor(config: ClawMindConfig);
    contribute(data: {
        intent: string;
        url: string;
        domSkeletonHash?: string;
        lobsterWorkflow: {
            steps: TraceEvent[];
        };
        sessionId?: string;
    }): Promise<any>;
    match(data: {
        intent: string;
        url: string;
        domSkeletonHash?: string;
    }): Promise<any>;
    reportSuccess(macroId: string): Promise<any>;
    reportFailure(macroId: string, failedStepIndex?: number, errorType?: string, domSnapshot?: string): Promise<any>;
}
