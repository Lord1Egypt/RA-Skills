import { ThetaConfig } from '../config.js';
import { callThetaMcpTool } from '../clients/edgecloudMcp.js';

type GpuResource = {
  resource_id?: string;
  provider?: string;
  country?: string;
  region?: string;
  gpu_model?: string;
  gpu_count_available?: number;
  price_per_hour_usd?: number;
  [key: string]: unknown;
};

export type GpuResourceFilter = {
  provider?: string;
  gpuModel?: string;
  region?: string;
  maxPricePerHourUsd?: number;
  availableOnly?: boolean;
  limit?: number;
};

export type GpuCreateRequest = {
  name: string;
  deploymentTemplateId: string;
  resourceId: string;
  maxPricePerHourUsd: number;
  confirm?: boolean;
  region?: string;
  displayName?: string;
  containerImage?: string;
  sshPublicKey?: string;
  sshPort?: number;
  httpPort?: number;
};

function withProject(projectId: string, args: Record<string, unknown> = {}): Record<string, unknown> {
  const out: Record<string, unknown> = { project_id: projectId };
  for (const [key, value] of Object.entries(args)) if (value !== undefined && value !== null && value !== '') out[key] = value;
  return out;
}

function requireConfirm(action: string, confirm: unknown): void {
  if (confirm !== true) {
    throw new Error(`${action} changes billable GPU capacity. State the price, get explicit approval, then pass confirm:true.`);
  }
}

function filterResources(resources: GpuResource[], filter: GpuResourceFilter): GpuResource[] {
  const model = filter.gpuModel?.toLowerCase();
  const region = filter.region?.toLowerCase();
  const filtered = resources.filter((r) =>
    (!filter.provider || r.provider === filter.provider)
    && (!model || String(r.gpu_model ?? '').toLowerCase().includes(model))
    && (!region || `${r.country ?? ''} ${r.region ?? ''}`.toLowerCase().includes(region))
    && (filter.maxPricePerHourUsd === undefined || (typeof r.price_per_hour_usd === 'number' && r.price_per_hour_usd <= filter.maxPricePerHourUsd))
    && (!filter.availableOnly || (r.gpu_count_available ?? 0) > 0));
  filtered.sort((a, b) => (a.price_per_hour_usd ?? Infinity) - (b.price_per_hour_usd ?? Infinity));
  return filter.limit ? filtered.slice(0, Math.max(1, Math.trunc(filter.limit))) : filtered;
}

function mutationPreview(tool: string, args: Record<string, unknown>) {
  return { dryRun: true, transport: 'theta-hosted-mcp', tool, arguments: args };
}

export const gpu = {
  listResources: async (cfg: ThetaConfig, projectId: string, filter: GpuResourceFilter = {}) => {
    const result = await callThetaMcpTool(cfg, 'list_gpu_resources', withProject(projectId)) as { resources?: GpuResource[]; [key: string]: unknown };
    const all = Array.isArray(result?.resources) ? result.resources : [];
    const resources = filterResources(all, filter);
    return { ...result, totalResources: all.length, matchedResources: resources.length, resources, priceCurrency: 'USD per hour' };
  },

  getResource: (cfg: ThetaConfig, projectId: string, resourceId: string, region?: string) =>
    callThetaMcpTool(cfg, 'get_gpu_resource', withProject(projectId, { resource_id: resourceId, region })),

  listTemplates: (cfg: ThetaConfig, projectId: string) =>
    callThetaMcpTool(cfg, 'list_gpu_deployment_templates', withProject(projectId)),

  listDeployments: (cfg: ThetaConfig, projectId: string) =>
    callThetaMcpTool(cfg, 'list_gpu_deployments', withProject(projectId)),

  getDeployment: (cfg: ThetaConfig, projectId: string, deploymentId: string) =>
    callThetaMcpTool(cfg, 'get_gpu_deployment', withProject(projectId, { deployment_id: deploymentId })),

  deploymentEvents: (cfg: ThetaConfig, projectId: string, deploymentId: string) =>
    callThetaMcpTool(cfg, 'get_gpu_deployment_events', withProject(projectId, { deployment_id: deploymentId })),

  deploymentLogs: (cfg: ThetaConfig, projectId: string, deploymentId: string) =>
    callThetaMcpTool(cfg, 'get_gpu_deployment_logs', withProject(projectId, { deployment_id: deploymentId })),

  createDeployment: async (cfg: ThetaConfig, projectId: string, req: GpuCreateRequest) => {
    if (!Number.isFinite(req.maxPricePerHourUsd) || req.maxPricePerHourUsd <= 0) {
      throw new Error('maxPricePerHourUsd is required: it is sent as Theta\'s provider-side hourly price cap');
    }
    const args = withProject(projectId, {
      name: req.name,
      display_name: req.displayName,
      deployment_template_id: req.deploymentTemplateId,
      resource_id: req.resourceId,
      region: req.region,
      container_image: req.containerImage,
      ssh_public_key: req.sshPublicKey,
      ssh_port: req.sshPort,
      http_port: req.httpPort,
      max_price_per_hour_usd: req.maxPricePerHourUsd,
      confirm: req.confirm === true
    });
    if (cfg.dryRun) return mutationPreview('create_gpu_deployment', args);
    requireConfirm('create_gpu_deployment', req.confirm);
    // The MCP client verifies the resource's listed price against the cap before provisioning.
    return callThetaMcpTool(cfg, 'create_gpu_deployment', args);
  },

  lifecycle: async (cfg: ThetaConfig, projectId: string, action: 'start' | 'stop' | 'delete', deploymentId: string, confirm?: boolean) => {
    const tool = `${action}_gpu_deployment`;
    const args = withProject(projectId, { deployment_id: deploymentId, confirm: confirm === true });
    if (cfg.dryRun) return mutationPreview(tool, args);
    requireConfirm(tool, confirm);
    return callThetaMcpTool(cfg, tool, args);
  }
};

export const billing = {
  balanceUsd: (cfg: ThetaConfig, projectId: string) =>
    callThetaMcpTool(cfg, 'get_billing_balance', withProject(projectId)),

  usage: (cfg: ThetaConfig, projectId: string, startDate?: string, endDate?: string) => {
    const parse = (label: string, value?: string): number | undefined => {
      if (value === undefined) return undefined;
      const ms = /^\d{4}-\d{2}-\d{2}$/.test(value) ? Date.parse(`${value}T00:00:00Z`) : NaN;
      if (!Number.isFinite(ms) || new Date(ms).toISOString().slice(0, 10) !== value) throw new Error(`${label} must be a real date in YYYY-MM-DD`);
      return ms;
    };
    const start = parse('startDate', startDate);
    const end = parse('endDate', endDate);
    if (start !== undefined && end !== undefined) {
      if (end < start) throw new Error('endDate must not be before startDate');
      if ((end - start) / 86400000 > 366) throw new Error('usage range is limited to 366 days');
    }
    return callThetaMcpTool(cfg, 'get_billing_usage', withProject(projectId, { start_date: startDate, end_date: endDate }));
  },

  topUps: (cfg: ThetaConfig, projectId: string, page?: number, number?: number) =>
    callThetaMcpTool(cfg, 'list_billing_top_ups', withProject(projectId, { page, number })),

  pricing: (cfg: ThetaConfig, projectId: string) =>
    callThetaMcpTool(cfg, 'get_billing_pricing', withProject(projectId))
};
