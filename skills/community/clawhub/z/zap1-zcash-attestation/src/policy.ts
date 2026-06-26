export interface PolicyRules {
  blockedTools?: string[];
  restrictedTools?: string[];
}

export interface PolicyResult {
  allowed: boolean;
  reason?: string;
}

export function evaluatePolicy(
  toolName: string,
  _params: Record<string, unknown>,
  rules: PolicyRules,
): PolicyResult {
  if (rules.blockedTools?.includes(toolName)) {
    return { allowed: false, reason: `tool "${toolName}" blocked by agent policy` };
  }

  if (rules.restrictedTools?.includes(toolName)) {
    return { allowed: false, reason: `tool "${toolName}" restricted by agent policy` };
  }

  return { allowed: true };
}
