"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.adjudicateSeverity = adjudicateSeverity;
function adjudicateSeverity(severity) {
    const normalizedSeverity = severity ?? 'medium';
    if (normalizedSeverity === 'low') {
        return {
            severity: 'low',
            action: 'track',
            approvalRequired: false,
            shouldEscalate: false,
            reason: 'Low severity loops can be tracked locally without escalation.',
            safety: { externalWrite: false },
        };
    }
    if (normalizedSeverity === 'medium') {
        return {
            severity: 'medium',
            action: 'propose',
            approvalRequired: false,
            shouldEscalate: false,
            reason: 'Medium severity loops should be surfaced as proposal candidates.',
            safety: { externalWrite: false },
        };
    }
    if (normalizedSeverity === 'high') {
        return {
            severity: 'high',
            action: 'require_approval',
            approvalRequired: true,
            shouldEscalate: false,
            reason: 'High severity loops require explicit human approval.',
            safety: { externalWrite: false },
        };
    }
    return {
        severity: 'critical',
        action: 'escalate',
        approvalRequired: true,
        shouldEscalate: true,
        reason: 'Critical severity loops should be escalated for immediate attention.',
        safety: { externalWrite: false },
    };
}
//# sourceMappingURL=severityPolicy.js.map