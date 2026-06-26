import { initPrefs, getPrefsPath } from '../notifications/prefs';

function printJson(value: unknown): void {
  console.log(JSON.stringify(value, null, 2));
}

function main(): void {
  const created = initPrefs();
  printJson({
    ok: true,
    created,
    path: getPrefsPath(),
    message: created
      ? 'Created default notification_prefs.json'
      : 'notification_prefs.json already exists — no changes made',
    safety: { externalWrite: false },
  });
}

main();
