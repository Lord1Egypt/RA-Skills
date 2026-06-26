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
const prefs_1 = require("../notifications/prefs");
const state_1 = require("../notifications/state");
const brief_1 = require("../brief");
const openclawGmail_1 = require("../adapters/openclawGmail");
const openclawCalendar_1 = require("../adapters/openclawCalendar");
const gogSnapshot_1 = require("../adapters/gogSnapshot");
const openclawMessages_1 = require("../adapters/openclawMessages");
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
    return JSON.parse(fs.readFileSync(path.resolve(filePath), 'utf8'));
}
async function main() {
    const prefs = (0, prefs_1.loadPrefs)();
    const state = (0, state_1.loadState)();
    const gmailEventInput = getFlagValue('--gmail-event');
    const calendarEventInput = getFlagValue('--calendar-event');
    const gogGmailInput = getFlagValue('--gog-gmail');
    const gogCalendarInput = getFlagValue('--gog-calendar');
    const messageReadInput = getFlagValue('--message-read');
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
        signals.push(...(0, openclawMessages_1.messagesToSignals)(payload, { channel: payload.channel, target: payload.target }));
        sources.push('openclaw.message_read');
    }
    if (signals.length === 0) {
        printJson({
            ok: true,
            mode: 'discovery',
            source: 'worldloops.local',
            surfaced: [],
            suppressed: 0,
            message: 'No signals provided. Pass fixture flags to run discovery.',
            preferences: prefs,
            safety: { externalWrite: false },
        });
        return;
    }
    const result = await (0, brief_1.callWorldLoopsBrief)({ signals, mode: 'reconciliation' });
    const allCandidates = result.proposalCandidates ?? [];
    const minSeverity = prefs.proactiveDiscovery.minSeverity;
    const suppressedSet = new Set(state.suppressedKeys);
    const severityFiltered = allCandidates.filter((c) => (0, prefs_1.meetsSeverity)(c.severity, minSeverity));
    const surfaced = [];
    let suppressedCount = 0;
    for (const candidate of severityFiltered) {
        if (suppressedSet.has(candidate.idempotencyKey)) {
            suppressedCount++;
        }
        else {
            surfaced.push(candidate);
            suppressedSet.add(candidate.idempotencyKey);
        }
    }
    const updatedState = {
        ...state,
        suppressedKeys: Array.from(suppressedSet),
        lastDiscoveryAt: new Date().toISOString(),
    };
    (0, state_1.saveState)(updatedState);
    printJson({
        ok: result.ok,
        mode: 'discovery',
        source: 'worldloops.local',
        surfaced,
        suppressed: suppressedCount,
        openLoops: result.openLoops ?? [],
        preferences: prefs,
        metadata: {
            ...(result.metadata ?? {}),
            signalCount: signals.length,
            sources,
            totalCandidates: allCandidates.length,
            severityFiltered: severityFiltered.length,
        },
        safety: { externalWrite: false },
    });
}
main().catch((err) => {
    console.log(JSON.stringify({
        ok: false,
        error: {
            code: 'DISCOVERY_RUN_FAILED',
            message: err instanceof Error ? err.message : String(err),
        },
        safety: { externalWrite: false },
    }, null, 2));
    process.exit(1);
});
//# sourceMappingURL=discoveryRun.js.map