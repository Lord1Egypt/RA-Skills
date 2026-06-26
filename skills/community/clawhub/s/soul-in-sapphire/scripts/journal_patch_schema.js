#!/usr/bin/env node
import fs from 'fs';
import os from 'os';
import path from 'path';
import { patchDataSource } from './notionctl_bridge.js';

function die(msg){ process.stderr.write(String(msg)+'\n'); process.exit(1); }

function parseArgs(argv) {
  const out = { journalDsid: null };
  for (let i = 2; i < argv.length; i++) {
    if (argv[i] === '--journal-dsid') out.journalDsid = argv[++i] || '';
  }
  return out;
}

async function main(){
  const args = parseArgs(process.argv);
  const dsid = args.journalDsid;
  if(!dsid) die('Missing --journal-dsid. Check TOOLS.md for the value.');

  const moodOpts = ['clear','wired','dull','tense','playful','guarded','tender'].map(name=>({name}));
  const intentOpts = ['build','fix','organize','explore','rest','socialize','reflect'].map(name=>({name}));
  const sourceOpts = ['cron','manual'].map(name=>({name}));

  await patchDataSource(dsid, {
    when: { date: {} },
    body: { rich_text: {} },
    worklog: { rich_text: {} },
    session_summary: { rich_text: {} },
    mood_label: { select: { options: moodOpts } },
    intent: { select: { options: intentOpts } },
    future: { rich_text: {} },
    world_news: { rich_text: {} },
    tags: { multi_select: { options: [] } },
    source: { select: { options: sourceOpts } },
  });

  console.log(JSON.stringify({ok:true, journal_data_source_id: dsid}, null, 2));
}

main().catch(err=>die(err?.stack || err?.message || String(err)));
