import type { Signal, WorldLoopsBriefResponse } from './types';
export declare function callWorldLoopsBrief(input: {
    signals: Signal[];
    mode?: 'demo' | 'connected' | 'reconciliation';
}): Promise<WorldLoopsBriefResponse>;
