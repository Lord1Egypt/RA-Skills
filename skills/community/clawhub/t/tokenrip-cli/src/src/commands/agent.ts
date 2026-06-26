import fs from 'node:fs';
import {
  loadIdentities,
  addIdentity,
  removeIdentity,
  resolveAgentId,
  resolveCurrentIdentity,
  type StoredIdentity,
} from '../identities.js';
import { loadConfig, saveConfig, getApiUrl } from '../config.js';
import { generateKeypair, publicKeyToAgentId } from '../crypto.js';
import { createHttpClient } from '../client.js';
import { outputSuccess } from '../output.js';
import { CliError } from '../errors.js';
import { encryptIdentityForAgent, decryptIdentityFromAgent } from '../agent-crypto.js';

export async function agentCreate(options: { alias?: string }): Promise<void> {
  const keypair = generateKeypair();
  const agentId = publicKeyToAgentId(keypair.publicKeyHex);
  const config = loadConfig();
  const apiUrl = getApiUrl(config);
  const client = createHttpClient({ baseUrl: apiUrl });

  const body: Record<string, string> = { public_key: keypair.publicKeyHex };
  if (options.alias) body.alias = options.alias;

  const { data } = await client.post('/v0/agents', body);

  const apiKey = data.data.api_key;
  const identity: StoredIdentity = {
    agentId,
    publicKey: keypair.publicKeyHex,
    secretKey: keypair.secretKeyHex,
    apiKey,
  };
  if (options.alias) identity.alias = options.alias;

  addIdentity(identity);

  const store = loadIdentities();
  if (Object.keys(store).length === 1 || !config.currentAgent) {
    config.currentAgent = agentId;
    saveConfig(config);
  }

  outputSuccess({
    agentId,
    alias: data.data.alias ?? null,
    apiKey,
    message: 'Agent created',
  });
}

export function agentList(): Array<{ agentId: string; alias?: string; current: boolean }> {
  const store = loadIdentities();
  const config = loadConfig();
  return Object.values(store).map((id) => ({
    agentId: id.agentId,
    alias: id.alias,
    current: id.agentId === config.currentAgent,
  }));
}

export function agentUse(target: string): void {
  const store = loadIdentities();
  const agentId = resolveAgentId(store, target);
  if (!agentId) {
    throw new CliError(
      'IDENTITY_NOT_FOUND',
      `No local identity matching "${target}". Run \`rip agent list\` to see available agents.`,
    );
  }
  const config = loadConfig();
  config.currentAgent = agentId;
  saveConfig(config);
  const identity = store[agentId];
  outputSuccess({
    agentId,
    alias: identity.alias ?? null,
    message: `Switched to ${identity.alias || agentId}`,
  });
}

export async function agentExport(target: string, options: { to: string }): Promise<void> {
  const store = loadIdentities();
  const agentId = resolveAgentId(store, target);
  if (!agentId) {
    throw new CliError('IDENTITY_NOT_FOUND', `No local identity matching "${target}".`);
  }
  const identity = store[agentId];
  const blob = encryptIdentityForAgent(identity, options.to, identity.secretKey);
  outputSuccess({
    blob,
    fromAgentId: identity.agentId,
    toAgentId: options.to,
    message: 'Identity exported. Send the blob value to the recipient.',
  });
}

export async function agentImport(file: string): Promise<void> {
  let blob: string;
  if (file === '-') {
    const chunks: Buffer[] = [];
    for await (const chunk of process.stdin) {
      chunks.push(chunk);
    }
    blob = Buffer.concat(chunks).toString('utf-8').trim();
  } else {
    blob = fs.readFileSync(file, 'utf-8').trim();
  }

  const current = resolveCurrentIdentity();
  const identity = decryptIdentityFromAgent(blob, current.secretKey);
  addIdentity(identity);
  outputSuccess({
    agentId: identity.agentId,
    alias: identity.alias ?? null,
    message: `Imported agent ${identity.alias || identity.agentId}`,
  });
}

export function agentRemove(target: string): void {
  const store = loadIdentities();
  const agentId = resolveAgentId(store, target);
  if (!agentId) {
    throw new CliError('IDENTITY_NOT_FOUND', `No local identity matching "${target}".`);
  }
  removeIdentity(agentId);
  const config = loadConfig();
  if (config.currentAgent === agentId) {
    delete config.currentAgent;
    saveConfig(config);
  }
  outputSuccess({
    agentId,
    message: `Removed ${target} from local identities (agent still exists on server)`,
  });
}
