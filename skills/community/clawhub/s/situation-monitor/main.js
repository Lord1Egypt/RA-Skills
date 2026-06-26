import { Actor, log } from 'apify';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const DEFAULT_INPUT = {
  includeGcpStatus: true,
  includeGithubStatus: true,
  includeKubernetesGithubIssues: true,
  gcpLookbackDays: 365,
  maxGcpIncidents: 6,
  githubIssuesLimit: 6,
  useFixtureWhenEmpty: true,
  fixturePath: 'examples/kubewatch_incidents.json',
};

const RELEVANT_GCP_TERMS = [
  'google kubernetes engine',
  'gke',
  'kubernetes',
  'compute engine',
  'cloud load balancing',
  'virtual private cloud',
  'vpc',
  'persistent disk',
  'network',
  'ingress',
];

const __dirname = path.dirname(fileURLToPath(import.meta.url));

await Actor.init();

const input = {
  ...DEFAULT_INPUT,
  ...(await Actor.getInput() ?? {}),
};

const runs = [];
const errors = [];

if (input.includeGcpStatus) {
  runs.push(
    collectSafely('gcp-status', () => fetchGcpIncidents(input), errors),
  );
}

if (input.includeGithubStatus) {
  runs.push(
    collectSafely('github-status', () => fetchGithubStatusIncidents(), errors),
  );
}

if (input.includeKubernetesGithubIssues) {
  runs.push(
    collectSafely(
      'k8s-github',
      () => fetchKubernetesGithubIssues(input),
      errors,
    ),
  );
}

const liveResults = (await Promise.all(runs)).flat();
let incidents = dedupeById(liveResults);
let usedFixture = false;

if (incidents.length === 0 && input.useFixtureWhenEmpty) {
  incidents = await loadFixtureIncidents(input.fixturePath);
  usedFixture = true;
  log.warning(
    `Live sources returned no incidents; using fixture fallback from ${input.fixturePath}.`,
  );
}

if (incidents.length > 0) {
  await Actor.pushData(incidents);
}

const summary = {
  itemCount: incidents.length,
  usedFixture,
  errorCount: errors.length,
  errors,
  sources: summarizeSources(incidents),
};

await Actor.setValue('OUTPUT', summary);
log.info(`Prepared ${incidents.length} incident record(s).`, summary);
await Actor.exit();

async function collectSafely(name, loader, errorsList) {
  try {
    const items = await loader();
    log.info(`Fetched ${items.length} item(s) from ${name}.`);
    return items;
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    errorsList.push({ source: name, error: message });
    log.warning(`Failed to fetch ${name}: ${message}`);
    return [];
  }
}

async function fetchGcpIncidents(inputConfig) {
  const incidents = await fetchJson('https://status.cloud.google.com/incidents.json');
  const cutoff = Date.now() - inputConfig.gcpLookbackDays * 24 * 60 * 60 * 1000;

  return incidents
    .filter((incident) => {
      const startedAt = Date.parse(
        incident.begin || incident.created || incident.modified || '',
      );
      return Number.isFinite(startedAt) && startedAt >= cutoff;
    })
    .filter(isRelevantGcpIncident)
    .sort(
      (left, right) =>
        Date.parse(right.begin || right.created || '') -
        Date.parse(left.begin || left.created || ''),
    )
    .slice(0, inputConfig.maxGcpIncidents)
    .map(normalizeGcpIncident);
}

async function fetchGithubStatusIncidents() {
  const payload = await fetchJson(
    'https://www.githubstatus.com/api/v2/incidents/unresolved.json',
  );
  return (payload.incidents || []).map(normalizeGithubStatusIncident);
}

async function fetchKubernetesGithubIssues(inputConfig) {
  const query = new URL(
    'https://api.github.com/repos/kubernetes/kubernetes/issues',
  );
  query.searchParams.set('state', 'open');
  query.searchParams.set('labels', 'kind/bug,priority/critical-urgent');
  query.searchParams.set('per_page', String(inputConfig.githubIssuesLimit));

  const issues = await fetchJson(query.toString(), {
    headers: { 'User-Agent': 'situation-monitor-apify-actor' },
  });

  return issues
    .filter((issue) => !issue.pull_request)
    .map(normalizeGithubIssue);
}

function normalizeGcpIncident(incident) {
  const service = inferGcpService(incident);
  const description = incident.external_desc || latestUpdateText(incident) || '';
  const locations = [
    ...(incident.currently_affected_locations || []),
    ...(incident.previously_affected_locations || []),
  ];
  return {
    id: `gcp-${incident.id}`,
    source: 'gcp-status',
    title: `${service} incident: ${trimSentence(description, 120)}`,
    severity: mapGcpSeverity(incident),
    service,
    region: locations[0]?.id || 'global',
    status: incident.end ? 'resolved' : 'active',
    started_at: incident.begin || incident.created || new Date().toISOString(),
    description,
    url: incident.uri
      ? `https://status.cloud.google.com/${incident.uri}`
      : 'https://status.cloud.google.com/',
    raw: incident,
  };
}

function normalizeGithubStatusIncident(incident) {
  const description =
    incident.incident_updates?.[0]?.body ||
    incident.shortlink ||
    incident.name ||
    '';
  return {
    id: `github-status-${incident.id}`,
    source: 'github-status',
    title: incident.name || 'GitHub status incident',
    severity: mapGithubStatusSeverity(incident.impact),
    service: 'github-platform',
    region: 'global',
    status: incident.status || 'active',
    started_at:
      incident.created_at || incident.updated_at || new Date().toISOString(),
    description,
    url: incident.shortlink || 'https://www.githubstatus.com/',
    raw: incident,
  };
}

function normalizeGithubIssue(issue) {
  const description = trimSentence(issue.body || '', 600);
  const labels = (issue.labels || []).map((label) => label.name).join(', ');
  return {
    id: `k8s-issue-${issue.number}`,
    source: 'k8s-github',
    title: issue.title,
    severity: 'high',
    service: inferGithubIssueService(`${issue.title}\n${issue.body || ''}`),
    region: 'global',
    status: issue.state || 'open',
    started_at: issue.created_at || new Date().toISOString(),
    description: labels
      ? `Labels: ${labels}. ${description}`.trim()
      : description,
    url: issue.html_url,
    raw: {
      number: issue.number,
      labels: issue.labels,
      assignees: issue.assignees,
      author: issue.user?.login,
      comments: issue.comments,
      updated_at: issue.updated_at,
    },
  };
}

function isRelevantGcpIncident(incident) {
  const productNames = (incident.affected_products || [])
    .map((product) => product.title || '')
    .join(' ');
  const haystack = [
    incident.service_name,
    incident.external_desc,
    productNames,
    latestUpdateText(incident),
  ]
    .filter(Boolean)
    .join(' ')
    .toLowerCase();

  return RELEVANT_GCP_TERMS.some((term) => haystack.includes(term));
}

function inferGcpService(incident) {
  const haystack = [
    incident.service_name,
    incident.external_desc,
    ...(incident.affected_products || []).map((product) => product.title || ''),
  ]
    .join(' ')
    .toLowerCase();

  if (haystack.includes('google kubernetes engine') || haystack.includes('gke')) {
    return 'gke';
  }
  if (haystack.includes('cloud load balancing') || haystack.includes('ingress')) {
    return 'ingress-gateway';
  }
  if (
    haystack.includes('virtual private cloud') ||
    haystack.includes('network') ||
    haystack.includes('compute engine')
  ) {
    return 'cluster-network';
  }
  if (haystack.includes('persistent disk')) {
    return 'persistent-disk';
  }
  return 'gke';
}

function inferGithubIssueService(text) {
  const lowered = text.toLowerCase();
  if (lowered.includes('crashloop') || lowered.includes('oom')) {
    return 'analytics-worker';
  }
  if (lowered.includes('imagepull') || lowered.includes('image pull')) {
    return 'user-service';
  }
  if (lowered.includes('statefulset') || lowered.includes('pod')) {
    return 'gke';
  }
  if (lowered.includes('ingress')) {
    return 'ingress-gateway';
  }
  return 'gke';
}

function mapGcpSeverity(incident) {
  const severity = String(incident.severity || '').toLowerCase();
  const impact = String(incident.status_impact || '').toLowerCase();
  if (severity === 'high' || impact.includes('outage')) {
    return 'critical';
  }
  if (severity === 'medium' || impact.includes('disruption')) {
    return 'high';
  }
  if (severity === 'low' || impact.includes('degradation')) {
    return 'medium';
  }
  return 'medium';
}

function mapGithubStatusSeverity(impact) {
  const lowered = String(impact || '').toLowerCase();
  if (lowered === 'critical') {
    return 'critical';
  }
  if (lowered === 'major') {
    return 'high';
  }
  if (lowered === 'minor') {
    return 'medium';
  }
  return 'low';
}

function latestUpdateText(incident) {
  const update = incident.updates?.[0];
  return update?.text || '';
}

function trimSentence(text, maxLength) {
  const normalized = String(text || '').replace(/\s+/g, ' ').trim();
  if (normalized.length <= maxLength) {
    return normalized;
  }
  return `${normalized.slice(0, maxLength - 1).trimEnd()}…`;
}

async function loadFixtureIncidents(fixturePath) {
  const absolutePath = path.resolve(__dirname, fixturePath);
  const payload = JSON.parse(await readFile(absolutePath, 'utf8'));
  return payload.map((item, index) => ({
    id: item.id || item.incident_id || `fixture-${index + 1}`,
    ...item,
  }));
}

function dedupeById(items) {
  const seen = new Set();
  return items.filter((item) => {
    if (!item.id || seen.has(item.id)) {
      return false;
    }
    seen.add(item.id);
    return true;
  });
}

function summarizeSources(items) {
  return items.reduce((accumulator, item) => {
    accumulator[item.source] = (accumulator[item.source] || 0) + 1;
    return accumulator;
  }, {});
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    signal: AbortSignal.timeout(15000),
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status} for ${url}`);
  }
  return response.json();
}
