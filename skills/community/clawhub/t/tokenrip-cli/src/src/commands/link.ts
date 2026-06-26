import { loadConfig, getApiUrl, saveConfig } from '../config.js';
import { createHttpClient } from '../client.js';
import { CliError } from '../errors.js';
import { outputSuccess } from '../output.js';
import { formatAuthKey } from '../formatters.js';
import { addIdentity, loadIdentities } from '../identities.js';
import { loadIdentity } from '../identity.js';

export async function link(options: { alias: string; password: string; force?: boolean }): Promise<void> {
  const existing = loadIdentity();
  if (existing && !options.force) {
    throw new CliError(
      'IDENTITY_EXISTS',
      'A local agent identity already exists. Use --force to overwrite, or use `rip auth register` for a new identity.',
    );
  }

  const config = loadConfig();
  const apiUrl = getApiUrl(config);
  const client = createHttpClient({ baseUrl: apiUrl });

  const { data } = await client.post('/oauth/cli-link', {
    alias: options.alias,
    password: options.password,
  });

  const { agent_id, public_key, secret_key, api_key } = data.data;

  addIdentity({
    agentId: agent_id,
    publicKey: public_key,
    secretKey: secret_key,
    apiKey: api_key,
  });

  const store = loadIdentities();
  if (Object.keys(store).length === 1 || !config.currentAgent) {
    config.currentAgent = agent_id;
    saveConfig(config);
  }

  outputSuccess(
    {
      agentId: agent_id,
      apiKey: api_key,
      message: 'CLI linked to existing agent',
      identity_file: '~/.config/tokenrip/identity.json',
      config_file: '~/.config/tokenrip/config.json',
    },
    formatAuthKey,
  );
}
