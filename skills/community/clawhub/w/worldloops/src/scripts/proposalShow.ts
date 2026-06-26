import { findProposalById, listProposals } from '../storage/proposals';
import type { Proposal } from '../types/proposal';

function printJson(value: unknown): void {
  console.log(JSON.stringify(value, null, 2));
}

function printHuman(proposal: Proposal): void {
  console.log(`Proposal: ${proposal.id}`);
  console.log(`  Template:         ${proposal.templateId}`);
  console.log(`  Title:            ${proposal.title}`);
  console.log(`  Status:           ${proposal.status}`);
  console.log(`  Category:         ${proposal.category}`);
  console.log(`  Risk level:       ${proposal.riskLevel}`);
  if (proposal.idempotencyKey) {
    console.log(`  IdempotencyKey:   ${proposal.idempotencyKey}`);
  }
  console.log(`  requiredReview:   true`);
  console.log(`  externalWrite:    false`);
  console.log(`  Created at:       ${proposal.createdAt}`);
  console.log(`  Updated at:       ${proposal.updatedAt}`);
  console.log(`  Source:           ${proposal.source}`);
  console.log('');
  console.log('  Intent:');
  console.log(`    ${proposal.intent}`);
  console.log('');
  console.log('  Suggested checks:');
  for (const check of proposal.checks) {
    console.log(`    - ${check}`);
  }
  console.log('');
  console.log('externalWrite: false');
}

function main(): void {
  const args = process.argv.slice(2);
  const jsonMode = args.includes('--json');
  const proposalId = args.find((a) => !a.startsWith('--'));

  if (!proposalId) {
    printJson({
      ok: false,
      error: {
        code: 'MISSING_PROPOSAL_ID',
        message: 'Usage: npm run proposal:show -- <proposalId> [--json]',
      },
      safety: { externalWrite: false },
    });
    process.exit(1);
  }

  const proposal = findProposalById(proposalId);

  if (!proposal) {
    const all = listProposals();
    printJson({
      ok: false,
      error: {
        code: 'PROPOSAL_NOT_FOUND',
        message: `Proposal not found: ${proposalId}`,
        availableProposalIds: all.map((p) => ({ id: p.id, templateId: p.templateId, status: p.status })),
      },
      safety: { externalWrite: false },
    });
    process.exit(1);
  }

  if (jsonMode) {
    printJson({
      ok: true,
      source: 'worldloops.local',
      proposal,
      safety: { externalWrite: false },
    });
  } else {
    printHuman(proposal);
  }
}

main();
