import yaml from 'js-yaml';
import { readFileSync, existsSync } from 'fs';
import { ConfigSchema, type Config } from './schema';

const PROJECT_ROOT = process.cwd();

function deepMerge<T extends Record<string, any>>(target: T, source: T): T {
  const output = { ...target };
  if (isObject(target) && isObject(source)) {
    Object.keys(source).forEach(key => {
      if (isObject(source[key])) {
        if (!(key in target)) {
          Object.assign(output, { [key]: source[key] });
        } else {
          output[key] = deepMerge(target[key], source[key]);
        }
      } else {
        Object.assign(output, { [key]: source[key] });
      }
    });
  }
  return output;
}

function isObject(item: any): item is Record<string, any> {
  return item && typeof item === 'object' && !Array.isArray(item);
}

function loadYaml(path: string): Record<string, any> {
  try {
    const content = readFileSync(path, 'utf8');
    return yaml.load(content) as Record<string, any>;
  } catch (err) {
    console.error(`Failed to load YAML from ${path}:`, err);
    process.exit(1);
  }
}

function applyEnvOverrides(config: Config): Config {
  // SPM_PROJECT_EXECUTION_MODE=inline → overrides project.execution_mode
  const overrides: Record<string, any> = {};

  for (const [key, value] of Object.entries(process.env)) {
    if (key.startsWith('SPM_')) {
      const path = key.slice(4).toLowerCase().replace(/_/g, '.');
      let parsed: any = value;
      if (/^\d+$/.test(value)) parsed = parseInt(value, 10);
      else if (/^\d*\.\d+$/.test(value)) parsed = parseFloat(value);
      else if (/^(true|false)$/i.test(value)) parsed = value.toLowerCase() === 'true';

      const parts = path.split('.');
      let current = overrides;
      for (let i = 0; i < parts.length - 1; i++) {
        if (!current[parts[i]]) current[parts[i]] = {};
        current = current[parts[i]];
      }
      current[parts[parts.length - 1]] = parsed;
    }
  }

  return deepMerge(config, overrides) as Config;
}

let _config: Config | null = null;

export function loadConfig(env?: string): Config {
  if (_config) return _config;

  const environment = env || process.env.SPM_ENV || 'development';

  const defaultPath = `${PROJECT_ROOT}/config/default.yaml`;
  if (!existsSync(defaultPath)) {
    console.error(`Missing config/default.yaml.`);
    process.exit(1);
  }
  const defaultCfg = loadYaml(defaultPath);

  const envPath = `${PROJECT_ROOT}/config/${environment}.yaml`;
  const envCfg = existsSync(envPath) ? loadYaml(envPath) : {};

  const merged = deepMerge(defaultCfg, envCfg);
  const withEnvOverrides = applyEnvOverrides(merged);

  try {
    _config = ConfigSchema.parse(withEnvOverrides);
  } catch (err) {
    console.error('Configuration validation failed:', err);
    process.exit(1);
  }

  return _config;
}

/**
 * Get a config value by dot-notation path.
 * Example: get('quality.coverage_target')
 */
export function get(path: string): any {
  if (!_config) {
    console.warn('Config not loaded yet. Call loadConfig() first.');
    return undefined;
  }
  const parts = path.split('.');
  let current: any = _config;
  for (const part of parts) {
    if (current && typeof current === 'object' && part in current) {
      current = current[part];
    } else {
      return undefined;
    }
  }
  return current;
}

export function getAll(): Config {
  if (!_config) {
    throw new Error('Config not loaded. Call loadConfig() first.');
  }
  return { ..._config };
}

export const isDevelopment = () => get('deployment.environment') === 'development';
export const isProduction = () => get('deployment.environment') === 'production';
export const isSubagentMode = () => get('project.execution_mode') === 'subagent';
export const getCoverageTarget = () => get('quality.coverage_target') as number;
export const getHeartbeatInterval = () => get('tracking.heartbeat_interval');
export const getModelForTier = (tier: 'fast' | 'standard' | 'strong') =>
  get(`model_routing.${tier}.model`) as string;
