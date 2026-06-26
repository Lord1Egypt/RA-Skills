import * as crypto from 'node:crypto';
import { findProposalById, listProposals } from '../storage/proposals';
import { saveExecutionPlan, getExecutionPlansPath } from '../storage/executionPlans';
import type { ExecutionPlan, ExecutionPlanStep, ExecutionPlanStepType } from '../types/executionPlan';
import type { ProposalRiskLevel, ProposalTemplateCategory } from '../types/proposalTemplate';

function printJson(value: unknown): void {
  console.log(JSON.stringify(value, null, 2));
}

function makeStep(
  type: ExecutionPlanStepType,
  title: string,
  description: string
): ExecutionPlanStep {
  return {
    id: crypto.randomUUID(),
    title,
    type,
    description,
    externalWrite: false,
  };
}

function buildSteps(
  templateId: string,
  category: ProposalTemplateCategory,
  riskLevel: ProposalRiskLevel
): ExecutionPlanStep[] {
  const steps: ExecutionPlanStep[] = [
    makeStep(
      'review',
      'Review approved proposal',
      `Confirm the approved proposal (templateId: ${templateId}, category: ${category}) is still valid before any further steps.`
    ),
    makeStep(
      'boundary_check',
      'Check capability boundary',
      'Verify this plan does not require capabilities beyond the local execution boundary. externalWrite must remain false.'
    ),
    makeStep(
      'prepare',
      'Prepare dry-run preview',
      'Assemble a dry-run description of what execution would require. No external action is taken at this step.'
    ),
  ];

  if (riskLevel === 'high' || riskLevel === 'critical') {
    steps.push(
      makeStep(
        'dry_run',
        'Dry-run validation',
        `Risk level is "${riskLevel}". Perform an additional dry-run validation pass before marking receipt-ready.`
      )
    );
  }

  steps.push(
    makeStep(
      'receipt_ready',
      'Mark receipt-ready',
      'Record that a local execution plan preview has been generated. This does not execute anything. externalWrite:false.'
    )
  );

  return steps;
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
        message: 'Usage: npm run plan:create -- <proposal-id> [--json]',
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

  if (proposal.status !== 'approved') {
    printJson({
      ok: false,
      error: {
        code: 'PROPOSAL_NOT_APPROVED',
        message: `Cannot create an execution plan for a proposal with status "${proposal.status}". Only approved proposals can become execution plans.`,
        currentStatus: proposal.status,
        requiredStatus: 'approved',
      },
      safety: { externalWrite: false },
    });
    process.exit(1);
  }

  const now = new Date().toISOString();
  const steps = buildSteps(proposal.templateId, proposal.category, proposal.riskLevel);

  const plan: ExecutionPlan = {
    id: crypto.randomUUID(),
    proposalId: proposal.id,
    templateId: proposal.templateId,
    title: `Execution Plan Preview: ${proposal.title}`,
    status: 'planned',
    riskLevel: proposal.riskLevel,
    steps,
    externalWrite: false,
    createdAt: now,
    updatedAt: now,
    source: 'worldloops.local',
  };

  saveExecutionPlan(plan);

  if (jsonMode) {
    printJson({
      ok: true,
      source: 'worldloops.local',
      path: getExecutionPlansPath(),
      plan,
      safety: { externalWrite: false },
    });
  } else {
    console.log(`Execution plan created: ${plan.id}`);
    console.log(`  Proposal:      ${plan.proposalId}`);
    console.log(`  Template:      ${plan.templateId}`);
    console.log(`  Title:         ${plan.title}`);
    console.log(`  Status:        ${plan.status}`);
    console.log(`  Risk level:    ${plan.riskLevel}`);
    console.log(`  Steps:         ${plan.steps.length}`);
    console.log(`  externalWrite: false`);
    console.log(`  Created at:    ${plan.createdAt}`);
    console.log(`  Stored at:     ${getExecutionPlansPath()}`);
    console.log('');
    console.log('Plan ≠ Execution. No external writes.');
    console.log('externalWrite: false');
  }
}

main();
