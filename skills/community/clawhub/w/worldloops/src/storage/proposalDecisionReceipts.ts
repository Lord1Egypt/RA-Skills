import * as fs from 'node:fs';
import * as path from 'node:path';
import type { ProposalDecisionReceipt } from '../types/proposalDecisionReceipt';

function getWorldLoopsDir(): string {
  return process.env.WORLDLOOPS_DIR ?? path.join(process.cwd(), '.worldloops');
}

export function getProposalDecisionReceiptsPath(): string {
  return path.join(getWorldLoopsDir(), 'proposal_decision_receipts.json');
}

export function loadProposalDecisionReceipts(): ProposalDecisionReceipt[] {
  const receiptsPath = getProposalDecisionReceiptsPath();
  if (!fs.existsSync(receiptsPath)) {
    return [];
  }
  return JSON.parse(fs.readFileSync(receiptsPath, 'utf8')) as ProposalDecisionReceipt[];
}

export function saveProposalDecisionReceipt(receipt: ProposalDecisionReceipt): void {
  const receiptsPath = getProposalDecisionReceiptsPath();
  const dir = path.dirname(receiptsPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  const existing = loadProposalDecisionReceipts();
  const upserted = existing.filter((r) => r.id !== receipt.id);
  upserted.push(receipt);
  fs.writeFileSync(receiptsPath, JSON.stringify(upserted, null, 2) + '\n', 'utf8');
}

export function listProposalDecisionReceipts(): ProposalDecisionReceipt[] {
  return loadProposalDecisionReceipts();
}

export function findProposalDecisionReceiptById(id: string): ProposalDecisionReceipt | null {
  return loadProposalDecisionReceipts().find((r) => r.id === id) ?? null;
}
