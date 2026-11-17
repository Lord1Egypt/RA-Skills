import os from 'node:os';
import path from 'node:path';

export const SKILL_NAME = 'read-figma-design';
export const SKILL_VERSION = '0.1.0';

export const DEFAULT_BUDGETS = Object.freeze({
  maxParentDepth: 6,
  maxChildDepth: 4,
  maxSiblings: 16,
  maxNodesPerUrl: 600,
  maxScreenshotsPerUrl: 24,
  maxArtifactMiBPerUrl: 100,
  screenshotScale: 2,
});

const FLAG_NAMES = new Set([
  '--issue-json',
  '--url',
  '--out',
  '--repo',
  '--env-file',
  '--token-store',
  '--max-parent-depth',
  '--max-child-depth',
  '--max-siblings',
  '--max-nodes-per-url',
  '--max-screenshots-per-url',
  '--max-artifact-mib-per-url',
  '--screenshot-scale',
]);

const BOOLEAN_FLAGS = new Set([
  '--help',
  '--version',
  '--require-code-connect',
  '--require-screenshots',
]);

const BUDGET_FLAG_MAP = {
  '--max-parent-depth': 'maxParentDepth',
  '--max-child-depth': 'maxChildDepth',
  '--max-siblings': 'maxSiblings',
  '--max-nodes-per-url': 'maxNodesPerUrl',
  '--max-screenshots-per-url': 'maxScreenshotsPerUrl',
  '--max-artifact-mib-per-url': 'maxArtifactMiBPerUrl',
  '--screenshot-scale': 'screenshotScale',
};

function getEnvValue(env, key) {
  if (!Object.hasOwn(env, key)) {
    return undefined;
  }

  const value = env[key];
  if (value === undefined || value === null) {
    return undefined;
  }
  return String(value);
}

function resolvePath(cwd, value) {
  return path.resolve(cwd, value);
}

function parseFlags(argv) {
  const args = argv.slice(2);
  const values = new Map();
  const booleans = new Set();

  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];

    if (BOOLEAN_FLAGS.has(arg)) {
      booleans.add(arg);
      continue;
    }

    if (!FLAG_NAMES.has(arg)) {
      return {
        ok: false,
        errorCode: 'unknown_argument',
        message: `Unknown argument: ${arg}`,
      };
    }

    const value = args[index + 1];
    if (value === undefined || value.startsWith('--')) {
      return {
        ok: false,
        errorCode: 'missing_argument_value',
        message: `Missing value for ${arg}`,
      };
    }

    values.set(arg, value);
    index += 1;
  }

  return {
    ok: true,
    values,
    booleans,
  };
}

function parsePositiveNumber(name, value) {
  const number = Number(value);
  if (!Number.isFinite(number) || number <= 0) {
    return {
      ok: false,
      errorCode: 'invalid_budget',
      message: `${name} must be a positive number`,
    };
  }
  return {
    ok: true,
    value: number,
  };
}

function buildEnvFiles(values, env, cwd, skillRoot) {
  if (values.has('--env-file')) {
    return [resolvePath(cwd, values.get('--env-file'))];
  }

  const envFile = getEnvValue(env, 'FIGMA_ENV_FILE');
  if (envFile) {
    return [resolvePath(cwd, envFile)];
  }

  return [
    path.resolve(skillRoot, '../../.env'),
    path.resolve(cwd, '.env'),
  ];
}

function buildTokenStore(values, env, cwd) {
  if (values.has('--token-store')) {
    return resolvePath(cwd, values.get('--token-store'));
  }

  const tokenStore = getEnvValue(env, 'FIGMA_TOKEN_STORE');
  if (tokenStore) {
    return resolvePath(cwd, tokenStore);
  }

  return path.join(os.homedir(), '.multica/secrets/figma-oauth.json');
}

function buildBudgets(values) {
  const budgets = { ...DEFAULT_BUDGETS };

  for (const [flag, budgetKey] of Object.entries(BUDGET_FLAG_MAP)) {
    if (!values.has(flag)) {
      continue;
    }

    const parsed = parsePositiveNumber(flag, values.get(flag));
    if (!parsed.ok) {
      return parsed;
    }
    budgets[budgetKey] = parsed.value;
  }

  return {
    ok: true,
    budgets,
  };
}

export function parseCliArgs(argv, env = process.env, cwd = process.cwd(), skillRoot = process.cwd()) {
  const flags = parseFlags(argv);
  if (!flags.ok) {
    return flags;
  }

  const { values, booleans } = flags;
  if (booleans.has('--help')) {
    return {
      ok: true,
      mode: 'help',
    };
  }

  if (booleans.has('--version')) {
    return {
      ok: true,
      mode: 'version',
    };
  }

  const hasIssueJson = values.has('--issue-json');
  const hasUrl = values.has('--url');
  if (hasIssueJson && hasUrl) {
    return {
      ok: false,
      errorCode: 'figma_input_conflict',
      message: '--issue-json and --url are mutually exclusive',
    };
  }

  if (!hasIssueJson && !hasUrl) {
    return {
      ok: false,
      errorCode: 'figma_input_required',
      message: 'One of --issue-json or --url is required',
    };
  }

  if (!values.has('--out')) {
    return {
      ok: false,
      errorCode: 'artifact_out_required',
      message: '--out is required',
    };
  }

  const parsedBudgets = buildBudgets(values);
  if (!parsedBudgets.ok) {
    return parsedBudgets;
  }

  const config = {
    ok: true,
    mode: hasUrl ? 'url' : 'issue-json',
    out: resolvePath(cwd, values.get('--out')),
    repo: values.has('--repo') ? resolvePath(cwd, values.get('--repo')) : null,
    envFiles: buildEnvFiles(values, env, cwd, skillRoot),
    tokenStore: buildTokenStore(values, env, cwd),
    budgets: parsedBudgets.budgets,
    requireCodeConnect: booleans.has('--require-code-connect'),
    requireScreenshots: booleans.has('--require-screenshots'),
  };

  if (hasUrl) {
    config.url = values.get('--url');
  } else {
    config.issueJson = resolvePath(cwd, values.get('--issue-json'));
  }

  return config;
}

export function formatHelp() {
  return `${SKILL_NAME}

Read Figma context for Multica issue figma_urls.

Usage:
  node scripts/read-figma-context.mjs --issue-json <path> --out <artifact-root> [--repo <repo>]
  node scripts/read-figma-context.mjs --url <figma-url> --out <artifact-root> [--repo <repo>]

Options:
  --issue-json <path>              Issue JSON containing figma_urls.
  --url <url>                      Single Figma design URL with node-id.
  --out <path>                     Artifact root directory.
  --repo <path>                    Repair repository for later artifact ignore and Code Connect scans.
  --env-file <path>                Env file path. Defaults to FIGMA_ENV_FILE, skill ../../.env, then cwd .env.
  --token-store <path>             Token store path. Defaults to FIGMA_TOKEN_STORE or ~/.multica/secrets/figma-oauth.json.
  --max-parent-depth <n>           Default ${DEFAULT_BUDGETS.maxParentDepth}.
  --max-child-depth <n>            Default ${DEFAULT_BUDGETS.maxChildDepth}.
  --max-siblings <n>               Default ${DEFAULT_BUDGETS.maxSiblings}.
  --max-nodes-per-url <n>          Default ${DEFAULT_BUDGETS.maxNodesPerUrl}.
  --max-screenshots-per-url <n>    Default ${DEFAULT_BUDGETS.maxScreenshotsPerUrl}.
  --max-artifact-mib-per-url <n>   Default ${DEFAULT_BUDGETS.maxArtifactMiBPerUrl}.
  --screenshot-scale <n>           Default ${DEFAULT_BUDGETS.screenshotScale}.
  --require-code-connect           Fail if Code Connect clues are unavailable.
  --require-screenshots            Fail if required screenshots cannot be exported.
  --help                           Print this text without reading credentials or network.
  --version                        Print version without reading credentials or network.
`;
}

export function formatVersion() {
  return `${SKILL_NAME} ${SKILL_VERSION}
artifact schema versions: manifest=1, target-node=1, context-tree=1, design-properties=1, code-connect=1
`;
}
