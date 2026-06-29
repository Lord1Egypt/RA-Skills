import { readdirSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import process from 'node:process';
import { Client } from 'pg';

interface BucketConfig {
  name: string;
  public?: boolean;
  fileSizeLimit?: number;
}

interface PersistentPreview {
  gitBranch: string;
  siteUrl?: string;
}

interface PreviewConfig {
  namePrefix?: string;
  redirectWildcard?: string;
  syncAuthConfig?: boolean;
  hydrateFromDevelop?: boolean;
  copyAuthUsers?: boolean;
  copyPublicData?: boolean;
  includePublicTables?: string[];
  excludePublicTables?: string[];
  storageBuckets?: Array<string | BucketConfig>;
  copyStorageBuckets?: string[];
}

interface BranchingConfig {
  supabase?: {
    parentProjectRef?: string;
    developBranchName?: string;
    developBranchRef?: string;
    schemaBranchCreateSource?: string;
    developHydrationSource?: string;
    previewHydrationSource?: string;
  };
  vercel?: {
    scope?: string;
    projectId?: string;
    projectName?: string;
  };
  envKeys?: {
    supabaseUrl?: string;
    supabaseAnonKey?: string;
    supabaseServiceRoleKey?: string;
  };
  preview?: PreviewConfig;
  persistentPreviews?: PersistentPreview[];
}

interface SupabaseBranch {
  name: string;
  git_branch?: string | null;
  status?: string;
  is_default?: boolean;
}

interface BranchDetails {
  SUPABASE_URL: string;
  SUPABASE_ANON_KEY: string;
  SUPABASE_SERVICE_ROLE_KEY: string;
  POSTGRES_URL: string;
}

interface AuthUser {
  id: string;
  email?: string;
  user_metadata?: Record<string, unknown>;
  app_metadata?: Record<string, unknown>;
}

interface AuthUsersPage {
  users?: AuthUser[];
}

interface AuthConfig {
  site_url?: string;
  uri_allow_list?: string;
  external_email_enabled?: boolean;
  external_google_enabled?: boolean;
  external_google_client_id?: string;
  external_google_secret?: string;
  external_google_skip_nonce_check?: boolean;
  external_google_email_optional?: boolean;
}

interface ColumnInfo {
  name: string;
  dataType: string;
  udtName: string;
}

interface ParsedArgs {
  positional: string[];
  flags: Record<string, string>;
}

const CONFIG_PATH = process.env.BRANCHING_CONFIG_PATH || 'branching-config.json';
const config: BranchingConfig = existsSync(CONFIG_PATH)
  ? (JSON.parse(readFileSync(CONFIG_PATH, 'utf8')) as BranchingConfig)
  : {};

const parentProjectRef = process.env.SUPABASE_PARENT_PROJECT_REF || config.supabase?.parentProjectRef;
const developBranchName = process.env.SUPABASE_DEVELOP_BRANCH_NAME || config.supabase?.developBranchName || 'develop';
const developBranchRef = process.env.SUPABASE_DEVELOP_BRANCH_REF || config.supabase?.developBranchRef;
const previewPrefix = process.env.PREVIEW_BRANCH_PREFIX || config.preview?.namePrefix || 'preview-';
const previewPassword = process.env.PREVIEW_USER_PASSWORD;
const envKeys = {
  supabaseUrl: config.envKeys?.supabaseUrl || 'NEXT_PUBLIC_SUPABASE_URL',
  supabaseAnonKey: config.envKeys?.supabaseAnonKey || 'NEXT_PUBLIC_SUPABASE_ANON_KEY',
  supabaseServiceRoleKey: config.envKeys?.supabaseServiceRoleKey || 'SUPABASE_SERVICE_ROLE_KEY',
};
const vercel = {
  scope: process.env.VERCEL_SCOPE || config.vercel?.scope,
  projectId: process.env.VERCEL_PROJECT_ID || config.vercel?.projectId,
  projectName: process.env.VERCEL_PROJECT_NAME || config.vercel?.projectName,
};

const qident = (value: string): string => `"${String(value).replace(/"/g, '""')}"`;
const sleep = (ms: number): Promise<void> => new Promise((resolve) => setTimeout(resolve, ms));

function parseArgs(argv: string[]): ParsedArgs {
  const args: ParsedArgs = { positional: [], flags: {} };
  for (let i = 2; i < argv.length; i += 1) {
    const part = argv[i];
    if (!part.startsWith('--')) {
      args.positional.push(part);
      continue;
    }
    const key = part.slice(2);
    args.flags[key] = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : 'true';
  }
  return args;
}

function slugify(value: string): string {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 45);
}

interface RunOptions {
  stdio?: 'inherit';
  timeout?: number;
}

function run(command: string, args: string[], options: RunOptions = {}): string {
  const result = spawnSync(command, args, {
    encoding: 'utf8',
    shell: process.platform === 'win32',
    env: process.env,
    stdio: options.stdio || ['ignore', 'pipe', 'pipe'],
    timeout: options.timeout,
  });
  if (result.error) throw new Error(`${command} ${args.join(' ')} failed to start: ${result.error.message}`);
  if (result.status !== 0) throw new Error(`${command} ${args.join(' ')} failed:\n${result.stdout || ''}\n${result.stderr || ''}`);
  return result.stdout || '';
}

function npx(args: string[], options: RunOptions = {}): string {
  return run(process.platform === 'win32' ? 'npx.cmd' : 'npx', args, options);
}

function supabase(args: string[]): string {
  return npx(['supabase', ...args]);
}

let vercelLinked = false;

function ensureVercelLinked(): void {
  if (vercelLinked || !process.env.VERCEL_TOKEN || !vercel.projectName) return;
  const args = ['vercel', 'link', '--yes', '--project', vercel.projectName];
  if (vercel.scope) args.push('--scope', vercel.scope);
  npx(args, { timeout: 90_000 });
  vercelLinked = true;
}

function jsonObject<T>(output: string): T {
  const first = output.indexOf('{');
  const last = output.lastIndexOf('}');
  if (first === -1 || last <= first) throw new Error(`Could not parse JSON:\n${output}`);
  return JSON.parse(output.slice(first, last + 1)) as T;
}

function jsonArray<T>(output: string): T[] {
  const first = output.indexOf('[');
  const last = output.lastIndexOf(']');
  if (first === -1 || last <= first) return [];
  return JSON.parse(output.slice(first, last + 1)) as T[];
}

function listBranches(projectRef = parentProjectRef): SupabaseBranch[] {
  return jsonArray<SupabaseBranch>(supabase(['branches', 'list', '--project-ref', String(projectRef), '-o', 'json']));
}

function getBranchDetails(name: string, projectRef = parentProjectRef): BranchDetails {
  return jsonObject<BranchDetails>(supabase(['branches', 'get', name, '--project-ref', String(projectRef), '-o', 'json']));
}

function branchRefFromUrl(url: string): string {
  return url.replace('https://', '').replace('.supabase.co', '');
}

function findBranch(name: string, gitBranch: string): SupabaseBranch | undefined {
  return listBranches().find((branch) => branch.name === name || branch.git_branch === gitBranch);
}

function createBranch(name: string, gitBranch: string): SupabaseBranch {
  console.log(`Creating Supabase preview branch ${name} for ${gitBranch}`);
  const created = jsonObject<SupabaseBranch>(supabase(['branches', 'create', name, '--project-ref', String(parentProjectRef), '-o', 'json']));
  supabase(['branches', 'update', name, '--project-ref', String(parentProjectRef), '--git-branch', gitBranch, '-o', 'json']);
  return created;
}

async function waitForBranch(name: string): Promise<void> {
  const ready = new Set(['ACTIVE_HEALTHY', 'FUNCTIONS_DEPLOYED', 'MIGRATIONS_PASSED']);
  for (let i = 0; i < 60; i += 1) {
    const branch = listBranches().find((candidate) => candidate.name === name);
    if (branch?.status && ready.has(branch.status)) {
      console.log(`Supabase branch ${name} ready: ${branch.status}`);
      return;
    }
    console.log(`Waiting for ${name}: ${branch?.status || 'not listed yet'}`);
    await sleep(5000);
  }
  throw new Error(`Timed out waiting for ${name}`);
}

function serviceHeaders(key: string, contentType = 'application/json'): Record<string, string> {
  return { authorization: `Bearer ${key}`, apikey: key, 'content-type': contentType };
}

async function requestJson<T>(url: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(url, options);
  const text = await response.text();
  if (!response.ok) throw new Error(`${options.method || 'GET'} ${url} failed ${response.status}: ${text}`);
  return (text ? JSON.parse(text) : null) as T;
}

async function ensureBucket(details: BranchDetails, bucket: BucketConfig): Promise<void> {
  const response = await fetch(`${details.SUPABASE_URL}/storage/v1/bucket`, {
    method: 'POST',
    headers: serviceHeaders(details.SUPABASE_SERVICE_ROLE_KEY),
    body: JSON.stringify({
      id: bucket.name,
      name: bucket.name,
      public: Boolean(bucket.public),
      file_size_limit: bucket.fileSizeLimit || 52_428_800,
    }),
  });
  if (!response.ok) {
    const text = await response.text();
    if (!text.includes('already exists')) throw new Error(`Could not create bucket ${bucket.name}: ${text}`);
  }
}

async function syncAuthConfig(sourceProjectRef: string | undefined, targetProjectRef: string, gitBranch: string): Promise<void> {
  if (!config.preview?.syncAuthConfig) return;
  if (!sourceProjectRef) throw new Error('syncAuthConfig is enabled but no source project ref was configured.');
  const headers = { authorization: `Bearer ${process.env.SUPABASE_ACCESS_TOKEN}`, 'content-type': 'application/json' };
  const source = await requestJson<AuthConfig>(`https://api.supabase.com/v1/projects/${sourceProjectRef}/config/auth`, { headers });
  const previewUrl = process.env.PREVIEW_SITE_URL || '';
  const allowList = [
    ...String(source.uri_allow_list || '').split(',').map((url) => url.trim()).filter(Boolean),
    previewUrl,
    previewUrl && `${previewUrl.replace(/\/$/, '')}/login`,
    previewUrl && `${previewUrl.replace(/\/$/, '')}/dashboard`,
    previewUrl && `${previewUrl.replace(/\/$/, '')}/reset-password`,
    process.env.PREVIEW_REDIRECT_WILDCARD || config.preview?.redirectWildcard,
  ].filter((entry): entry is string => Boolean(entry));
  await requestJson(`https://api.supabase.com/v1/projects/${targetProjectRef}/config/auth`, {
    method: 'PATCH',
    headers,
    body: JSON.stringify({
      site_url: previewUrl || source.site_url,
      uri_allow_list: [...new Set(allowList)].join(','),
      external_email_enabled: source.external_email_enabled,
      external_google_enabled: source.external_google_enabled,
      external_google_client_id: source.external_google_client_id,
      external_google_secret: source.external_google_secret,
      external_google_skip_nonce_check: source.external_google_skip_nonce_check,
      external_google_email_optional: source.external_google_email_optional,
    }),
  });
  console.log(`Synced Auth config to ${targetProjectRef} for ${gitBranch}`);
}

async function listAllAuthUsers(details: BranchDetails): Promise<AuthUser[]> {
  const users: AuthUser[] = [];
  for (let page = 1; ; page += 1) {
    const data = await requestJson<AuthUsersPage>(`${details.SUPABASE_URL}/auth/v1/admin/users?page=${page}&per_page=1000`, {
      headers: serviceHeaders(details.SUPABASE_SERVICE_ROLE_KEY),
    });
    users.push(...(data.users || []));
    if (!data.users || data.users.length < 1000) return users;
  }
}

interface AuthCopyCounts {
  sourceUsers: number;
  created: number;
}

async function copyAuthUsers(source: BranchDetails, target: BranchDetails): Promise<AuthCopyCounts | null> {
  if (!config.preview?.copyAuthUsers) return null;
  if (!previewPassword) throw new Error('copyAuthUsers is enabled but PREVIEW_USER_PASSWORD is missing.');
  const sourceUsers = await listAllAuthUsers(source);
  const targetUsers = await listAllAuthUsers(target);
  const sourceIds = new Set(sourceUsers.map((user) => user.id));
  for (const user of targetUsers.filter((user) => !sourceIds.has(user.id))) {
    await fetch(`${target.SUPABASE_URL}/auth/v1/admin/users/${user.id}`, {
      method: 'DELETE',
      headers: serviceHeaders(target.SUPABASE_SERVICE_ROLE_KEY),
    });
  }
  const existing = await listAllAuthUsers(target);
  const targetIds = new Set(existing.map((user) => user.id));
  let created = 0;
  for (const user of sourceUsers.filter((user) => !targetIds.has(user.id))) {
    const response = await fetch(`${target.SUPABASE_URL}/auth/v1/admin/users`, {
      method: 'POST',
      headers: serviceHeaders(target.SUPABASE_SERVICE_ROLE_KEY),
      body: JSON.stringify({
        id: user.id,
        email: user.email,
        password: previewPassword,
        email_confirm: true,
        user_metadata: user.user_metadata,
        app_metadata: user.app_metadata,
      }),
    });
    if (!response.ok) throw new Error(`Could not create auth user ${user.id}: ${await response.text()}`);
    created += 1;
  }
  for (const user of sourceUsers) {
    const response = await fetch(`${target.SUPABASE_URL}/auth/v1/admin/users/${user.id}`, {
      method: 'PUT',
      headers: serviceHeaders(target.SUPABASE_SERVICE_ROLE_KEY),
      body: JSON.stringify({ password: previewPassword }),
    });
    if (!response.ok) throw new Error(`Could not set preview password for ${user.id}: ${await response.text()}`);
  }
  console.log(`Auth synced: source=${sourceUsers.length}, created=${created}`);
  return { sourceUsers: sourceUsers.length, created };
}

async function columns(client: Client, table: string): Promise<ColumnInfo[]> {
  const { rows } = await client.query(
    `select column_name, data_type, udt_name
       from information_schema.columns
      where table_schema = 'public'
        and table_name = $1
        and is_generated = 'NEVER'
      order by ordinal_position`,
    [table],
  );
  return (rows as Array<{ column_name: string; data_type: string; udt_name: string }>).map((row) => ({
    name: row.column_name,
    dataType: row.data_type,
    udtName: row.udt_name,
  }));
}

function normalize(value: unknown, column: ColumnInfo): unknown {
  if (value === undefined || value === null) return null;
  const isJson = ['json', 'jsonb'].includes(column.dataType) || ['json', 'jsonb'].includes(column.udtName);
  return isJson && typeof value !== 'string' ? JSON.stringify(value) : value;
}

async function copyPublicData(sourceDetails: BranchDetails, targetDetails: BranchDetails): Promise<Record<string, number> | null> {
  if (!config.preview?.copyPublicData) return null;
  const copiedCounts: Record<string, number> = {};
  const source = new Client({ connectionString: sourceDetails.POSTGRES_URL, ssl: { rejectUnauthorized: false } });
  const target = new Client({ connectionString: targetDetails.POSTGRES_URL, ssl: { rejectUnauthorized: false } });
  await source.connect();
  await target.connect();
  await source.query('set role postgres');
  await target.query('set role postgres');
  const excluded = new Set(config.preview?.excludePublicTables || []);
  const include = new Set(config.preview?.includePublicTables || []);
  const sourceTables = new Set(
    ((await source.query(
      `select table_name from information_schema.tables where table_schema='public' and table_type='BASE TABLE'`,
    )).rows as Array<{ table_name: string }>).map((row) => row.table_name),
  );
  const tables = ((await target.query(
    `select table_name from information_schema.tables where table_schema='public' and table_type='BASE TABLE' order by table_name`,
  )).rows as Array<{ table_name: string }>)
    .map((row) => row.table_name)
    .filter((table) => sourceTables.has(table))
    .filter((table) => include.size === 0 || include.has(table))
    .filter((table) => !excluded.has(table));
  await target.query('begin');
  await target.query('set session_replication_role = replica');
  if (tables.length) {
    await target.query(`truncate table ${tables.map((table) => `public.${qident(table)}`).join(', ')} restart identity cascade`);
  }
  await target.query('commit');
  for (const table of tables) {
    const sourceColumns = new Set((await columns(source, table)).map((column) => column.name));
    const shared = (await columns(target, table)).filter((column) => sourceColumns.has(column.name));
    if (!shared.length) continue;
    const rows = (await source.query(`select ${shared.map((column) => qident(column.name)).join(', ')} from public.${qident(table)}`)).rows as Array<Record<string, unknown>>;
    for (let start = 0; start < rows.length; start += 250) {
      const batch = rows.slice(start, start + 250);
      const values: unknown[] = [];
      const tuples = batch.map((row, rowIndex) => `(${shared.map((column, columnIndex) => {
        values.push(normalize(row[column.name], column));
        return `$${rowIndex * shared.length + columnIndex + 1}`;
      }).join(', ')})`);
      if (tuples.length) {
        await target.query(
          `insert into public.${qident(table)} (${shared.map((column) => qident(column.name)).join(', ')}) values ${tuples.join(', ')}`,
          values,
        );
      }
    }
    copiedCounts[table] = rows.length;
    console.log(`${table}: copied ${rows.length} rows`);
  }
  await target.query('reset all');
  await source.end();
  await target.end();
  return copiedCounts;
}

async function applyPendingMigrations(targetDetails: BranchDetails): Promise<void> {
  const client = new Client({ connectionString: targetDetails.POSTGRES_URL, ssl: { rejectUnauthorized: false } });
  await client.connect();
  await client.query('set role postgres');
  const { rows } = await client.query('select version from supabase_migrations.schema_migrations');
  const applied = new Set((rows as Array<{ version: string }>).map((row) => row.version));
  const files = readdirSync('supabase/migrations').filter((file) => file.endsWith('.sql')).sort();
  for (const file of files) {
    const match = file.match(/^(\d+)_(.+)\.sql$/);
    if (!match || applied.has(match[1])) continue;
    const sql = readFileSync(`supabase/migrations/${file}`, 'utf8');
    console.log(`Applying migration to preview only: ${file}`);
    await client.query('begin');
    try {
      await client.query(sql);
      await client.query(
        'insert into supabase_migrations.schema_migrations(version, statements, name) values ($1, $2, $3) on conflict (version) do nothing',
        [match[1], [sql], match[2]],
      );
      await client.query('commit');
    } catch (error) {
      await client.query('rollback');
      throw error;
    }
  }
  await client.end();
}

function objectPath(bucket: string, path: string): string {
  return `${bucket}/${path.split('/').map(encodeURIComponent).join('/')}`;
}

async function copyStorageBucket(source: BranchDetails, target: BranchDetails, bucketName: string): Promise<void> {
  const client = new Client({ connectionString: source.POSTGRES_URL, ssl: { rejectUnauthorized: false } });
  await client.connect();
  await client.query('set role postgres');
  const { rows } = await client.query('select name from storage.objects where bucket_id=$1 order by name', [bucketName]);
  await client.end();
  for (const { name } of rows as Array<{ name: string }>) {
    const from = await fetch(`${source.SUPABASE_URL}/storage/v1/object/${objectPath(bucketName, name)}`, {
      headers: serviceHeaders(source.SUPABASE_SERVICE_ROLE_KEY),
    });
    if (!from.ok) throw new Error(`Could not download ${bucketName}/${name}: ${await from.text()}`);
    const bytes = Buffer.from(await from.arrayBuffer());
    const to = await fetch(`${target.SUPABASE_URL}/storage/v1/object/${objectPath(bucketName, name)}`, {
      method: 'POST',
      headers: { ...serviceHeaders(target.SUPABASE_SERVICE_ROLE_KEY, from.headers.get('content-type') || 'application/octet-stream'), 'x-upsert': 'true' },
      body: bytes,
    });
    if (!to.ok) throw new Error(`Could not upload ${bucketName}/${name}: ${await to.text()}`);
  }
  console.log(`Copied ${bucketName} objects: ${rows.length}`);
}

function setVercelEnv(name: string, value: string, gitBranch: string): void {
  if (!process.env.VERCEL_TOKEN) {
    console.log(`Skipping Vercel env ${name}: VERCEL_TOKEN missing`);
    return;
  }
  ensureVercelLinked();
  const args = ['vercel', 'env', 'add', name, 'preview', gitBranch, '--value', value, '--force', '--yes'];
  if (vercel.scope) args.push('--scope', vercel.scope);
  try {
    npx(args, { timeout: 90_000 });
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    if (!message.includes('Added Environment Variable') && !message.includes('Overrode Environment Variable')) {
      throw error;
    }
  }
  console.log(`Set Vercel preview env ${name}`);
}

interface VercelDeployment {
  url: string;
  meta?: {
    githubCommitRef?: string;
  };
}

async function redeployVercelPreview(gitBranch: string): Promise<void> {
  if (!process.env.VERCEL_TOKEN || !vercel.projectId) return;
  ensureVercelLinked();
  const query = new URLSearchParams({ projectId: vercel.projectId, limit: '20' });
  if (vercel.scope) query.set('teamId', vercel.scope);
  const response = await fetch(`https://api.vercel.com/v6/deployments?${query}`, {
    headers: { authorization: `Bearer ${process.env.VERCEL_TOKEN}` },
  });
  if (!response.ok) throw new Error(`Could not list Vercel deployments: ${response.status} ${await response.text()}`);
  const data = (await response.json()) as { deployments?: VercelDeployment[] };
  const deployment = (data.deployments || []).find((item) => item.meta?.githubCommitRef === gitBranch);
  if (!deployment) {
    console.log(`No Vercel deployment found for ${gitBranch}; skipping redeploy`);
    return;
  }
  const args = ['vercel', 'redeploy', deployment.url, '--target', 'preview', '--no-wait'];
  if (vercel.scope) args.push('--scope', vercel.scope);
  npx(args, { timeout: 90_000, stdio: 'inherit' });
}

function sourceBranchName(): string {
  if (config.supabase?.previewHydrationSource && config.supabase.previewHydrationSource !== 'develop') {
    return config.supabase.previewHydrationSource;
  }
  return developBranchName;
}

async function main(): Promise<void> {
  if (!parentProjectRef) throw new Error('Missing SUPABASE_PARENT_PROJECT_REF or branching-config.json supabase.parentProjectRef.');
  if (!process.env.SUPABASE_ACCESS_TOKEN) throw new Error('Missing SUPABASE_ACCESS_TOKEN');
  const args = parseArgs(process.argv);
  const gitBranch = args.flags['git-branch'] || args.positional[0] || process.env.GITHUB_HEAD_REF || process.env.GITHUB_REF_NAME;
  if (!gitBranch) throw new Error('Missing git branch');
  const branchName = args.flags.name || `${previewPrefix}${slugify(gitBranch)}`;

  const persistentPreview = (config.persistentPreviews || []).find((preview) => preview.gitBranch === gitBranch);
  if (persistentPreview?.siteUrl && !process.env.PREVIEW_SITE_URL) {
    process.env.PREVIEW_SITE_URL = persistentPreview.siteUrl;
  }

  let branch = findBranch(branchName, gitBranch);
  const createdNow = !branch;

  if (args.flags['dry-run'] === 'true') {
    const wouldHydrate = createdNow || process.env.FORCE_HYDRATE === 'true';
    console.log(`Dry run for git branch ${gitBranch}:`);
    console.log(` - Supabase branch: ${branchName} (${branch ? 'reuse existing' : 'create new'})`);
    console.log(` - Hydration source: ${sourceBranchName()}`);
    console.log(` - Would hydrate this run: ${wouldHydrate}`);
    console.log(` - Copy auth users: ${Boolean(config.preview?.copyAuthUsers && wouldHydrate)}`);
    console.log(` - Copy public data: ${Boolean(config.preview?.copyPublicData && wouldHydrate)}`);
    console.log(` - Ensure buckets: ${(config.preview?.storageBuckets || []).map((bucket) => (typeof bucket === 'string' ? bucket : bucket.name)).join(', ') || 'none'}`);
    console.log(` - Copy storage buckets: ${(config.preview?.copyStorageBuckets || []).join(', ') || 'none'}`);
    console.log(` - Would set Vercel preview env vars: ${Object.values(envKeys).join(', ')}${process.env.VERCEL_TOKEN ? '' : ' (skipped: VERCEL_TOKEN missing)'}`);
    console.log(` - Would redeploy Vercel preview for ${gitBranch}`);
    if (persistentPreview) console.log(` - Persistent preview environment, site URL: ${persistentPreview.siteUrl || '(none)'}`);
    console.log('No changes were made.');
    return;
  }

  if (!branch) branch = createBranch(branchName, gitBranch);
  await waitForBranch(branchName);

  const source = getBranchDetails(sourceBranchName());
  const target = getBranchDetails(branchName);
  const buckets = config.preview?.storageBuckets || [];
  for (const bucket of buckets) await ensureBucket(target, typeof bucket === 'string' ? { name: bucket } : bucket);

  await syncAuthConfig(developBranchRef || branchRefFromUrl(source.SUPABASE_URL), branchRefFromUrl(target.SUPABASE_URL), gitBranch);
  await applyPendingMigrations(target);

  const shouldHydrate = createdNow || process.env.FORCE_HYDRATE === 'true';
  let authCounts: AuthCopyCounts | null = null;
  let tableCounts: Record<string, number> | null = null;
  if (shouldHydrate) {
    authCounts = await copyAuthUsers(source, target);
    tableCounts = await copyPublicData(source, target);
  } else {
    console.log('Preview branch already exists; preserving existing data. Set FORCE_HYDRATE=true to recopy source data.');
  }

  for (const bucket of config.preview?.copyStorageBuckets || []) await copyStorageBucket(source, target, bucket);

  setVercelEnv(envKeys.supabaseUrl, target.SUPABASE_URL, gitBranch);
  setVercelEnv(envKeys.supabaseAnonKey, target.SUPABASE_ANON_KEY, gitBranch);
  setVercelEnv(envKeys.supabaseServiceRoleKey, target.SUPABASE_SERVICE_ROLE_KEY, gitBranch);
  await redeployVercelPreview(gitBranch);

  const authLine = authCounts
    ? `Copied auth users: \`${authCounts.created} created, ${authCounts.sourceUsers} in source\``
    : `Copied auth users: \`${Boolean(config.preview?.copyAuthUsers && shouldHydrate)}\``;
  const tableLines = tableCounts && Object.keys(tableCounts).length
    ? `\nCopied table row counts:\n\n${Object.entries(tableCounts).map(([table, count]) => `- \`${table}\`: ${count}`).join('\n')}\n`
    : '';
  const summary = `# Preview Supabase Branch

Git branch: \`${gitBranch}\`
Supabase branch: \`${branchName}\`
Project ref: \`${branchRefFromUrl(target.SUPABASE_URL)}\`
Hydration source: \`${sourceBranchName()}\`
Hydrated this run: \`${shouldHydrate}\`
${authLine}
Copied public data: \`${Boolean(config.preview?.copyPublicData && shouldHydrate)}\`
Copied storage buckets: \`${(config.preview?.copyStorageBuckets || []).join(', ') || 'none'}\`
${tableLines}
OAuth callback URL for this branch (add to your OAuth provider if third-party login is needed):

\`\`\`text
${target.SUPABASE_URL}/auth/v1/callback
\`\`\`
`;
  writeFileSync('preview-branch-summary.md', summary);
  console.log(summary);
}

main().catch((error: unknown) => {
  console.error(error instanceof Error ? error.stack : error);
  process.exit(1);
});
