import { loadPrefs, savePrefs, setDotPath } from '../notifications/prefs';
import type { NotificationPrefs } from '../types';

function printJson(value: unknown): void {
  console.log(JSON.stringify(value, null, 2));
}

function coerceValue(raw: string): unknown {
  if (raw === 'true') return true;
  if (raw === 'false') return false;
  const n = Number(raw);
  if (!Number.isNaN(n) && raw.trim() !== '') return n;
  return raw;
}

function main(): void {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    printJson({
      ok: false,
      error: {
        code: 'MISSING_ARGS',
        message: 'Usage: notifications:set <dotPath> <value>   e.g. dailyBrief.time 09:00',
      },
      safety: { externalWrite: false },
    });
    process.exit(1);
  }

  const [dotPath, rawValue] = args;
  const value = coerceValue(rawValue);

  const prefs = loadPrefs();
  setDotPath(prefs as unknown as Record<string, unknown>, dotPath, value);
  savePrefs(prefs as NotificationPrefs);

  printJson({
    ok: true,
    set: { [dotPath]: value },
    safety: { externalWrite: false },
  });
}

main();
