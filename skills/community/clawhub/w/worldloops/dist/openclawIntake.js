"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.canonicalKeyForObservation = canonicalKeyForObservation;
exports.adjudicateObservation = adjudicateObservation;
exports.runIntake = runIntake;
exports.loadObservations = loadObservations;
const fs = __importStar(require("node:fs"));
const path = __importStar(require("node:path"));
const crypto = __importStar(require("node:crypto"));
const dailyBriefRunner_1 = require("./dailyBriefRunner");
const openLoopStates_1 = require("./storage/openLoopStates");
const severityPolicy_1 = require("./policy/severityPolicy");
function getWorldLoopsDir() {
    return process.env.WORLDLOOPS_DIR ?? path.join(process.cwd(), '.worldloops');
}
function getSuppressionReceiptsPath() {
    return path.join(getWorldLoopsDir(), 'openclaw_suppression_receipts.json');
}
function loadSuppressionReceipts() {
    const p = getSuppressionReceiptsPath();
    if (!fs.existsSync(p))
        return [];
    return JSON.parse(fs.readFileSync(p, 'utf8'));
}
function saveSuppressionReceipts(receipts) {
    const p = getSuppressionReceiptsPath();
    const dir = path.dirname(p);
    if (!fs.existsSync(dir))
        fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(p, JSON.stringify(receipts, null, 2) + '\n', 'utf8');
}
function canonicalKeyForObservation(obs) {
    return `openclaw-${obs.source}-${obs.sourceId}`;
}
const KNOWN_SOURCES = ['slack', 'gmail', 'calendar', 'github', 'manual'];
function toSignalSource(source) {
    return KNOWN_SOURCES.includes(source) ? source : 'manual';
}
const COMPLETION_INDICATORS = [
    'resolved', 'completed', 'done', 'confirmed', 'sent', 'received',
    'closed', 'finished', 'addressed',
];
const ESCALATION_INDICATORS = [
    'overdue', 'urgent', 'escalate', 'missed deadline', 'critical',
    'past due', 'immediately', 'asap',
];
const SNOOZE_INDICATORS = [
    'can wait', 'snooze', 'deprioritize', 'defer', 'postpone', 'not urgent',
];
function detectTransitionTarget(text) {
    const lower = text.toLowerCase();
    if (ESCALATION_INDICATORS.some(w => lower.includes(w)))
        return 'escalated';
    if (COMPLETION_INDICATORS.some(w => lower.includes(w)))
        return 'done';
    if (SNOOZE_INDICATORS.some(w => lower.includes(w)))
        return 'snoozed';
    return 'still_open';
}
function adjudicateObservation(obs, acceptedKeysInBatch, existingLoopKeys, createdLoopsInBatch, existingLoops) {
    // Step 0: explicit state_transition intent — handle before heuristics
    if (obs.observationIntent === 'state_transition') {
        const relCtx = obs.relatedContext;
        const targetKey = typeof relCtx?.existingLoopKey === 'string' ? relCtx.existingLoopKey : undefined;
        if (!targetKey) {
            return { verdict: 'needs_review', suppressionReason: 'weak_evidence' };
        }
        const targetLoop = createdLoopsInBatch.get(targetKey) ??
            existingLoops.find(l => l.canonicalKey === targetKey);
        if (!targetLoop) {
            return { verdict: 'needs_review', suppressionReason: 'weak_evidence' };
        }
        const toStatus = detectTransitionTarget(obs.text);
        const applied = toStatus !== 'still_open' && toStatus !== targetLoop.status;
        if (applied) {
            const note = toStatus === 'done' ? 'closed_by_new_evidence' :
                toStatus === 'escalated' ? 'escalated_due_to_deadline' : toStatus;
            (0, openLoopStates_1.transitionOpenLoopState)(targetLoop.id, toStatus, {
                actor: 'worldloops.openclaw-intake',
                note: `${note}; observationId=${obs.id}`,
            });
        }
        const stateTransition = {
            loopId: targetLoop.id,
            loopTitle: targetLoop.title,
            canonicalKey: targetKey,
            fromStatus: targetLoop.status,
            toStatus,
            transitionApplied: applied,
            note: toStatus === 'done' ? 'closed_by_new_evidence' :
                toStatus === 'escalated' ? 'escalated_due_to_deadline' :
                    toStatus === 'snoozed' ? 'snoozed_by_observation' : 'still_open',
        };
        return { verdict: 'state_transition', stateTransition };
    }
    // Step 0.5: explicit observationIntent is authoritative — skip heuristics that would override it
    if (obs.observationIntent !== undefined) {
        if (obs.observationIntent === 'noise') {
            return { verdict: 'suppressed', suppressionReason: 'promotional_or_informational' };
        }
        if (obs.observationIntent === 'related_context' || obs.observationIntent === 'evidence') {
            return { verdict: 'attached_context', suppressionReason: 'context_only' };
        }
        // new_loop: still guard against duplicates and low confidence
        const key = canonicalKeyForObservation(obs);
        if (acceptedKeysInBatch.has(key) || existingLoopKeys.has(key)) {
            return { verdict: 'suppressed', suppressionReason: 'duplicate_signal' };
        }
        if (typeof obs.confidence === 'number' && obs.confidence < 0.4) {
            return { verdict: 'needs_review', suppressionReason: 'weak_evidence' };
        }
        return { verdict: 'accepted' };
    }
    // Steps 1–7: heuristic adjudication (for observations without explicit intent)
    const evidenceTitle = typeof obs.evidence.title === 'string' ? obs.evidence.title : obs.title;
    const evidenceDesc = typeof obs.evidence.description === 'string' ? obs.evidence.description :
        typeof obs.evidence.snippet === 'string' ? obs.evidence.snippet : obs.text;
    const evidenceLocation = typeof obs.evidence.location === 'string' ? obs.evidence.location : '';
    const combinedText = [
        obs.title, obs.text,
        ...Object.values(obs.evidence).filter((v) => typeof v === 'string'),
    ].join(' ');
    if ((0, dailyBriefRunner_1.isPromotionalText)(combinedText)) {
        return { verdict: 'suppressed', suppressionReason: 'promotional_or_informational' };
    }
    if ((0, dailyBriefRunner_1.hasNegativeIntent)(combinedText)) {
        return { verdict: 'suppressed', suppressionReason: 'negative_intent_no_action' };
    }
    if ((0, dailyBriefRunner_1.isTravelContextEvent)(evidenceTitle, evidenceDesc, evidenceLocation)) {
        return { verdict: 'attached_context', suppressionReason: 'context_only' };
    }
    const key = canonicalKeyForObservation(obs);
    if (acceptedKeysInBatch.has(key) || existingLoopKeys.has(key)) {
        return { verdict: 'suppressed', suppressionReason: 'duplicate_signal' };
    }
    if (obs.relatedContext !== null && obs.relatedContext !== undefined) {
        return { verdict: 'attached_context', suppressionReason: 'context_only' };
    }
    if (typeof obs.confidence === 'number' && obs.confidence < 0.4) {
        return { verdict: 'needs_review', suppressionReason: 'weak_evidence' };
    }
    return { verdict: 'accepted' };
}
function runIntake(observations) {
    const now = new Date().toISOString();
    const existingLoops = (0, openLoopStates_1.loadOpenLoopStates)();
    const existingLoopKeys = new Set(existingLoops.map(l => l.canonicalKey));
    const acceptedKeysInBatch = new Set();
    const createdLoopsInBatch = new Map();
    const results = [];
    const receipts = [];
    for (const obs of observations) {
        const { verdict, suppressionReason, stateTransition } = adjudicateObservation(obs, acceptedKeysInBatch, existingLoopKeys, createdLoopsInBatch, existingLoops);
        const result = { observation: obs, verdict, suppressionReason, stateTransition };
        if (verdict === 'accepted') {
            const key = canonicalKeyForObservation(obs);
            acceptedKeysInBatch.add(key);
            const loopState = {
                id: crypto.randomUUID(),
                canonicalKey: key,
                title: obs.title,
                sourceSignals: [{
                        source: toSignalSource(obs.source),
                        text: obs.text,
                        createdAt: obs.timestamp,
                    }],
                status: 'todo',
                severity: 'medium',
                adjudication: (0, severityPolicy_1.adjudicateSeverity)('medium'),
                owner: obs.actor ?? null,
                dueAt: obs.dueAt ?? null,
                lastObservedAt: now,
                updatedAt: now,
                history: [{
                        at: now,
                        from: null,
                        to: 'todo',
                        actor: 'worldloops.openclaw-intake',
                        note: `Accepted from OpenClaw observation; observedBy=${obs.observedBy}; userQuery=${obs.userQuery ?? 'unspecified'}`,
                    }],
                safety: { externalWrite: false },
            };
            (0, openLoopStates_1.saveOpenLoopState)(loopState);
            createdLoopsInBatch.set(key, loopState);
            result.openLoopId = loopState.id;
            result.openLoopTitle = loopState.title;
        }
        if (verdict !== 'accepted') {
            receipts.push({
                id: crypto.randomUUID(),
                observationId: obs.id,
                source: obs.source,
                title: obs.title,
                verdict,
                suppressionReason,
                stateTransition,
                adjudicatedAt: now,
                safety: { externalWrite: false },
            });
        }
        results.push(result);
    }
    if (receipts.length > 0) {
        const existing = loadSuppressionReceipts();
        saveSuppressionReceipts([...existing, ...receipts]);
    }
    return {
        total: observations.length,
        accepted: results.filter(r => r.verdict === 'accepted').length,
        suppressed: results.filter(r => r.verdict === 'suppressed').length,
        attached_context: results.filter(r => r.verdict === 'attached_context').length,
        needs_review: results.filter(r => r.verdict === 'needs_review').length,
        state_transition: results.filter(r => r.verdict === 'state_transition').length,
        results,
        receipts,
        morningBriefLines: buildMorningBriefLines(results),
        safety: { externalWrite: false },
    };
}
function buildMorningBriefLines(results) {
    const lines = [];
    const accepted = results.filter(r => r.verdict === 'accepted');
    const appliedTransitions = results.filter(r => r.verdict === 'state_transition' && r.stateTransition?.transitionApplied);
    const transitionByKey = new Map();
    for (const r of appliedTransitions) {
        if (r.stateTransition) {
            transitionByKey.set(r.stateTransition.canonicalKey, r.stateTransition);
        }
    }
    const stillOpen = [];
    const closedByEvidence = [];
    const escalatedLoops = [];
    const snoozedLoops = [];
    for (const r of accepted) {
        const key = canonicalKeyForObservation(r.observation);
        const transition = transitionByKey.get(key);
        const title = r.openLoopTitle ?? r.observation.title;
        if (transition) {
            if (transition.toStatus === 'done')
                closedByEvidence.push(title);
            else if (transition.toStatus === 'escalated')
                escalatedLoops.push(title);
            else if (transition.toStatus === 'snoozed')
                snoozedLoops.push(title);
            else
                stillOpen.push(title);
        }
        else {
            stillOpen.push(title);
        }
    }
    const suppressed = results.filter(r => r.verdict === 'suppressed').length;
    const needsReview = results.filter(r => r.verdict === 'needs_review').length;
    const attachedContext = results.filter(r => r.verdict === 'attached_context').length;
    if (stillOpen.length > 0) {
        lines.push(`- ${stillOpen.length} loop${stillOpen.length > 1 ? 's' : ''} still open`);
        for (const t of stillOpen)
            lines.push(`  ${t}`);
    }
    if (closedByEvidence.length > 0) {
        lines.push(`- ${closedByEvidence.length} loop${closedByEvidence.length > 1 ? 's' : ''} closed by new evidence`);
        for (const t of closedByEvidence)
            lines.push(`  ${t}`);
    }
    if (escalatedLoops.length > 0) {
        lines.push(`- ${escalatedLoops.length} loop${escalatedLoops.length > 1 ? 's' : ''} escalated`);
        for (const t of escalatedLoops)
            lines.push(`  ${t}`);
    }
    if (snoozedLoops.length > 0) {
        lines.push(`- ${snoozedLoops.length} loop${snoozedLoops.length > 1 ? 's' : ''} snoozed`);
        for (const t of snoozedLoops)
            lines.push(`  ${t}`);
    }
    if (suppressed > 0) {
        lines.push(`- ${suppressed} observed signal${suppressed > 1 ? 's' : ''} suppressed as noise`);
    }
    if (attachedContext > 0) {
        lines.push(`- ${attachedContext} signal${attachedContext > 1 ? 's' : ''} attached as context`);
    }
    if (needsReview > 0) {
        lines.push(`- ${needsReview} signal${needsReview > 1 ? 's' : ''} need${needsReview === 1 ? 's' : ''} review`);
    }
    return lines;
}
function loadObservations(filePath) {
    const raw = fs.readFileSync(path.resolve(filePath), 'utf8');
    return JSON.parse(raw);
}
//# sourceMappingURL=openclawIntake.js.map