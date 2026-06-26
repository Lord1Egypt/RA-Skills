import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';
import { listCommunities, getCommunity } from './commands/communities';
import { listSpaces, getSpace } from './commands/spaces';
import { createPost, listPosts, getPost, updatePost, deletePost, reschedulePost, publishNow, bulkSchedule } from './commands/posts';
import { listWorkflows, getWorkflow, createWorkflow, updateWorkflow, deleteWorkflow, toggleWorkflow, runWorkflow, listWorkflowRuns, testWorkflow, getWorkflowRegistry } from './commands/workflows';
import { listSequences, getSequence, createSequence, updateSequence, deleteSequence, toggleSequence, enrollMember, listEnrollments, manageEnrollment, getStepTypes } from './commands/sequences';
import { listWebhooks, createWebhook, deleteWebhook } from './commands/webhooks';
import type { Argv } from 'yargs';

yargs(hideBin(process.argv))
  .scriptName('stickyhive')
  .usage('$0 <command> [options]')

  // ── Communities ──────────────────────────────────────────────
  .command('communities:list', 'List all communities in your organization', {}, listCommunities as any)
  .command(
    'communities:get <id>',
    'Get a community by ID',
    (y: Argv) => y.positional('id', { type: 'number', demandOption: true }),
    getCommunity as any,
  )

  // ── Spaces ──────────────────────────────────────────────────
  .command('spaces:list', 'List all spaces (posting destinations)', {}, listSpaces as any)
  .command(
    'spaces:get <id>',
    'Get a space by ID',
    (y: Argv) => y.positional('id', { type: 'number', demandOption: true }),
    getSpace as any,
  )

  // ── Scheduled Posts ─────────────────────────────────────────
  .command(
    'posts:create',
    'Create a scheduled post or draft',
    (y: Argv) =>
      y
        .option('title', { alias: 't', type: 'string', demandOption: true, describe: 'Post title' })
        .option('content', { alias: 'c', type: 'string', demandOption: true, describe: 'Post body content' })
        .option('spaceId', { alias: 'i', type: 'number', demandOption: true, describe: 'Space ID to post to' })
        .option('date', { alias: 's', type: 'string', describe: 'Scheduled time (ISO 8601). Omit for draft.' })
        .option('pin', { type: 'boolean', default: false, describe: 'Pin on publish (Skool only)' })
        .option('comment', { type: 'string', describe: 'First comment text' })
        .option('poll', { type: 'string', describe: 'Poll options as JSON array or comma-separated' })
        .example('$0 posts:create -t "Hello" -c "World" -i 42 -s "2026-06-01T09:00:00Z"', 'Schedule a post')
        .example('$0 posts:create -t "Draft" -c "Content" -i 42', 'Save as draft'),
    createPost as any,
  )
  .command(
    'posts:list',
    'List scheduled posts with optional filters',
    (y: Argv) =>
      y
        .option('status', { type: 'string', choices: ['pending', 'publishing', 'published', 'failed', 'expired'] })
        .option('draft', { type: 'boolean', describe: 'Filter drafts' })
        .option('spaceId', { type: 'number', describe: 'Filter by space' })
        .option('dateFrom', { type: 'string', describe: 'Start date (ISO 8601)' })
        .option('dateTo', { type: 'string', describe: 'End date (ISO 8601)' }),
    listPosts as any,
  )
  .command(
    'posts:get <id>',
    'Get a scheduled post by ID',
    (y: Argv) => y.positional('id', { type: 'number', demandOption: true }),
    getPost as any,
  )
  .command(
    'posts:update <id>',
    'Update a scheduled post',
    (y: Argv) =>
      y
        .positional('id', { type: 'number', demandOption: true })
        .option('data', { alias: 'd', type: 'string', demandOption: true, describe: 'JSON object with fields to update' })
        .example('$0 posts:update 123 -d \'{"title":"New title"}\'', 'Update title'),
    updatePost as any,
  )
  .command(
    'posts:delete <id>',
    'Delete a scheduled post',
    (y: Argv) => y.positional('id', { type: 'number', demandOption: true }),
    deletePost as any,
  )
  .command(
    'posts:reschedule <id>',
    'Change the scheduled time of a post',
    (y: Argv) =>
      y
        .positional('id', { type: 'number', demandOption: true })
        .option('date', { alias: 's', type: 'string', demandOption: true, describe: 'New scheduled time (ISO 8601)' }),
    reschedulePost as any,
  )
  .command(
    'posts:publish <id>',
    'Queue a post for immediate publishing',
    (y: Argv) => y.positional('id', { type: 'number', demandOption: true }),
    publishNow as any,
  )
  .command(
    'posts:bulk-schedule',
    'Schedule multiple draft posts with even spacing',
    (y: Argv) =>
      y
        .option('ids', { type: 'string', demandOption: true, describe: 'Comma-separated post IDs' })
        .option('startTime', { type: 'string', demandOption: true, describe: 'Start time (ISO 8601)' })
        .option('interval', { type: 'number', default: 1, describe: 'Hours between posts' }),
    bulkSchedule as any,
  )

  // ── Workflows ───────────────────────────────────────────────
  .command(
    'workflows:list',
    'List workflows for a community',
    (y: Argv) => y.option('communityId', { alias: 'C', type: 'number', demandOption: true }),
    listWorkflows as any,
  )
  .command(
    'workflows:get <id>',
    'Get workflow details with run stats',
    (y: Argv) =>
      y
        .positional('id', { type: 'number', demandOption: true })
        .option('communityId', { alias: 'C', type: 'number', demandOption: true }),
    getWorkflow as any,
  )
  .command(
    'workflows:create',
    'Create a new custom workflow',
    (y: Argv) =>
      y
        .option('communityId', { alias: 'C', type: 'number', demandOption: true })
        .option('name', { alias: 'n', type: 'string', demandOption: true })
        .option('config', { type: 'string', demandOption: true, describe: 'Workflow config as JSON string' })
        .option('dailyLimit', { type: 'number', default: 50 }),
    createWorkflow as any,
  )
  .command(
    'workflows:update <id>',
    'Update a workflow',
    (y: Argv) =>
      y
        .positional('id', { type: 'number', demandOption: true })
        .option('communityId', { alias: 'C', type: 'number', demandOption: true })
        .option('data', { alias: 'd', type: 'string', demandOption: true, describe: 'JSON with fields to update' }),
    updateWorkflow as any,
  )
  .command(
    'workflows:delete <id>',
    'Soft-delete a workflow',
    (y: Argv) =>
      y
        .positional('id', { type: 'number', demandOption: true })
        .option('communityId', { alias: 'C', type: 'number', demandOption: true }),
    deleteWorkflow as any,
  )
  .command(
    'workflows:toggle <id>',
    'Enable or disable a workflow',
    (y: Argv) =>
      y
        .positional('id', { type: 'number', demandOption: true })
        .option('communityId', { alias: 'C', type: 'number', demandOption: true }),
    toggleWorkflow as any,
  )
  .command(
    'workflows:run <id>',
    'Manually trigger a workflow',
    (y: Argv) =>
      y
        .positional('id', { type: 'number', demandOption: true })
        .option('communityId', { alias: 'C', type: 'number', demandOption: true }),
    runWorkflow as any,
  )
  .command(
    'workflows:runs <id>',
    'Get run history for a workflow',
    (y: Argv) =>
      y
        .positional('id', { type: 'number', demandOption: true })
        .option('communityId', { alias: 'C', type: 'number', demandOption: true })
        .option('limit', { type: 'number', default: 20 }),
    listWorkflowRuns as any,
  )
  .command(
    'workflows:test <id>',
    'Dry-run a workflow and preview actions',
    (y: Argv) =>
      y
        .positional('id', { type: 'number', demandOption: true })
        .option('communityId', { alias: 'C', type: 'number', demandOption: true })
        .option('triggerData', { type: 'string', describe: 'Sample trigger data as JSON' }),
    testWorkflow as any,
  )
  .command(
    'workflows:registry',
    'Get available triggers, actions, conditions, and operators',
    (y: Argv) => y.option('platform', { type: 'string', default: 'skool', choices: ['skool', 'circle', 'mighty', 'discord', 'slack'] }),
    getWorkflowRegistry as any,
  )

  // ── Sequences ───────────────────────────────────────────────
  .command(
    'sequences:list',
    'List DM sequences for a community',
    (y: Argv) => y.option('communityId', { alias: 'C', type: 'number', demandOption: true }),
    listSequences as any,
  )
  .command(
    'sequences:get <id>',
    'Get sequence details with steps and enrollment stats',
    (y: Argv) =>
      y
        .positional('id', { type: 'number', demandOption: true })
        .option('communityId', { alias: 'C', type: 'number', demandOption: true }),
    getSequence as any,
  )
  .command(
    'sequences:create',
    'Create a new DM sequence',
    (y: Argv) =>
      y
        .option('communityId', { alias: 'C', type: 'number', demandOption: true })
        .option('name', { alias: 'n', type: 'string', demandOption: true })
        .option('description', { type: 'string' })
        .option('steps', { type: 'string', describe: 'Step tree as JSON' }),
    createSequence as any,
  )
  .command(
    'sequences:update <id>',
    'Update a sequence',
    (y: Argv) =>
      y
        .positional('id', { type: 'number', demandOption: true })
        .option('communityId', { alias: 'C', type: 'number', demandOption: true })
        .option('data', { alias: 'd', type: 'string', demandOption: true, describe: 'JSON with fields to update' }),
    updateSequence as any,
  )
  .command(
    'sequences:delete <id>',
    'Soft-delete a sequence',
    (y: Argv) =>
      y
        .positional('id', { type: 'number', demandOption: true })
        .option('communityId', { alias: 'C', type: 'number', demandOption: true }),
    deleteSequence as any,
  )
  .command(
    'sequences:toggle <id>',
    'Enable or disable a sequence',
    (y: Argv) =>
      y
        .positional('id', { type: 'number', demandOption: true })
        .option('communityId', { alias: 'C', type: 'number', demandOption: true }),
    toggleSequence as any,
  )
  .command(
    'sequences:enroll <id>',
    'Enroll a member in a sequence',
    (y: Argv) =>
      y
        .positional('id', { type: 'number', demandOption: true })
        .option('communityId', { alias: 'C', type: 'number', demandOption: true })
        .option('memberId', { alias: 'm', type: 'string', demandOption: true, describe: 'Platform ID or numeric ID' }),
    enrollMember as any,
  )
  .command(
    'sequences:enrollments <id>',
    'List enrollments for a sequence',
    (y: Argv) =>
      y
        .positional('id', { type: 'number', demandOption: true })
        .option('communityId', { alias: 'C', type: 'number', demandOption: true })
        .option('status', { type: 'string', choices: ['active', 'paused', 'completed', 'exited', 'cancelled'] }),
    listEnrollments as any,
  )
  .command(
    'sequences:manage-enrollment',
    'Pause, resume, or cancel an enrollment',
    (y: Argv) =>
      y
        .option('sequenceId', { type: 'number', demandOption: true })
        .option('enrollmentId', { type: 'number', demandOption: true })
        .option('communityId', { alias: 'C', type: 'number', demandOption: true })
        .option('action', { alias: 'a', type: 'string', demandOption: true, choices: ['pause', 'resume', 'cancel'] }),
    manageEnrollment as any,
  )
  .command('sequences:step-types', 'Get available step types for building sequences', {}, getStepTypes as any)

  // ── Webhooks ────────────────────────────────────────────────
  .command('webhooks:list', 'List registered webhook endpoints', {}, listWebhooks as any)
  .command(
    'webhooks:create',
    'Register a webhook endpoint',
    (y: Argv) =>
      y
        .option('url', { alias: 'u', type: 'string', demandOption: true })
        .option('events', { alias: 'e', type: 'string', demandOption: true, describe: 'Comma-separated events or * for all' }),
    createWebhook as any,
  )
  .command(
    'webhooks:delete <id>',
    'Delete a webhook endpoint',
    (y: Argv) => y.positional('id', { type: 'number', demandOption: true }),
    deleteWebhook as any,
  )

  .demandCommand(1, 'You need at least one command')
  .help()
  .alias('h', 'help')
  .version()
  .alias('v', 'version')
  .epilogue(
    'For more information, visit: https://stickyhive.com\n\n' +
    'Authentication:\n' +
    '  export STICKYHIVE_API_KEY=hm_live_...\n\n' +
    'All commands output structured JSON for AI agent consumption.'
  )
  .parse();
