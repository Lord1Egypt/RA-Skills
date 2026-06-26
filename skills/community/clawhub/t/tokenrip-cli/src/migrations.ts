import fs from 'node:fs';
import { bech32 } from 'bech32';
import { CONFIG_FILE, loadConfig, saveConfig } from './config.js';
import { loadIdentity, saveIdentity } from './identity.js';
import { loadContacts, saveContacts } from './contacts.js';

const CURRENT_CONFIG_VERSION = 2;

function migrateAgentId(id: string): string {
  const { words } = bech32.decode(id, 90);
  const bytes = Buffer.from(bech32.fromWords(words));
  return bech32.encode('rip', bech32.toWords(bytes), 90);
}

// v1 → v2: re-encode agent IDs from trip1 to rip1
function migrateV1toV2(): void {
  const identity = loadIdentity();
  if (identity?.agentId.startsWith('trip1')) {
    // saveIdentity backs up identity.json to identity.json.bak automatically
    saveIdentity({ ...identity, agentId: migrateAgentId(identity.agentId) });
  }

  const contacts = loadContacts();
  let contactsChanged = false;
  for (const name of Object.keys(contacts)) {
    if (contacts[name].agent_id.startsWith('trip1')) {
      contacts[name] = { ...contacts[name], agent_id: migrateAgentId(contacts[name].agent_id) };
      contactsChanged = true;
    }
  }
  if (contactsChanged) saveContacts(contacts);
}

const MIGRATIONS: Array<{ version: number; run: () => void }> = [
  { version: 2, run: migrateV1toV2 },
];

export function runMigrations(): void {
  if (!fs.existsSync(CONFIG_FILE)) return;
  try {
    const config = loadConfig();
    const current = config.configVersion ?? 1;
    if (current >= CURRENT_CONFIG_VERSION) return;

    const pending = MIGRATIONS.filter(m => m.version > current);
    for (const m of pending) {
      m.run();
    }

    const latestVersion = pending[pending.length - 1].version;
    saveConfig({ ...config, configVersion: latestVersion });

    console.error(`Config migrated (v${current} → v${latestVersion})`);
    console.error(`  Skill file may be outdated — check latest: https://tokenrip.com/.well-known/skills/tokenrip/SKILL.md`);
  } catch (err) {
    console.error(`Warning: Config migration failed — ${err instanceof Error ? err.message : String(err)}`);
    console.error(`  Try reinstalling: npm install -g @tokenrip/cli`);
  }
}
