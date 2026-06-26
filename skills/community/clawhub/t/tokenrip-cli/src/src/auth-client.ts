import { AxiosInstance } from 'axios';
import { loadConfig, getApiUrl, TokenripConfig } from './config.js';
import { createHttpClient } from './client.js';
import { CliError } from './errors.js';
import { resolveCurrentIdentity } from './identities.js';

export interface AuthContext {
  client: AxiosInstance;
  config: TokenripConfig;
  apiUrl: string;
}

export function requireAuthClient(): AuthContext {
  const identity = resolveCurrentIdentity();
  const config = loadConfig();
  const apiKey = process.env.TOKENRIP_API_KEY || identity.apiKey;
  if (!apiKey) {
    throw new CliError(
      'NO_API_KEY',
      `No API key for agent ${identity.alias || identity.agentId}. Run \`rip agent create\` to re-register.`,
    );
  }
  const apiUrl = getApiUrl(config);
  const client = createHttpClient({ baseUrl: apiUrl, apiKey });
  return { client, config, apiUrl };
}

export function optionalAuthClient(): { client: AxiosInstance; apiUrl: string } {
  const config = loadConfig();
  let apiKey: string | undefined = process.env.TOKENRIP_API_KEY || config.apiKey;
  if (!apiKey) {
    try { apiKey = resolveCurrentIdentity().apiKey; } catch { /* public access */ }
  }
  const apiUrl = getApiUrl(config);
  const client = createHttpClient({ baseUrl: apiUrl, apiKey: apiKey || undefined });
  return { client, apiUrl };
}
