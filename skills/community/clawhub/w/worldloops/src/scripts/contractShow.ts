import { findExecutionContractById, listExecutionContracts } from '../storage/executionContracts';
import type { ExecutionContract } from '../types/executionContract';

function printJson(value: unknown): void {
  console.log(JSON.stringify(value, null, 2));
}

function printHuman(contract: ExecutionContract): void {
  console.log(`Execution Contract: ${contract.id}`);
  console.log(`  Plan:          ${contract.planId}`);
  console.log(`  Proposal:      ${contract.proposalId}`);
  console.log(`  Template:      ${contract.templateId}`);
  console.log(`  Title:         ${contract.title}`);
  console.log(`  Status:        ${contract.status}`);
  console.log(`  Risk level:    ${contract.riskLevel}`);
  console.log(`  externalWrite: false`);
  console.log(`  Created at:    ${contract.createdAt}`);
  console.log(`  Updated at:    ${contract.updatedAt}`);
  console.log(`  Source:        ${contract.source}`);
  console.log('');
  console.log('  Execution Boundary:');
  console.log(`    externalWrite:    false`);
  console.log(`    allowedBoundary:  ${contract.executionBoundary.allowedBoundary}`);
  console.log(`    deniedCapabilities:`);
  for (const cap of contract.executionBoundary.deniedCapabilities) {
    console.log(`      - ${cap}`);
  }
  console.log(`    reason: ${contract.executionBoundary.reason}`);
  console.log('');
  console.log('  Preconditions:');
  for (const pre of contract.preconditions) {
    const mark = pre.satisfied ? '✓' : '✗';
    console.log(`    [${mark}] ${pre.description}`);
    console.log(`        required: ${pre.required}`);
  }
  console.log('');
  console.log('  Required Approvals:');
  for (const approval of contract.requiredApprovals) {
    const mark = approval.satisfied ? '✓' : '✗';
    console.log(`    [${mark}] role: ${approval.role}`);
    console.log(`        required: ${approval.required}`);
    console.log(`        reason: ${approval.reason}`);
  }
  console.log('');
  console.log('  Rollback Plan:');
  console.log(`    available: ${contract.rollbackPlan.available}`);
  console.log(`    reason: ${contract.rollbackPlan.reason}`);
  console.log('');
  console.log('  Audit:');
  console.log(`    proposalExists:       ${contract.audit.proposalExists}`);
  console.log(`    proposalApproved:     ${contract.audit.proposalApproved}`);
  console.log(`    decisionReceiptExists: ${contract.audit.decisionReceiptExists}`);
  console.log(`    planExists:           ${contract.audit.planExists}`);
  console.log(`    planStatus:           ${contract.audit.planStatus}`);
  console.log(`    externalWrite:        false`);
  console.log('');
  console.log('externalWrite: false');
}

function main(): void {
  const args = process.argv.slice(2);
  const jsonMode = args.includes('--json');
  const contractId = args.find((a) => !a.startsWith('--'));

  if (!contractId) {
    printJson({
      ok: false,
      error: {
        code: 'MISSING_CONTRACT_ID',
        message: 'Usage: npm run contract:show -- <contract-id> [--json]',
      },
      safety: { externalWrite: false },
    });
    process.exit(1);
  }

  const contract = findExecutionContractById(contractId);

  if (!contract) {
    const all = listExecutionContracts();
    printJson({
      ok: false,
      error: {
        code: 'EXECUTION_CONTRACT_NOT_FOUND',
        message: `Execution contract not found: ${contractId}`,
        availableContractIds: all.map((c) => ({ id: c.id, planId: c.planId, status: c.status })),
      },
      safety: { externalWrite: false },
    });
    process.exit(1);
  }

  if (jsonMode) {
    printJson({
      ok: true,
      source: 'worldloops.local',
      contract,
      safety: { externalWrite: false },
    });
  } else {
    printHuman(contract);
  }
}

main();
