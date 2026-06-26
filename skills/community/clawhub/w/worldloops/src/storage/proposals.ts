import * as fs from 'node:fs';
import * as path from 'node:path';
import * as crypto from 'node:crypto';
import type { ProposalCandidate } from '../types';
import type { Proposal } from '../types/proposal';
import type { ProposalTemplateId } from '../types/proposalTemplate';
import { PROPOSAL_TEMPLATES } from '../data/proposalTemplates';

function getWorldLoopsDir(): string {
  return process.env.WORLDLOOPS_DIR ?? path.join(process.cwd(), '.worldloops');
}

export function getProposalsPath(): string {
  return path.join(getWorldLoopsDir(), 'proposals.json');
}

export function loadProposals(): Proposal[] {
  const proposalsPath = getProposalsPath();
  if (!fs.existsSync(proposalsPath)) {
    return [];
  }
  return JSON.parse(fs.readFileSync(proposalsPath, 'utf8')) as Proposal[];
}

export function saveProposal(proposal: Proposal): void {
  const proposalsPath = getProposalsPath();
  const dir = path.dirname(proposalsPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  const existing = loadProposals();
  const upserted = existing.filter((p) => p.id !== proposal.id);
  upserted.push(proposal);
  fs.writeFileSync(proposalsPath, JSON.stringify(upserted, null, 2) + '\n', 'utf8');
}

export function findProposalById(id: string): Proposal | null {
  return loadProposals().find((p) => p.id === id) ?? null;
}

export function listProposals(): Proposal[] {
  return loadProposals();
}

export function findProposalByIdempotencyKey(key: string): Proposal | null {
  return loadProposals().find((p) => p.idempotencyKey === key) ?? null;
}

function candidateToTemplateId(candidate: ProposalCandidate): ProposalTemplateId {
  if (candidate.severity === 'critical' || candidate.severity === 'high') return 'escalation';
  return 'state-transition';
}

export function buildProposalFromCandidate(candidate: ProposalCandidate): Proposal {
  const templateId = candidateToTemplateId(candidate);
  const template = PROPOSAL_TEMPLATES.find((t) => t.id === templateId)!;
  const now = new Date().toISOString();
  return {
    id: crypto.randomUUID(),
    templateId: template.id,
    title: candidate.actionHint || candidate.reason || candidate.entityType,
    intent: candidate.reason,
    category: template.category,
    riskLevel: template.riskLevel,
    requiredReview: true,
    externalWrite: false,
    checks: template.suggestedChecks,
    status: 'proposed',
    createdAt: now,
    updatedAt: now,
    source: 'worldloops.local',
    idempotencyKey: candidate.idempotencyKey,
  };
}
