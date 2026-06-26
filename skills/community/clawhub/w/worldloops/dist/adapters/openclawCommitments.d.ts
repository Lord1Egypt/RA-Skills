import type { Signal } from '../types';
export interface OpenClawCommitmentsPayload {
    count?: number;
    status?: string | null;
    agentId?: string | null;
    store?: string;
    commitments?: unknown[];
}
export declare function commitmentsToSignals(payload: OpenClawCommitmentsPayload): Signal[];
