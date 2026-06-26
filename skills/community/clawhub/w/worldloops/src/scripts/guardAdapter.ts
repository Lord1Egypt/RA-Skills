import * as fs from 'node:fs';
import * as path from 'node:path';

import type { Signal } from '../types';
import { callWorldLoopsBrief } from '../brief';
import { validateAdapterSignal } from '../adapter/validateAdapterSignal';
import { toWorldLoopsSignal } from '../adapter/toWorldLoopsSignal';
import { buildTransitionReceipt, saveTransitionReceipt } from '../storage/transitionReceipts';
import { buildOpenLoopStateFromProposal, loadOpenLoopStates, saveOpenLoopState } from '../storage/openLoopStates';
import { buildProposalFromCandidate, findProposalByIdempotencyKey, saveProposal } from '../storage/proposals';
import { printMessengerOutput, printCompactOutput } from '../output/messengerFormat';
import { isGogGmailPayload, gogGmailToAdapterSignal } from '../adapters/gogGmail';
import { isGogCalendarPayload, gogCalendarToAdapterSignal } from '../adapters/gogCalendar';
import { isSlackHostPayload, slackPayloadToAdapterSignal } from '../adapters/slackPayload';

const SUPPORTED_SOURCES = ['gmail', 'calendar', 'slack', 'github', 'generic'];

function getFlagValue(flag: string): string | undefined {
  const args = process.argv.slice(2);
  const idx = args.indexOf(flag);
  if (idx === -1 || idx + 1 >= args.length) return undefined;
  return args[idx + 1];
}

function hasFlag(flag: string): boolean {
  return process.argv.slice(2).includes(flag);
}

function resolveFormat(): string {
  if (hasFlag('--compact')) return 'compact';
  return getFlagValue('--format') ?? 'messenger';
}

function printError(lines: string[], outputFormat: string): void {
  if (outputFormat === 'compact') {
    console.log('🦞 Agent Execution Guard');
    console.log('');
    for (const line of lines) console.log(line);
    console.log('');
    console.log('✅ Safe');
    console.log('externalWrite:false');
    console.log('No email, draft, call, or external change made.');
  } else {
    console.log('');
    console.log('🦞 WorldLoops Guard');
    console.log('');
    for (const line of lines) console.log(line);
    console.log('');
    console.log('✅ Safe');
    console.log('externalWrite: false');
    console.log('No external system changed.');
    console.log('');
  }
}

async function main(): Promise<void> {
  const inputPath = getFlagValue('--input');
  const source = getFlagValue('--source');
  const outputFormat = resolveFormat();

  if (!inputPath) {
    printError(
      ['❌ No input provided.', 'Usage: npm run guard:adapter -- --source gmail --input <payload.json>'],
      outputFormat
    );
    process.exit(1);
  }

  if (source && !SUPPORTED_SOURCES.includes(source)) {
    printError(
      [`❌ Unknown source: "${source}".`, `Supported: ${SUPPORTED_SOURCES.join(', ')}`],
      outputFormat
    );
    process.exit(1);
  }

  let raw: unknown;
  try {
    raw = JSON.parse(fs.readFileSync(path.resolve(inputPath), 'utf8'));
  } catch (e) {
    printError([`❌ Could not read input file: ${inputPath}`], outputFormat);
    process.exit(1);
  }

  // Source-specific normalization for gog and host tool payloads before AdapterSignal validation
  if (source && typeof raw === 'object' && raw !== null && !Array.isArray(raw)) {
    if (source === 'gmail' && isGogGmailPayload(raw)) {
      raw = gogGmailToAdapterSignal(raw);
    } else if (source === 'calendar' && isGogCalendarPayload(raw)) {
      raw = gogCalendarToAdapterSignal(raw);
    } else if (source === 'slack' && isSlackHostPayload(raw)) {
      raw = slackPayloadToAdapterSignal(raw);
    } else {
      // Simple field injection for AdapterSignal-like partial payloads
      const obj = raw as Record<string, unknown>;
      if (!obj.source) obj.source = source;
      if (!obj.sourceType) obj.sourceType = 'message';
      if (obj.externalWrite === undefined) obj.externalWrite = false;
      if (!obj.observedAt) obj.observedAt = new Date().toISOString();
    }
  }

  const validation = validateAdapterSignal(raw);
  if (!validation.ok) {
    printError(['❌ Invalid adapter signal.', ...validation.errors], outputFormat);
    process.exit(1);
  }

  const signal = toWorldLoopsSignal(validation.signal);
  const signals: Signal[] = [signal];

  const result = await callWorldLoopsBrief({ signals, mode: 'reconciliation' });

  const candidates = result.proposalCandidates ?? [];
  let receiptsGenerated = 0;
  let proposalsPersisted = 0;
  let proposalsAlreadyTracked = 0;

  if (result.ok && candidates.length > 0) {
    const existingOpenLoops = loadOpenLoopStates();
    const existingCanonicalKeys = new Set(existingOpenLoops.map((loop) => loop.canonicalKey));
    for (const candidate of candidates) {
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

      if (!existingCanonicalKeys.has(candidate.idempotencyKey)) {
        const openLoopState = buildOpenLoopStateFromProposal(candidate, signals);
        saveOpenLoopState(openLoopState);
        existingCanonicalKeys.add(candidate.idempotencyKey);
      }
    }
  }

  if (outputFormat === 'compact') {
    printCompactOutput({ ok: result.ok, candidates });
  } else {
    printMessengerOutput({
      ok: result.ok,
      candidates,
      openLoopCount: result.openLoops?.length ?? candidates.length,
      receiptsGenerated,
      proposalsPersisted,
      proposalsAlreadyTracked,
    });
  }
}

main().catch((err: unknown) => {
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
  } else {
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
