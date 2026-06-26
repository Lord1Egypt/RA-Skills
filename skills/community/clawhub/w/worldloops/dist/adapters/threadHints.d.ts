export declare function isReplyOrForward(subject: string): boolean;
export declare function hasRequestIntent(text: string): boolean;
export type ThreadHint = 'potential_open_loop' | 'needs_inspection' | null;
/**
 * Returns a classification hint for Re:/Fwd: threads so the API can avoid
 * suppressing them as already-handled. Does not write externally.
 */
export declare function classifyThreadHint(opts: {
    subject?: string;
    snippet?: string;
}): ThreadHint;
