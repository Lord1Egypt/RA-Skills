import type { MinSeverity, SignalSource } from '../types';
import type { SeverityAdjudication } from './severityPolicy';
export type OpenLoopStatus = 'todo' | 'doing' | 'done' | 'snoozed' | 'escalated';
export interface OpenLoopStateHistoryEntry {
    at: string;
    from: OpenLoopStatus | null;
    to: OpenLoopStatus;
    actor: string | null;
    note: string | null;
}
export interface OpenLoopState {
    id: string;
    canonicalKey: string;
    title: string;
    sourceSignals: {
        source: SignalSource;
        text: string;
        url?: string;
        createdAt?: string;
    }[];
    status: OpenLoopStatus;
    severity: MinSeverity;
    adjudication: SeverityAdjudication;
    owner: string | null;
    dueAt: string | null;
    lastObservedAt: string;
    updatedAt: string;
    history: OpenLoopStateHistoryEntry[];
    safety: {
        externalWrite: false;
    };
}
