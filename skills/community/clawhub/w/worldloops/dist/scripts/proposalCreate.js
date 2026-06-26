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
const crypto = __importStar(require("node:crypto"));
const proposalTemplates_1 = require("../data/proposalTemplates");
const proposals_1 = require("../storage/proposals");
function printJson(value) {
    console.log(JSON.stringify(value, null, 2));
}
function main() {
    const args = process.argv.slice(2);
    const jsonMode = args.includes('--json');
    const templateId = args.find((a) => !a.startsWith('--'));
    if (!templateId) {
        printJson({
            ok: false,
            error: {
                code: 'MISSING_TEMPLATE_ID',
                message: 'Usage: npm run proposal:create -- <template-id> [--json]',
                availableTemplateIds: proposalTemplates_1.PROPOSAL_TEMPLATES.map((t) => t.id),
            },
            safety: { externalWrite: false },
        });
        process.exit(1);
    }
    const template = proposalTemplates_1.PROPOSAL_TEMPLATES.find((t) => t.id === templateId);
    if (!template) {
        printJson({
            ok: false,
            error: {
                code: 'PROPOSAL_TEMPLATE_NOT_FOUND',
                message: `Proposal template not found: ${templateId}`,
                availableTemplateIds: proposalTemplates_1.PROPOSAL_TEMPLATES.map((t) => t.id),
            },
            safety: { externalWrite: false },
        });
        process.exit(1);
    }
    const now = new Date().toISOString();
    const proposal = {
        id: crypto.randomUUID(),
        templateId: template.id,
        title: template.title,
        intent: template.description,
        category: template.category,
        riskLevel: template.riskLevel,
        requiredReview: true,
        externalWrite: false,
        checks: template.suggestedChecks,
        status: 'proposed',
        createdAt: now,
        updatedAt: now,
        source: 'worldloops.local',
    };
    (0, proposals_1.saveProposal)(proposal);
    if (jsonMode) {
        printJson({
            ok: true,
            source: 'worldloops.local',
            path: (0, proposals_1.getProposalsPath)(),
            proposal,
            safety: { externalWrite: false },
        });
    }
    else {
        console.log(`Proposal created: ${proposal.id}`);
        console.log(`  Template:       ${proposal.templateId}`);
        console.log(`  Title:          ${proposal.title}`);
        console.log(`  Status:         ${proposal.status}`);
        console.log(`  Risk level:     ${proposal.riskLevel}`);
        console.log(`  Category:       ${proposal.category}`);
        console.log(`  requiredReview: true`);
        console.log(`  externalWrite:  false`);
        console.log(`  Created at:     ${proposal.createdAt}`);
        console.log(`  Stored at:      ${(0, proposals_1.getProposalsPath)()}`);
        console.log('');
        console.log('externalWrite: false');
    }
}
main();
//# sourceMappingURL=proposalCreate.js.map