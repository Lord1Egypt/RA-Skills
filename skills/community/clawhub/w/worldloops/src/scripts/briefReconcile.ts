import * as fs from 'node:fs';
import * as path from 'node:path';

import type { Signal } from '../types';
import { callWorldLoopsBrief } from '../brief';
import { gmailWebhookToSignals } from '../adapters/openclawGmail';
import { calendarEventsToSignals } from '../adapters/openclawCalendar';
import { gogGmailToSignals, gogCalendarToSignals } from '../adapters/gogSnapshot';
import { messagesToSignals } from '../adapters/openclawMessages';
import { validateAdapterSignal } from '../adapter/validateAdapterSignal';
import { toWorldLoopsSignal } from '../adapter/toWorldLoopsSignal';
import { buildTransitionReceipt, saveTransitionReceipt } from '../storage/transitionReceipts';
import { buildOpenLoopStateFromProposal, loadOpenLoopStates, saveOpenLoopState } from '../storage/openLoopStates';
import { buildProposalFromCandidate, findProposalByIdempotencyKey, saveProposal } from '../storage/proposals';
import { getCapabilityBoundary } from '../policy/capabilityBoundary';
import { printMessengerOutput } from '../output/messengerFormat';

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
  const resolved = path.resolve(filePath);
  return JSON.parse(fs.readFileSync(resolved, 'utf8')) as T;
}

async function main(): Promise<void> {
  const outputFormat = getFlagValue('--format') ?? 'json';
  const gmailEventInput = getFlagValue('--gmail-event');
  const calendarEventInput = getFlagValue('--calendar-event');
  const gogGmailInput = getFlagValue('--gog-gmail');
  const gogCalendarInput = getFlagValue('--gog-calendar');
  const messageReadInput = getFlagValue('--message-read');
  const adapterSignalInput = getFlagValue('--adapter-signal');

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
    signals.push(
      ...messagesToSignals(payload, {
        channel: payload.channel,
        target: payload.target,
      })
    );
    sources.push('openclaw.message_read');
  }

  if (adapterSignalInput) {
    const raw = loadJson<unknown>(adapterSignalInput);
    const validation = validateAdapterSignal(raw);
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
      } else {
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
    signals.push(toWorldLoopsSignal(validation.signal));
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
    } else {
      printJson({
        ok: false,
        error: {
          code: 'MISSING_SIGNALS',
          message:
            'Provide at least one input: --gmail-event, --calendar-event, --gog-gmail, --gog-calendar, --message-read, or --adapter-signal.',
        },
        safety: {
          externalWrite: false,
        },
      });
    }
    process.exit(1);
  }

  const result = await callWorldLoopsBrief({
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
    const existingOpenLoops = loadOpenLoopStates();
    const existingCanonicalKeys = new Set(existingOpenLoops.map((loop) => loop.canonicalKey));
    for (const candidate of candidates) {
      // Resolve or create proposal first so the receipt references the local UUID.
      let proposalLocalId: string;
      const existingProposal = findProposalByIdempotencyKey(candidate.idempotencyKey);
      if (existingProposal) {
        proposalsAlreadyTracked++;
        proposalLocalId = existingProposal.id;
      } else {
        const proposal = buildProposalFromCandidate(candidate);
        saveProposal(proposal);
        proposalsPersisted++;
        proposalLocalId = proposal.id;
      }

      const receipt = buildTransitionReceipt(candidate, signals, {
        proposalId: proposalLocalId,
        adjudicationResult: result.ok ? 'proposed' : 'api_error',
        decision: result.ok ? 'surfaced_for_review' : null,
        boundaryCrossed: 'local_commit',
      });
      saveTransitionReceipt(receipt);
      receiptsGenerated++;

      if (existingCanonicalKeys.has(candidate.idempotencyKey)) {
        openLoopsAlreadyTracked++;
      } else {
        const openLoopState = buildOpenLoopStateFromProposal(candidate, signals);
        saveOpenLoopState(openLoopState);
        existingCanonicalKeys.add(candidate.idempotencyKey);
        openLoopsPersisted++;
      }
    }
  }

  if (outputFormat === 'messenger') {
    printMessengerOutput({
      ok: result.ok,
      candidates,
      openLoopCount: result.openLoops?.length ?? candidates.length,
      receiptsGenerated,
      proposalsPersisted,
      proposalsAlreadyTracked,
    });
  } else {
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
      capabilityBoundary: getCapabilityBoundary(),
      safety: {
        ...(result.safety ?? {}),
        externalWrite: false,
      },
    });
  }
}

main().catch((err: unknown) => {
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
  } else {
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
