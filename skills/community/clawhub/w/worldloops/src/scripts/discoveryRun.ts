import * as fs from 'node:fs';
import * as path from 'node:path';

import type { Signal, ProposalCandidate } from '../types';
import { loadPrefs, meetsSeverity } from '../notifications/prefs';
import { loadState, saveState } from '../notifications/state';
import { callWorldLoopsBrief } from '../brief';
import { gmailWebhookToSignals } from '../adapters/openclawGmail';
import { calendarEventsToSignals } from '../adapters/openclawCalendar';
import { gogGmailToSignals, gogCalendarToSignals } from '../adapters/gogSnapshot';
import { messagesToSignals } from '../adapters/openclawMessages';

function getFlagValue(flag: string): string | undefined {
  const args = process.argv.slice(2);
  const idx = args.indexOf(flag);
  if (idx === -1 || idx + 1 >= args.length) return undefined;
  return args[idx + 1];
}

function printJson(value: unknown): void {
  console.log(JSON.stringify(value, null, 2));
}

function loadJson<T>(filePath: string): T {
  return JSON.parse(fs.readFileSync(path.resolve(filePath), 'utf8')) as T;
}

async function main(): Promise<void> {
  const prefs = loadPrefs();
  const state = loadState();

  const gmailEventInput = getFlagValue('--gmail-event');
  const calendarEventInput = getFlagValue('--calendar-event');
  const gogGmailInput = getFlagValue('--gog-gmail');
  const gogCalendarInput = getFlagValue('--gog-calendar');
  const messageReadInput = getFlagValue('--message-read');

  const signals: Signal[] = [];
  const sources: string[] = [];

  if (gmailEventInput) {
    signals.push(...gmailWebhookToSignals(loadJson(gmailEventInput)));
    sources.push('openclaw.gmail_event');
  }
  if (calendarEventInput) {
    signals.push(...calendarEventsToSignals(loadJson(calendarEventInput)));
    sources.push('openclaw.calendar_event');
  }
  if (gogGmailInput) {
    signals.push(...gogGmailToSignals(loadJson(gogGmailInput)));
    sources.push('gog.gmail_snapshot');
  }
  if (gogCalendarInput) {
    signals.push(...gogCalendarToSignals(loadJson(gogCalendarInput)));
    sources.push('gog.calendar_snapshot');
  }
  if (messageReadInput) {
    const payload = loadJson<{ channel?: string; target?: string }>(messageReadInput);
    signals.push(...messagesToSignals(payload, { channel: payload.channel, target: payload.target }));
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

  const result = await callWorldLoopsBrief({ signals, mode: 'reconciliation' });

  const allCandidates: ProposalCandidate[] = result.proposalCandidates ?? [];
  const minSeverity = prefs.proactiveDiscovery.minSeverity;
  const suppressedSet = new Set(state.suppressedKeys);

  const severityFiltered = allCandidates.filter((c) =>
    meetsSeverity(c.severity, minSeverity)
  );

  const surfaced: ProposalCandidate[] = [];
  let suppressedCount = 0;

  for (const candidate of severityFiltered) {
    if (suppressedSet.has(candidate.idempotencyKey)) {
      suppressedCount++;
    } else {
      surfaced.push(candidate);
      suppressedSet.add(candidate.idempotencyKey);
    }
  }

  const updatedState = {
    ...state,
    suppressedKeys: Array.from(suppressedSet),
    lastDiscoveryAt: new Date().toISOString(),
  };
  saveState(updatedState);

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

main().catch((err: unknown) => {
  console.log(
    JSON.stringify(
      {
        ok: false,
        error: {
          code: 'DISCOVERY_RUN_FAILED',
          message: err instanceof Error ? err.message : String(err),
        },
        safety: { externalWrite: false },
      },
      null,
      2
    )
  );
  process.exit(1);
});
