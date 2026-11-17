import { BasicAuth } from './types.js';

export type ThetaConfig = {
  dryRun: boolean;
  edgecloudApiKey?: string;
  edgecloudProjectId?: string;
  edgecloudOrgId?: string;
  videoSaId?: string;
  videoSaSecret?: string;
  charactersApiKey?: string;
  inferenceEndpoint?: string;
  inferenceAuth?: BasicAuth;
  onDemandApiToken?: string;
  onDemandApiBaseUrl?: string;
  httpTimeoutMs: number;
  httpMaxRetries: number;
  httpRetryBackoffMs: number;
};

const processEnv = process.env;

function readInt(name: string, fallback: number, opts?: { min?: number; max?: number }): number {
  const raw = processEnv[name];
  if (!raw) return fallback;
  const parsed = Number.parseInt(raw, 10);
  if (!Number.isFinite(parsed)) return fallback;

  const min = opts?.min;
  const max = opts?.max;
  if (min !== undefined && parsed < min) return min;
  if (max !== undefined && parsed > max) return max;
  return parsed;
}

export function loadConfig(): ThetaConfig {
  const user = processEnv.THETA_INFERENCE_AUTH_USER;
  const pass = processEnv.THETA_INFERENCE_AUTH_PASS;
  return {
    dryRun: ['1', 'true', 'yes', 'on'].includes(String(processEnv.THETA_DRY_RUN ?? '').trim().toLowerCase()),
    edgecloudApiKey: processEnv.THETA_EC_API_KEY,
    edgecloudProjectId: processEnv.THETA_EC_PROJECT_ID,
    edgecloudOrgId: processEnv.THETA_ORG_ID,
    videoSaId: processEnv.THETA_VIDEO_SA_ID,
    videoSaSecret: processEnv.THETA_VIDEO_SA_SECRET,
    charactersApiKey: processEnv.THETA_CHARACTERS_API_KEY,
    inferenceEndpoint: processEnv.THETA_INFERENCE_ENDPOINT,
    inferenceAuth: user && pass ? { user, pass } : undefined,
    onDemandApiToken: processEnv.THETA_ONDEMAND_API_TOKEN ?? processEnv.THETA_ONDEMAND_API_KEY ?? processEnv.THETA_API_KEY,
    onDemandApiBaseUrl: processEnv.THETA_ONDEMAND_API_BASE_URL ?? processEnv.THETA_API_BASE_URL,
    httpTimeoutMs: readInt('THETA_HTTP_TIMEOUT_MS', 20000, { min: 1000, max: 120000 }),
    httpMaxRetries: readInt('THETA_HTTP_MAX_RETRIES', 2, { min: 0, max: 6 }),
    httpRetryBackoffMs: readInt('THETA_HTTP_RETRY_BACKOFF_MS', 250, { min: 25, max: 10000 })
  };
}
