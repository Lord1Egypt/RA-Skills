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
exports.getOpenLoopStatesPath = getOpenLoopStatesPath;
exports.loadOpenLoopStates = loadOpenLoopStates;
exports.saveOpenLoopStates = saveOpenLoopStates;
exports.saveOpenLoopState = saveOpenLoopState;
exports.findOpenLoopStateById = findOpenLoopStateById;
exports.transitionOpenLoopState = transitionOpenLoopState;
exports.selectRelevantSignalsForProposal = selectRelevantSignalsForProposal;
exports.buildOpenLoopStateFromProposal = buildOpenLoopStateFromProposal;
const fs = __importStar(require("node:fs"));
const path = __importStar(require("node:path"));
const crypto = __importStar(require("node:crypto"));
const severityPolicy_1 = require("../policy/severityPolicy");
function getWorldLoopsDir() {
    return process.env.WORLDLOOPS_DIR ?? path.join(process.cwd(), '.worldloops');
}
function getOpenLoopStatesPath() {
    return path.join(getWorldLoopsDir(), 'open_loop_states.json');
}
function loadOpenLoopStates() {
    const statesPath = getOpenLoopStatesPath();
    if (!fs.existsSync(statesPath)) {
        return [];
    }
    return JSON.parse(fs.readFileSync(statesPath, 'utf8'));
}
function saveOpenLoopStates(states) {
    const statesPath = getOpenLoopStatesPath();
    const dir = path.dirname(statesPath);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(statesPath, JSON.stringify(states, null, 2) + '\n', 'utf8');
}
function saveOpenLoopState(state) {
    const existing = loadOpenLoopStates();
    const upserted = existing.filter((s) => s.id !== state.id);
    upserted.push(state);
    saveOpenLoopStates(upserted);
}
function findOpenLoopStateById(id) {
    return loadOpenLoopStates().find((state) => state.id === id) ?? null;
}
function transitionOpenLoopState(id, to, opts = {}) {
    const states = loadOpenLoopStates();
    const index = states.findIndex((state) => state.id === id);
    if (index === -1) {
        throw new Error(`Open loop not found: ${id}`);
    }
    const current = states[index];
    const now = new Date().toISOString();
    const updated = {
        ...current,
        status: to,
        updatedAt: now,
        history: [
            ...current.history,
            {
                at: now,
                from: current.status,
                to,
                actor: opts.actor ?? null,
                note: opts.note ?? null,
            },
        ],
        safety: {
            externalWrite: false,
        },
    };
    states[index] = updated;
    saveOpenLoopStates(states);
    return updated;
}
function selectRelevantSignalsForProposal(candidate, signals) {
    const sameSourceSignals = signals.filter((signal) => signal.source === candidate.source);
    if (sameSourceSignals.length > 0) {
        return sameSourceSignals;
    }
    if (signals.length > 0) {
        return [signals[0]];
    }
    return [];
}
function buildOpenLoopStateFromProposal(candidate, signals) {
    const now = new Date().toISOString();
    const adjudication = (0, severityPolicy_1.adjudicateSeverity)(candidate.severity);
    return {
        id: crypto.randomUUID(),
        canonicalKey: candidate.idempotencyKey,
        title: candidate.actionHint || candidate.reason || candidate.entityType,
        sourceSignals: selectRelevantSignalsForProposal(candidate, signals).map((signal) => ({
            source: signal.source,
            text: signal.text,
            url: signal.url,
            createdAt: signal.createdAt,
        })),
        status: adjudication.shouldEscalate ? 'escalated' : 'todo',
        severity: adjudication.severity,
        adjudication,
        owner: null,
        dueAt: null,
        lastObservedAt: now,
        updatedAt: now,
        history: [
            {
                at: now,
                from: null,
                to: adjudication.shouldEscalate ? 'escalated' : 'todo',
                actor: 'worldloops.local',
                note: `Created from proposal candidate; adjudication=${adjudication.action}`,
            },
        ],
        safety: {
            externalWrite: false,
        },
    };
}
//# sourceMappingURL=openLoopStates.js.map