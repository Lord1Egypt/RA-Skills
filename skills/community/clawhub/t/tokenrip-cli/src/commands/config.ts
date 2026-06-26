import { loadConfig, saveConfig, getApiUrl, getApiKey, getFrontendUrl } from '../config.js';
import { outputSuccess } from '../output.js';
import { CliError } from '../errors.js';
import { formatConfigSaved, formatConfigShow } from '../formatters.js';

export async function configSetKey(key: string): Promise<void> {
  const config = loadConfig();
  config.apiKey = key;
  saveConfig(config);
  outputSuccess({ message: 'API key saved' }, formatConfigSaved);
}

export async function configSetUrl(url: string): Promise<void> {
  const config = loadConfig();
  config.apiUrl = url;
  saveConfig(config);
  outputSuccess({ message: 'API URL saved', apiUrl: url }, formatConfigSaved);
}

export async function configSetOutput(format: string): Promise<void> {
  if (format !== 'json' && format !== 'human') {
    throw new CliError('INVALID_OUTPUT_FORMAT', 'Output format must be "json" or "human".');
  }
  const config = loadConfig();
  config.preferences = { ...config.preferences, outputFormat: format };
  saveConfig(config);
  outputSuccess({ message: `Output format set to "${format}"` }, formatConfigSaved);
}

export async function configShow(): Promise<void> {
  const config = loadConfig();
  const apiUrl = getApiUrl(config);
  const apiKey = getApiKey(config);
  const frontendUrl = getFrontendUrl(config);
  const hasKey = apiKey ? 'yes (saved)' : 'no (env/not set)';
  const outputFormat = (config.preferences?.outputFormat as string | undefined) ?? 'json (default)';
  outputSuccess({
    apiUrl,
    frontendUrl,
    apiKey: hasKey,
    outputFormat,
    configFile: '~/.config/tokenrip/config.json',
  }, formatConfigShow);
}
