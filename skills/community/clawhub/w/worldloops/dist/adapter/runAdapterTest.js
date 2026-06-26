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
exports.runAdapterTest = runAdapterTest;
const fs = __importStar(require("node:fs"));
const os = __importStar(require("node:os"));
const path = __importStar(require("node:path"));
const crypto = __importStar(require("node:crypto"));
const validateAdapterSignal_1 = require("./validateAdapterSignal");
const toWorldLoopsSignal_1 = require("./toWorldLoopsSignal");
const openLoopStates_1 = require("../storage/openLoopStates");
const proposals_1 = require("../storage/proposals");
const transitionReceipts_1 = require("../storage/transitionReceipts");
function buildLocalProposalCandidate(signal) {
    const hash = crypto
        .createHash('sha1')
        .update(`${signal.source}|${signal.sourceType}|${signal.text}`)
        .digest('hex')
        .slice(0, 12);
    const idempotencyKey = `adapter-test-${signal.source}-${signal.sourceType}-${hash}`;
    const worldSignal = (0, toWorldLoopsSignal_1.toWorldLoopsSignal)(signal);
    return {
        idempotencyKey,
        entityType: signal.sourceType,
        source: worldSignal.source,
        currentState: 'observed',
        proposedState: 'reviewed',
        reason: signal.summary ?? signal.text.slice(0, 120),
        approvalRequired: true,
        actionHint: `Review ${signal.source} ${signal.sourceType}`,
        severity: 'medium',
    };
}
function runLocalReconcile(signal) {
    const worldSignal = (0, toWorldLoopsSignal_1.toWorldLoopsSignal)(signal);
    const candidate = buildLocalProposalCandidate(signal);
    // Resolve or create proposal first so the receipt references the local UUID.
    let proposalLocalId;
    let proposalNew = false;
    const existingProposal = (0, proposals_1.findProposalByIdempotencyKey)(candidate.idempotencyKey);
    if (existingProposal) {
        proposalLocalId = existingProposal.id;
    }
    else {
        const proposal = (0, proposals_1.buildProposalFromCandidate)(candidate);
        (0, proposals_1.saveProposal)(proposal);
        proposalLocalId = proposal.id;
        proposalNew = true;
    }
    const receipt = (0, transitionReceipts_1.buildTransitionReceipt)(candidate, [worldSignal], {
        proposalId: proposalLocalId,
        adjudicationResult: 'proposed',
        decision: 'surfaced_for_review',
        boundaryCrossed: 'local_commit',
    });
    (0, transitionReceipts_1.saveTransitionReceipt)(receipt);
    const existingLoops = (0, openLoopStates_1.loadOpenLoopStates)();
    const existingKeys = new Set(existingLoops.map((l) => l.canonicalKey));
    let openLoopNew = false;
    if (!existingKeys.has(candidate.idempotencyKey)) {
        (0, openLoopStates_1.saveOpenLoopState)((0, openLoopStates_1.buildOpenLoopStateFromProposal)(candidate, [worldSignal]));
        openLoopNew = true;
    }
    return { openLoopNew, proposalNew };
}
function _runAdapterTestCore(filePath) {
    const result = {
        file: filePath,
        validate: 'failed',
        reconcile: 'failed',
        openLoopPersisted: false,
        proposalPersisted: false,
        idempotency: 'failed',
        externalWrite: false,
        reconcileMode: 'local_heuristic',
    };
    let raw;
    try {
        raw = JSON.parse(fs.readFileSync(path.resolve(filePath), 'utf8'));
    }
    catch (err) {
        result.reconcileError = err instanceof Error ? err.message : String(err);
        return result;
    }
    const validation = (0, validateAdapterSignal_1.validateAdapterSignal)(raw);
    if (!validation.ok) {
        result.validateErrors = validation.errors;
        return result;
    }
    result.validate = 'passed';
    const signal = validation.signal;
    try {
        const first = runLocalReconcile(signal);
        result.openLoopPersisted = first.openLoopNew;
        result.proposalPersisted = first.proposalNew;
    }
    catch (err) {
        result.reconcileError = err instanceof Error ? err.message : String(err);
        return result;
    }
    if (!result.openLoopPersisted) {
        result.reconcileError = 'No open loop was persisted during reconciliation';
        return result;
    }
    if (!result.proposalPersisted) {
        result.reconcileError = 'No proposal was persisted during reconciliation';
        return result;
    }
    result.reconcile = 'passed';
    try {
        const second = runLocalReconcile(signal);
        result.idempotency = !second.openLoopNew && !second.proposalNew ? 'passed' : 'failed';
    }
    catch {
        result.idempotency = 'failed';
    }
    return result;
}
function runAdapterTest(filePath, opts = {}) {
    const ownedDir = !opts.worldloopsDir;
    const testDir = opts.worldloopsDir
        ?? fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-adapter-test-'));
    const prevDir = process.env.WORLDLOOPS_DIR;
    process.env.WORLDLOOPS_DIR = testDir;
    try {
        return _runAdapterTestCore(filePath);
    }
    finally {
        if (prevDir !== undefined) {
            process.env.WORLDLOOPS_DIR = prevDir;
        }
        else {
            delete process.env.WORLDLOOPS_DIR;
        }
        if (ownedDir) {
            try {
                fs.rmSync(testDir, { recursive: true, force: true });
            }
            catch {
                // best-effort cleanup
            }
        }
    }
}
//# sourceMappingURL=runAdapterTest.js.map