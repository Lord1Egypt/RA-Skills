import * as fs from 'node:fs';
import * as os from 'node:os';
import * as path from 'node:path';
import * as crypto from 'node:crypto';
import type { AdapterSignal } from '../types/adapterSignal';
import type { ProposalCandidate } from '../types';
import { validateAdapterSignal } from './validateAdapterSignal';
import { toWorldLoopsSignal } from './toWorldLoopsSignal';
import {
  buildOpenLoopStateFromProposal,
  loadOpenLoopStates,
  saveOpenLoopState,
} from '../storage/openLoopStates';
import {
  buildProposalFromCandidate,
  findProposalByIdempotencyKey,
  saveProposal,
} from '../storage/proposals';
import { buildTransitionReceipt, saveTransitionReceipt } from '../storage/transitionReceipts';

export interface AdapterTestResult {
  file: string;
  validate: 'passed' | 'failed';
  validateErrors?: string[];
  reconcile: 'passed' | 'failed';
  reconcileError?: string;
  openLoopPersisted: boolean;
  proposalPersisted: boolean;
  idempotency: 'passed' | 'failed';
  externalWrite: false;
  reconcileMode: 'local_heuristic';
}

function buildLocalProposalCandidate(signal: AdapterSignal): ProposalCandidate {
  const hash = crypto
    .createHash('sha1')
    .update(`${signal.source}|${signal.sourceType}|${signal.text}`)
    .digest('hex')
    .slice(0, 12);
  const idempotencyKey = `adapter-test-${signal.source}-${signal.sourceType}-${hash}`;
  const worldSignal = toWorldLoopsSignal(signal);
  return {
    idempotencyKey,
    entityType: signal.sourceType,
    source: worldSignal.source,
    currentState: 'observed',
    proposedState: 'reviewed',
    reason: signal.summary ?? signal.text.slice(0, 120),
    approvalRequired: true,
    actionHint: `Review ${signal.source} ${signal.sourceType}`,
    severity: 'medium',
  };
}

function runLocalReconcile(signal: AdapterSignal): { openLoopNew: boolean; proposalNew: boolean } {
  const worldSignal = toWorldLoopsSignal(signal);
  const candidate = buildLocalProposalCandidate(signal);

  // Resolve or create proposal first so the receipt references the local UUID.
  let proposalLocalId: string;
  let proposalNew = false;
  const existingProposal = findProposalByIdempotencyKey(candidate.idempotencyKey);
  if (existingProposal) {
    proposalLocalId = existingProposal.id;
  } else {
    const proposal = buildProposalFromCandidate(candidate);
    saveProposal(proposal);
    proposalLocalId = proposal.id;
    proposalNew = true;
  }

  const receipt = buildTransitionReceipt(candidate, [worldSignal], {
    proposalId: proposalLocalId,
    adjudicationResult: 'proposed',
    decision: 'surfaced_for_review',
    boundaryCrossed: 'local_commit',
  });
  saveTransitionReceipt(receipt);

  const existingLoops = loadOpenLoopStates();
  const existingKeys = new Set(existingLoops.map((l) => l.canonicalKey));
  let openLoopNew = false;
  if (!existingKeys.has(candidate.idempotencyKey)) {
    saveOpenLoopState(buildOpenLoopStateFromProposal(candidate, [worldSignal]));
    openLoopNew = true;
  }

  return { openLoopNew, proposalNew };
}

function _runAdapterTestCore(filePath: string): AdapterTestResult {
  const result: AdapterTestResult = {
    file: filePath,
    validate: 'failed',
    reconcile: 'failed',
    openLoopPersisted: false,
    proposalPersisted: false,
    idempotency: 'failed',
    externalWrite: false,
    reconcileMode: 'local_heuristic',
  };

  let raw: unknown;
  try {
    raw = JSON.parse(fs.readFileSync(path.resolve(filePath), 'utf8'));
  } catch (err) {
    result.reconcileError = err instanceof Error ? err.message : String(err);
    return result;
  }

  const validation = validateAdapterSignal(raw);
  if (!validation.ok) {
    result.validateErrors = validation.errors;
    return result;
  }
  result.validate = 'passed';

  const signal = validation.signal;

  try {
    const first = runLocalReconcile(signal);
    result.openLoopPersisted = first.openLoopNew;
    result.proposalPersisted = first.proposalNew;
  } catch (err) {
    result.reconcileError = err instanceof Error ? err.message : String(err);
    return result;
  }

  if (!result.openLoopPersisted) {
    result.reconcileError = 'No open loop was persisted during reconciliation';
    return result;
  }
  if (!result.proposalPersisted) {
    result.reconcileError = 'No proposal was persisted during reconciliation';
    return result;
  }
  result.reconcile = 'passed';

  try {
    const second = runLocalReconcile(signal);
    result.idempotency = !second.openLoopNew && !second.proposalNew ? 'passed' : 'failed';
  } catch {
    result.idempotency = 'failed';
  }

  return result;
}

export function runAdapterTest(
  filePath: string,
  opts: { worldloopsDir?: string } = {}
): AdapterTestResult {
  const ownedDir = !opts.worldloopsDir;
  const testDir = opts.worldloopsDir
    ?? fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-adapter-test-'));

  const prevDir = process.env.WORLDLOOPS_DIR;
  process.env.WORLDLOOPS_DIR = testDir;

  try {
    return _runAdapterTestCore(filePath);
  } finally {
    if (prevDir !== undefined) {
      process.env.WORLDLOOPS_DIR = prevDir;
    } else {
      delete process.env.WORLDLOOPS_DIR;
    }
    if (ownedDir) {
      try {
        fs.rmSync(testDir, { recursive: true, force: true });
      } catch {
        // best-effort cleanup
      }
    }
  }
}
