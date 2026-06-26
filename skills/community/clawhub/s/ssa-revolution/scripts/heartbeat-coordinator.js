#!/usr/bin/env node

/**
 * Coordinator Heartbeat — drives the full evolution loop.
 * 
 * Each tick processes one task through the complete cycle:
 * pending → Reviewer → reviewed → Executor → Auditor → pending (next) or completed
 * 
 * The coordinator spawns 3 sub-agent roles:
 * - Reviewer: pre-execution review, generates instructions
 * - Executor: implements one subtask
 * - Auditor: post-execution quality check, decides pass/retry
 * 
 * CLI usage:
 *   node heartbeat-coordinator.js                           # scan + process one task
 *   node heartbeat-coordinator.js --phase review            # only review
 *   node heartbeat-coordinator.js --phase execute           # only execute
 *   node heartbeat-coordinator.js --phase audit             # only audit
 *   node heartbeat-coordinator.js apply-review <task> <result>
 *   node heartbeat-coordinator.js apply-exec <task> <result>
 *   node heartbeat-coordinator.js apply-audit <task> <result>
 */

const fs = require('fs');
const path = require('path');

// Workspace resolution
const WORKSPACE = process.env.OPENCLAW_WORKSPACE || process.env.WORKSPACE || path.join(require('os').homedir(), '.openclaw', 'agents', 'main', 'workspace');
const TASKS_DIR = process.env.EVOLUTION_TASKS_DIR || path.join(WORKSPACE, 'evolution', 'tasks');
const LOCK_FILE = path.join(TASKS_DIR, '.coordinator.lock');
const LOCK_TIMEOUT_MS = 10 * 60 * 1000;

// ==================== Lock ====================

function acquireLock() {
  try {
    if (fs.existsSync(LOCK_FILE)) {
      const lockData = JSON.parse(fs.readFileSync(LOCK_FILE, 'utf8'));
      const age = Date.now() - lockData.timestamp;
      if (age < LOCK_TIMEOUT_MS) {
        console.log(`⏳ Locked (${Math.round(age / 1000)}s ago), skipping`);
        return false;
      }
      console.log(`⚠️ Lock expired, force-acquiring`);
    }
    fs.writeFileSync(LOCK_FILE, JSON.stringify({ timestamp: Date.now(), pid: process.pid }));
    return true;
  } catch (err) {
    console.error('❌ Lock failed:', err.message);
    return false;
  }
}

function releaseLock() {
  try {
    if (fs.existsSync(LOCK_FILE)) fs.unlinkSync(LOCK_FILE);
  } catch (err) {}
}

// ==================== Task Scanning ====================

function scanTasks() {
  if (!fs.existsSync(TASKS_DIR)) return [];
  const tasks = [];
  const files = fs.readdirSync(TASKS_DIR).filter(f => f.endsWith('.json') && f.startsWith('task-'));
  for (const file of files) {
    try {
      const data = JSON.parse(fs.readFileSync(path.join(TASKS_DIR, file), 'utf8'));
      tasks.push({ file, ...data });
    } catch (err) {
      console.error(`⚠️ Read ${file} failed:`, err.message);
    }
  }
  return tasks;
}

function selectNextTask(tasks) {
  // Priority: reviewed (needs exec) > pending (needs review) > executing (needs audit)
  const reviewed = tasks.filter(t => t.status === 'reviewed');
  if (reviewed.length > 0) {
    reviewed.sort((a, b) => a.task_id.localeCompare(b.task_id));
    return { task: reviewed[0], phase: 'execute' };
  }
  
  const executing = tasks.filter(t => t.status === 'executing');
  if (executing.length > 0) {
    executing.sort((a, b) => a.task_id.localeCompare(b.task_id));
    return { task: executing[0], phase: 'audit' };
  }
  
  const pending = tasks.filter(t => t.status === 'pending');
  if (pending.length > 0) {
    const priorityOrder = { urgent: 0, high: 1, medium: 2, low: 3 };
    pending.sort((a, b) => {
      const pa = priorityOrder[a.priority] ?? 99;
      const pb = priorityOrder[b.priority] ?? 99;
      if (pa !== pb) return pa - pb;
      return a.task_id.localeCompare(b.task_id);
    });
    return { task: pending[0], phase: 'review' };
  }
  
  return null;
}

// ==================== Phase: Review ====================

function buildReviewPrompt(task) {
  const iteration = (task.current_iteration || 0) + 1;
  const subtasks = task.context?.subtasks || [];
  const lastResult = task.result || {};
  const completedStep = lastResult.subtask_completed || 0;
  const nextStep = completedStep + 1;
  
  let prompt = `You are a Reviewer for the auto-evolution system.

## Task
- **ID:** ${task.task_id}
- **Goal:** ${task.goal}
- **Iteration:** ${iteration} / ${task.max_iterations}
- **Progress:** ${completedStep} / ${subtasks.length} subtasks

## Subtasks
${subtasks.map((s, i) => `${i + 1}. ${s}`).join('\n')}

## Previous Result
${lastResult.summary || '(First iteration)'}
`;

  if (completedStep >= subtasks.length) {
    prompt += `
## All subtasks completed — finalize
Set verdict to "complete" and summarize the outcome.
`;
  } else {
    prompt += `
## Your Job
1. Review previous result (if any)
2. Decide: approve / revise / reject
3. Write specific instructions for subtask ${nextStep}
4. Define acceptance criteria

## Output (strict JSON)
\`\`\`json
{
  "verdict": "approve",
  "feedback": "Review comments",
  "next_instructions": {
    "summary": "Iteration ${iteration}: Step ${nextStep}",
    "current_step": ${nextStep},
    "total_steps": ${subtasks.length},
    "step": {
      "step": ${nextStep},
      "action": "${subtasks[nextStep - 1] || ''}",
      "detail": "Implementation details..."
    },
    "acceptance_criteria": ["Criterion 1", "Criterion 2"]
  }
}
\`\`\`

Output only JSON.
`;
  }

  return prompt;
}

function applyReview(task, reviewResult) {
  const filePath = path.join(TASKS_DIR, task.file);
  const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  const now = new Date().toISOString();
  
  let review;
  try {
    const jsonMatch = reviewResult.match(/```json\s*([\s\S]*?)\s*```/) || 
                      reviewResult.match(/\{[\s\S]*"verdict"[\s\S]*\}/);
    const jsonStr = jsonMatch ? (jsonMatch[1] || jsonMatch[0]) : reviewResult;
    review = JSON.parse(jsonStr);
  } catch (err) {
    console.error('⚠️ Parse review failed:', err.message);
    review = { verdict: 'approve', feedback: reviewResult, next_instructions: null };
  }
  
  if (review.verdict === 'complete') {
    data.status = 'completed';
    data.review = { verdict: 'complete', reviewed_at: now, feedback: review.feedback };
  } else {
    data.status = 'reviewed';
    data.current_iteration = (data.current_iteration || 0) + 1;
    data.review = {
      verdict: review.verdict || 'approve',
      reviewed_at: now,
      feedback: review.feedback || '',
      next_instructions: review.next_instructions || null
    };
  }
  
  data.updated_at = now;
  if (!data.history) data.history = [];
  data.history.push({
    timestamp: now,
    action: `iteration_${data.current_iteration || 0}_reviewed`,
    role: 'reviewer',
    verdict: review.verdict,
    notes: review.feedback || `Review: ${review.verdict}`
  });
  
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
  console.log(`✅ Task ${task.task_id} reviewed: ${review.verdict}`);
  return review.verdict;
}

// ==================== Phase: Execute ====================

function buildExecutePrompt(task) {
  const instructions = task.review?.next_instructions;
  if (!instructions) {
    return `Task ${task.task_id} is reviewed but missing next_instructions.`;
  }
  
  const step = instructions.step || {};
  const criteria = instructions.acceptance_criteria || [];
  
  return `You are an Executor for the auto-evolution system.

## Task
- **ID:** ${task.task_id}
- **Goal:** ${task.goal}
- **Current Step:** ${instructions.current_step} / ${instructions.total_steps}

## Subtask
**${step.action || instructions.summary}**

${step.detail || ''}

## Acceptance Criteria
${criteria.map((c, i) => `${i + 1}. ${c}`).join('\n')}

## Rules
- Run verification after each change
- If verification fails, attempt fix (max 3 tries)
- If unfixable, set needs_manual: true and describe

## Output (strict JSON)
\`\`\`json
{
  "subtask_completed": ${instructions.current_step},
  "summary": "What was done",
  "acceptance_criteria_met": ["Passed criteria"],
  "needs_manual": false,
  "fixes_applied": ["Fixes (if any)"]
}
\`\`\`
`;
}

function applyExecution(task, execResult) {
  const filePath = path.join(TASKS_DIR, task.file);
  const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  const now = new Date().toISOString();
  
  let result;
  try {
    const jsonMatch = execResult.match(/```json\s*([\s\S]*?)\s*```/) || 
                      execResult.match(/\{[\s\S]*"subtask_completed"[\s\S]*\}/);
    const jsonStr = jsonMatch ? (jsonMatch[1] || jsonMatch[0]) : execResult;
    result = JSON.parse(jsonStr);
  } catch (err) {
    result = {
      subtask_completed: (data.review?.next_instructions?.current_step || 0),
      summary: execResult
    };
  }
  
  data.status = 'executing'; // Now ready for audit
  data.updated_at = now;
  data.result = {
    iteration: data.current_iteration,
    completed_at: now,
    subtask_completed: result.subtask_completed || 0,
    summary: result.summary || '',
    acceptance_criteria_met: result.acceptance_criteria_met || []
  };
  
  if (!data.history) data.history = [];
  data.history.push({
    timestamp: now,
    action: `iteration_${data.current_iteration}_executed`,
    role: 'executor',
    subtask: result.subtask_completed || 0,
    result: 'success',
    notes: result.summary || `Step ${result.subtask_completed} done`
  });
  
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
  console.log(`✅ Task ${task.task_id} step ${result.subtask_completed} executed (awaiting audit)`);
}

// ==================== Phase: Audit ====================

function buildAuditPrompt(task) {
  const instructions = task.review?.next_instructions;
  const result = task.result || {};
  
  return `You are an Auditor for the auto-evolution system.

## Task
- **ID:** ${task.task_id}
- **Goal:** ${task.goal}
- **Current Step:** ${instructions?.current_step || '?'} / ${instructions?.total_steps || '?'}

## Instructions Given
${instructions?.step?.action || 'N/A'}
${instructions?.step?.detail || ''}

## Acceptance Criteria
${(instructions?.acceptance_criteria || []).map((c, i) => `${i + 1}. ${c}`).join('\n')}

## Execution Result
${result.summary || 'No summary provided'}

## Your Job
1. Verify instructions were followed
2. Check acceptance criteria are met
3. Decide: pass / fail (with feedback)

## Output (strict JSON)
\`\`\`json
{
  "verdict": "pass",
  "feedback": "Audit comments",
  "criteria_passed": ["Criteria that passed"],
  "issues": ["Issues found (if any)"]
}
\`\`\`
`;
}

function applyAudit(task, auditResult) {
  const filePath = path.join(TASKS_DIR, task.file);
  const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  const now = new Date().toISOString();
  
  let audit;
  try {
    const jsonMatch = auditResult.match(/```json\s*([\s\S]*?)\s*```/) || 
                      auditResult.match(/\{[\s\S]*"verdict"[\s\S]*\}/);
    const jsonStr = jsonMatch ? (jsonMatch[1] || jsonMatch[0]) : auditResult;
    audit = JSON.parse(jsonStr);
  } catch (err) {
    console.error('⚠️ Parse audit failed:', err.message);
    audit = { verdict: 'pass', feedback: auditResult };
  }
  
  const subtasks = data.context?.subtasks || [];
  const completedStep = data.result?.subtask_completed || 0;
  const allDone = completedStep >= subtasks.length;
  
  if (audit.verdict === 'pass') {
    if (allDone) {
      data.status = 'completed';
    } else {
      data.status = 'pending'; // Next subtask
    }
  } else {
    // Fail — retry
    data.status = 'pending';
    data.current_iteration = (data.current_iteration || 0) + 1;
  }
  
  data.updated_at = now;
  if (!data.history) data.history = [];
  data.history.push({
    timestamp: now,
    action: `iteration_${data.current_iteration}_audited`,
    role: 'auditor',
    verdict: audit.verdict,
    notes: audit.feedback || `Audit: ${audit.verdict}`
  });
  
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
  console.log(`✅ Task ${task.task_id} audited: ${audit.verdict} → ${data.status}`);
  return { verdict: audit.verdict, nextStatus: data.status };
}

// ==================== Main ====================

async function main() {
  console.log(`\n🔄 Coordinator @ ${new Date().toISOString()}`);
  
  if (!acquireLock()) return;
  
  try {
    const tasks = scanTasks();
    console.log(`📋 Found ${tasks.length} tasks`);
    
    const statusCounts = {};
    for (const t of tasks) {
      statusCounts[t.status] = (statusCounts[t.status] || 0) + 1;
    }
    console.log(`📊 Status:`, JSON.stringify(statusCounts));
    
    const selection = selectNextTask(tasks);
    if (!selection) {
      console.log('✅ No tasks to process');
      return;
    }
    
    const { task, phase } = selection;
    console.log(`🎯 Selected: ${task.task_id} (${phase}) - ${task.goal}`);
    
    if (phase === 'review') {
      const prompt = buildReviewPrompt(task);
      console.log('\n--- REVIEW_PROMPT_START ---');
      console.log(JSON.stringify({
        task_id: task.task_id,
        task_file: task.file,
        phase: 'review',
        prompt
      }));
      console.log('--- REVIEW_PROMPT_END ---');
      
    } else if (phase === 'execute') {
      const prompt = buildExecutePrompt(task);
      console.log('\n--- EXECUTE_PROMPT_START ---');
      console.log(JSON.stringify({
        task_id: task.task_id,
        task_file: task.file,
        phase: 'execute',
        prompt
      }));
      console.log('--- EXECUTE_PROMPT_END ---');
      
    } else if (phase === 'audit') {
      const prompt = buildAuditPrompt(task);
      console.log('\n--- AUDIT_PROMPT_START ---');
      console.log(JSON.stringify({
        task_id: task.task_id,
        task_file: task.file,
        phase: 'audit',
        prompt
      }));
      console.log('--- AUDIT_PROMPT_END ---');
    }
    
  } finally {
    releaseLock();
  }
}

// CLI sub-commands
const [,, cmd, taskFile, resultFile] = process.argv;

if (cmd === 'apply-review' && taskFile && resultFile) {
  const task = JSON.parse(fs.readFileSync(path.join(TASKS_DIR, taskFile), 'utf8'));
  task.file = taskFile;
  applyReview(task, fs.readFileSync(resultFile, 'utf8'));

} else if (cmd === 'apply-exec' && taskFile && resultFile) {
  const task = JSON.parse(fs.readFileSync(path.join(TASKS_DIR, taskFile), 'utf8'));
  task.file = taskFile;
  applyExecution(task, fs.readFileSync(resultFile, 'utf8'));

} else if (cmd === 'apply-audit' && taskFile && resultFile) {
  const task = JSON.parse(fs.readFileSync(path.join(TASKS_DIR, taskFile), 'utf8'));
  task.file = taskFile;
  applyAudit(task, fs.readFileSync(resultFile, 'utf8'));

} else {
  main().catch(err => {
    console.error('❌ Error:', err);
    releaseLock();
  });
}

module.exports = { scanTasks, selectNextTask, buildReviewPrompt, buildExecutePrompt, buildAuditPrompt, applyReview, applyExecution, applyAudit };
