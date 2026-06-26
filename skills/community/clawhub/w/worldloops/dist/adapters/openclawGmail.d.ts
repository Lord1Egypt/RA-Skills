import type { Signal } from '../types';
export interface OpenClawGmailWebhookPayload {
    account?: string;
    email?: string;
    label?: string;
    messages?: unknown[];
    items?: unknown[];
    events?: unknown[];
    count?: number;
}
export declare function gmailWebhookToSignals(payload: OpenClawGmailWebhookPayload): Signal[];
