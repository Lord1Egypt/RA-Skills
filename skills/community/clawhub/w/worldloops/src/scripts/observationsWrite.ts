import * as fs from 'node:fs';
import * as path from 'node:path';
import type { OpenClawObservation } from '../openclawIntake';

const OUTPUT_DIR = path.join(process.cwd(), '.worldloops', 'inbox');
const OUTPUT_FILE = path.join(OUTPUT_DIR, 'openclaw-observations.json');

function getFlagValue(flag: string): string | undefined {
  const args = process.argv.slice(2);
  const idx = args.indexOf(flag);
  if (idx === -1 || idx + 1 >= args.length) return undefined;
  return args[idx + 1];
}

function fail(msg: string): never {
  process.stderr.write(`observations:write error: ${msg}\n`);
  process.exit(1);
}

function validateObservation(item: unknown, index: number): string[] {
  const errors: string[] = [];
  if (typeof item !== 'object' || item === null || Array.isArray(item)) {
    errors.push(`[${index}] must be an object`);
    return errors;
  }
  const obs = item as Record<string, unknown>;

  if (typeof obs.id !== 'string' || !obs.id) errors.push(`[${index}] id: required string`);
  if (typeof obs.source !== 'string' || !obs.source) errors.push(`[${index}] source: required string`);
  if (typeof obs.sourceId !== 'string' || !obs.sourceId) errors.push(`[${index}] sourceId: required string`);
  if (obs.observedBy !== 'openclaw') errors.push(`[${index}] observedBy: must be "openclaw"`);
  if (typeof obs.title !== 'string' || !obs.title) errors.push(`[${index}] title: required string`);
  if (typeof obs.text !== 'string' || !obs.text) errors.push(`[${index}] text: required string`);
  if (typeof obs.timestamp !== 'string' || !obs.timestamp) errors.push(`[${index}] timestamp: required string`);
  if (typeof obs.evidence !== 'object' || obs.evidence === null || Array.isArray(obs.evidence)) {
    errors.push(`[${index}] evidence: required object`);
  }

  const validIntents = ['new_loop', 'state_transition', 'noise', 'related_context', 'evidence'];
  if (obs.observationIntent !== undefined && !validIntents.includes(obs.observationIntent as string)) {
    errors.push(`[${index}] observationIntent: must be one of ${validIntents.join(', ')}`);
  }

  if (obs.confidence !== undefined && (typeof obs.confidence !== 'number' || obs.confidence < 0 || obs.confidence > 1)) {
    errors.push(`[${index}] confidence: must be a number between 0 and 1`);
  }

  return errors;
}

function main(): void {
  const inputArg = getFlagValue('--input');
  if (!inputArg) {
    fail('--input <json-file> is required\nUsage: npm run observations:write -- --input <path/to/observations.json>');
  }

  const inputPath = path.resolve(process.cwd(), inputArg);
  if (!fs.existsSync(inputPath)) {
    fail(`input file not found: ${inputPath}`);
  }

  let raw: string;
  try {
    raw = fs.readFileSync(inputPath, 'utf8');
  } catch (err) {
    fail(`could not read input file: ${String(err)}`);
  }

  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch (err) {
    fail(`invalid JSON: ${String(err)}`);
  }

  if (!Array.isArray(parsed)) {
    fail('input must be a JSON array of ObservedSignal objects');
  }

  const allErrors: string[] = [];
  for (let i = 0; i < parsed.length; i++) {
    allErrors.push(...validateObservation(parsed[i], i));
  }

  if (allErrors.length > 0) {
    process.stderr.write('observations:write validation failed:\n');
    for (const err of allErrors) {
      process.stderr.write(`  ${err}\n`);
    }
    process.exit(1);
  }

  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }

  const observations = parsed as OpenClawObservation[];
  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(observations, null, 2) + '\n', 'utf8');

  console.log(`Observations written: ${observations.length}`);
  console.log(`Output: .worldloops/inbox/openclaw-observations.json`);
  console.log('externalWrite:false');
}

main();
