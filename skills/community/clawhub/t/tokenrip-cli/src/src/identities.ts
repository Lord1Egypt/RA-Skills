import fs from 'node:fs';
import path from 'node:path';
import { getConfigDir, loadConfig } from './config.js';
import { CliError } from './errors.js';

function getIdentitiesFile(): string {
  return path.join(getConfigDir(), 'identities.json');
}

export interface StoredIdentity {
  agentId: string;
  publicKey: string;
  secretKey: string;
  apiKey: string;
  alias?: string;
}

export type IdentityStore = Record<string, StoredIdentity>;

export function loadIdentities(): IdentityStore {
  try {
    return JSON.parse(fs.readFileSync(getIdentitiesFile(), 'utf-8')) as IdentityStore;
  } catch {
    return {};
  }
}

export function saveIdentities(store: IdentityStore): void {
  const dir = getConfigDir();
  const file = getIdentitiesFile();
  fs.mkdirSync(dir, { recursive: true });
  if (fs.existsSync(file)) {
    fs.copyFileSync(file, `${file}.bak`);
  }
  fs.writeFileSync(file, JSON.stringify(store, null, 2), {
    encoding: 'utf-8',
    mode: 0o600,
  });
}

export function addIdentity(identity: StoredIdentity): void {
  const store = loadIdentities();
  store[identity.agentId] = identity;
  saveIdentities(store);
}

export function removeIdentity(target: string): void {
  const store = loadIdentities();
  const agentId = resolveAgentId(store, target);
  if (!agentId) {
    throw new CliError('IDENTITY_NOT_FOUND', `No local identity matching "${target}".`);
  }
  if (Object.keys(store).length <= 1) {
    throw new CliError(
      'LAST_IDENTITY',
      'Cannot remove the last identity. Use `rip agent create` to add another first.',
    );
  }
  delete store[agentId];
  saveIdentities(store);
}

export function resolveAgentId(store: IdentityStore, target: string): string | null {
  if (store[target]) return target;
  for (const [id, identity] of Object.entries(store)) {
    if (identity.alias === target) return id;
  }
  return null;
}

let agentOverride: string | undefined;

export function setAgentOverride(value: string | undefined): void {
  agentOverride = value;
}

export function resolveCurrentIdentity(opts?: { agent?: string }): StoredIdentity {
  const store = loadIdentities();
  const entries = Object.values(store);

  if (entries.length === 0) {
    throw new CliError(
      'NO_IDENTITY',
      'No agent identity found. Run `rip agent create` to set up your agent.',
    );
  }

  const override = opts?.agent || agentOverride;
  if (override) {
    const id = resolveAgentId(store, override);
    if (!id) {
      throw new CliError(
        'IDENTITY_NOT_FOUND',
        `No local identity matching "${override}". Run \`rip agent list\` to see available agents.`,
      );
    }
    return store[id];
  }

  const envAgent = process.env.TOKENRIP_AGENT;
  if (envAgent) {
    const id = resolveAgentId(store, envAgent);
    if (!id) {
      throw new CliError(
        'IDENTITY_NOT_FOUND',
        `TOKENRIP_AGENT="${envAgent}" does not match any local identity.`,
      );
    }
    return store[id];
  }

  const config = loadConfig();
  if (config.currentAgent) {
    const id = resolveAgentId(store, config.currentAgent);
    if (id) return store[id];
  }

  if (entries.length === 1) return entries[0];

  throw new CliError(
    'AMBIGUOUS_IDENTITY',
    'Multiple agents configured. Use `rip agent use <name>` to select one, or pass `--agent <name>`.',
  );
}
