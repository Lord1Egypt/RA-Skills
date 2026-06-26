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
exports.getTransitionReceiptsPath = getTransitionReceiptsPath;
exports.loadTransitionReceipts = loadTransitionReceipts;
exports.saveTransitionReceipt = saveTransitionReceipt;
exports.saveTransitionReceipts = saveTransitionReceipts;
exports.buildTransitionReceipt = buildTransitionReceipt;
const fs = __importStar(require("node:fs"));
const path = __importStar(require("node:path"));
const crypto = __importStar(require("node:crypto"));
function getWorldLoopsDir() {
    return process.env.WORLDLOOPS_DIR ?? path.join(process.cwd(), '.worldloops');
}
function getTransitionReceiptsPath() {
    return path.join(getWorldLoopsDir(), 'transition_receipts.json');
}
function loadTransitionReceipts() {
    const receiptsPath = getTransitionReceiptsPath();
    if (!fs.existsSync(receiptsPath)) {
        return [];
    }
    return JSON.parse(fs.readFileSync(receiptsPath, 'utf8'));
}
function saveTransitionReceipt(receipt) {
    const receiptsPath = getTransitionReceiptsPath();
    const dir = path.dirname(receiptsPath);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    const existing = loadTransitionReceipts();
    const upserted = existing.filter((r) => r.id !== receipt.id);
    upserted.push(receipt);
    fs.writeFileSync(receiptsPath, JSON.stringify(upserted, null, 2) + '\n', 'utf8');
}
function saveTransitionReceipts(receipts) {
    const receiptsPath = getTransitionReceiptsPath();
    const dir = path.dirname(receiptsPath);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(receiptsPath, JSON.stringify(receipts, null, 2) + '\n', 'utf8');
}
function buildTransitionReceipt(candidate, signals, opts) {
    return {
        id: `${candidate.idempotencyKey}-${crypto.randomUUID()}`,
        createdAt: new Date().toISOString(),
        proposalId: opts.proposalId !== undefined ? opts.proposalId : candidate.idempotencyKey,
        sourceSignalsObserved: signals.map((s) => `[${s.source}] ${s.text}`),
        normalizedResponsibility: candidate.entityType,
        proposedTransition: {
            currentState: candidate.currentState,
            proposedState: candidate.proposedState,
        },
        reason: candidate.reason,
        adjudicationResult: opts.adjudicationResult,
        boundaryCrossed: opts.boundaryCrossed,
        externalWrite: false,
        actor: null,
        decision: opts.decision,
        unresolvedState: null,
        redactions: {
            applied: false,
            fields: [],
        },
    };
}
//# sourceMappingURL=transitionReceipts.js.map