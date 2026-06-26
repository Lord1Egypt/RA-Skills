import { loadConfig, getApiUrl } from '../config.js';
import { createHttpClient } from '../client.js';
import { CliError } from '../errors.js';
import { outputSuccess } from '../output.js';
import { formatAuthKey, formatProfileUpdated, formatWhoami } from '../formatters.js';
import { signPayload } from '../crypto.js';
import { resolveCurrentIdentity, loadIdentities, saveIdentities } from '../identities.js';
import { requireAuthClient } from '../auth-client.js';
import { parseJsonObjectOption } from '../json.js';

export async function authRegister(options: { alias?: string; force?: boolean }): Promise<void> {
  let hasExisting = false;
  try {
    resolveCurrentIdentity();
    hasExisting = true;
  } catch {
    // no identity found
  }

  if (hasExisting && !options.force) {
    await recoverApiKey();
    return;
  }

  const { agentCreate } = await import('./agent.js');
  await agentCreate({ alias: options.alias });
}

async function recoverApiKey(): Promise<void> {
  const identity = resolveCurrentIdentity();
  const config = loadConfig();
  const apiUrl = getApiUrl(config);

  const exp = Math.floor(Date.now() / 1000) + 300;
  const token = signPayload(
    { sub: 'key-recovery', iss: identity.agentId, exp, jti: Math.random().toString(36).slice(2) },
    identity.secretKey,
  );

  const client = createHttpClient({ baseUrl: apiUrl });
  const { data } = await client.post('/v0/agents/recover-key', { token });
  const apiKey = data.data.api_key;

  const store = loadIdentities();
  if (store[identity.agentId]) {
    store[identity.agentId].apiKey = apiKey;
    saveIdentities(store);
  }

  outputSuccess(
    { agentId: identity.agentId, apiKey, message: 'API key recovered and saved' },
    formatAuthKey,
  );
}

export async function authCreateKey(): Promise<void> {
  const { client } = requireAuthClient();
  const identity = resolveCurrentIdentity();

  try {
    const { data } = await client.post('/v0/agents/revoke-key');
    const apiKey = data.data.api_key;

    const store = loadIdentities();
    if (store[identity.agentId]) {
      store[identity.agentId].apiKey = apiKey;
      saveIdentities(store);
    }

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
      tag: data.data.tag,
      description: data.data.description,
      website: data.data.website,
      email: data.data.email,
      is_public: data.data.is_public,
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
  tag?: string;
  description?: string;
  website?: string;
  email?: string;
  public?: string;
}): Promise<void> {
  const { client } = requireAuthClient();

  const body: Record<string, unknown> = {};
  if (options.alias !== undefined) {
    body.alias = options.alias === '' ? null : options.alias;
  }
  if (options.metadata !== undefined) {
    body.metadata = parseJsonObjectOption(options.metadata, '--metadata');
  }
  if (options.tag !== undefined) {
    body.tag = options.tag === '' ? null : options.tag;
  }
  if (options.description !== undefined) {
    body.description = options.description === '' ? null : options.description;
  }
  if (options.website !== undefined) {
    body.website = options.website === '' ? null : options.website;
  }
  if (options.email !== undefined) {
    body.email = options.email === '' ? null : options.email;
  }
  if (options.public !== undefined) {
    body.is_public = options.public === 'true';
  }

  if (Object.keys(body).length === 0) {
    throw new CliError('MISSING_OPTION', 'Provide at least one option to update (--alias, --tag, --description, --website, --email, --public, --metadata)');
  }

  const { data } = await client.patch('/v0/agents/me', body);
  outputSuccess(data.data, formatProfileUpdated);
}
