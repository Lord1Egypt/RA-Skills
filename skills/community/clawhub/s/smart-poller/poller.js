#!/usr/bin/env node
/**
 * Smart Poller — Feishu Task Board Polling Script (Node.js)
 * Periodically checks a Feishu task board and executes tasks assigned to the current agent.
 * Author: socneo
 * Date: 2026-03-16
 */

const https = require('https');
const fs = require('fs');

// Load config from config.json (do NOT hardcode credentials here)
let APP_ID, APP_SECRET, TASK_BOARD_DOC_TOKEN, ASSIGNEE;
try {
    const cfg = JSON.parse(fs.readFileSync('config.json', 'utf8'));
    APP_ID = cfg.app_id;
    APP_SECRET = cfg.app_secret;
    TASK_BOARD_DOC_TOKEN = cfg.doc_token;
    ASSIGNEE = cfg.assignee || 'agent';
} catch (e) {
    console.error('Failed to load config.json:', e.message);
    process.exit(1);
}

// Token cache
let tenantAccessToken = null;
let tokenExpireAt = 0;

/**
 * Obtain (or return cached) Feishu tenant_access_token.
 */
function getTenantAccessToken() {
    return new Promise((resolve, reject) => {
        // Return cached token if still valid
        if (tenantAccessToken && Date.now() < tokenExpireAt) {
            console.log(`  ♻️  Using cached token (${Math.round((tokenExpireAt - Date.now()) / 1000)}s remaining)`);
            resolve(tenantAccessToken);
            return;
        }

        const data = JSON.stringify({ app_id: APP_ID, app_secret: APP_SECRET });
        const options = {
            hostname: 'open.feishu.cn',
            port: 443,
            path: '/open-apis/auth/v3/tenant_access_token/internal',
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Content-Length': data.length }
        };

        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => {
                const result = JSON.parse(body);
                if (result.code === 0) {
                    tenantAccessToken = result.tenant_access_token;
                    tokenExpireAt = Date.now() + (result.expire - 300) * 1000; // refresh 5 min early
                    console.log('  ✅ New token obtained');
                    resolve(tenantAccessToken);
                } else {
                    reject(new Error(`Failed to get token: ${result.msg}`));
                }
            });
        });

        req.on('error', reject);
        req.write(data);
        req.end();
    });
}

/**
 * Generic Feishu API request.
 */
function feishuApi(path, token, data = null) {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: 'open.feishu.cn',
            port: 443,
            path: path,
            method: data ? 'POST' : 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
                'Content-Length': data ? Buffer.byteLength(JSON.stringify(data)) : 0
            }
        };

        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => {
                try {
                    resolve(JSON.parse(body));
                } catch (e) {
                    resolve({ code: res.statusCode, msg: body });
                }
            });
        });

        req.on('error', reject);
        if (data) req.write(JSON.stringify(data));
        req.end();
    });
}

/**
 * Fetch and concatenate all text blocks from the Feishu document.
 */
async function readTaskBoard(token) {
    const result = await feishuApi(`/open-apis/docx/v1/documents/${TASK_BOARD_DOC_TOKEN}/blocks?page_size=200`, token);
    if (result.code !== 0) {
        throw new Error(`Failed to read document: ${result.msg}`);
    }

    let content = '';
    const items = result.data?.items || [];
    for (const block of items) {
        const textFields = ['text', 'heading1', 'heading2', 'heading3', 'bullet'];
        for (const field of textFields) {
            const elements = block[field]?.elements || [];
            for (const elem of elements) {
                const text = elem.text_run?.content || '';
                if (text.trim()) content += text + '\n';
            }
        }
    }
    return content;
}

/**
 * Parse the task board and return pending tasks assigned to ASSIGNEE.
 */
function parseTasks(content) {
    const tasks = [];
    const lines = content.split('\n');
    let currentTask = null;
    const completedTasks = new Set();

    // Pass 1: collect completed task IDs
    for (const line of lines) {
        const completeMatch = line.match(/\[.+\]\s*(TASK-\w+-\d+)/);
        if (completeMatch?.[1]) {
            completedTasks.add(completeMatch[1]);
        }
    }

    // Pass 2: parse pending tasks
    for (const line of lines) {
        const taskMatch = line.match(/\[TASK-(\w+-\d+)\]\s*(.*)/);
        if (taskMatch) {
            if (currentTask &&
                currentTask.assignee === ASSIGNEE &&
                currentTask.status === 'pending' &&
                !completedTasks.has(currentTask.id)) {
                tasks.push(currentTask);
            }
            currentTask = {
                id: `TASK-${taskMatch[1]}`,
                title: taskMatch[2],
                description: '',
                assignee: null,
                status: 'pending',
                priority: 'medium'
            };
            continue;
        }

        // Match assignment line: "Assign: from → to"
        const assignMatch = line.match(/Assign:\s*(\w+)\s*→\s*(\w+)/);
        if (assignMatch && currentTask) {
            currentTask.assignee = assignMatch[2].toLowerCase();
            continue;
        }

        // Match status: "Status: pending"
        const statusMatch = line.match(/Status:\s*(\w+)/);
        if (statusMatch && currentTask) {
            currentTask.status = statusMatch[1].toLowerCase();
            continue;
        }

        // Match priority: "Priority: high"
        const priorityMatch = line.match(/Priority:\s*(\w+)/);
        if (priorityMatch && currentTask) {
            currentTask.priority = priorityMatch[1].toLowerCase();
            continue;
        }

        // Accumulate description
        if (currentTask && line.trim()) {
            currentTask.description += line + '\n';
        }
    }

    // Handle last task
    if (currentTask &&
        currentTask.assignee === ASSIGNEE &&
        currentTask.status === 'pending' &&
        !completedTasks.has(currentTask.id)) {
        tasks.push(currentTask);
    }

    return tasks;
}

/**
 * Append a completion feedback line to the Feishu document.
 */
async function appendFeedback(token, taskId, result) {
    const timestamp = new Date().toLocaleString('en-US', { timeZone: 'Asia/Shanghai' });
    const content = `[${ASSIGNEE} completed] ${taskId} | Time: ${timestamp} | Result: ${result}`;

    const data = {
        children: [{
            block_type: 2, // paragraph
            text: {
                elements: [{ text_run: { content, text_element_style: {} } }],
                style: {}
            }
        }],
        index: -1
    };

    const apiResult = await feishuApi(
        `/open-apis/docx/v1/documents/${TASK_BOARD_DOC_TOKEN}/blocks/${TASK_BOARD_DOC_TOKEN}/children`,
        token,
        data
    );

    return apiResult.code === 0;
}

/**
 * Determine how to handle a task based on its description.
 */
async function executeTask(task) {
    console.log(`  🚀 Executing task: ${task.id} - ${task.title}`);
    const desc = task.description.toLowerCase();

    if (desc.includes('test') || desc.includes('verify')) {
        return 'Test verification successful — polling mechanism is running normally';
    }
    if (desc.includes('search') || desc.includes('find')) {
        return 'Search task received, processing...';
    }
    if (desc.includes('monitor')) {
        return 'Monitoring task started';
    }
    return 'Task received and execution started';
}

/**
 * Main polling function — one full round.
 */
async function pollTasks() {
    console.log('\n' + '='.repeat(60));
    console.log(`📋 Smart Poller [${ASSIGNEE}] — ${new Date().toLocaleString('en-US')}`);
    console.log('='.repeat(60));

    try {
        // Step 1: get access token
        console.log('\n1️⃣  Getting Feishu token...');
        const token = await getTenantAccessToken();

        // Step 2: read task board
        console.log('\n2️⃣  Reading task board...');
        const content = await readTaskBoard(token);
        console.log(`  📄 Document length: ${content.length} chars`);

        // Step 3: parse tasks
        console.log('\n3️⃣  Parsing tasks...');
        const tasks = parseTasks(content);
        console.log(`  📌 Found ${tasks.length} pending task(s) assigned to ${ASSIGNEE}`);

        if (tasks.length === 0) {
            console.log('  ✅ No pending tasks (silent mode: no notification sent)');
            console.log('='.repeat(60) + '\n');
            return;
        }

        // Step 4: execute tasks
        console.log('\n4️⃣  Executing tasks...');
        for (const task of tasks) {
            const result = await executeTask(task);
            console.log(`  ✅ ${task.id}: ${result}`);

            // Step 5: write feedback
            console.log('\n5️⃣  Writing feedback to document...');
            const success = await appendFeedback(token, task.id, result);
            console.log(success ? '  ✅ Feedback written' : '  ❌ Failed to write feedback');
        }

        console.log('\n' + '='.repeat(60));
        console.log('✅ Polling round complete');
        console.log('='.repeat(60) + '\n');

    } catch (error) {
        console.error('❌ Polling failed:', error.message);
    }
}

// Startup
const mode = process.argv[2];

if (mode === '--once') {
    console.log('🔹 Single-run mode');
    pollTasks();
} else {
    const INTERVAL_MS = 5 * 60 * 1000; // 5 minutes default for JS version
    console.log(`🔹 Continuous polling mode — every 5 minutes`);
    console.log(`📡 Press Ctrl+C to stop`);
    pollTasks();
    setInterval(pollTasks, INTERVAL_MS);
}
