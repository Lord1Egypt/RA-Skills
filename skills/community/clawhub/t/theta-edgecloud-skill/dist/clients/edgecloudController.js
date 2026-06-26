import { deleteEmpty, getJson, postJson, putEmpty, putJson } from './http.js';
import { isStructuredError } from '../errors.js';
const BASE_CTRL = 'https://controller.thetaedgecloud.com';
const BASE_API = 'https://api.thetaedgecloud.com';
const CONTROLLER_DEFAULT_HEADERS = {
    accept: 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
};
function k(cfg) {
    if (!cfg.edgecloudApiKey)
        throw new Error('THETA_EC_API_KEY missing');
    return { ...CONTROLLER_DEFAULT_HEADERS, 'x-api-key': cfg.edgecloudApiKey };
}
function net(cfg, service, headers) {
    return {
        service,
        headers,
        timeoutMs: cfg.httpTimeoutMs,
        maxRetries: cfg.httpMaxRetries,
        retryBackoffMs: cfg.httpRetryBackoffMs
    };
}
function segment(value, field) {
    if (typeof value !== 'string' || !value.trim())
        throw new Error(`${field} must be a non-empty string`);
    return encodeURIComponent(value.trim());
}
function url(base, path, params = {}) {
    const query = new URLSearchParams();
    for (const [key, value] of Object.entries(params)) {
        if (value === undefined || value === null)
            continue;
        query.set(key, String(value));
    }
    const qs = query.toString();
    return `${base}${path}${qs ? `?${qs}` : ''}`;
}
function shouldTryNextRoute(error) {
    if (!isStructuredError(error))
        return false;
    return error.status === 404 || error.status === 405;
}
async function firstRoute(routes, request) {
    const errors = [];
    for (const route of routes) {
        try {
            return await request(route);
        }
        catch (error) {
            errors.push(error);
            if (!shouldTryNextRoute(error))
                throw error;
        }
    }
    throw errors[errors.length - 1] ?? new Error('No controller routes attempted');
}
function documentForm(projectId, file, metadata) {
    if (!file || typeof file !== 'object')
        throw new Error('file must be an object');
    if (!file.filename?.trim())
        throw new Error('file.filename is required');
    if (typeof file.content !== 'string')
        throw new Error('file.content must be a string');
    const bytes = file.encoding === 'base64'
        ? Buffer.from(file.content, 'base64')
        : Buffer.from(file.content, 'utf8');
    const form = new FormData();
    form.set('project_id', projectId);
    form.set('metadata', JSON.stringify(metadata ?? {}));
    form.set('file', new Blob([bytes], { type: file.contentType ?? 'text/plain' }), file.filename);
    return form;
}
async function postForm(targetUrl, form, cfg) {
    const res = await fetch(targetUrl, {
        method: 'POST',
        headers: k(cfg),
        body: form,
        signal: AbortSignal.timeout(cfg.httpTimeoutMs)
    });
    if (!res.ok)
        throw new Error(await res.text());
    return res.json();
}
async function putForm(targetUrl, form, cfg) {
    const res = await fetch(targetUrl, {
        method: 'PUT',
        headers: k(cfg),
        body: form,
        signal: AbortSignal.timeout(cfg.httpTimeoutMs)
    });
    if (!res.ok)
        throw new Error(await res.text());
    return res.json();
}
export const edgecloudControllerClient = {
    listStandardTemplates: (cfg, category) => getJson(`${BASE_CTRL}/deployment_template/list_standard_templates?category=${category}`, net(cfg, 'edgecloud-controller', k(cfg))),
    listCustomTemplates: (cfg, projectId) => getJson(`${BASE_CTRL}/deployment_template/list_custom_templates?project_id=${projectId}`, net(cfg, 'edgecloud-controller', k(cfg))),
    listVmTypes: (cfg) => getJson(`${BASE_API}/resource/vm/list`, net(cfg, 'edgecloud-controller', CONTROLLER_DEFAULT_HEADERS)),
    createDeployment: (cfg, payload) => postJson(`${BASE_CTRL}/deployment`, payload, net(cfg, 'edgecloud-controller', k(cfg))),
    listDeployments: (cfg, projectId) => firstRoute([
        url(BASE_CTRL, '/deployment/list', { project_id: projectId }),
        url(BASE_CTRL, '/deployments/list', { project_id: projectId })
    ], (route) => getJson(route, net(cfg, 'edgecloud-controller', k(cfg)))),
    routeProbeDeploymentsList: async (cfg, projectId) => {
        const routes = [
            url(BASE_CTRL, '/deployment/list', { project_id: projectId }),
            url(BASE_CTRL, '/deployments/list', { project_id: projectId })
        ];
        const attempts = [];
        for (const route of routes) {
            try {
                const response = await getJson(route, net(cfg, 'edgecloud-controller', k(cfg)));
                attempts.push({ route, ok: true });
                return { ok: true, selectedRoute: route, attempts, response };
            }
            catch (error) {
                attempts.push({
                    route,
                    ok: false,
                    status: isStructuredError(error) ? error.status : undefined,
                    code: isStructuredError(error) ? error.code : error?.name,
                    message: error?.message ?? String(error)
                });
            }
        }
        return { ok: false, attempts };
    },
    balance: (cfg, orgId) => getJson(url(BASE_API, '/balance', { orgID: orgId }), net(cfg, 'edgecloud-controller', k(cfg))),
    createChatbot: (cfg, payload) => postJson(`${BASE_CTRL}/chatbot`, payload, net(cfg, 'edgecloud-controller', k(cfg))),
    getChatbot: (cfg, chatbotId, projectId) => getJson(url(BASE_CTRL, `/chatbot/${segment(chatbotId, 'chatbotId')}`, { project_id: projectId }), net(cfg, 'edgecloud-controller', k(cfg))),
    updateChatbot: (cfg, chatbotId, payload) => putJson(`${BASE_CTRL}/chatbot/${segment(chatbotId, 'chatbotId')}`, payload, net(cfg, 'edgecloud-controller', k(cfg))),
    listChatbots: (cfg, projectId, page = 0, number = 100) => getJson(url(BASE_CTRL, '/chatbot/list', { project_id: projectId, page, number }), net(cfg, 'edgecloud-controller', k(cfg))),
    createChatbotDocument: (cfg, chatbotId, projectId, file, metadata) => postForm(url(BASE_CTRL, `/chatbot/${segment(chatbotId, 'chatbotId')}/document`), documentForm(projectId, file, metadata), cfg),
    updateChatbotDocument: (cfg, chatbotId, documentId, projectId, file, metadata) => putForm(url(BASE_CTRL, `/chatbot/${segment(chatbotId, 'chatbotId')}/document/${segment(documentId, 'documentId')}`), documentForm(projectId, file, metadata), cfg),
    getChatbotDocument: (cfg, chatbotId, documentId) => getJson(url(BASE_CTRL, `/chatbot/${segment(chatbotId, 'chatbotId')}/document/${segment(documentId, 'documentId')}`), net(cfg, 'edgecloud-controller', k(cfg))),
    listChatbotDocuments: (cfg, chatbotId, projectId, page = 0, number = 30) => getJson(url(BASE_CTRL, `/chatbot/${segment(chatbotId, 'chatbotId')}/document/list`, { project_id: projectId, page, number }), net(cfg, 'edgecloud-controller', k(cfg))),
    stopDeployment: (cfg, projectId, shard, suffix) => firstRoute([
        url(BASE_CTRL, `/deployment/${segment(shard, 'shard')}/${segment(suffix, 'suffix')}/stop`, { project_id: projectId }),
        url(BASE_CTRL, `/deployments/${segment(shard, 'shard')}/${segment(suffix, 'suffix')}/stop`, { project_id: projectId })
    ], (route) => putEmpty(route, net(cfg, 'edgecloud-controller', k(cfg)))),
    startDeployment: (cfg, projectId, shard, suffix) => firstRoute([
        url(BASE_CTRL, `/deployment/${segment(shard, 'shard')}/${segment(suffix, 'suffix')}/start`, { project_id: projectId }),
        url(BASE_CTRL, `/deployments/${segment(shard, 'shard')}/${segment(suffix, 'suffix')}/start`, { project_id: projectId })
    ], (route) => putEmpty(route, net(cfg, 'edgecloud-controller', k(cfg)))),
    deleteDeployment: (cfg, projectId, shard, suffix) => firstRoute([
        url(BASE_CTRL, `/deployment/${segment(shard, 'shard')}/${segment(suffix, 'suffix')}`, { project_id: projectId }),
        url(BASE_CTRL, `/deployments/${segment(shard, 'shard')}/${segment(suffix, 'suffix')}`, { project_id: projectId })
    ], (route) => deleteEmpty(route, net(cfg, 'edgecloud-controller', k(cfg))))
};
