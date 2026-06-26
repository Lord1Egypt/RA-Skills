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
exports.repairWorldState = repairWorldState;
exports.loadRepairReceipts = loadRepairReceipts;
const fs = __importStar(require("node:fs"));
const path = __importStar(require("node:path"));
const crypto = __importStar(require("node:crypto"));
function resolveDir(options) {
    return (options?.worldloopsDir ?? process.env.WORLDLOOPS_DIR ?? path.join(process.cwd(), '.worldloops'));
}
function generateId() {
    return `repair-${Date.now()}-${crypto.randomBytes(4).toString('hex')}`;
}
function tryReadJsonArray(filePath) {
    if (!fs.existsSync(filePath))
        return { data: null };
    let raw;
    try {
        raw = fs.readFileSync(filePath, 'utf8');
    }
    catch {
        return { data: null, error: 'read_error' };
    }
    let parsed;
    try {
        parsed = JSON.parse(raw);
    }
    catch {
        return { data: null, error: 'malformed_json' };
    }
    if (!Array.isArray(parsed)) {
        return { data: null, error: 'invalid_shape' };
    }
    return { data: parsed };
}
function idSet(data) {
    const s = new Set();
    if (!data)
        return s;
    for (const item of data) {
        if (typeof item === 'object' && item !== null) {
            const id = item['id'];
            if (typeof id === 'string')
                s.add(id);
        }
    }
    return s;
}
const VALID_BOUNDARY = new Set(['read_only', 'local_commit', 'external_write']);
function detectFileIssues(filePath, result, repairs) {
    if (!fs.existsSync(filePath))
        return;
    if (result.error === 'malformed_json') {
        repairs.push({
            code: 'MALFORMED_JSON',
            status: 'non_repairable',
            file: filePath,
            message: 'File contains malformed JSON. Manual repair required.',
        });
        return;
    }
    if (result.error === 'invalid_shape') {
        repairs.push({
            code: 'INVALID_FILE_SHAPE',
            status: 'non_repairable',
            file: filePath,
            message: 'File has invalid shape (expected JSON array). Manual repair required.',
        });
        return;
    }
    if (!result.data)
        return;
    for (const item of result.data) {
        if (typeof item !== 'object' || item === null)
            continue;
        const obj = item;
        const itemId = typeof obj['id'] === 'string' ? obj['id'] : undefined;
        if ('externalWrite' in obj && obj['externalWrite'] !== false) {
            repairs.push({
                code: 'EXTERNAL_WRITE_VIOLATION',
                status: 'non_repairable',
                file: filePath,
                referenceId: itemId,
                message: `Item "${itemId ?? 'unknown'}" has externalWrite: ${JSON.stringify(obj['externalWrite'])}. Cannot repair automatically.`,
            });
        }
        if ('boundaryCrossed' in obj && !VALID_BOUNDARY.has(String(obj['boundaryCrossed']))) {
            repairs.push({
                code: 'INVALID_BOUNDARY_CROSSED',
                status: 'non_repairable',
                file: filePath,
                referenceId: itemId,
                message: `Item "${itemId ?? 'unknown'}" has invalid boundaryCrossed value. Cannot repair automatically.`,
            });
        }
    }
}
function planAction(code, file, referenceId, message, alreadyMarked, mode) {
    if (alreadyMarked) {
        return { code, status: 'skipped', file, referenceId, message: message + ' (already marked, skipped)' };
    }
    return { code, status: mode === 'apply' ? 'applied' : 'planned', file, referenceId, message };
}
function buildSummary(repairs) {
    const nonRepairable = repairs.filter((r) => r.status === 'non_repairable');
    const repairable = repairs.filter((r) => r.status !== 'non_repairable');
    const planned = repairs.filter((r) => r.status === 'planned');
    const applied = repairs.filter((r) => r.status === 'applied');
    return {
        issuesObserved: repairs.length,
        repairableIssues: repairable.length,
        nonRepairableIssues: nonRepairable.length,
        repairsPlanned: planned.length,
        repairsApplied: applied.length,
    };
}
function writeJson(filePath, data) {
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2) + '\n', 'utf8');
}
function repairWorldState(options) {
    const dir = resolveDir(options);
    const mode = options?.apply ? 'apply' : 'dry_run';
    const receiptId = generateId();
    const createdAt = new Date().toISOString();
    const fp = (name) => path.join(dir, name);
    const proposalsPath = fp('proposals.json');
    const plansPath = fp('execution_plans.json');
    const contractsPath = fp('execution_contracts.json');
    const transReceiptsPath = fp('transition_receipts.json');
    const decReceiptsPath = fp('proposal_decision_receipts.json');
    const repairReceiptsPath = fp('repair_receipts.json');
    const proposalsResult = tryReadJsonArray(proposalsPath);
    const plansResult = tryReadJsonArray(plansPath);
    const contractsResult = tryReadJsonArray(contractsPath);
    const transReceiptsResult = tryReadJsonArray(transReceiptsPath);
    const decReceiptsResult = tryReadJsonArray(decReceiptsPath);
    const repairs = [];
    // ── detect non-repairable issues in each file ────────────────────────────────
    detectFileIssues(proposalsPath, proposalsResult, repairs);
    detectFileIssues(plansPath, plansResult, repairs);
    detectFileIssues(contractsPath, contractsResult, repairs);
    detectFileIssues(transReceiptsPath, transReceiptsResult, repairs);
    detectFileIssues(decReceiptsPath, decReceiptsResult, repairs);
    const proposalIds = idSet(proposalsResult.data);
    const planIds = idSet(plansResult.data);
    // ── duplicate idempotencyKey in proposals ────────────────────────────────────
    if (proposalsResult.data) {
        const seen = new Map();
        for (const item of proposalsResult.data) {
            if (typeof item !== 'object' || item === null)
                continue;
            const key = item['idempotencyKey'];
            if (typeof key === 'string' && key !== '') {
                seen.set(key, (seen.get(key) ?? 0) + 1);
            }
        }
        for (const [key, count] of seen) {
            if (count > 1) {
                repairs.push({
                    code: 'FLAG_DUPLICATE_IDEMPOTENCY_KEY',
                    status: mode === 'apply' ? 'applied' : 'planned',
                    file: proposalsPath,
                    referenceId: key,
                    message: `Duplicate idempotencyKey "${key}" found ${count} times. Flagged in repair receipt (no deletion performed).`,
                });
            }
        }
    }
    // ── plans with unresolved proposal references ────────────────────────────────
    if (plansResult.data && fs.existsSync(proposalsPath)) {
        for (const item of plansResult.data) {
            if (typeof item !== 'object' || item === null)
                continue;
            const obj = item;
            const pid = obj['proposalId'];
            if (typeof pid !== 'string' || pid === '' || proposalIds.has(pid))
                continue;
            const planId = typeof obj['id'] === 'string' ? obj['id'] : undefined;
            const alreadyMarked = typeof obj['_worldloopsRepair'] === 'object' && obj['_worldloopsRepair'] !== null;
            repairs.push(planAction('MARK_PLAN_UNRESOLVED_PROPOSAL', plansPath, planId, `Plan "${planId ?? 'unknown'}" references missing proposal "${pid}". Marked with local metadata.`, alreadyMarked, mode));
        }
    }
    // ── contracts with unresolved plan references ────────────────────────────────
    if (contractsResult.data && fs.existsSync(plansPath)) {
        for (const item of contractsResult.data) {
            if (typeof item !== 'object' || item === null)
                continue;
            const obj = item;
            const pid = obj['planId'];
            if (typeof pid !== 'string' || pid === '' || planIds.has(pid))
                continue;
            const contractId = typeof obj['id'] === 'string' ? obj['id'] : undefined;
            const alreadyMarked = typeof obj['_worldloopsRepair'] === 'object' && obj['_worldloopsRepair'] !== null;
            repairs.push(planAction('MARK_CONTRACT_UNRESOLVED_PLAN', contractsPath, contractId, `Contract "${contractId ?? 'unknown'}" references missing plan "${pid}". Marked with local metadata.`, alreadyMarked, mode));
        }
    }
    // ── orphaned transition receipts ─────────────────────────────────────────────
    if (transReceiptsResult.data && fs.existsSync(proposalsPath)) {
        for (const item of transReceiptsResult.data) {
            if (typeof item !== 'object' || item === null)
                continue;
            const obj = item;
            const pid = obj['proposalId'];
            if (typeof pid !== 'string' || pid === '' || proposalIds.has(pid))
                continue;
            const receiptEntryId = typeof obj['id'] === 'string' ? obj['id'] : undefined;
            const alreadyMarked = typeof obj['_worldloopsRepair'] === 'object' && obj['_worldloopsRepair'] !== null;
            repairs.push(planAction('MARK_ORPHAN_RECEIPT', transReceiptsPath, receiptEntryId, `Transition receipt "${receiptEntryId ?? 'unknown'}" references missing proposal "${pid}". Marked as orphan.`, alreadyMarked, mode));
        }
    }
    // ── orphaned decision receipts ───────────────────────────────────────────────
    if (decReceiptsResult.data && fs.existsSync(proposalsPath)) {
        for (const item of decReceiptsResult.data) {
            if (typeof item !== 'object' || item === null)
                continue;
            const obj = item;
            const pid = obj['proposalId'];
            if (typeof pid !== 'string' || pid === '' || proposalIds.has(pid))
                continue;
            const receiptEntryId = typeof obj['id'] === 'string' ? obj['id'] : undefined;
            const alreadyMarked = typeof obj['_worldloopsRepair'] === 'object' && obj['_worldloopsRepair'] !== null;
            repairs.push(planAction('MARK_ORPHAN_RECEIPT', decReceiptsPath, receiptEntryId, `Decision receipt "${receiptEntryId ?? 'unknown'}" references missing proposal "${pid}". Marked as orphan.`, alreadyMarked, mode));
        }
    }
    // ── apply repairs ─────────────────────────────────────────────────────────────
    if (mode === 'apply') {
        const repairMeta = { repairReceiptId: receiptId, repairedAt: createdAt };
        if (plansResult.data) {
            let modified = false;
            const updated = plansResult.data.map((item) => {
                if (typeof item !== 'object' || item === null)
                    return item;
                const obj = item;
                const pid = obj['proposalId'];
                if (typeof pid === 'string' &&
                    pid !== '' &&
                    !proposalIds.has(pid) &&
                    !(typeof obj['_worldloopsRepair'] === 'object' && obj['_worldloopsRepair'] !== null)) {
                    modified = true;
                    return { ...obj, _worldloopsRepair: { status: 'unresolved_proposal', missingProposalId: pid, ...repairMeta } };
                }
                return obj;
            });
            if (modified)
                writeJson(plansPath, updated);
        }
        if (contractsResult.data) {
            let modified = false;
            const updated = contractsResult.data.map((item) => {
                if (typeof item !== 'object' || item === null)
                    return item;
                const obj = item;
                const pid = obj['planId'];
                if (typeof pid === 'string' &&
                    pid !== '' &&
                    !planIds.has(pid) &&
                    !(typeof obj['_worldloopsRepair'] === 'object' && obj['_worldloopsRepair'] !== null)) {
                    modified = true;
                    return { ...obj, _worldloopsRepair: { status: 'unresolved_plan', missingPlanId: pid, ...repairMeta } };
                }
                return obj;
            });
            if (modified)
                writeJson(contractsPath, updated);
        }
        if (transReceiptsResult.data) {
            let modified = false;
            const updated = transReceiptsResult.data.map((item) => {
                if (typeof item !== 'object' || item === null)
                    return item;
                const obj = item;
                const pid = obj['proposalId'];
                if (typeof pid === 'string' &&
                    pid !== '' &&
                    !proposalIds.has(pid) &&
                    !(typeof obj['_worldloopsRepair'] === 'object' && obj['_worldloopsRepair'] !== null)) {
                    modified = true;
                    return { ...obj, _worldloopsRepair: { status: 'orphan', missingProposalId: pid, ...repairMeta } };
                }
                return obj;
            });
            if (modified)
                writeJson(transReceiptsPath, updated);
        }
        if (decReceiptsResult.data) {
            let modified = false;
            const updated = decReceiptsResult.data.map((item) => {
                if (typeof item !== 'object' || item === null)
                    return item;
                const obj = item;
                const pid = obj['proposalId'];
                if (typeof pid === 'string' &&
                    pid !== '' &&
                    !proposalIds.has(pid) &&
                    !(typeof obj['_worldloopsRepair'] === 'object' && obj['_worldloopsRepair'] !== null)) {
                    modified = true;
                    return { ...obj, _worldloopsRepair: { status: 'orphan', missingProposalId: pid, ...repairMeta } };
                }
                return obj;
            });
            if (modified)
                writeJson(decReceiptsPath, updated);
        }
        // write repair receipt
        let existingReceipts = [];
        if (fs.existsSync(repairReceiptsPath)) {
            try {
                const raw = fs.readFileSync(repairReceiptsPath, 'utf8');
                const parsed = JSON.parse(raw);
                if (Array.isArray(parsed))
                    existingReceipts = parsed;
            }
            catch {
                // start fresh if unreadable
            }
        }
        existingReceipts.push({
            id: receiptId,
            createdAt,
            mode,
            externalWrite: false,
            summary: buildSummary(repairs),
            repairs: repairs.map((r) => ({ ...r })),
        });
        fs.mkdirSync(dir, { recursive: true });
        writeJson(repairReceiptsPath, existingReceipts);
    }
    const summary = buildSummary(repairs);
    return {
        ok: summary.nonRepairableIssues === 0,
        mode,
        summary,
        repairs,
        receipt: {
            id: receiptId,
            createdAt,
            externalWrite: false,
        },
        safety: { externalWrite: false },
    };
}
function loadRepairReceipts(options) {
    const dir = options?.worldloopsDir ??
        process.env.WORLDLOOPS_DIR ??
        path.join(process.cwd(), '.worldloops');
    const filePath = path.join(dir, 'repair_receipts.json');
    if (!fs.existsSync(filePath))
        return [];
    try {
        const raw = fs.readFileSync(filePath, 'utf8');
        const parsed = JSON.parse(raw);
        return Array.isArray(parsed) ? parsed : [];
    }
    catch {
        return [];
    }
}
//# sourceMappingURL=repairWorldState.js.map