import type { AdapterSignal } from '../types/adapterSignal';
export interface GogCalendarPayload {
    events?: unknown[];
    count?: number;
}
export declare function isGogCalendarPayload(raw: unknown): raw is GogCalendarPayload;
export declare function gogCalendarToAdapterSignal(payload: GogCalendarPayload): AdapterSignal;
