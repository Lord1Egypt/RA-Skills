import { getJson, postJson } from './http.js';
const ALLOWED_INFERENCE_DOMAIN_SUFFIXES = ['.thetaedgecloud.com', '.onthetaedgecloud.com'];
function isLoopbackOrPrivateHost(hostname) {
    const host = hostname.toLowerCase();
    if (host === 'localhost' || host === '::1' || host === '0.0.0.0' || host === '::ffff:127.0.0.1')
        return true;
    if (/^\d{1,3}(\.\d{1,3}){3}$/.test(host)) {
        const parts = host.split('.').map((p) => Number.parseInt(p, 10));
        if (parts.some((p) => !Number.isInteger(p) || p < 0 || p > 255))
            return true;
        if (parts[0] === 10 || parts[0] === 127)
            return true;
        if (parts[0] === 169 && parts[1] === 254)
            return true;
        if (parts[0] === 192 && parts[1] === 168)
            return true;
        if (parts[0] === 172 && parts[1] >= 16 && parts[1] <= 31)
            return true;
    }
    return host.startsWith('fe80:') || host.startsWith('fc') || host.startsWith('fd');
}
function parseEndpoint(raw, label) {
    try {
        const parsed = new URL(raw.trim());
        if (parsed.protocol !== 'https:')
            throw new Error(`${label} must use https://`);
        if (parsed.username || parsed.password)
            throw new Error(`${label} must not include embedded credentials`);
        if (!parsed.hostname || isLoopbackOrPrivateHost(parsed.hostname)) {
            throw new Error(`${label} host is unsafe (private/loopback not allowed)`);
        }
        return parsed;
    }
    catch (error) {
        if (error instanceof Error && error.message.includes(label))
            throw error;
        throw new Error(`${label} must be an absolute https URL`);
    }
}
function isAllowedHost(hostname) {
    const host = hostname.toLowerCase();
    return ALLOWED_INFERENCE_DOMAIN_SUFFIXES.some((suffix) => host === suffix.slice(1) || host.endsWith(suffix));
}
function endpoint(cfg, e) {
    const v = e ?? cfg.inferenceEndpoint;
    if (!v)
        throw new Error('THETA_INFERENCE_ENDPOINT missing');
    const parsed = parseEndpoint(v, 'THETA_INFERENCE_ENDPOINT');
    if (!isAllowedHost(parsed.hostname)) {
        throw new Error('THETA_INFERENCE_ENDPOINT host is not allowed; use a Theta EdgeCloud endpoint');
    }
    return parsed.href.replace(/\/$/, '');
}
function auth(cfg, a) {
    return a ?? cfg.inferenceAuth;
}
function net(cfg, service, authOverride) {
    return {
        service,
        auth: authOverride,
        timeoutMs: cfg.httpTimeoutMs,
        maxRetries: cfg.httpMaxRetries,
        retryBackoffMs: cfg.httpRetryBackoffMs
    };
}
export const edgecloudInferenceClient = {
    listModels: (cfg, e, a) => getJson(`${endpoint(cfg, e)}/v1/models`, net(cfg, 'edgecloud-inference', auth(cfg, a))),
    gradioConfig: (cfg, e, a) => getJson(`${endpoint(cfg, e)}/config`, net(cfg, 'edgecloud-inference', auth(cfg, a))),
    chat: (cfg, body, e, a) => postJson(`${endpoint(cfg, e)}/v1/chat/completions`, body, net(cfg, 'edgecloud-inference', auth(cfg, a)))
};
