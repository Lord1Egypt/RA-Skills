export function evaluatePolicy(toolName, _params, rules) {
    if (rules.blockedTools?.includes(toolName)) {
        return { allowed: false, reason: `tool "${toolName}" blocked by agent policy` };
    }
    if (rules.restrictedTools?.includes(toolName)) {
        return { allowed: false, reason: `tool "${toolName}" restricted by agent policy` };
    }
    return { allowed: true };
}
