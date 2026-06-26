import type { Signal } from '../types';
export interface OpenClawCalendarPayload {
    account?: string;
    calendarId?: string;
    events?: unknown[];
    items?: unknown[];
    count?: number;
}
export declare function calendarEventsToSignals(payload: OpenClawCalendarPayload): Signal[];
