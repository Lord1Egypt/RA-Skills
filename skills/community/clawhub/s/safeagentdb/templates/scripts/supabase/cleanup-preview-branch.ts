import { readFileSync, existsSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import process from 'node:process';

interface PersistentPreview {
  gitBranch: string;
  siteUrl?: string;
}

interface BranchingConfig {
  supabase?: {
    parentProjectRef?: string;
    developBranchRef?: string;
  };
  vercel?: {
    scope?: string;
    projectName?: string;
  };
  envKeys?: {
    supabaseUrl?: string;
    supabaseAnonKey?: string;
    supabaseServiceRoleKey?: string;
  };
  preview?: {
    namePrefix?: string;
  };
  persistentPreviews?: PersistentPreview[];
}

interface SupabaseBranch {
  name: string;
  git_branch?: string | null;
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
const developBranchRef = process.env.SUPABASE_DEVELOP_BRANCH_REF || config.supabase?.developBranchRef;
const previewPrefix = process.env.PREVIEW_BRANCH_PREFIX || config.preview?.namePrefix || 'preview-';
const vercelScope = process.env.VERCEL_SCOPE || config.vercel?.scope;
const vercelProjectName = process.env.VERCEL_PROJECT_NAME || config.vercel?.projectName;
const envNames: string[] = Object.values({
  supabaseUrl: config.envKeys?.supabaseUrl || 'NEXT_PUBLIC_SUPABASE_URL',
  supabaseAnonKey: config.envKeys?.supabaseAnonKey || 'NEXT_PUBLIC_SUPABASE_ANON_KEY',
  supabaseServiceRoleKey: config.envKeys?.supabaseServiceRoleKey || 'SUPABASE_SERVICE_ROLE_KEY',
});

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

function run(command: string, args: string[]): string {
  const result = spawnSync(command, args, {
    encoding: 'utf8',
    shell: process.platform === 'win32',
    env: process.env,
    stdio: ['ignore', 'pipe', 'pipe'],
    timeout: 90_000,
  });
  if (result.error) throw new Error(`${command} ${args.join(' ')} failed to start: ${result.error.message}`);
  if (result.status !== 0) throw new Error(`${command} ${args.join(' ')} failed:\n${result.stdout || ''}\n${result.stderr || ''}`);
  return result.stdout || '';
}

function npx(args: string[]): string {
  return run(process.platform === 'win32' ? 'npx.cmd' : 'npx', args);
}

function supabase(args: string[]): string {
  return npx(['supabase', ...args]);
}

let vercelLinked = false;

function ensureVercelLinked(): void {
  if (vercelLinked || !process.env.VERCEL_TOKEN || !vercelProjectName) return;
  const args = ['vercel', 'link', '--yes', '--project', vercelProjectName];
  if (vercelScope) args.push('--scope', vercelScope);
  npx(args);
  vercelLinked = true;
}

function jsonArray<T>(output: string): T[] {
  const first = output.indexOf('[');
  const last = output.lastIndexOf(']');
  if (first === -1 || last <= first) return [];
  return JSON.parse(output.slice(first, last + 1)) as T[];
}

function listBranches(projectRef: string): SupabaseBranch[] {
  try {
    return jsonArray<SupabaseBranch>(supabase(['branches', 'list', '--project-ref', projectRef, '-o', 'json']));
  } catch (error) {
    console.log(`Could not list branches for ${projectRef}: ${error instanceof Error ? error.message : String(error)}`);
    return [];
  }
}

function removeVercelEnv(name: string, gitBranch: string): void {
  if (!process.env.VERCEL_TOKEN) return;
  ensureVercelLinked();
  const args = ['vercel', 'env', 'rm', name, 'preview', gitBranch, '--yes'];
  if (vercelScope) args.push('--scope', vercelScope);
  try {
    npx(args);
    console.log(`Removed Vercel env ${name}`);
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    if (message.includes('not found')) return;
    console.log(`Vercel env cleanup warning for ${name}:\n${message}`);
  }
}

function main(): void {
  if (!parentProjectRef) throw new Error('Missing SUPABASE_PARENT_PROJECT_REF or branching-config.json supabase.parentProjectRef.');
  if (!process.env.SUPABASE_ACCESS_TOKEN) throw new Error('Missing SUPABASE_ACCESS_TOKEN');
  const args = parseArgs(process.argv);
  const gitBranch = args.flags['git-branch'] || args.positional[0] || process.env.GITHUB_HEAD_REF || process.env.GITHUB_REF_NAME;
  if (!gitBranch) throw new Error('Missing git branch');
  if ((config.persistentPreviews || []).some((preview) => preview.gitBranch === gitBranch)) {
    console.log(`${gitBranch} is a persistent preview environment; skipping cleanup. Remove it from persistentPreviews in branching-config.json to allow deletion.`);
    return;
  }
  const expectedName = args.flags.name || `${previewPrefix}${slugify(gitBranch)}`;
  let foundBranch = false;
  for (const projectRef of [parentProjectRef, developBranchRef].filter((ref): ref is string => Boolean(ref))) {
    const branch = listBranches(projectRef).find((item) => item.name === expectedName || item.git_branch === gitBranch);
    if (!branch) continue;
    foundBranch = true;
    console.log(`Deleting Supabase preview branch ${branch.name}`);
    supabase(['branches', 'delete', branch.name, '--project-ref', projectRef, '--yes']);
  }
  if (!foundBranch) {
    console.log(`No Supabase preview branch found for ${gitBranch}; skipping Vercel env cleanup.`);
    return;
  }
  for (const name of envNames) removeVercelEnv(name, gitBranch);
}

try {
  main();
} catch (error) {
  console.error(error instanceof Error ? error.stack : error);
  process.exit(1);
}
