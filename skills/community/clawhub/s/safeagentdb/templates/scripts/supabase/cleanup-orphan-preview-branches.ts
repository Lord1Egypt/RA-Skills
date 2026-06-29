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
    developBranchName?: string;
  };
  vercel?: {
    scope?: string;
    projectName?: string;
  };
  github?: {
    repository?: string;
  };
  envKeys?: {
    supabaseUrl?: string;
    supabaseAnonKey?: string;
    supabaseServiceRoleKey?: string;
  };
  persistentPreviews?: PersistentPreview[];
}

interface SupabaseBranch {
  name: string;
  git_branch?: string | null;
  is_default?: boolean;
}

const CONFIG_PATH = process.env.BRANCHING_CONFIG_PATH || 'branching-config.json';
const config: BranchingConfig = existsSync(CONFIG_PATH)
  ? (JSON.parse(readFileSync(CONFIG_PATH, 'utf8')) as BranchingConfig)
  : {};
const parentProjectRef = process.env.SUPABASE_PARENT_PROJECT_REF || config.supabase?.parentProjectRef;
const developBranchName = process.env.SUPABASE_DEVELOP_BRANCH_NAME || config.supabase?.developBranchName || 'develop';
const vercelScope = process.env.VERCEL_SCOPE || config.vercel?.scope;
const vercelProjectName = process.env.VERCEL_PROJECT_NAME || config.vercel?.projectName;
const githubRepository = process.env.GITHUB_REPOSITORY || config.github?.repository;
const envNames: string[] = Object.values({
  supabaseUrl: config.envKeys?.supabaseUrl || 'NEXT_PUBLIC_SUPABASE_URL',
  supabaseAnonKey: config.envKeys?.supabaseAnonKey || 'NEXT_PUBLIC_SUPABASE_ANON_KEY',
  supabaseServiceRoleKey: config.envKeys?.supabaseServiceRoleKey || 'SUPABASE_SERVICE_ROLE_KEY',
});

function run(command: string, args: string[]): string {
  const result = spawnSync(command, args, {
    encoding: 'utf8',
    shell: process.platform === 'win32',
    env: process.env,
    stdio: ['ignore', 'pipe', 'pipe'],
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

async function githubBranchExists(branchName: string): Promise<boolean> {
  if (!process.env.GITHUB_TOKEN) throw new Error('Missing GITHUB_TOKEN');
  if (!githubRepository) throw new Error('Missing GITHUB_REPOSITORY or branching-config.json github.repository.');
  const response = await fetch(
    `https://api.github.com/repos/${githubRepository}/branches/${encodeURIComponent(branchName)}`,
    {
      headers: {
        authorization: `Bearer ${process.env.GITHUB_TOKEN}`,
        accept: 'application/vnd.github+json',
      },
    },
  );
  if (response.status === 404) return false;
  if (!response.ok) throw new Error(`GitHub branch lookup failed for ${branchName}: ${response.status} ${await response.text()}`);
  return true;
}

function removeVercelEnv(name: string, gitBranch: string): void {
  if (!process.env.VERCEL_TOKEN) return;
  ensureVercelLinked();
  const args = ['vercel', 'env', 'rm', name, 'preview', gitBranch, '--yes'];
  if (vercelScope) args.push('--scope', vercelScope);
  try {
    npx(args);
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    if (!message.includes('not found')) {
      console.log(`Vercel env cleanup warning for ${name} (${gitBranch}):\n${message}`);
    }
  }
}

async function main(): Promise<void> {
  if (!parentProjectRef) throw new Error('Missing SUPABASE_PARENT_PROJECT_REF or branching-config.json supabase.parentProjectRef.');
  if (!process.env.SUPABASE_ACCESS_TOKEN) throw new Error('Missing SUPABASE_ACCESS_TOKEN');
  const branches = jsonArray<SupabaseBranch>(supabase(['branches', 'list', '--project-ref', parentProjectRef, '-o', 'json']));
  const persistentGitBranches = new Set((config.persistentPreviews || []).map((preview) => preview.gitBranch));
  const previews = branches.filter((branch): branch is SupabaseBranch & { git_branch: string } => (
    !branch.is_default &&
    branch.name !== developBranchName &&
    Boolean(branch.git_branch) &&
    !persistentGitBranches.has(branch.git_branch as string)
  ));

  for (const branch of previews) {
    const exists = await githubBranchExists(branch.git_branch);
    if (exists) {
      console.log(`Keeping ${branch.name}: Git branch ${branch.git_branch} exists`);
      continue;
    }

    console.log(`Deleting orphan Supabase branch ${branch.name}; Git branch ${branch.git_branch} no longer exists`);
    supabase(['branches', 'delete', branch.name, '--project-ref', parentProjectRef, '--yes']);
    for (const envName of envNames) removeVercelEnv(envName, branch.git_branch);
  }
}

main().catch((error: unknown) => {
  console.error(error instanceof Error ? error.stack : error);
  process.exit(1);
});
