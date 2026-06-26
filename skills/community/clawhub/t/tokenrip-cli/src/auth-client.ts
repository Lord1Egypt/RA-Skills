import { AxiosInstance } from 'axios';
import { loadConfig, getApiUrl, getApiKey, TokenripConfig } from './config.js';
import { createHttpClient } from './client.js';
import { CliError } from './errors.js';

export interface AuthContext {
  client: AxiosInstance;
  config: TokenripConfig;
  apiUrl: string;
}

export function requireAuthClient(): AuthContext {
  const config = loadConfig();
  const apiKey = getApiKey(config);
  if (!apiKey) {
    throw new CliError(
      'NO_API_KEY',
      'No API key configured. Run `rip auth register` to set up your agent.',
    );
  }
  const apiUrl = getApiUrl(config);
  const client = createHttpClient({ baseUrl: apiUrl, apiKey });
  return { client, config, apiUrl };
}

export function optionalAuthClient(): { client: AxiosInstance; apiUrl: string } {
  const config = loadConfig();
  const apiKey = getApiKey(config);
  const apiUrl = getApiUrl(config);
  const client = createHttpClient({ baseUrl: apiUrl, apiKey: apiKey || undefined });
  return { client, apiUrl };
}
