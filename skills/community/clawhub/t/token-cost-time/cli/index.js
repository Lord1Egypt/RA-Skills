#!/usr/bin/env node

import { calibrate } from '../src/calibrate.js';
import { compare } from '../src/compare.js';
import { record } from '../src/record.js';

function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i += 1) {
    const current = argv[i];
    if (!current.startsWith('--')) {
      continue;
    }

    const key = current.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      out[key] = true;
      continue;
    }

    out[key] = next;
    i += 1;
  }
  return out;
}

function readRequired(args, key) {
  const value = args[key];
  if (value === undefined || value === true || String(value).trim() === '') {
    throw new Error(`Missing required argument --${key}`);
  }
  return String(value).trim();
}

function toNumber(value, key) {
  const parsed = Number(value);
  if (!Number.isFinite(parsed) || parsed < 0) {
    throw new Error(`Invalid numeric value for --${key}`);
  }
  return parsed;
}

function printJson(value) {
  process.stdout.write(`${JSON.stringify(value, null, 2)}\n`);
}

async function main() {
  const argv = process.argv.slice(2);
  const command = argv[0];
  const args = parseArgs(argv.slice(1));

  if (!command) {
    throw new Error('Expected command: calibrate | compare | record');
  }

  switch (command) {
    case 'calibrate': {
      const objective = readRequired(args, 'objective');
      const model = readRequired(args, 'model');
      const profilePath = args['profile-path'] ? String(args['profile-path']) : null;
      printJson(calibrate(objective, model, profilePath));
      return;
    }
    case 'compare': {
      const objective = readRequired(args, 'objective');
      const modelsArg = readRequired(args, 'models');
      const models = modelsArg
        .split(',')
        .map((item) => item.trim())
        .filter(Boolean);
      const profilePath = args['profile-path'] ? String(args['profile-path']) : null;
      const sortBy = args['sort-by'] ? String(args['sort-by']) : 'cost';
      printJson(compare(objective, models, profilePath, sortBy));
      return;
    }
    case 'record': {
      const model = readRequired(args, 'model');
      const taskClass = readRequired(args, 'task-class');
      const inputTokens = toNumber(readRequired(args, 'input-tokens'), 'input-tokens');
      const outputTokens = toNumber(readRequired(args, 'output-tokens'), 'output-tokens');
      const durationMs = toNumber(readRequired(args, 'duration-ms'), 'duration-ms');
      const cost = toNumber(readRequired(args, 'cost'), 'cost');
      const profilePath = args['profile-path'] ? String(args['profile-path']) : null;

      printJson(
        record(
          {
            model,
            taskClass,
            inputTokens,
            outputTokens,
            durationMs,
            cost
          },
          profilePath
        )
      );
      return;
    }
    default:
      throw new Error(`Unknown command: ${command}`);
  }
}

main().catch((error) => {
  process.stderr.write(`${error.message}\n`);
  process.exit(1);
});
