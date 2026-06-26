import { PROPOSAL_TEMPLATES } from '../data/proposalTemplates';
import type { ProposalTemplate } from '../types/proposalTemplate';

function printJson(value: unknown): void {
  console.log(JSON.stringify(value, null, 2));
}

function printHuman(templates: ProposalTemplate[]): void {
  console.log('Proposal Templates');
  console.log('');
  console.log(`Available templates: ${templates.length}`);
  console.log('');

  for (const t of templates) {
    console.log(`  ${t.id}`);
    console.log(`    Title:          ${t.title}`);
    console.log(`    Description:    ${t.description}`);
    console.log(`    Category:       ${t.category}`);
    console.log(`    Risk level:     ${t.riskLevel}`);
    console.log(`    externalWrite:  false`);
    console.log(`    requiredReview: true`);
    console.log('');
  }

  console.log('externalWrite: false');
}

function main(): void {
  const args = process.argv.slice(2);
  const jsonMode = args.includes('--json');

  if (jsonMode) {
    printJson({
      ok: true,
      source: 'worldloops.local',
      count: PROPOSAL_TEMPLATES.length,
      templates: PROPOSAL_TEMPLATES,
      safety: { externalWrite: false },
    });
  } else {
    printHuman(PROPOSAL_TEMPLATES);
  }
}

main();
