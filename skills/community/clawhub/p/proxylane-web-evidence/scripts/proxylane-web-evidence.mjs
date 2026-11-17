#!/usr/bin/env node
// Thin deployment-neutral bridge; source libraries remain in Python.
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const python = process.env.PROXYLANE_EVIDENCE_PYTHON || 'python3';
const script = fileURLToPath(new URL('./collect.py', import.meta.url));
const run = spawnSync(python, [script, ...process.argv.slice(2)], { stdio: 'inherit' });
if (run.error) {
  const args = process.argv.slice(2);
  const modeIndex = args.indexOf('--mode');
  process.stdout.write(JSON.stringify({schema_version:'1.0',mode:modeIndex >= 0 ? args[modeIndex + 1] : 'unspecified',status:'missing_dependency',proof_mode:args.includes('--fixture') ? 'fixture' : 'live',observed_at:new Date().toISOString(),observations:[],diagnostics:[{code:'python_unavailable',message:'Set PROXYLANE_EVIDENCE_PYTHON to an installed Python 3.10+ interpreter'}],evidence:[]})+'\n');
}
process.exit(run.status ?? 2);
