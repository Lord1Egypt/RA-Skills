const env = process.env;
function readInt(name, fallback, opts) {
    const raw = env[name];
    if (!raw)
        return fallback;
    const parsed = Number.parseInt(raw, 10);
    if (!Number.isFinite(parsed))
        return fallback;
    const min = opts?.min;
    const max = opts?.max;
    if (min !== undefined && parsed < min)
        return min;
    if (max !== undefined && parsed > max)
        return max;
    return parsed;
}
export function loadConfig() {
    const user = env.THETA_INFERENCE_AUTH_USER;
    const pass = env.THETA_INFERENCE_AUTH_PASS;
    return {
        dryRun: env.THETA_DRY_RUN === '1',
        edgecloudApiKey: env.THETA_EC_API_KEY,
        edgecloudProjectId: env.THETA_EC_PROJECT_ID,
        edgecloudOrgId: env.THETA_ORG_ID,
        videoSaId: env.THETA_VIDEO_SA_ID,
        videoSaSecret: env.THETA_VIDEO_SA_SECRET,
        inferenceEndpoint: env.THETA_INFERENCE_ENDPOINT,
        inferenceAuth: user && pass ? { user, pass } : undefined,
        onDemandApiToken: env.THETA_ONDEMAND_API_TOKEN ?? env.THETA_ONDEMAND_API_KEY ?? env.THETA_API_KEY,
        onDemandApiBaseUrl: env.THETA_ONDEMAND_API_BASE_URL ?? env.THETA_API_BASE_URL,
        edgecloudRpcUrl: env.THETA_EDGECLOUD_RPC_URL,
        chainRpcUrl: env.THETA_CHAIN_RPC_URL,
        cliRpcUrl: env.THETA_CLI_RPC_URL,
        httpTimeoutMs: readInt('THETA_HTTP_TIMEOUT_MS', 20000, { min: 1000, max: 120000 }),
        httpMaxRetries: readInt('THETA_HTTP_MAX_RETRIES', 2, { min: 0, max: 6 }),
        httpRetryBackoffMs: readInt('THETA_HTTP_RETRY_BACKOFF_MS', 250, { min: 25, max: 10000 })
    };
}
