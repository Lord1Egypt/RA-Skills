import * as fs from 'node:fs';
import * as path from 'node:path';
import * as crypto from 'node:crypto';
import { isPromotionalText, hasNegativeIntent, isTravelContextEvent } from './dailyBriefRunner';
import { loadOpenLoopStates, saveOpenLoopState, transitionOpenLoopState } from './storage/openLoopStates';
import { adjudicateSeverity } from './policy/severityPolicy';
import type { OpenLoopState, OpenLoopStatus } from './types/openLoopState';
import type { SignalSource } from './types';

export type ObservationIntent =
  | 'new_loop'
  | 'state_transition'
  | 'noise'
  | 'related_context'
  | 'evidence';

export interface OpenClawObservation {
  id: string;
  source: string;
  sourceId: string;
  observedBy: 'openclaw';
  userQuery?: string;
  observationIntent?: ObservationIntent;
  title: string;
  text: string;
  timestamp: string;
  actor?: string | null;
  dueAt?: string;
  evidence: Record<string, unknown>;
  confidence?: number;
  relatedContext?: Record<string, unknown> | null;
}

export type AdjudicationVerdict =
  | 'accepted'
  | 'suppressed'
  | 'attached_context'
  | 'needs_review'
  | 'state_transition';

export type SuppressionReason =
  | 'promotional_or_informational'
  | 'negative_intent_no_action'
  | 'duplicate_signal'
  | 'weak_evidence'
  | 'context_only';

export interface StateTransitionInfo {
  loopId: string;
  loopTitle: string;
  canonicalKey: string;
  fromStatus: OpenLoopStatus;
  toStatus: OpenLoopStatus | 'still_open';
  transitionApplied: boolean;
  note: string;
}

export interface AdjudicationResult {
  observation: OpenClawObservation;
  verdict: AdjudicationVerdict;
  suppressionReason?: SuppressionReason;
  openLoopId?: string;
  openLoopTitle?: string;
  stateTransition?: StateTransitionInfo;
}

export interface SuppressionReceipt {
  id: string;
  observationId: string;
  source: string;
  title: string;
  verdict: AdjudicationVerdict;
  suppressionReason?: SuppressionReason;
  stateTransition?: StateTransitionInfo;
  adjudicatedAt: string;
  safety: { externalWrite: false };
}

export interface IntakeSummary {
  total: number;
  accepted: number;
  suppressed: number;
  attached_context: number;
  needs_review: number;
  state_transition: number;
  results: AdjudicationResult[];
  receipts: SuppressionReceipt[];
  morningBriefLines: string[];
  safety: { externalWrite: false };
}

function getWorldLoopsDir(): string {
  return process.env.WORLDLOOPS_DIR ?? path.join(process.cwd(), '.worldloops');
}

function getSuppressionReceiptsPath(): string {
  return path.join(getWorldLoopsDir(), 'openclaw_suppression_receipts.json');
}

function loadSuppressionReceipts(): SuppressionReceipt[] {
  const p = getSuppressionReceiptsPath();
  if (!fs.existsSync(p)) return [];
  return JSON.parse(fs.readFileSync(p, 'utf8')) as SuppressionReceipt[];
}

function saveSuppressionReceipts(receipts: SuppressionReceipt[]): void {
  const p = getSuppressionReceiptsPath();
  const dir = path.dirname(p);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(p, JSON.stringify(receipts, null, 2) + '\n', 'utf8');
}

export function canonicalKeyForObservation(obs: OpenClawObservation): string {
  return `openclaw-${obs.source}-${obs.sourceId}`;
}

const KNOWN_SOURCES: SignalSource[] = ['slack', 'gmail', 'calendar', 'github', 'manual'];

function toSignalSource(source: string): SignalSource {
  return (KNOWN_SOURCES as string[]).includes(source) ? source as SignalSource : 'manual';
}

const COMPLETION_INDICATORS = [
  'resolved', 'completed', 'done', 'confirmed', 'sent', 'received',
  'closed', 'finished', 'addressed',
];

const ESCALATION_INDICATORS = [
  'overdue', 'urgent', 'escalate', 'missed deadline', 'critical',
  'past due', 'immediately', 'asap',
];

const SNOOZE_INDICATORS = [
  'can wait', 'snooze', 'deprioritize', 'defer', 'postpone', 'not urgent',
];

function detectTransitionTarget(text: string): OpenLoopStatus | 'still_open' {
  const lower = text.toLowerCase();
  if (ESCALATION_INDICATORS.some(w => lower.includes(w))) return 'escalated';
  if (COMPLETION_INDICATORS.some(w => lower.includes(w))) return 'done';
  if (SNOOZE_INDICATORS.some(w => lower.includes(w))) return 'snoozed';
  return 'still_open';
}

export function adjudicateObservation(
  obs: OpenClawObservation,
  acceptedKeysInBatch: Set<string>,
  existingLoopKeys: Set<string>,
  createdLoopsInBatch: Map<string, OpenLoopState>,
  existingLoops: OpenLoopState[]
): { verdict: AdjudicationVerdict; suppressionReason?: SuppressionReason; stateTransition?: StateTransitionInfo } {

  // Step 0: explicit state_transition intent — handle before heuristics
  if (obs.observationIntent === 'state_transition') {
    const relCtx = obs.relatedContext as Record<string, unknown> | null | undefined;
    const targetKey = typeof relCtx?.existingLoopKey === 'string' ? relCtx.existingLoopKey : undefined;

    if (!targetKey) {
      return { verdict: 'needs_review', suppressionReason: 'weak_evidence' };
    }

    const targetLoop = createdLoopsInBatch.get(targetKey) ??
                       existingLoops.find(l => l.canonicalKey === targetKey);

    if (!targetLoop) {
      return { verdict: 'needs_review', suppressionReason: 'weak_evidence' };
    }

    const toStatus = detectTransitionTarget(obs.text);
    const applied = toStatus !== 'still_open' && toStatus !== targetLoop.status;

    if (applied) {
      const note = toStatus === 'done' ? 'closed_by_new_evidence' :
                   toStatus === 'escalated' ? 'escalated_due_to_deadline' : toStatus;
      transitionOpenLoopState(targetLoop.id, toStatus as OpenLoopStatus, {
        actor: 'worldloops.openclaw-intake',
        note: `${note}; observationId=${obs.id}`,
      });
    }

    const stateTransition: StateTransitionInfo = {
      loopId: targetLoop.id,
      loopTitle: targetLoop.title,
      canonicalKey: targetKey,
      fromStatus: targetLoop.status,
      toStatus,
      transitionApplied: applied,
      note: toStatus === 'done' ? 'closed_by_new_evidence' :
            toStatus === 'escalated' ? 'escalated_due_to_deadline' :
            toStatus === 'snoozed' ? 'snoozed_by_observation' : 'still_open',
    };

    return { verdict: 'state_transition', stateTransition };
  }

  // Step 0.5: explicit observationIntent is authoritative — skip heuristics that would override it
  if (obs.observationIntent !== undefined) {
    if (obs.observationIntent === 'noise') {
      return { verdict: 'suppressed', suppressionReason: 'promotional_or_informational' };
    }
    if (obs.observationIntent === 'related_context' || obs.observationIntent === 'evidence') {
      return { verdict: 'attached_context', suppressionReason: 'context_only' };
    }
    // new_loop: still guard against duplicates and low confidence
    const key = canonicalKeyForObservation(obs);
    if (acceptedKeysInBatch.has(key) || existingLoopKeys.has(key)) {
      return { verdict: 'suppressed', suppressionReason: 'duplicate_signal' };
    }
    if (typeof obs.confidence === 'number' && obs.confidence < 0.4) {
      return { verdict: 'needs_review', suppressionReason: 'weak_evidence' };
    }
    return { verdict: 'accepted' };
  }

  // Steps 1–7: heuristic adjudication (for observations without explicit intent)
  const evidenceTitle = typeof obs.evidence.title === 'string' ? obs.evidence.title : obs.title;
  const evidenceDesc = typeof obs.evidence.description === 'string' ? obs.evidence.description :
                       typeof obs.evidence.snippet === 'string' ? obs.evidence.snippet : obs.text;
  const evidenceLocation = typeof obs.evidence.location === 'string' ? obs.evidence.location : '';

  const combinedText = [
    obs.title, obs.text,
    ...Object.values(obs.evidence).filter((v): v is string => typeof v === 'string'),
  ].join(' ');

  if (isPromotionalText(combinedText)) {
    return { verdict: 'suppressed', suppressionReason: 'promotional_or_informational' };
  }

  if (hasNegativeIntent(combinedText)) {
    return { verdict: 'suppressed', suppressionReason: 'negative_intent_no_action' };
  }

  if (isTravelContextEvent(evidenceTitle, evidenceDesc, evidenceLocation)) {
    return { verdict: 'attached_context', suppressionReason: 'context_only' };
  }

  const key = canonicalKeyForObservation(obs);
  if (acceptedKeysInBatch.has(key) || existingLoopKeys.has(key)) {
    return { verdict: 'suppressed', suppressionReason: 'duplicate_signal' };
  }

  if (obs.relatedContext !== null && obs.relatedContext !== undefined) {
    return { verdict: 'attached_context', suppressionReason: 'context_only' };
  }

  if (typeof obs.confidence === 'number' && obs.confidence < 0.4) {
    return { verdict: 'needs_review', suppressionReason: 'weak_evidence' };
  }

  return { verdict: 'accepted' };
}

export function runIntake(observations: OpenClawObservation[]): IntakeSummary {
  const now = new Date().toISOString();
  const existingLoops = loadOpenLoopStates();
  const existingLoopKeys = new Set(existingLoops.map(l => l.canonicalKey));
  const acceptedKeysInBatch = new Set<string>();
  const createdLoopsInBatch = new Map<string, OpenLoopState>();

  const results: AdjudicationResult[] = [];
  const receipts: SuppressionReceipt[] = [];

  for (const obs of observations) {
    const { verdict, suppressionReason, stateTransition } = adjudicateObservation(
      obs,
      acceptedKeysInBatch,
      existingLoopKeys,
      createdLoopsInBatch,
      existingLoops
    );

    const result: AdjudicationResult = { observation: obs, verdict, suppressionReason, stateTransition };

    if (verdict === 'accepted') {
      const key = canonicalKeyForObservation(obs);
      acceptedKeysInBatch.add(key);

      const loopState: OpenLoopState = {
        id: crypto.randomUUID(),
        canonicalKey: key,
        title: obs.title,
        sourceSignals: [{
          source: toSignalSource(obs.source),
          text: obs.text,
          createdAt: obs.timestamp,
        }],
        status: 'todo',
        severity: 'medium',
        adjudication: adjudicateSeverity('medium'),
        owner: (obs.actor as string | null) ?? null,
        dueAt: obs.dueAt ?? null,
        lastObservedAt: now,
        updatedAt: now,
        history: [{
          at: now,
          from: null,
          to: 'todo',
          actor: 'worldloops.openclaw-intake',
          note: `Accepted from OpenClaw observation; observedBy=${obs.observedBy}; userQuery=${obs.userQuery ?? 'unspecified'}`,
        }],
        safety: { externalWrite: false },
      };

      saveOpenLoopState(loopState);
      createdLoopsInBatch.set(key, loopState);
      result.openLoopId = loopState.id;
      result.openLoopTitle = loopState.title;
    }

    if (verdict !== 'accepted') {
      receipts.push({
        id: crypto.randomUUID(),
        observationId: obs.id,
        source: obs.source,
        title: obs.title,
        verdict,
        suppressionReason,
        stateTransition,
        adjudicatedAt: now,
        safety: { externalWrite: false },
      });
    }

    results.push(result);
  }

  if (receipts.length > 0) {
    const existing = loadSuppressionReceipts();
    saveSuppressionReceipts([...existing, ...receipts]);
  }

  return {
    total: observations.length,
    accepted: results.filter(r => r.verdict === 'accepted').length,
    suppressed: results.filter(r => r.verdict === 'suppressed').length,
    attached_context: results.filter(r => r.verdict === 'attached_context').length,
    needs_review: results.filter(r => r.verdict === 'needs_review').length,
    state_transition: results.filter(r => r.verdict === 'state_transition').length,
    results,
    receipts,
    morningBriefLines: buildMorningBriefLines(results),
    safety: { externalWrite: false },
  };
}

function buildMorningBriefLines(results: AdjudicationResult[]): string[] {
  const lines: string[] = [];

  const accepted = results.filter(r => r.verdict === 'accepted');
  const appliedTransitions = results.filter(
    r => r.verdict === 'state_transition' && r.stateTransition?.transitionApplied
  );

  const transitionByKey = new Map<string, StateTransitionInfo>();
  for (const r of appliedTransitions) {
    if (r.stateTransition) {
      transitionByKey.set(r.stateTransition.canonicalKey, r.stateTransition);
    }
  }

  const stillOpen: string[] = [];
  const closedByEvidence: string[] = [];
  const escalatedLoops: string[] = [];
  const snoozedLoops: string[] = [];

  for (const r of accepted) {
    const key = canonicalKeyForObservation(r.observation);
    const transition = transitionByKey.get(key);
    const title = r.openLoopTitle ?? r.observation.title;
    if (transition) {
      if (transition.toStatus === 'done') closedByEvidence.push(title);
      else if (transition.toStatus === 'escalated') escalatedLoops.push(title);
      else if (transition.toStatus === 'snoozed') snoozedLoops.push(title);
      else stillOpen.push(title);
    } else {
      stillOpen.push(title);
    }
  }

  const suppressed = results.filter(r => r.verdict === 'suppressed').length;
  const needsReview = results.filter(r => r.verdict === 'needs_review').length;
  const attachedContext = results.filter(r => r.verdict === 'attached_context').length;

  if (stillOpen.length > 0) {
    lines.push(`- ${stillOpen.length} loop${stillOpen.length > 1 ? 's' : ''} still open`);
    for (const t of stillOpen) lines.push(`  ${t}`);
  }
  if (closedByEvidence.length > 0) {
    lines.push(`- ${closedByEvidence.length} loop${closedByEvidence.length > 1 ? 's' : ''} closed by new evidence`);
    for (const t of closedByEvidence) lines.push(`  ${t}`);
  }
  if (escalatedLoops.length > 0) {
    lines.push(`- ${escalatedLoops.length} loop${escalatedLoops.length > 1 ? 's' : ''} escalated`);
    for (const t of escalatedLoops) lines.push(`  ${t}`);
  }
  if (snoozedLoops.length > 0) {
    lines.push(`- ${snoozedLoops.length} loop${snoozedLoops.length > 1 ? 's' : ''} snoozed`);
    for (const t of snoozedLoops) lines.push(`  ${t}`);
  }
  if (suppressed > 0) {
    lines.push(`- ${suppressed} observed signal${suppressed > 1 ? 's' : ''} suppressed as noise`);
  }
  if (attachedContext > 0) {
    lines.push(`- ${attachedContext} signal${attachedContext > 1 ? 's' : ''} attached as context`);
  }
  if (needsReview > 0) {
    lines.push(`- ${needsReview} signal${needsReview > 1 ? 's' : ''} need${needsReview === 1 ? 's' : ''} review`);
  }

  return lines;
}

export function loadObservations(filePath: string): OpenClawObservation[] {
  const raw = fs.readFileSync(path.resolve(filePath), 'utf8');
  return JSON.parse(raw) as OpenClawObservation[];
}
