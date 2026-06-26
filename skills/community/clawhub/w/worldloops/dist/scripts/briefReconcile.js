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
const openclawGmail_1 = require("../adapters/openclawGmail");
const openclawCalendar_1 = require("../adapters/openclawCalendar");
const gogSnapshot_1 = require("../adapters/gogSnapshot");
const openclawMessages_1 = require("../adapters/openclawMessages");
const validateAdapterSignal_1 = require("../adapter/validateAdapterSignal");
const toWorldLoopsSignal_1 = require("../adapter/toWorldLoopsSignal");
const transitionReceipts_1 = require("../storage/transitionReceipts");
const openLoopStates_1 = require("../storage/openLoopStates");
const proposals_1 = require("../storage/proposals");
const capabilityBoundary_1 = require("../policy/capabilityBoundary");
const messengerFormat_1 = require("../output/messengerFormat");
function getFlagValue(flag) {
    const args = process.argv.slice(2);
    const idx = args.indexOf(flag);
    if (idx === -1 || idx + 1 >= args.length)
        return undefined;
    return args[idx + 1];
}
function printJson(value) {
    console.log(JSON.stringify(value, null, 2));
}
function loadJson(filePath) {
    const resolved = path.resolve(filePath);
    return JSON.parse(fs.readFileSync(resolved, 'utf8'));
}
async function main() {
    const outputFormat = getFlagValue('--format') ?? 'json';
    const gmailEventInput = getFlagValue('--gmail-event');
    const calendarEventInput = getFlagValue('--calendar-event');
    const gogGmailInput = getFlagValue('--gog-gmail');
    const gogCalendarInput = getFlagValue('--gog-calendar');
    const messageReadInput = getFlagValue('--message-read');
    const adapterSignalInput = getFlagValue('--adapter-signal');
    const signals = [];
    const sources = [];
    if (gmailEventInput) {
        signals.push(...(0, openclawGmail_1.gmailWebhookToSignals)(loadJson(gmailEventInput)));
        sources.push('openclaw.gmail_event');
    }
    if (calendarEventInput) {
        signals.push(...(0, openclawCalendar_1.calendarEventsToSignals)(loadJson(calendarEventInput)));
        sources.push('openclaw.calendar_event');
    }
    if (gogGmailInput) {
        signals.push(...(0, gogSnapshot_1.gogGmailToSignals)(loadJson(gogGmailInput)));
        sources.push('gog.gmail_snapshot');
    }
    if (gogCalendarInput) {
        signals.push(...(0, gogSnapshot_1.gogCalendarToSignals)(loadJson(gogCalendarInput)));
        sources.push('gog.calendar_snapshot');
    }
    if (messageReadInput) {
        const payload = loadJson(messageReadInput);
        signals.push(...(0, openclawMessages_1.messagesToSignals)(payload, {
            channel: payload.channel,
            target: payload.target,
        }));
        sources.push('openclaw.message_read');
    }
    if (adapterSignalInput) {
        const raw = loadJson(adapterSignalInput);
        const validation = (0, validateAdapterSignal_1.validateAdapterSignal)(raw);
        if (!validation.ok) {
            if (outputFormat === 'messenger') {
                console.log('');
                console.log('🦞 WorldLoops Guard');
                console.log('');
                console.log('❌ Invalid adapter signal');
                console.log(validation.errors.join('\n'));
                console.log('');
                console.log('✅ Safe');
                console.log('externalWrite: false');
                console.log('No external system changed.');
                console.log('');
            }
            else {
                printJson({
                    ok: false,
                    error: {
                        code: 'INVALID_ADAPTER_SIGNAL',
                        message: 'Adapter signal validation failed. Fix the errors below before reconciling.',
                        errors: validation.errors,
                    },
                    safety: { externalWrite: false },
                });
            }
            process.exit(1);
        }
        signals.push((0, toWorldLoopsSignal_1.toWorldLoopsSignal)(validation.signal));
        sources.push('adapter.signal');
    }
    if (signals.length === 0) {
        if (outputFormat === 'messenger') {
            console.log('');
            console.log('🦞 WorldLoops Guard');
            console.log('');
            console.log('❌ No signals provided');
            console.log('Provide at least one input: --gmail-event, --calendar-event, --gog-gmail, --gog-calendar, --message-read, or --adapter-signal.');
            console.log('');
            console.log('✅ Safe');
            console.log('externalWrite: false');
            console.log('No external system changed.');
            console.log('');
        }
        else {
            printJson({
                ok: false,
                error: {
                    code: 'MISSING_SIGNALS',
                    message: 'Provide at least one input: --gmail-event, --calendar-event, --gog-gmail, --gog-calendar, --message-read, or --adapter-signal.',
                },
                safety: {
                    externalWrite: false,
                },
            });
        }
        process.exit(1);
    }
    const result = await (0, brief_1.callWorldLoopsBrief)({
        signals,
        mode: 'reconciliation',
    });
    const candidates = result.proposalCandidates ?? [];
    let receiptsGenerated = 0;
    let openLoopsPersisted = 0;
    let openLoopsAlreadyTracked = 0;
    let proposalsPersisted = 0;
    let proposalsAlreadyTracked = 0;
    if (result.ok && candidates.length > 0) {
        const existingOpenLoops = (0, openLoopStates_1.loadOpenLoopStates)();
        const existingCanonicalKeys = new Set(existingOpenLoops.map((loop) => loop.canonicalKey));
        for (const candidate of candidates) {
            // Resolve or create proposal first so the receipt references the local UUID.
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
            if (existingCanonicalKeys.has(candidate.idempotencyKey)) {
                openLoopsAlreadyTracked++;
            }
            else {
                const openLoopState = (0, openLoopStates_1.buildOpenLoopStateFromProposal)(candidate, signals);
                (0, openLoopStates_1.saveOpenLoopState)(openLoopState);
                existingCanonicalKeys.add(candidate.idempotencyKey);
                openLoopsPersisted++;
            }
        }
    }
    if (outputFormat === 'messenger') {
        (0, messengerFormat_1.printMessengerOutput)({
            ok: result.ok,
            candidates,
            openLoopCount: result.openLoops?.length ?? candidates.length,
            receiptsGenerated,
            proposalsPersisted,
            proposalsAlreadyTracked,
        });
    }
    else {
        printJson({
            ...result,
            mode: 'reconciliation',
            source: 'worldloops.public',
            metadata: {
                ...(result.metadata ?? {}),
                signalCount: signals.length,
                sources,
                receiptsGenerated,
                openLoopsPersisted,
                openLoopsAlreadyTracked,
                proposalsPersisted,
                proposalsAlreadyTracked,
            },
            capabilityBoundary: (0, capabilityBoundary_1.getCapabilityBoundary)(),
            safety: {
                ...(result.safety ?? {}),
                externalWrite: false,
            },
        });
    }
}
main().catch((err) => {
    const outputFormat = getFlagValue('--format') ?? 'json';
    if (outputFormat === 'messenger') {
        console.log('');
        console.log('🦞 WorldLoops Guard');
        console.log('');
        console.log('❌ Reconcile failed');
        console.log(err instanceof Error ? err.message : String(err));
        console.log('');
        console.log('✅ Safe');
        console.log('externalWrite: false');
        console.log('No external system changed.');
        console.log('');
    }
    else {
        printJson({
            ok: false,
            error: {
                code: 'WORLDLOOPS_PUBLIC_BRIEF_FAILED',
                message: err instanceof Error ? err.message : String(err),
            },
            safety: {
                externalWrite: false,
            },
        });
    }
    process.exit(1);
});
//# sourceMappingURL=briefReconcile.js.map