import type { AdapterSignal } from '../types/adapterSignal';
export interface GogGmailPayload {
    messages?: unknown[];
    count?: number;
}
export declare function isGogGmailPayload(raw: unknown): raw is GogGmailPayload;
export declare function gogGmailToAdapterSignal(payload: GogGmailPayload): AdapterSignal;
