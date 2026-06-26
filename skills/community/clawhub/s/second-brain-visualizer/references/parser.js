#!/usr/bin/env node
/**
 * build-second-brain.js
 * Parses second-brain.md into atoms JSON for the SBV clustering pipeline.
 * Output: data/second-brain-atoms.json
 */

const fs = require('fs');
const path = require('path');

// Configure via environment variables — see references/install.md
const VAULT   = process.env.OPENCLAW_VAULT || process.env.VAULT_DIR || path.join(process.env.HOME, 'vault');
const SB_FILE = process.env.SBV_LEDGER_FILE || path.join(VAULT, 'memory/second-brain.md');
const OUT_FILE = process.env.SBV_ATOMS_FILE || path.join(__dirname, '../data/second-brain-atoms.json');

function parseAtoms(md) {
  const atoms = [];
  // Split on atom headers — ### ts: <timestamp>
  const sections = md.split(/(?=### ts: \d+)/);

  for (const section of sections) {
    const tsMatch = section.match(/### ts: (\d+)/);
    if (!tsMatch) continue;

    const ts = tsMatch[1];
    const dateMatch = section.match(/\*\*date:\*\*\s*(.+)/);
    const rawMatch = section.match(/\*\*raw:\*\*\s*"?([^"\n]+)"?/);
    const typeMatch = section.match(/\*\*type:\*\*\s*(.+)/);
    const tagsMatch = section.match(/\*\*tags:\*\*\s*(.+)/);
    const signalMatch = section.match(/\*\*signal:\*\*\s*(.+)/);
    const actionableMatch = section.match(/\*\*actionable:\*\*\s*(.+)/);
    const nextActionMatch = section.match(/\*\*nextAction:\*\*\s*(.+)/);
    const sourceTypeMatch = section.match(/\*\*source_type:\*\*\s*(.+)/);

    // Skip image-only atoms with no raw text
    const raw = rawMatch ? rawMatch[1].trim() : null;
    if (!raw || raw === '*(image only)*') continue;

    atoms.push({
      id: `sb-${ts}`,
      ts: parseInt(ts),
      date: dateMatch ? dateMatch[1].trim() : null,
      raw,
      type: typeMatch ? typeMatch[1].trim() : 'thought',
      source_type: sourceTypeMatch ? sourceTypeMatch[1].trim() : 'text',
      tags: tagsMatch ? tagsMatch[1].split(',').map(t => t.trim()) : [],
      signal: signalMatch ? signalMatch[1].trim() : 'cool',
      actionable: actionableMatch ? actionableMatch[1].trim() === 'yes' : false,
      nextAction: nextActionMatch ? nextActionMatch[1].trim() : null,
    });
  }

  return atoms;
}

function main() {
  if (!fs.existsSync(SB_FILE)) {
    console.error(`second-brain.md not found at ${SB_FILE}`);
    process.exit(1);
  }

  const md = fs.readFileSync(SB_FILE, 'utf8');
  const atoms = parseAtoms(md);

  const output = {
    generated: new Date().toISOString(),
    atomCount: atoms.length,
    dateRange: atoms.length ? {
      earliest: new Date(atoms[atoms.length - 1].ts * 1000).toISOString().slice(0, 10),
      latest: new Date(atoms[0].ts * 1000).toISOString().slice(0, 10),
    } : null,
    atoms,
  };

  fs.mkdirSync(path.dirname(OUT_FILE), { recursive: true });
  fs.writeFileSync(OUT_FILE, JSON.stringify(output, null, 2));
  // log(`Parsed ${atoms.length} atoms → ${OUT_FILE}`);
}

main();
