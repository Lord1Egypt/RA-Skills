import * as fs from 'node:fs';
import * as path from 'node:path';
import * as crypto from 'node:crypto';
import type { ProposalCandidate, Signal } from '../types';
import type { OpenLoopState, OpenLoopStatus } from '../types/openLoopState';
import { adjudicateSeverity } from '../policy/severityPolicy';

function getWorldLoopsDir(): string {
  return process.env.WORLDLOOPS_DIR ?? path.join(process.cwd(), '.worldloops');
}

export function getOpenLoopStatesPath(): string {
  return path.join(getWorldLoopsDir(), 'open_loop_states.json');
}

export function loadOpenLoopStates(): OpenLoopState[] {
  const statesPath = getOpenLoopStatesPath();
  if (!fs.existsSync(statesPath)) {
    return [];
  }
  return JSON.parse(fs.readFileSync(statesPath, 'utf8')) as OpenLoopState[];
}

export function saveOpenLoopStates(states: OpenLoopState[]): void {
  const statesPath = getOpenLoopStatesPath();
  const dir = path.dirname(statesPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(statesPath, JSON.stringify(states, null, 2) + '\n', 'utf8');
}

export function saveOpenLoopState(state: OpenLoopState): void {
  const existing = loadOpenLoopStates();
  const upserted = existing.filter((s) => s.id !== state.id);
  upserted.push(state);
  saveOpenLoopStates(upserted);
}

export function findOpenLoopStateById(id: string): OpenLoopState | null {
  return loadOpenLoopStates().find((state) => state.id === id) ?? null;
}

export function transitionOpenLoopState(
  id: string,
  to: OpenLoopStatus,
  opts: {
    actor?: string | null;
    note?: string | null;
  } = {}
): OpenLoopState {
  const states = loadOpenLoopStates();
  const index = states.findIndex((state) => state.id === id);

  if (index === -1) {
    throw new Error(`Open loop not found: ${id}`);
  }

  const current = states[index];
  const now = new Date().toISOString();

  const updated: OpenLoopState = {
    ...current,
    status: to,
    updatedAt: now,
    history: [
      ...current.history,
      {
        at: now,
        from: current.status,
        to,
        actor: opts.actor ?? null,
        note: opts.note ?? null,
      },
    ],
    safety: {
      externalWrite: false,
    },
  };

  states[index] = updated;
  saveOpenLoopStates(states);

  return updated;
}

export function selectRelevantSignalsForProposal(
  candidate: ProposalCandidate,
  signals: Signal[]
): Signal[] {
  const sameSourceSignals = signals.filter((signal) => signal.source === candidate.source);

  if (sameSourceSignals.length > 0) {
    return sameSourceSignals;
  }

  if (signals.length > 0) {
    return [signals[0]];
  }

  return [];
}

export function buildOpenLoopStateFromProposal(
  candidate: ProposalCandidate,
  signals: Signal[]
): OpenLoopState {
  const now = new Date().toISOString();
  const adjudication = adjudicateSeverity(candidate.severity);

  return {
    id: crypto.randomUUID(),
    canonicalKey: candidate.idempotencyKey,
    title: candidate.actionHint || candidate.reason || candidate.entityType,
    sourceSignals: selectRelevantSignalsForProposal(candidate, signals).map((signal) => ({
      source: signal.source,
      text: signal.text,
      url: signal.url,
      createdAt: signal.createdAt,
    })),
    status: adjudication.shouldEscalate ? 'escalated' : 'todo',
    severity: adjudication.severity,
    adjudication,
    owner: null,
    dueAt: null,
    lastObservedAt: now,
    updatedAt: now,
    history: [
      {
        at: now,
        from: null,
        to: adjudication.shouldEscalate ? 'escalated' : 'todo',
        actor: 'worldloops.local',
        note: `Created from proposal candidate; adjudication=${adjudication.action}`,
      },
    ],
    safety: {
      externalWrite: false,
    },
  };
}
