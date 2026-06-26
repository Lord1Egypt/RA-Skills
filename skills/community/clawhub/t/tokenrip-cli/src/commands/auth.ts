import fs from 'node:fs';
import path from 'node:path';
import { loadConfig, getApiUrl, saveConfig, getFrontendUrl, CONFIG_DIR } from '../config.js';
import { createHttpClient } from '../client.js';
import { CliError } from '../errors.js';
import { outputSuccess } from '../output.js';
import { formatAuthKey, formatProfileUpdated, formatWhoami } from '../formatters.js';
import { generateKeypair, publicKeyToAgentId, signPayload } from '../crypto.js';
import { loadIdentity, saveIdentity } from '../identity.js';
import { requireAuthClient } from '../auth-client.js';
import { parseJsonObjectOption } from '../json.js';

export async function authRegister(options: { alias?: string; force?: boolean }): Promise<void> {
  const existing = loadIdentity();

  const config = loadConfig();
  const apiUrl = getApiUrl(config);
  const client = createHttpClient({ baseUrl: apiUrl });

  // Reuse existing identity unless --force creates a fresh one
  const keypair = existing && !options.force
    ? { publicKeyHex: existing.publicKey, secretKeyHex: existing.secretKey }
    : generateKeypair();
  const agentId = publicKeyToAgentId(keypair.publicKeyHex);

  const body: Record<string, string> = { public_key: keypair.publicKeyHex };
  if (options.alias) body.alias = options.alias;

  try {
    const { data } = await client.post('/v0/agents', body);
    const apiKey = data.data.api_key;

    // Only write identity if it's new or forced
    if (!existing || options.force) {
      saveIdentity({
        agentId,
        publicKey: keypair.publicKeyHex,
        secretKey: keypair.secretKeyHex,
      });
    }

    config.apiKey = apiKey;
    saveConfig(config);

    const result: Record<string, unknown> = {
      agentId,
      alias: data.data.alias ?? null,
      apiKey,
      message: existing && !options.force ? 'Registered existing identity with server' : 'Agent registered',
      identity_file: '~/.config/tokenrip/identity.json',
      config_file: '~/.config/tokenrip/config.json',
    };
    if (existing && options.force) {
      result.previous_identity_backup = '~/.config/tokenrip/identity.json.bak';
      result.previous_agent_id = existing.agentId;
    }

    // Best-effort: save skill file on first register so users have a stable path to it
    const skillPath = path.join(CONFIG_DIR, 'SKILL.md');
    if (!fs.existsSync(skillPath)) {
      try {
        const frontendUrl = getFrontendUrl(config);
        const controller = new AbortController();
        setTimeout(() => controller.abort(), 3000);
        const manifestRes = await fetch(`${frontendUrl}/.well-known/skills/tokenrip/manifest.json`, { signal: controller.signal });
        if (manifestRes.ok) {
          const manifest = await manifestRes.json() as { skill_url?: string };
          if (manifest.skill_url) {
            const skillRes = await fetch(manifest.skill_url);
            if (skillRes.ok) {
              fs.mkdirSync(CONFIG_DIR, { recursive: true });
              fs.writeFileSync(skillPath, await skillRes.text(), 'utf-8');
              result.skill_file = skillPath;
            }
          }
        }
      } catch {}
    }

    outputSuccess(result, formatAuthKey);
  } catch (error) {
    // If this identity is already registered, recover the API key via signed token
    if (error instanceof CliError && error.code === 'AGENT_EXISTS' && existing && !options.force) {
      await recoverApiKey(existing, config, apiUrl);
      return;
    }
    if (error instanceof CliError) throw error;
    throw new CliError('REGISTRATION_FAILED', 'Failed to register agent. Is the server running?');
  }
}

async function recoverApiKey(
  identity: { agentId: string; secretKey: string },
  config: ReturnType<typeof loadConfig>,
  apiUrl: string,
): Promise<void> {
  const exp = Math.floor(Date.now() / 1000) + 300; // 5 minutes
  const token = signPayload(
    { sub: 'key-recovery', iss: identity.agentId, exp, jti: Math.random().toString(36).slice(2) },
    identity.secretKey,
  );

  const client = createHttpClient({ baseUrl: apiUrl });
  const { data } = await client.post('/v0/agents/recover-key', { token });
  const apiKey = data.data.api_key;

  config.apiKey = apiKey;
  saveConfig(config);

  outputSuccess(
    { agentId: identity.agentId, apiKey, message: 'API key recovered and saved' },
    formatAuthKey,
  );
}

export async function authCreateKey(): Promise<void> {
  const { client } = requireAuthClient();

  try {
    const { data } = await client.post('/v0/agents/revoke-key');
    const apiKey = data.data.api_key;

    const config = loadConfig();
    config.apiKey = apiKey;
    saveConfig(config);

    outputSuccess({
      apiKey,
      message: 'API key regenerated and saved',
      note: 'Previous key has been revoked',
    }, formatAuthKey);
  } catch (error) {
    if (error instanceof CliError) throw error;
    throw new CliError('KEY_ROTATION_FAILED', 'Failed to regenerate API key.');
  }
}

export async function authWhoami(): Promise<void> {
  const { client } = requireAuthClient();

  try {
    const { data } = await client.get('/v0/agents/me');
    outputSuccess({
      agent_id: data.data.agent_id,
      alias: data.data.alias,
      registered_at: data.data.registered_at,
    }, formatWhoami);
  } catch (error) {
    if (error instanceof CliError) throw error;
    throw new CliError('WHOAMI_FAILED', 'Failed to fetch agent profile.');
  }
}

export async function authUpdate(options: {
  alias?: string;
  metadata?: string;
}): Promise<void> {
  const { client } = requireAuthClient();

  const body: Record<string, unknown> = {};
  if (options.alias !== undefined) {
    body.alias = options.alias === '' ? null : options.alias;
  }
  if (options.metadata !== undefined) {
    body.metadata = parseJsonObjectOption(options.metadata, '--metadata');
  }

  if (Object.keys(body).length === 0) {
    throw new CliError('MISSING_OPTION', 'Provide --alias or --metadata to update');
  }

  const { data } = await client.patch('/v0/agents/me', body);
  outputSuccess(data.data, formatProfileUpdated);
}
