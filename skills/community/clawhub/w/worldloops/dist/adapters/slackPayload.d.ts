import type { AdapterSignal } from '../types/adapterSignal';
export interface SlackHostPayload {
    channel?: string;
    channel_id?: string;
    channel_name?: string;
    messages?: unknown[];
    items?: unknown[];
    text?: string;
    user?: string;
    username?: string;
    ts?: string;
    thread_ts?: string;
    permalink?: string;
}
export declare function isSlackHostPayload(raw: unknown): raw is SlackHostPayload;
export declare function slackPayloadToAdapterSignal(payload: SlackHostPayload): AdapterSignal;
