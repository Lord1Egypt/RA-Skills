/**
 * Redacta — deterministic pattern engine.
 *
 * Pure TypeScript: no DOM, no network, no storage. Replaces fixed-format
 * identifiers and PII with labelled tokens, catches keyword-anchored names
 * (patients, relatives, carers — clinician names preserved), self-checks the
 * output, and reverses the process from a token map.
 */
export type Category = "clinical" | "general" | "safeharbor";
/** Validate a 10-digit NHS number using the Modulus-11 check digit. */
export declare function isValidNhs(digits: string): boolean;
/** Validate the two-letter prefix of a UK National Insurance number. */
export declare function isValidNi(prefix: string): boolean;
/** Luhn checksum for payment card numbers. */
export declare function isValidLuhn(digits: string): boolean;
export interface RedactionResult {
    text: string;
    changed: boolean;
}
export interface ResidualFinding {
    label: string;
    sample: string;
}
/**
 * A Redactor keeps one Tokeniser across many texts, so the same identifier
 * gets the same token on every sticky note on the board.
 */
export declare class Redactor {
    private tok;
    private passes;
    constructor(categories: Category[]);
    redactText(input: string): RedactionResult;
    /** {token_type: number_of_distinct_values} */
    get report(): Record<string, number>;
    /** {token: original_value} — for review / re-identification. Handle with care. */
    get tokenMap(): Record<string, string>;
}
/**
 * Re-scan already-redacted text for anything that still looks like an
 * identifier, so the UI can warn the user to check manually. Returns one
 * finding per distinct sample (deduplicated, capped). A clean result is not a
 * guarantee — it's a second pair of eyes, not a proof.
 */
/**
 * Re-identification: replace tokens with their original values, using a token
 * map produced by an earlier redaction. The inverse of redaction — for putting
 * real data back into AI output before it returns to the board.
 *
 * Tokens always end in "]", so "[NAME_1]" never matches inside "[NAME_10]";
 * plain string replacement is safe.
 */
export declare function reinstate(text: string, tokenMap: Record<string, string>): RedactionResult;
/** Validate that a parsed object is a usable token map ([TOKEN] -> string). */
export declare function isValidTokenMap(value: unknown): value is Record<string, string>;
export declare function selfCheck(redactedText: string): ResidualFinding[];
