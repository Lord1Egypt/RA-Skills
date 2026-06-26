import * as crypto from 'node:crypto';
import { PROPOSAL_TEMPLATES } from '../data/proposalTemplates';
import { saveProposal, getProposalsPath } from '../storage/proposals';
import type { Proposal } from '../types/proposal';
import type { ProposalTemplateId } from '../types/proposalTemplate';

function printJson(value: unknown): void {
  console.log(JSON.stringify(value, null, 2));
}

function main(): void {
  const args = process.argv.slice(2);
  const jsonMode = args.includes('--json');
  const templateId = args.find((a) => !a.startsWith('--')) as ProposalTemplateId | undefined;

  if (!templateId) {
    printJson({
      ok: false,
      error: {
        code: 'MISSING_TEMPLATE_ID',
        message: 'Usage: npm run proposal:create -- <template-id> [--json]',
        availableTemplateIds: PROPOSAL_TEMPLATES.map((t) => t.id),
      },
      safety: { externalWrite: false },
    });
    process.exit(1);
  }

  const template = PROPOSAL_TEMPLATES.find((t) => t.id === templateId);

  if (!template) {
    printJson({
      ok: false,
      error: {
        code: 'PROPOSAL_TEMPLATE_NOT_FOUND',
        message: `Proposal template not found: ${templateId}`,
        availableTemplateIds: PROPOSAL_TEMPLATES.map((t) => t.id),
      },
      safety: { externalWrite: false },
    });
    process.exit(1);
  }

  const now = new Date().toISOString();

  const proposal: Proposal = {
    id: crypto.randomUUID(),
    templateId: template.id,
    title: template.title,
    intent: template.description,
    category: template.category,
    riskLevel: template.riskLevel,
    requiredReview: true,
    externalWrite: false,
    checks: template.suggestedChecks,
    status: 'proposed',
    createdAt: now,
    updatedAt: now,
    source: 'worldloops.local',
  };

  saveProposal(proposal);

  if (jsonMode) {
    printJson({
      ok: true,
      source: 'worldloops.local',
      path: getProposalsPath(),
      proposal,
      safety: { externalWrite: false },
    });
  } else {
    console.log(`Proposal created: ${proposal.id}`);
    console.log(`  Template:       ${proposal.templateId}`);
    console.log(`  Title:          ${proposal.title}`);
    console.log(`  Status:         ${proposal.status}`);
    console.log(`  Risk level:     ${proposal.riskLevel}`);
    console.log(`  Category:       ${proposal.category}`);
    console.log(`  requiredReview: true`);
    console.log(`  externalWrite:  false`);
    console.log(`  Created at:     ${proposal.createdAt}`);
    console.log(`  Stored at:      ${getProposalsPath()}`);
    console.log('');
    console.log('externalWrite: false');
  }
}

main();
