/**
 * Intent parser — extracts structured intent from natural language
 * and current browser context. Lightweight local heuristics,
 * no LLM call needed for basic intent normalization.
 */
export interface ParsedIntent {
    raw: string;
    normalized: string;
    domain: string;
    action_verb: string;
    object_noun: string;
}
export declare function parseIntent(raw: string, url: string): ParsedIntent;
