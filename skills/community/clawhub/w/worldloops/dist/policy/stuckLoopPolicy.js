"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.evaluateStuckLoop = evaluateStuckLoop;
exports.getDefaultStuckLoopPolicyConfig = getDefaultStuckLoopPolicyConfig;
const DEFAULT_CONFIG = {
    todoTimeoutHours: 48,
    doingTimeoutHours: 24,
};
function hoursBetween(fromIso, nowIso) {
    const from = new Date(fromIso).getTime();
    const now = new Date(nowIso).getTime();
    if (!Number.isFinite(from) || !Number.isFinite(now)) {
        return 0;
    }
    return Math.max(0, (now - from) / (1000 * 60 * 60));
}
function isOverdue(loop, nowIso) {
    if (!loop.dueAt)
        return false;
    return new Date(loop.dueAt).getTime() < new Date(nowIso).getTime();
}
function unchanged(loop) {
    return {
        shouldTransition: false,
        from: loop.status,
        to: loop.status,
        reason: 'none',
        note: 'No stuck-loop transition needed.',
        safety: { externalWrite: false },
    };
}
function evaluateStuckLoop(loop, nowIso = new Date().toISOString(), config = DEFAULT_CONFIG) {
    if ((loop.severity === 'high' || loop.severity === 'critical') &&
        isOverdue(loop, nowIso) &&
        loop.status !== 'done' &&
        loop.status !== 'escalated') {
        return {
            shouldTransition: true,
            from: loop.status,
            to: 'escalated',
            reason: 'high_or_critical_overdue',
            note: 'High or critical severity loop is overdue and should be escalated.',
            safety: { externalWrite: false },
        };
    }
    if (loop.status === 'snoozed' && loop.dueAt && isOverdue(loop, nowIso)) {
        return {
            shouldTransition: true,
            from: 'snoozed',
            to: 'todo',
            reason: 'snooze_expired',
            note: 'Snoozed loop expired and should return to todo.',
            safety: { externalWrite: false },
        };
    }
    if (loop.status === 'todo') {
        const hours = hoursBetween(loop.updatedAt, nowIso);
        if (hours >= config.todoTimeoutHours) {
            return {
                shouldTransition: true,
                from: 'todo',
                to: 'escalated',
                reason: 'todo_timeout',
                note: `Todo loop exceeded ${config.todoTimeoutHours} hour timeout.`,
                safety: { externalWrite: false },
            };
        }
    }
    if (loop.status === 'doing') {
        const hours = hoursBetween(loop.updatedAt, nowIso);
        if (hours >= config.doingTimeoutHours) {
            return {
                shouldTransition: true,
                from: 'doing',
                to: 'escalated',
                reason: 'doing_timeout',
                note: `Doing loop exceeded ${config.doingTimeoutHours} hour timeout.`,
                safety: { externalWrite: false },
            };
        }
    }
    return unchanged(loop);
}
function getDefaultStuckLoopPolicyConfig() {
    return { ...DEFAULT_CONFIG };
}
//# sourceMappingURL=stuckLoopPolicy.js.map