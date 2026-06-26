/**
 * Local PII sanitizer — the primary privacy gate.
 * Runs BEFORE any data leaves the node.
 * Strips all identifiable information from action traces
 * and replaces them with Lobster argument placeholders.
 */
interface SanitizeResult {
    sanitized: string;
    extractedArgs: Map<string, ArgDefinition>;
}
interface ArgDefinition {
    type: "string" | "number" | "boolean";
    placeholder: string;
    originalPattern: string;
}
export declare function sanitizeTrace(raw: string): SanitizeResult;
export declare function sanitizeActionArgs(args: Record<string, unknown>): {
    sanitized: Record<string, unknown>;
    extractedArgs: Map<string, ArgDefinition>;
};
export {};
