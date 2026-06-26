import { apiRequest, output } from '../api';

export async function listWorkflows(argv: { communityId: number }) {
  output(await apiRequest('GET', '/workflows/', undefined, { community_id: String(argv.communityId) }));
}

export async function getWorkflow(argv: { id: number; communityId: number }) {
  output(await apiRequest('GET', `/workflows/${argv.id}/`, undefined, { community_id: String(argv.communityId) }));
}

export async function createWorkflow(argv: { communityId: number; name: string; config: string; dailyLimit?: number }) {
  output(await apiRequest('POST', '/workflows/', {
    community_id: argv.communityId,
    name: argv.name,
    config: JSON.parse(argv.config),
    daily_limit: argv.dailyLimit ?? 50,
  }));
}

export async function updateWorkflow(argv: { id: number; communityId: number; data: string }) {
  const body = JSON.parse(argv.data);
  body.community_id = argv.communityId;
  output(await apiRequest('PATCH', `/workflows/${argv.id}/`, body));
}

export async function deleteWorkflow(argv: { id: number; communityId: number }) {
  output(await apiRequest('DELETE', `/workflows/${argv.id}/`, undefined, { community_id: String(argv.communityId) }));
}

export async function toggleWorkflow(argv: { id: number; communityId: number }) {
  output(await apiRequest('POST', `/workflows/${argv.id}/toggle/`, { community_id: argv.communityId }));
}

export async function runWorkflow(argv: { id: number; communityId: number }) {
  output(await apiRequest('POST', `/workflows/${argv.id}/run/`, { community_id: argv.communityId }));
}

export async function listWorkflowRuns(argv: { id: number; communityId: number; limit?: number }) {
  output(await apiRequest('GET', `/workflows/${argv.id}/runs/`, undefined, {
    community_id: String(argv.communityId),
    ...(argv.limit ? { limit: String(argv.limit) } : {}),
  }));
}

export async function testWorkflow(argv: { id: number; communityId: number; triggerData?: string }) {
  const body: Record<string, unknown> = { community_id: argv.communityId };
  if (argv.triggerData) body.trigger_data = JSON.parse(argv.triggerData);
  output(await apiRequest('POST', `/workflows/${argv.id}/test/`, body));
}

export async function getWorkflowRegistry(argv: { platform?: string }) {
  output(await apiRequest('GET', '/workflows/registry/', undefined, { platform: argv.platform ?? 'skool' }));
}
