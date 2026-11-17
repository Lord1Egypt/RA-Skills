// Data flow: sends the project-scoped EdgeCloud API key (x-api-key) plus deployment, chatbot and
// document payloads (including uploaded document contents) to Theta controller/API hosts only.
// Every create/update/start/stop/delete call requires confirm:true here, in the client.
import { ThetaConfig } from '../config.js';
import { deleteEmpty, getJson, postJson, putEmpty, putJson } from './http.js';
import { isStructuredError, fromHttpError } from '../errors.js';
import { pathSegment } from '../security.js';
import { assertApproved } from '../approval.js';

const BASE_CTRL = 'https://controller.thetaedgecloud.com';
const BASE_API = 'https://api.thetaedgecloud.com';
const CONTROLLER_DEFAULT_HEADERS = {
  accept: 'application/json, text/plain, */*',
  'user-agent': 'theta-edgecloud-skill'
};

function k(cfg: ThetaConfig): HeadersInit {
  if (!cfg.edgecloudApiKey) throw new Error('THETA_EC_API_KEY missing');
  return { ...CONTROLLER_DEFAULT_HEADERS, 'x-api-key': cfg.edgecloudApiKey };
}

function net(cfg: ThetaConfig, service: string, headers?: HeadersInit) {
  return {
    service,
    headers,
    timeoutMs: cfg.httpTimeoutMs,
    maxRetries: cfg.httpMaxRetries,
    retryBackoffMs: cfg.httpRetryBackoffMs
  };
}

function segment(value: string, field: string): string {
  return pathSegment(value, field);
}

function url(base: string, path: string, params: Record<string, unknown> = {}): string {
  const query = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value === undefined || value === null) continue;
    query.set(key, String(value));
  }
  const qs = query.toString();
  return `${base}${path}${qs ? `?${qs}` : ''}`;
}

function shouldTryNextRoute(error: unknown): boolean {
  if (!isStructuredError(error)) return false;
  return error.status === 404 || error.status === 405;
}

async function firstRoute<T>(routes: string[], request: (route: string) => Promise<T>): Promise<T> {
  const errors: unknown[] = [];
  for (const route of routes) {
    try {
      return await request(route);
    } catch (error) {
      errors.push(error);
      if (!shouldTryNextRoute(error)) throw error;
    }
  }
  throw errors[errors.length - 1] ?? new Error('No controller routes attempted');
}

export type ChatbotDocumentFile = {
  filename: string;
  content: string;
  contentType?: string;
  encoding?: 'utf8' | 'base64';
};

function documentForm(projectId: string, file: ChatbotDocumentFile, metadata?: Record<string, unknown>): FormData {
  if (!file || typeof file !== 'object') throw new Error('file must be an object');
  if (!file.filename?.trim()) throw new Error('file.filename is required');
  if (typeof file.content !== 'string') throw new Error('file.content must be a string');

  const bytes = file.encoding === 'base64'
    ? Buffer.from(file.content, 'base64')
    : Buffer.from(file.content, 'utf8');
  const form = new FormData();
  form.set('project_id', projectId);
  form.set('metadata', JSON.stringify(metadata ?? {}));
  form.set('file', new Blob([bytes], { type: file.contentType ?? 'text/plain' }), file.filename);
  return form;
}

async function postForm<T>(targetUrl: string, form: FormData, cfg: ThetaConfig): Promise<T> {
  const res = await fetch(targetUrl, {
    redirect: 'error',
    method: 'POST',
    headers: k(cfg),
    body: form,
    signal: AbortSignal.timeout(cfg.httpTimeoutMs)
  });
  if (!res.ok) throw fromHttpError('edgecloud-controller', targetUrl, res.status, await res.text());
  return res.json() as Promise<T>;
}

async function putForm<T>(targetUrl: string, form: FormData, cfg: ThetaConfig): Promise<T> {
  const res = await fetch(targetUrl, {
    redirect: 'error',
    method: 'PUT',
    headers: k(cfg),
    body: form,
    signal: AbortSignal.timeout(cfg.httpTimeoutMs)
  });
  if (!res.ok) throw fromHttpError('edgecloud-controller', targetUrl, res.status, await res.text());
  return res.json() as Promise<T>;
}

export const edgecloudControllerClient = {
  startDeploymentByBaseId: (cfg: ThetaConfig, projectId: string, baseId: string, confirm?: boolean) =>
    assertApproved(cfg, confirm, 'theta.deployments.startByBaseId') ?? putEmpty(url(BASE_CTRL, `/deployments/base/${segment(baseId, 'baseId')}/start`, {project_id:projectId}), net(cfg,'edgecloud-controller',k(cfg))),
  listStandardTemplates: (cfg: ThetaConfig, category: 'prototyping' | 'serving' | 'training') =>
    getJson(url(BASE_CTRL, '/deployment_template/list_standard_templates', {category}), net(cfg, 'edgecloud-controller', k(cfg))),

  listCustomTemplates: (cfg: ThetaConfig, projectId: string) =>
    getJson(url(BASE_CTRL, '/deployment_template/list_custom_templates', {project_id:projectId}), net(cfg, 'edgecloud-controller', k(cfg))),

  listVmTypes: (cfg: ThetaConfig) => getJson(`${BASE_API}/resource/vm/list`, net(cfg, 'edgecloud-controller', CONTROLLER_DEFAULT_HEADERS)),

  createDeployment: (cfg: ThetaConfig, payload: Record<string, unknown>, confirm?: boolean) =>
    assertApproved(cfg, confirm, 'theta.deployments.create') ?? postJson(`${BASE_CTRL}/deployment`, payload, net(cfg, 'edgecloud-controller', k(cfg))),

  listDeployments: (cfg: ThetaConfig, projectId: string) =>
    firstRoute(
      [
        url(BASE_CTRL, '/deployment/list', { project_id: projectId }),
        url(BASE_CTRL, '/deployments/list', { project_id: projectId })
      ],
      (route) => getJson(route, net(cfg, 'edgecloud-controller', k(cfg)))
    ),

  routeProbeDeploymentsList: async (cfg: ThetaConfig, projectId: string) => {
    const routes = [
      url(BASE_CTRL, '/deployment/list', { project_id: projectId }),
      url(BASE_CTRL, '/deployments/list', { project_id: projectId })
    ];
    const attempts: Array<Record<string, unknown>> = [];
    for (const route of routes) {
      try {
        const response = await getJson(route, net(cfg, 'edgecloud-controller', k(cfg)));
        attempts.push({ route, ok: true });
        return { ok: true, selectedRoute: route, attempts, response };
      } catch (error) {
        attempts.push({
          route,
          ok: false,
          status: isStructuredError(error) ? error.status : undefined,
          code: isStructuredError(error) ? error.code : (error as { name?: string } | undefined)?.name,
          message: (error as { message?: string } | undefined)?.message ?? String(error)
        });
      }
    }
    return { ok: false, attempts };
  },

  balance: (cfg: ThetaConfig, orgId: string) =>
    getJson(url(BASE_API, '/balance', { orgID: orgId }), net(cfg, 'edgecloud-controller', k(cfg))),

  createChatbot: (cfg: ThetaConfig, payload: Record<string, unknown>, confirm?: boolean) =>
    assertApproved(cfg, confirm, 'theta.ai.agent.create') ?? postJson(`${BASE_CTRL}/chatbot`, payload, net(cfg, 'edgecloud-controller', k(cfg))),

  getChatbot: (cfg: ThetaConfig, chatbotId: string, projectId: string) =>
    getJson(url(BASE_CTRL, `/chatbot/${segment(chatbotId, 'chatbotId')}`, { project_id: projectId }), net(cfg, 'edgecloud-controller', k(cfg))),

  updateChatbot: (cfg: ThetaConfig, chatbotId: string, payload: Record<string, unknown>, confirm?: boolean) =>
    assertApproved(cfg, confirm, 'theta.ai.agent.update') ?? putJson(`${BASE_CTRL}/chatbot/${segment(chatbotId, 'chatbotId')}`, payload, net(cfg, 'edgecloud-controller', k(cfg))),

  listChatbots: (cfg: ThetaConfig, projectId: string, page = 0, number = 100) =>
    getJson(url(BASE_CTRL, '/chatbot/list', { project_id: projectId, page, number }), net(cfg, 'edgecloud-controller', k(cfg))),

  createChatbotDocument: (cfg: ThetaConfig, chatbotId: string, projectId: string, file: ChatbotDocumentFile, metadata?: Record<string, unknown>, confirm?: boolean) =>
    assertApproved(cfg, confirm, 'theta.ai.agent.document.create') ?? postForm(url(BASE_CTRL, `/chatbot/${segment(chatbotId, 'chatbotId')}/document`), documentForm(projectId, file, metadata), cfg),

  updateChatbotDocument: (cfg: ThetaConfig, chatbotId: string, documentId: string, projectId: string, file: ChatbotDocumentFile, metadata?: Record<string, unknown>, confirm?: boolean) =>
    assertApproved(cfg, confirm, 'theta.ai.agent.document.update') ?? putForm(url(BASE_CTRL, `/chatbot/${segment(chatbotId, 'chatbotId')}/document/${segment(documentId, 'documentId')}`), documentForm(projectId, file, metadata), cfg),

  getChatbotDocument: (cfg: ThetaConfig, chatbotId: string, documentId: string) =>
    getJson(url(BASE_CTRL, `/chatbot/${segment(chatbotId, 'chatbotId')}/document/${segment(documentId, 'documentId')}`), net(cfg, 'edgecloud-controller', k(cfg))),

  listChatbotDocuments: (cfg: ThetaConfig, chatbotId: string, projectId: string, page = 0, number = 30) =>
    getJson(url(BASE_CTRL, `/chatbot/${segment(chatbotId, 'chatbotId')}/document/list`, { project_id: projectId, page, number }), net(cfg, 'edgecloud-controller', k(cfg))),

  stopDeployment: (cfg: ThetaConfig, projectId: string, shard: string, suffix: string, confirm?: boolean) =>
    assertApproved(cfg, confirm, 'theta.deployments.stop') ?? firstRoute(
      [
        url(BASE_CTRL, `/deployment/${segment(shard, 'shard')}/${segment(suffix, 'suffix')}/stop`, { project_id: projectId }),
        url(BASE_CTRL, `/deployments/${segment(shard, 'shard')}/${segment(suffix, 'suffix')}/stop`, { project_id: projectId })
      ],
      (route) => putEmpty(route, net(cfg, 'edgecloud-controller', k(cfg)))
    ),

  startDeployment: (cfg: ThetaConfig, projectId: string, shard: string, suffix: string, confirm?: boolean) =>
    assertApproved(cfg, confirm, 'theta.deployments.start') ?? firstRoute(
      [
        url(BASE_CTRL, `/deployment/${segment(shard, 'shard')}/${segment(suffix, 'suffix')}/start`, { project_id: projectId }),
        url(BASE_CTRL, `/deployments/${segment(shard, 'shard')}/${segment(suffix, 'suffix')}/start`, { project_id: projectId })
      ],
      (route) => putEmpty(route, net(cfg, 'edgecloud-controller', k(cfg)))
    ),

  deleteDeployment: (cfg: ThetaConfig, projectId: string, shard: string, suffix: string, confirm?: boolean) =>
    assertApproved(cfg, confirm, 'theta.deployments.delete') ?? firstRoute(
      [
        url(BASE_CTRL, `/deployment/${segment(shard, 'shard')}/${segment(suffix, 'suffix')}`, { project_id: projectId }),
        url(BASE_CTRL, `/deployments/${segment(shard, 'shard')}/${segment(suffix, 'suffix')}`, { project_id: projectId })
      ],
      (route) => deleteEmpty(route, net(cfg, 'edgecloud-controller', k(cfg)))
    )
};
