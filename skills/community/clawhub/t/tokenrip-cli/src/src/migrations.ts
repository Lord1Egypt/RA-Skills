import fs from 'node:fs';
import path from 'node:path';
import { bech32 } from 'bech32';
import { getConfigDir, loadConfig, saveConfig } from './config.js';
import { loadIdentity, saveIdentity } from './identity.js';
import { loadContacts, saveContacts } from './contacts.js';
import { saveIdentities } from './identities.js';

const CURRENT_CONFIG_VERSION = 3;

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

// v2 → v3: move identity.json + config.apiKey into identities.json store
function migrateV2toV3(): void {
  const dir = getConfigDir();
  const identityFile = path.join(dir, 'identity.json');
  if (!fs.existsSync(identityFile)) return;

  let identity: { agentId: string; publicKey: string; secretKey: string } | null = null;
  try {
    identity = JSON.parse(fs.readFileSync(identityFile, 'utf-8'));
  } catch {
    return;
  }
  if (!identity) return;

  const config = loadConfig();
  const stored: Record<string, unknown> = {
    agentId: identity.agentId,
    publicKey: identity.publicKey,
    secretKey: identity.secretKey,
  };
  if (config.apiKey) stored.apiKey = config.apiKey;

  saveIdentities({ [identity.agentId]: stored as any });

  const updated = { ...config, currentAgent: identity.agentId };
  delete (updated as any).apiKey;
  saveConfig(updated);

  fs.renameSync(identityFile, `${identityFile}.migrated`);
}

const MIGRATIONS: Array<{ version: number; run: () => void }> = [
  { version: 2, run: migrateV1toV2 },
  { version: 3, run: migrateV2toV3 },
];

export function runMigrations(): void {
  const configFile = path.join(getConfigDir(), 'config.json');
  if (!fs.existsSync(configFile)) return;
  try {
    const config = loadConfig();
    const current = config.configVersion ?? 1;
    if (current >= CURRENT_CONFIG_VERSION) return;

    const pending = MIGRATIONS.filter(m => m.version > current);
    for (const m of pending) {
      m.run();
    }

    const latestVersion = pending[pending.length - 1].version;
    const postMigrationConfig = loadConfig();
    saveConfig({ ...postMigrationConfig, configVersion: latestVersion });

    console.error(`Config migrated (v${current} → v${latestVersion})`);
    console.error(`  Skill file may be outdated — check latest: https://tokenrip.com/.well-known/skills/tokenrip/SKILL.md`);
  } catch (err) {
    console.error(`Warning: Config migration failed — ${err instanceof Error ? err.message : String(err)}`);
    console.error(`  Try reinstalling: npm install -g @tokenrip/cli`);
  }
}
