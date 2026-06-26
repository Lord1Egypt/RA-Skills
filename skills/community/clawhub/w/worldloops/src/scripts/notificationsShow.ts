import { loadPrefs, getPrefsPath } from '../notifications/prefs';

function printJson(value: unknown): void {
  console.log(JSON.stringify(value, null, 2));
}

function main(): void {
  const prefs = loadPrefs();
  printJson({
    ok: true,
    path: getPrefsPath(),
    prefs,
    safety: { externalWrite: false },
  });
}

main();
