import * as fs from 'node:fs';
import * as path from 'node:path';
import * as crypto from 'node:crypto';
import type { TransitionReceipt, BoundaryCrossed } from '../types/transitionReceipt';
import type { ProposalCandidate, Signal } from '../types';

function getWorldLoopsDir(): string {
  return process.env.WORLDLOOPS_DIR ?? path.join(process.cwd(), '.worldloops');
}

export function getTransitionReceiptsPath(): string {
  return path.join(getWorldLoopsDir(), 'transition_receipts.json');
}

export function loadTransitionReceipts(): TransitionReceipt[] {
  const receiptsPath = getTransitionReceiptsPath();
  if (!fs.existsSync(receiptsPath)) {
    return [];
  }
  return JSON.parse(fs.readFileSync(receiptsPath, 'utf8')) as TransitionReceipt[];
}

export function saveTransitionReceipt(receipt: TransitionReceipt): void {
  const receiptsPath = getTransitionReceiptsPath();
  const dir = path.dirname(receiptsPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  const existing = loadTransitionReceipts();
  const upserted = existing.filter((r) => r.id !== receipt.id);
  upserted.push(receipt);
  fs.writeFileSync(receiptsPath, JSON.stringify(upserted, null, 2) + '\n', 'utf8');
}

export function saveTransitionReceipts(receipts: TransitionReceipt[]): void {
  const receiptsPath = getTransitionReceiptsPath();
  const dir = path.dirname(receiptsPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(receiptsPath, JSON.stringify(receipts, null, 2) + '\n', 'utf8');
}

export function buildTransitionReceipt(
  candidate: ProposalCandidate,
  signals: Signal[],
  opts: {
    proposalId?: string | null;
    adjudicationResult: string | null;
    decision: string | null;
    boundaryCrossed: BoundaryCrossed;
  }
): TransitionReceipt {
  return {
    id: `${candidate.idempotencyKey}-${crypto.randomUUID()}`,
    createdAt: new Date().toISOString(),
    proposalId: opts.proposalId !== undefined ? opts.proposalId : candidate.idempotencyKey,
    sourceSignalsObserved: signals.map((s) => `[${s.source}] ${s.text}`),
    normalizedResponsibility: candidate.entityType,
    proposedTransition: {
      currentState: candidate.currentState,
      proposedState: candidate.proposedState,
    },
    reason: candidate.reason,
    adjudicationResult: opts.adjudicationResult,
    boundaryCrossed: opts.boundaryCrossed,
    externalWrite: false,
    actor: null,
    decision: opts.decision,
    unresolvedState: null,
    redactions: {
      applied: false,
      fields: [],
    },
  };
}
