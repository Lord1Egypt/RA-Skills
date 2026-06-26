import { edgecloudControllerClient } from '../clients/edgecloudController.js';
import { edgecloudInferenceClient } from '../clients/edgecloudInference.js';
import { redactObject } from '../redaction.js';
import { randomBytes } from 'node:crypto';
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
function requireText(value, field) {
    if (value === undefined || value === null || String(value).trim() === '') {
        throw new Error(`${field} must be a non-empty string`);
    }
    return String(value).trim();
}
function clampInt(value, fallback, min, max) {
    if (!Number.isFinite(value))
        return fallback;
    return Math.min(Math.max(Math.trunc(value), min), max);
}
function generatedPassword() {
    return randomBytes(18).toString('base64url');
}
function findKey(obj, names) {
    if (obj && typeof obj === 'object') {
        if (Array.isArray(obj)) {
            for (const item of obj) {
                const found = findKey(item, names);
                if (found !== undefined && found !== null && found !== '')
                    return found;
            }
            return undefined;
        }
        for (const [key, value] of Object.entries(obj)) {
            if (names.has(key.toLowerCase()) && value !== undefined && value !== null && value !== '')
                return value;
        }
        for (const value of Object.values(obj)) {
            const found = findKey(value, names);
            if (found !== undefined && found !== null && found !== '')
                return found;
        }
    }
    return undefined;
}
function extractNumericValue(obj, names) {
    if (obj && typeof obj === 'object') {
        if (Array.isArray(obj)) {
            for (const item of obj) {
                const found = extractNumericValue(item, names);
                if (found !== undefined)
                    return found;
            }
            return undefined;
        }
        for (const [key, value] of Object.entries(obj)) {
            if (!names.has(key.toLowerCase()))
                continue;
            const parsed = Number(value);
            if (Number.isFinite(parsed))
                return parsed;
        }
        for (const value of Object.values(obj)) {
            const found = extractNumericValue(value, names);
            if (found !== undefined)
                return found;
        }
    }
    return undefined;
}
function balanceValue(response) {
    return extractNumericValue(response, new Set(['balance', 'amount', 'available', 'credit', 'credits', 'remaining', 'total']));
}
async function balanceSnapshot(cfg, orgId) {
    const resolvedOrgId = orgId ?? cfg.edgecloudOrgId;
    if (!resolvedOrgId)
        return { skipped: true, reason: 'missing_org_id' };
    if (!cfg.edgecloudApiKey)
        return { skipped: true, reason: 'missing_THETA_EC_API_KEY' };
    try {
        const response = await edgecloudControllerClient.balance(cfg, resolvedOrgId);
        return { skipped: false, orgId: resolvedOrgId, value: balanceValue(response), response };
    }
    catch (error) {
        return {
            skipped: true,
            reason: 'balance_lookup_failed',
            error: error?.message ?? String(error)
        };
    }
}
function balanceDelta(before, after) {
    const beforeValue = typeof before.value === 'number' ? before.value : undefined;
    const afterValue = typeof after.value === 'number' ? after.value : undefined;
    return {
        before,
        after,
        delta: beforeValue !== undefined && afterValue !== undefined ? afterValue - beforeValue : null
    };
}
async function waitForDedicatedProbe(cfg, endpoint, auth, probe, timeoutMs, intervalMs) {
    const startedAt = Date.now();
    const attempts = [];
    while (Date.now() - startedAt < timeoutMs) {
        const attemptStartedAt = Date.now();
        try {
            const response = probe === 'gradio'
                ? await edgecloudInferenceClient.gradioConfig(cfg, endpoint, auth)
                : await edgecloudInferenceClient.listModels(cfg, endpoint, auth);
            attempts.push({ ok: true, elapsedMs: Date.now() - attemptStartedAt });
            return { ready: true, probe, endpoint, elapsedMs: Date.now() - startedAt, attempts, response };
        }
        catch (error) {
            attempts.push({
                ok: false,
                elapsedMs: Date.now() - attemptStartedAt,
                status: error?.status,
                code: error?.code ?? error?.name,
                message: error?.message ?? String(error)
            });
        }
        const remainingMs = timeoutMs - (Date.now() - startedAt);
        if (remainingMs <= 0)
            break;
        await sleep(Math.min(intervalMs, remainingMs));
    }
    return { ready: false, probe, endpoint, elapsedMs: Date.now() - startedAt, attempts };
}
export const deployments = {
    listStandard: (cfg, category) => edgecloudControllerClient.listStandardTemplates(cfg, category),
    listCustom: (cfg, projectId) => edgecloudControllerClient.listCustomTemplates(cfg, projectId),
    listVm: (cfg) => edgecloudControllerClient.listVmTypes(cfg),
    balance: (cfg, orgId) => edgecloudControllerClient.balance(cfg, requireText(orgId ?? cfg.edgecloudOrgId, 'orgId')),
    balanceSnapshot,
    routeProbe: (cfg, projectId) => edgecloudControllerClient.routeProbeDeploymentsList(cfg, projectId),
    create: (cfg, payload) => cfg.dryRun ? { dryRun: true, payload } : edgecloudControllerClient.createDeployment(cfg, payload),
    list: (cfg, projectId) => edgecloudControllerClient.listDeployments(cfg, projectId),
    start: (cfg, projectId, shard, suffix) => cfg.dryRun ? { dryRun: true, action: 'start', projectId, shard, suffix } : edgecloudControllerClient.startDeployment(cfg, projectId, shard, suffix),
    stop: (cfg, projectId, shard, suffix) => cfg.dryRun ? { dryRun: true, action: 'stop', projectId, shard, suffix } : edgecloudControllerClient.stopDeployment(cfg, projectId, shard, suffix),
    delete: (cfg, projectId, shard, suffix) => cfg.dryRun ? { dryRun: true, action: 'delete', projectId, shard, suffix } : edgecloudControllerClient.deleteDeployment(cfg, projectId, shard, suffix),
    validateDisposable: async (cfg, opts) => {
        const payload = { ...opts.payload };
        const projectId = String(opts.projectId ?? payload.project_id ?? cfg.edgecloudProjectId ?? '').trim();
        if (!projectId)
            throw new Error('projectId or payload.project_id is required');
        payload.project_id = projectId;
        const authUser = String(payload.auth_username ?? `openclaw_${randomBytes(4).toString('hex')}`);
        const authPass = String(payload.auth_password ?? generatedPassword());
        payload.auth_username = authUser;
        payload.auth_password = authPass;
        const auth = { user: authUser, pass: authPass };
        const probe = opts.probe ?? 'openai';
        const readyTimeoutMs = clampInt(opts.readyTimeoutMs, 120000, 1000, 1800000);
        const intervalMs = clampInt(opts.intervalMs, 10000, 500, 60000);
        if (cfg.dryRun) {
            return redactObject({
                dryRun: true,
                would: [
                    'read org balance before if orgId is configured',
                    'create deployment with generated Basic Auth',
                    `poll ${probe} readiness`,
                    'run one minimal smoke call for OpenAI-compatible probes',
                    'delete deployment in cleanup',
                    'verify cleanup from deployment list',
                    'read org balance after and report delta'
                ],
                payload,
                probe,
                readyTimeoutMs,
                intervalMs,
                orgIdConfigured: Boolean(opts.orgId ?? cfg.edgecloudOrgId)
            });
        }
        let created;
        let readiness;
        let smoke;
        let deleteResult;
        let cleanupVerification;
        const before = await balanceSnapshot(cfg, opts.orgId);
        try {
            created = await edgecloudControllerClient.createDeployment(cfg, payload);
            const endpoint = String(findKey(created, new Set(['endpoint', 'endpointurl', 'url'])) ?? '').trim();
            if (!endpoint)
                throw new Error('Deployment create response did not include an endpoint');
            readiness = await waitForDedicatedProbe(cfg, endpoint, auth, probe, readyTimeoutMs, intervalMs);
            if (probe === 'openai' && readiness.ready && opts.smokeMessage) {
                const readinessModel = findKey(readiness.response, new Set(['id', 'model']));
                smoke = await edgecloudInferenceClient.chat(cfg, {
                    model: opts.model ?? String(readinessModel ?? 'default'),
                    messages: [{ role: 'user', content: opts.smokeMessage }],
                    max_tokens: 32
                }, endpoint, auth);
            }
        }
        finally {
            const baseId = created ? findKey(created, new Set(['baseid', 'base_id', 'deployment_id', 'id'])) : undefined;
            const shard = created ? findKey(created, new Set(['shard'])) : undefined;
            const suffix = created ? findKey(created, new Set(['suffix'])) : undefined;
            if (created && shard && suffix) {
                try {
                    await edgecloudControllerClient.deleteDeployment(cfg, projectId, String(shard), String(suffix));
                    deleteResult = { ok: true, shard, suffix };
                }
                catch (error) {
                    deleteResult = { ok: false, error: error?.message ?? String(error) };
                }
            }
            else {
                deleteResult = { ok: false, warning: 'could_not_determine_delete_handle', baseId, shard, suffix };
            }
            try {
                const listed = await edgecloudControllerClient.listDeployments(cfg, projectId);
                const needleValues = [baseId, shard, suffix].filter((value) => value !== undefined && value !== null && value !== '').map(String);
                const listedText = JSON.stringify(listed);
                cleanupVerification = {
                    checked: true,
                    projectId,
                    deletedHandlesAbsent: !needleValues.some((value) => listedText.includes(value)),
                    handlesChecked: needleValues
                };
            }
            catch (error) {
                cleanupVerification = { checked: false, error: error?.message ?? String(error) };
            }
        }
        const after = await balanceSnapshot(cfg, opts.orgId);
        return redactObject({
            createResponse: created,
            readiness,
            smokeResponse: smoke,
            deleteResult,
            cleanupVerification,
            balance: balanceDelta(before, after)
        });
    },
    chatbotCreate: (cfg, payload) => cfg.dryRun ? { dryRun: true, payload } : edgecloudControllerClient.createChatbot(cfg, payload),
    chatbotGet: (cfg, chatbotId, projectId) => edgecloudControllerClient.getChatbot(cfg, chatbotId, projectId),
    chatbotUpdate: (cfg, chatbotId, payload) => cfg.dryRun ? { dryRun: true, chatbotId, payload } : edgecloudControllerClient.updateChatbot(cfg, chatbotId, payload),
    chatbotList: (cfg, projectId, page = 0, number = 100) => edgecloudControllerClient.listChatbots(cfg, projectId, page, number),
    chatbotDocumentCreate: (cfg, chatbotId, projectId, file, metadata) => cfg.dryRun ? { dryRun: true, chatbotId, projectId, file: { ...file, content: '[redacted]' }, metadata } : edgecloudControllerClient.createChatbotDocument(cfg, chatbotId, projectId, file, metadata),
    chatbotDocumentUpdate: (cfg, chatbotId, documentId, projectId, file, metadata) => cfg.dryRun ? { dryRun: true, chatbotId, documentId, projectId, file: { ...file, content: '[redacted]' }, metadata } : edgecloudControllerClient.updateChatbotDocument(cfg, chatbotId, documentId, projectId, file, metadata),
    chatbotDocumentGet: (cfg, chatbotId, documentId) => edgecloudControllerClient.getChatbotDocument(cfg, chatbotId, documentId),
    chatbotDocumentList: (cfg, chatbotId, projectId, page = 0, number = 30) => edgecloudControllerClient.listChatbotDocuments(cfg, chatbotId, projectId, page, number),
};
