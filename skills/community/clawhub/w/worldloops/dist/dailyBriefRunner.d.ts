import type { ProposalCandidate } from './types';
export declare const DEFAULT_INBOX_DIR = ".worldloops/inbox";
export declare function isPromotionalText(text: string): boolean;
export declare function hasNegativeIntent(text: string): boolean;
export declare function isTravelContextEvent(title?: string, description?: string, location?: string): boolean;
export declare const SOURCES: ({
    id: "gmail";
    file: string;
    label: string;
    emoji: string;
} | {
    id: "calendar";
    file: string;
    label: string;
    emoji: string;
} | {
    id: "slack";
    file: string;
    label: string;
    emoji: string;
})[];
export type SourceId = 'gmail' | 'calendar' | 'slack';
interface SampleMessage {
    from?: string;
    subject?: string;
    user?: string;
    text?: string;
}
interface CalendarEventSample {
    title?: string;
    start?: string;
    location?: string;
}
interface EvidenceData {
    snippet?: string;
    subject?: string;
    from?: string;
    title?: string;
    start?: string;
    end?: string;
    location?: string;
    description?: string;
    text?: string;
    channel?: string;
    user?: string;
    itemCount?: number;
    messageId?: string;
    threadId?: string;
    eventId?: string;
    ts?: string;
    thread_ts?: string;
    permalink?: string;
    sampleMessages?: SampleMessage[];
    sampleEvents?: CalendarEventSample[];
}
export interface SourceResult {
    id: SourceId;
    label: string;
    emoji: string;
    file: string;
    found: boolean;
    ok: boolean;
    candidates: ProposalCandidate[];
    summaryLines: string[];
}
export declare function buildSummaryLines(sourceId: SourceId, label: string, _emoji: string, candidates: ProposalCandidate[], evidence: EvidenceData, details?: boolean): string[];
export declare function processSource(sourceId: SourceId, file: string, label: string, emoji: string, inboxDir: string, details?: boolean): Promise<SourceResult>;
export declare function processAllSources(inboxDir: string, details?: boolean): Promise<SourceResult[]>;
export declare function buildBriefLines(results: SourceResult[]): string[];
export {};
