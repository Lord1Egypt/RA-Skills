import type { Signal } from '../types';
export interface OpenClawMessagesPayload {
    messages?: unknown[];
    items?: unknown[];
    results?: unknown[];
    payload?: {
        messages?: unknown[];
        items?: unknown[];
        results?: unknown[];
    };
    count?: number;
    channel?: string;
    target?: string;
}
export declare function messagesToSignals(payload: OpenClawMessagesPayload, options?: {
    channel?: string;
    target?: string;
}): Signal[];
