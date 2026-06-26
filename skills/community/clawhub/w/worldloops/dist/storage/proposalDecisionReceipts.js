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
exports.getProposalDecisionReceiptsPath = getProposalDecisionReceiptsPath;
exports.loadProposalDecisionReceipts = loadProposalDecisionReceipts;
exports.saveProposalDecisionReceipt = saveProposalDecisionReceipt;
exports.listProposalDecisionReceipts = listProposalDecisionReceipts;
exports.findProposalDecisionReceiptById = findProposalDecisionReceiptById;
const fs = __importStar(require("node:fs"));
const path = __importStar(require("node:path"));
function getWorldLoopsDir() {
    return process.env.WORLDLOOPS_DIR ?? path.join(process.cwd(), '.worldloops');
}
function getProposalDecisionReceiptsPath() {
    return path.join(getWorldLoopsDir(), 'proposal_decision_receipts.json');
}
function loadProposalDecisionReceipts() {
    const receiptsPath = getProposalDecisionReceiptsPath();
    if (!fs.existsSync(receiptsPath)) {
        return [];
    }
    return JSON.parse(fs.readFileSync(receiptsPath, 'utf8'));
}
function saveProposalDecisionReceipt(receipt) {
    const receiptsPath = getProposalDecisionReceiptsPath();
    const dir = path.dirname(receiptsPath);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    const existing = loadProposalDecisionReceipts();
    const upserted = existing.filter((r) => r.id !== receipt.id);
    upserted.push(receipt);
    fs.writeFileSync(receiptsPath, JSON.stringify(upserted, null, 2) + '\n', 'utf8');
}
function listProposalDecisionReceipts() {
    return loadProposalDecisionReceipts();
}
function findProposalDecisionReceiptById(id) {
    return loadProposalDecisionReceipts().find((r) => r.id === id) ?? null;
}
//# sourceMappingURL=proposalDecisionReceipts.js.map