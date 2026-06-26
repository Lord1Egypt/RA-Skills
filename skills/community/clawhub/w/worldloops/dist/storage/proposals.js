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
exports.getProposalsPath = getProposalsPath;
exports.loadProposals = loadProposals;
exports.saveProposal = saveProposal;
exports.findProposalById = findProposalById;
exports.listProposals = listProposals;
exports.findProposalByIdempotencyKey = findProposalByIdempotencyKey;
exports.buildProposalFromCandidate = buildProposalFromCandidate;
const fs = __importStar(require("node:fs"));
const path = __importStar(require("node:path"));
const crypto = __importStar(require("node:crypto"));
const proposalTemplates_1 = require("../data/proposalTemplates");
function getWorldLoopsDir() {
    return process.env.WORLDLOOPS_DIR ?? path.join(process.cwd(), '.worldloops');
}
function getProposalsPath() {
    return path.join(getWorldLoopsDir(), 'proposals.json');
}
function loadProposals() {
    const proposalsPath = getProposalsPath();
    if (!fs.existsSync(proposalsPath)) {
        return [];
    }
    return JSON.parse(fs.readFileSync(proposalsPath, 'utf8'));
}
function saveProposal(proposal) {
    const proposalsPath = getProposalsPath();
    const dir = path.dirname(proposalsPath);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    const existing = loadProposals();
    const upserted = existing.filter((p) => p.id !== proposal.id);
    upserted.push(proposal);
    fs.writeFileSync(proposalsPath, JSON.stringify(upserted, null, 2) + '\n', 'utf8');
}
function findProposalById(id) {
    return loadProposals().find((p) => p.id === id) ?? null;
}
function listProposals() {
    return loadProposals();
}
function findProposalByIdempotencyKey(key) {
    return loadProposals().find((p) => p.idempotencyKey === key) ?? null;
}
function candidateToTemplateId(candidate) {
    if (candidate.severity === 'critical' || candidate.severity === 'high')
        return 'escalation';
    return 'state-transition';
}
function buildProposalFromCandidate(candidate) {
    const templateId = candidateToTemplateId(candidate);
    const template = proposalTemplates_1.PROPOSAL_TEMPLATES.find((t) => t.id === templateId);
    const now = new Date().toISOString();
    return {
        id: crypto.randomUUID(),
        templateId: template.id,
        title: candidate.actionHint || candidate.reason || candidate.entityType,
        intent: candidate.reason,
        category: template.category,
        riskLevel: template.riskLevel,
        requiredReview: true,
        externalWrite: false,
        checks: template.suggestedChecks,
        status: 'proposed',
        createdAt: now,
        updatedAt: now,
        source: 'worldloops.local',
        idempotencyKey: candidate.idempotencyKey,
    };
}
//# sourceMappingURL=proposals.js.map