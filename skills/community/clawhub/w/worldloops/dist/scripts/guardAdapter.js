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
const fs = __importStar(require("node:fs"));
const path = __importStar(require("node:path"));
const brief_1 = require("../brief");
const validateAdapterSignal_1 = require("../adapter/validateAdapterSignal");
const toWorldLoopsSignal_1 = require("../adapter/toWorldLoopsSignal");
const transitionReceipts_1 = require("../storage/transitionReceipts");
const openLoopStates_1 = require("../storage/openLoopStates");
const proposals_1 = require("../storage/proposals");
const messengerFormat_1 = require("../output/messengerFormat");
const gogGmail_1 = require("../adapters/gogGmail");
const gogCalendar_1 = require("../adapters/gogCalendar");
const slackPayload_1 = require("../adapters/slackPayload");
const SUPPORTED_SOURCES = ['gmail', 'calendar', 'slack', 'github', 'generic'];
function getFlagValue(flag) {
    const args = process.argv.slice(2);
    const idx = args.indexOf(flag);
    if (idx === -1 || idx + 1 >= args.length)
        return undefined;
    return args[idx + 1];
}
function hasFlag(flag) {
    return process.argv.slice(2).includes(flag);
}
function resolveFormat() {
    if (hasFlag('--compact'))
        return 'compact';
    return getFlagValue('--format') ?? 'messenger';
}
function printError(lines, outputFormat) {
    if (outputFormat === 'compact') {
        console.log('🦞 Agent Execution Guard');
        console.log('');
        for (const line of lines)
            console.log(line);
        console.log('');
        console.log('✅ Safe');
        console.log('externalWrite:false');
        console.log('No email, draft, call, or external change made.');
    }
    else {
        console.log('');
        console.log('🦞 WorldLoops Guard');
        console.log('');
        for (const line of lines)
            console.log(line);
        console.log('');
        console.log('✅ Safe');
        console.log('externalWrite: false');
        console.log('No external system changed.');
        console.log('');
    }
}
async function main() {
    const inputPath = getFlagValue('--input');
    const source = getFlagValue('--source');
    const outputFormat = resolveFormat();
    if (!inputPath) {
        printError(['❌ No input provided.', 'Usage: npm run guard:adapter -- --source gmail --input <payload.json>'], outputFormat);
        process.exit(1);
    }
    if (source && !SUPPORTED_SOURCES.includes(source)) {
        printError([`❌ Unknown source: "${source}".`, `Supported: ${SUPPORTED_SOURCES.join(', ')}`], outputFormat);
        process.exit(1);
    }
    let raw;
    try {
        raw = JSON.parse(fs.readFileSync(path.resolve(inputPath), 'utf8'));
    }
    catch (e) {
        printError([`❌ Could not read input file: ${inputPath}`], outputFormat);
        process.exit(1);
    }
    // Source-specific normalization for gog and host tool payloads before AdapterSignal validation
    if (source && typeof raw === 'object' && raw !== null && !Array.isArray(raw)) {
        if (source === 'gmail' && (0, gogGmail_1.isGogGmailPayload)(raw)) {
            raw = (0, gogGmail_1.gogGmailToAdapterSignal)(raw);
        }
        else if (source === 'calendar' && (0, gogCalendar_1.isGogCalendarPayload)(raw)) {
            raw = (0, gogCalendar_1.gogCalendarToAdapterSignal)(raw);
        }
        else if (source === 'slack' && (0, slackPayload_1.isSlackHostPayload)(raw)) {
            raw = (0, slackPayload_1.slackPayloadToAdapterSignal)(raw);
        }
        else {
            // Simple field injection for AdapterSignal-like partial payloads
            const obj = raw;
            if (!obj.source)
                obj.source = source;
            if (!obj.sourceType)
                obj.sourceType = 'message';
            if (obj.externalWrite === undefined)
                obj.externalWrite = false;
            if (!obj.observedAt)
                obj.observedAt = new Date().toISOString();
        }
    }
    const validation = (0, validateAdapterSignal_1.validateAdapterSignal)(raw);
    if (!validation.ok) {
        printError(['❌ Invalid adapter signal.', ...validation.errors], outputFormat);
        process.exit(1);
    }
    const signal = (0, toWorldLoopsSignal_1.toWorldLoopsSignal)(validation.signal);
    const signals = [signal];
    const result = await (0, brief_1.callWorldLoopsBrief)({ signals, mode: 'reconciliation' });
    const candidates = result.proposalCandidates ?? [];
    let receiptsGenerated = 0;
    let proposalsPersisted = 0;
    let proposalsAlreadyTracked = 0;
    if (result.ok && candidates.length > 0) {
        const existingOpenLoops = (0, openLoopStates_1.loadOpenLoopStates)();
        const existingCanonicalKeys = new Set(existingOpenLoops.map((loop) => loop.canonicalKey));
        for (const candidate of candidates) {
            let proposalLocalId;
            const existingProposal = (0, proposals_1.findProposalByIdempotencyKey)(candidate.idempotencyKey);
            if (existingProposal) {
                proposalsAlreadyTracked++;
                proposalLocalId = existingProposal.id;
            }
            else {
                const proposal = (0, proposals_1.buildProposalFromCandidate)(candidate);
                (0, proposals_1.saveProposal)(proposal);
                proposalsPersisted++;
                proposalLocalId = proposal.id;
            }
            const receipt = (0, transitionReceipts_1.buildTransitionReceipt)(candidate, signals, {
                proposalId: proposalLocalId,
                adjudicationResult: result.ok ? 'proposed' : 'api_error',
                decision: result.ok ? 'surfaced_for_review' : null,
                boundaryCrossed: 'local_commit',
            });
            (0, transitionReceipts_1.saveTransitionReceipt)(receipt);
            receiptsGenerated++;
            if (!existingCanonicalKeys.has(candidate.idempotencyKey)) {
                const openLoopState = (0, openLoopStates_1.buildOpenLoopStateFromProposal)(candidate, signals);
                (0, openLoopStates_1.saveOpenLoopState)(openLoopState);
                existingCanonicalKeys.add(candidate.idempotencyKey);
            }
        }
    }
    if (outputFormat === 'compact') {
        (0, messengerFormat_1.printCompactOutput)({ ok: result.ok, candidates });
    }
    else {
        (0, messengerFormat_1.printMessengerOutput)({
            ok: result.ok,
            candidates,
            openLoopCount: result.openLoops?.length ?? candidates.length,
            receiptsGenerated,
            proposalsPersisted,
            proposalsAlreadyTracked,
        });
    }
}
main().catch((err) => {
    const outputFormat = resolveFormat();
    if (outputFormat === 'compact') {
        console.log('🦞 Agent Execution Guard');
        console.log('');
        console.log('❌ Guard failed');
        console.log(err instanceof Error ? err.message : String(err));
        console.log('');
        console.log('✅ Safe');
        console.log('externalWrite:false');
        console.log('No email, draft, call, or external change made.');
    }
    else {
        console.log('');
        console.log('🦞 WorldLoops Guard');
        console.log('');
        console.log('❌ Guard failed');
        console.log(err instanceof Error ? err.message : String(err));
        console.log('');
        console.log('✅ Safe');
        console.log('externalWrite: false');
        console.log('No external system changed.');
        console.log('');
    }
    process.exit(1);
});
//# sourceMappingURL=guardAdapter.js.map