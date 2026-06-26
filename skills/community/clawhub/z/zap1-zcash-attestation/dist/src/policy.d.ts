export interface PolicyRules {
    blockedTools?: string[];
    restrictedTools?: string[];
}
export interface PolicyResult {
    allowed: boolean;
    reason?: string;
}
export declare function evaluatePolicy(toolName: string, _params: Record<string, unknown>, rules: PolicyRules): PolicyResult;
