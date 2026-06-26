#!/usr/bin/env node
/**
 * Batch Scheduling for Publishing
 * Batch create scheduled publishing tasks based on a weekly plan file
 *
 * Usage:
 *   node scripts/schedule_batch.js --plan-file ./output/weekly_plan.json
 */

const path = require('path');
const fs = require('fs');

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].replace(/^--/, '');
      const val = args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : 'true';
      opts[key] = val;
      if (val !== 'true') i++;
    }
  }
  return opts;
}

function validatePlan(plan) {
  const errors = [];
  if (!plan.week) errors.push('Missing week field');
  if (!plan.posts || !Array.isArray(plan.posts)) errors.push('Missing posts array');
  if (plan.posts) {
    plan.posts.forEach((post, i) => {
      if (!post.schedule) errors.push(`Post ${i + 1} is missing schedule`);
      if (!post.platforms) errors.push(`Post ${i + 1} is missing platforms`);
      if (!post.contentFile && !post.topic) errors.push(`Post ${i + 1} is missing contentFile or topic`);
    });
  }
  return errors;
}

function buildCronJobs(plan) {
  const jobs = [];
  const publishScript = path.join(__dirname, 'publish.js');
  const generateScript = path.join(__dirname, 'generate_content.js');

  for (let i = 0; i < plan.posts.length; i++) {
    const post = plan.posts[i];
    const platforms = Array.isArray(post.platforms) ? post.platforms.join(',') : post.platforms;

    let message;
    if (post.contentFile) {
      message = `Publish social media content:\nnode ${publishScript} --platforms "${platforms}" --content-file "${post.contentFile}"`;
    } else {
      const contentFile = path.join(__dirname, '..', '..', '..', 'output', `batch_${Date.now()}_${i}.json`);
      message = `Generate content first, then publish:\n1. node ${generateScript} --topic "${post.topic}" --platforms "${platforms}" --tone "${post.tone || 'default'}" \n2. node ${publishScript} --platforms "${platforms}" --content-file "${contentFile}"`;
    }

    jobs.push({
      name: `social-batch-${plan.week}-${i + 1}`,
      schedule: {
        kind: 'at',
        at: new Date(post.schedule).toISOString(),
      },
      payload: {
        kind: 'agentTurn',
        message,
      },
      delivery: { mode: 'announce' },
      deleteAfterRun: true,
      enabled: true,
      meta: {
        topic: post.topic || 'from file',
        platforms,
        schedule: post.schedule,
      },
    });
  }

  return jobs;
}

function main() {
  const opts = parseArgs();

  if (!opts['plan-file']) {
    console.error('Usage: node schedule_batch.js --plan-file ./output/weekly_plan.json');
    process.exit(1);
  }

  const planFile = path.resolve(opts['plan-file']);
  if (!fs.existsSync(planFile)) {
    console.error(`[error] File does not exist: ${planFile}`);
    process.exit(1);
  }

  const plan = JSON.parse(fs.readFileSync(planFile, 'utf-8'));
  const errors = validatePlan(plan);
  if (errors.length > 0) {
    console.error('[error] Plan file format errors:');
    errors.forEach(e => console.error(`  - ${e}`));
    console.error('Refer to template: assets/templates/weekly_plan.json');
    process.exit(1);
  }

  const jobs = buildCronJobs(plan);

  console.log(`─── Batch Schedule: ${plan.week} ───`);
  console.log(`Total ${jobs.length} publishing task(s):\n`);

  jobs.forEach((job, i) => {
    const d = new Date(job.meta.schedule);
    console.log(`  [${i + 1}] ${job.meta.topic}`);
    console.log(`      Platform(s): ${job.meta.platforms}`);
    console.log(`      Time: ${d.toLocaleString('en-US', { timeZone: 'Asia/Shanghai' })}`);
  });

  // Output cron job configuration
  const outputFile = path.join(__dirname, '..', '..', '..', 'output', `cron_jobs_${Date.now()}.json`);
  const outputDir = path.dirname(outputFile);
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });
  fs.writeFileSync(outputFile, JSON.stringify(jobs, null, 2));

  console.log(`\nCron job configuration saved: ${outputFile}`);
  console.log('\nPlease register these tasks using the OpenClaw cron tool');
}

main();