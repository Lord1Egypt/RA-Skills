import type { Signal } from '../types';
export interface GogGmailSnapshotPayload {
    messages?: unknown[];
    items?: unknown[];
    results?: unknown[];
    threads?: unknown[];
    thread?: unknown;
    count?: number;
}
export interface GogCalendarSnapshotPayload {
    events?: unknown[];
    items?: unknown[];
    results?: unknown[];
    count?: number;
}
export declare function gogGmailToSignals(payload: GogGmailSnapshotPayload): Signal[];
export declare function gogCalendarToSignals(payload: GogCalendarSnapshotPayload): Signal[];
