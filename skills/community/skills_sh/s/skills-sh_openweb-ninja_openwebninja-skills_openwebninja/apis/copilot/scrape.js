#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, writeOutput } = require('../../lib/utils');
const path = require('path');
const fs = require('fs');

function printHelp() {
    console.log(`
Usage: node scrape.js --message <prompt> [options]

Send a message to Microsoft Copilot and save the response.

Required:
  --message         The message / prompt to send

Optional:
  --conversation-id Continue a previous conversation (returned in prior response)
  --context         Path to a file whose contents will be prepended as context
  --format          json | csv (default: json)
  --output          Output file path (auto-generated if omitted)
  --dry-run         Print response to console only, do not write file
  --help            Show this help
`);
}

function parseArgs(argv) {
    const args = {};
    for (let i = 2; i < argv.length; i++) {
        const arg = argv[i];
        if (arg === '--help') { args.help = true; continue; }
        if (arg === '--dry-run') { args.dryRun = true; continue; }
        if (arg.startsWith('--') && i + 1 < argv.length) {
            const key = arg.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
            args[key] = argv[++i];
        }
    }
    return args;
}

async function main() {
    const args = parseArgs(process.argv);
    if (args.help) { printHelp(); process.exit(0); }
    if (!args.message) { console.error('Error: --message required. Use --help for usage.'); process.exit(1); }

    const apiKey = getApiKey();
    const meta = loadMeta('copilot');
    const host = meta.rapidapi_host || 'copilot5.p.rapidapi.com';
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `copilot_${ts}.${format}`);

    // Build the prompt
    let prompt = args.message;
    if (args.context) {
        const contextPath = path.resolve(args.context);
        if (!fs.existsSync(contextPath)) { console.error(`Error: context file not found: ${contextPath}`); process.exit(1); }
        const contextContent = fs.readFileSync(contextPath, 'utf8');
        prompt = `Context:\n${contextContent}\n\n${args.message}`;
    }

    console.error('Sending message to Copilot...');
    const body = { message: prompt };
    if (args.conversationId) body.conversation_id = args.conversationId;

    const data = await apiCall(host, '/copilot', {}, apiKey, 'POST', body);

    const record = {
        message: args.message,
        conversation_id: data.conversation_id || args.conversationId || null,
        context_file: args.context || null,
        response: data.response || data.result || data.answer || data.message || JSON.stringify(data),
        raw: data,
    };

    if (dryRun) {
        console.log(JSON.stringify(record, null, 2));
        return;
    }

    writeOutput([record], outputPath, format, { api: 'copilot', endpoint: '/copilot', totalCalls: 1 });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
