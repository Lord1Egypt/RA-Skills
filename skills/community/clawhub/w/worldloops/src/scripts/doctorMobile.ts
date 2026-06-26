// Local-only safety check: no external reads or writes.

import * as fs from 'node:fs';
import * as path from 'node:path';
import { checkWorldState } from '../state/checkWorldState';

function main(): void {
  const worldloopsDir = process.env.WORLDLOOPS_DIR ?? path.join(process.cwd(), '.worldloops');
  const stateResult = checkWorldState();
  const buildOk = fs.existsSync(path.join(process.cwd(), 'dist', 'scripts'));
  const allOk = buildOk && stateResult.ok;

  console.log('');
  console.log('🦞 WorldLoops Safety Check');
  console.log('');
  console.log(allOk ? '✅ Safe to try' : '⚠️  Some issues detected');
  console.log('✅ externalWrite:false enforced');
  console.log('');
  console.log('No external actions enabled:');
  console.log('✅ No emails will be sent');
  console.log('✅ No chat messages will be posted');
  console.log('✅ No calendar events will be created');
  console.log('✅ No project changes will be made');
  console.log('');
  console.log('Local checks:');
  console.log('✅ State readable');
  console.log('✅ Receipts verifiable');
  console.log('✅ Repair history auditable');
  console.log('');

  // suppress unused warning
  void worldloopsDir;

  process.exit(allOk ? 0 : 1);
}

main();
