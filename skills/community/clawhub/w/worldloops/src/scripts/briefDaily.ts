import * as fs from 'node:fs';
import * as path from 'node:path';

import type { Signal } from '../types';
import { loadPrefs } from '../notifications/prefs';
import { isInQuietHours } from '../notifications/prefs';
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
  const quietHoursActive = isInQuietHours(prefs);

  if (quietHoursActive) {
    printJson({
      ok: true,
      mode: 'daily_brief',
      source: 'worldloops.local',
      quietHoursActive: true,
      message: 'Quiet hours are active. Daily brief suppressed.',
      preferences: prefs,
      safety: { externalWrite: false },
    });
    return;
  }

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
      mode: 'daily_brief',
      source: 'worldloops.local',
      quietHoursActive: false,
      brief: 'No signals provided. Pass fixture flags to generate a meaningful brief.',
      openLoops: [],
      proposalCandidates: [],
      preferences: prefs,
      safety: { externalWrite: false },
    });
    return;
  }

  const result = await callWorldLoopsBrief({ signals, mode: 'reconciliation' });

  printJson({
    ...result,
    mode: 'daily_brief',
    source: 'worldloops.local',
    quietHoursActive: false,
    preferences: prefs,
    metadata: {
      ...(result.metadata ?? {}),
      signalCount: signals.length,
      sources,
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
          code: 'BRIEF_DAILY_FAILED',
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
