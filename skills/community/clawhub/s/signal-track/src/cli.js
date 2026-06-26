const fs = require('node:fs/promises');
const path = require('node:path');
const os = require('node:os');

const PRIMARY_API_BASE = 'https://younews.k.sohu.com/';

const OPENCLAW_CONFIG_DIR = path.join(os.homedir(), '.openclaw');
const OPENCLAW_CONFIG_PATH = path.join(OPENCLAW_CONFIG_DIR, 'openclaw.json');
const LEGACY_CONFIG_DIR = path.join(os.homedir(), '.signal-track');
const LEGACY_CONFIG_PATH = path.join(LEGACY_CONFIG_DIR, 'config.json');
const SKILL_NAME = 'signal-track';


function parseArgs(argv) {
  const positional = [];
  const options = {};

  for (let i = 0; i < argv.length; i += 1) {
    const current = argv[i];
    if (current === '-h' || current === '-help') {
      options.help = true;
      continue;
    }
    if (!current.startsWith('--')) {
      positional.push(current);
      continue;
    }

    const raw = current.slice(2);
    const equalIdx = raw.indexOf('=');
    const key = equalIdx === -1 ? raw : raw.slice(0, equalIdx);
    const directValue = equalIdx === -1 ? undefined : raw.slice(equalIdx + 1);

    if (key === 'json') {
      options[key] = true;
      continue;
    }

    if (directValue !== undefined) {
      options[key] = directValue;
      continue;
    }

    const next = argv[i + 1];
    if (next && !next.startsWith('--')) {
      options[key] = next;
      i += 1;
      continue;
    }

    options[key] = true;
  }

  return { positional, options };
}

function usage() {
  return [
    'signal-track CLI',
    '',
    'Usage:',
    '  signal-track login --api-key <api_key>',
    '  signal-track topic show --topic-id <topic_id> [--cursor <cursor>] [--page-size <page_size>]',
    '  signal-track topics my',
    '  signal-track topics list',
    '  signal-track topics follow --topic-id <topic_id>',
    '  signal-track topics unfollow --topic-id <topic_id>',
    '  signal-track topics search --scope my --query <keyword>',
    '  signal-track topics search --scope square --query <keyword>',
    '  signal-track news_cards feed my [--cursor <cursor>] [--page-size <page_size>]',
    '  signal-track news_cards feed --topic-id <topic_id> [--cursor <cursor>] [--page-size <page_size>]',
    '  signal-track news_cards get <news_id>',
    '  signal-track news_cards search --query <keyword>',
    '  signal-track articles content --article-id <article_id>',
    '',
    'Options:',
    '  --json           Machine-readable output',
    '  --scope <scope>  topics search scope: my | square',
  ].join('\n');
}

async function readConfigFromPath(configPath) {
  try {
    const raw = await fs.readFile(configPath, 'utf8');
    const parsed = JSON.parse(raw || '{}');
    return parsed && typeof parsed === 'object' ? parsed : null;
  } catch (error) {
    if (error.code === 'ENOENT') {
      return null;
    }
    throw new Error(`Load config failed: ${error.message}`);
  }
}

async function readConfig() {
  const openclawConfig = await readConfigFromPath(OPENCLAW_CONFIG_PATH);
  const legacyConfig = await readConfigFromPath(LEGACY_CONFIG_PATH);

  if (!openclawConfig && !legacyConfig) {
    return {};
  }

  if (!openclawConfig) {
    return legacyConfig;
  }

  const openclawApiKey = getStoredApiKey(openclawConfig);
  if (openclawApiKey) {
    return openclawConfig;
  }

  if (!legacyConfig) {
    return openclawConfig;
  }

  const legacyApiKey = getStoredApiKey(legacyConfig);
  if (!legacyApiKey) {
    return openclawConfig;
  }

  return {
    ...openclawConfig,
    apiKey: legacyApiKey,
  };
}

async function configFileExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function resolveConfigPath() {
  if (await configFileExists(OPENCLAW_CONFIG_PATH)) {
    return OPENCLAW_CONFIG_PATH;
  }
  return LEGACY_CONFIG_PATH;
}

async function writeConfig(partial, configPath) {
  const targetPath = configPath || await resolveConfigPath();
  await fs.mkdir(path.dirname(targetPath), { recursive: true });
  const normalized = {
    ...partial,
  };
  await fs.writeFile(targetPath, JSON.stringify(normalized, null, 2), 'utf8');
  return normalized;
}

function getSkillConfig(config) {
  return config?.skills?.entries?.[SKILL_NAME] || {};
}

function getStoredApiKey(config) {
  return config?.apiKey || getSkillConfig(config)?.apiKey;
}

function getAuthConfig(config) {
  return {
    ...config,
    apiKey: getStoredApiKey(config),
  };
}

async function persistLoginConfig(apiKey) {
  const rawConfig = await readConfig();
  const targetPath = await resolveConfigPath();
  const skillConfig = getSkillConfig(rawConfig);

  const nextConfig = targetPath === OPENCLAW_CONFIG_PATH
    ? (() => {
      const {
        apiKey: _legacyApiKey,
        endpointHint: _legacyEndpointHint,
        ...openclawBase
      } = rawConfig;
      return {
        ...openclawBase,
        skills: {
          ...rawConfig.skills,
        entries: {
            ...rawConfig?.skills?.entries,
            [SKILL_NAME]: {
              ...skillConfig,
              enabled: true,
              apiKey,
            },
          },
        },
      };
    })()
    : {
      ...rawConfig,
      apiKey,
      endpointHint: 'logged-in',
    };

  const config = await writeConfig(nextConfig, targetPath);
  return config;
}

function getApiUrls() {
  return [PRIMARY_API_BASE];
}

function addQueryParams(url, params) {
  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null || value === '') return;
    url.searchParams.set(key, String(value));
  });
}

async function apiRequest(pathname, params = {}, options = {}, method = 'GET') {
  const urls = getApiUrls();
  let lastError;
  const payload = (typeof params === 'object' && params !== null) ? params : {};

  const headers = {
    Accept: 'application/json',
    ...(options.apiKey ? { Authorization: `Bearer ${options.apiKey}` } : {}),
  };

  for (const base of urls) {
    const url = new URL(base);
    url.pathname = pathname.startsWith('/') ? pathname : `/${pathname}`;
    const requestInit = {
      method,
      headers,
    };

    if (method === 'GET') {
      addQueryParams(url, payload);
    } else {
      const bodyEntries = Object.entries(payload).filter(([, value]) => value !== undefined && value !== null && value !== '');
      if (bodyEntries.length > 0) {
        requestInit.body = JSON.stringify(Object.fromEntries(bodyEntries));
        requestInit.headers = {
          ...headers,
          'Content-Type': 'application/json',
        };
      }
    }

    try {
      const response = await fetch(url.toString(), requestInit);
      const raw = await response.text();

      const body = raw ? parseJsonSafe(raw) : null;
      if (!response.ok) {
        const msg = body && body.message ? body.message : raw || response.statusText;
        lastError = new Error(`HTTP ${response.status}: ${msg}`);
        continue;
      }

      return { url: url.toString(), body };
    } catch (error) {
      lastError = error;
    }
  }

  throw lastError || new Error('Request failed');
}

async function apiGet(pathname, params = {}, options = {}) {
  return apiRequest(pathname, params, options, 'GET');
}

async function apiPost(pathname, params = {}, options = {}) {
  return apiRequest(pathname, params, options, 'POST');
}

function parseJsonSafe(raw) {
  try {
    return JSON.parse(raw);
  } catch {
    return raw;
  }
}

function getOutputPayload(response) {
  return response.body === null ? {} : response.body;
}

function printOutput(payload, jsonMode) {
  if (jsonMode) {
    process.stdout.write(`${JSON.stringify(payload, null, 2)}\n`);
    return;
  }
  if (payload === null || payload === undefined) {
    process.stdout.write('ok\n');
    return;
  }
  if (typeof payload === 'string') {
    process.stdout.write(`${payload}\n`);
    return;
  }
  process.stdout.write(`${JSON.stringify(payload, null, 2)}\n`);
}

function printDeprecation(message, jsonMode) {
  if (!jsonMode) {
    process.stderr.write(`Warning: ${message}\n`);
  }
}

function parsePaginationOptions(options) {
  const cursor = options.cursor;
  const pageSize = options['page-size'] !== undefined
    ? options['page-size']
    : options.page_size;
  const pageNumber = options['page-number'] !== undefined
    ? options['page-number']
    : options.page_number;
  let normalizedPageSize;

  if (pageSize !== undefined) {
    normalizedPageSize = Number.parseInt(pageSize, 10);
    if (Number.isNaN(normalizedPageSize) || normalizedPageSize < 1) {
      throw new Error('Invalid --page-size: must be integer >= 1');
    }
  }

  let normalizedPageNumber;
  if (pageNumber !== undefined) {
    normalizedPageNumber = Number.parseInt(pageNumber, 10);
    if (Number.isNaN(normalizedPageNumber) || normalizedPageNumber < 1) {
      throw new Error('Invalid --page-number: must be integer >= 1');
    }
  }

  return {
    ...(cursor ? { cursor } : {}),
    ...(normalizedPageSize ? { page_size: normalizedPageSize } : {}),
    ...(normalizedPageNumber ? { page_number: normalizedPageNumber } : {}),
  };
}

function requireAuth(config) {
  if (!config.apiKey) {
    throw new Error('You have not logged in yet. Run: signal-track login --api-key <api_key>');
  }
}

async function loginCommand(options, jsonMode) {
  const apiKey = options['api-key'];
  if (!apiKey) {
    throw new Error('Please provide api key: signal-track login --api-key <api_key>');
  }

  // use API-key header to verify key validity
  const result = getOutputPayload(await apiPost('/api/younews/subscription/identity/login', {}, { apiKey }));
  if (!result || result.code !== 200) {
    const msg = (result && (result.displayMessage || result.message)) || 'Login failed';
    throw new Error(msg);
  }
  await persistLoginConfig(apiKey);

  printOutput({
    status: 'SUCCESS',
    message: 'Login success',
  }, jsonMode);
}

async function requireSignedUser() {
  const config = getAuthConfig(await readConfig());
  requireAuth(config);
  return config;
}

async function topicsMyCommand(jsonMode) {
  const config = await requireSignedUser();
  const payload = getOutputPayload(await apiGet('/api/younews/subscription/content/topic/followed', {}, { apiKey: config.apiKey }));
  printOutput(payload, jsonMode);
}

async function topicsListCommand(jsonMode) {
  const config = await requireSignedUser();
  const payload = getOutputPayload(await apiGet('/api/younews/subscription/content/topic/all', {}, { apiKey: config.apiKey }));
  printOutput(payload, jsonMode);
}

async function topicsFollowCommand(options, _jsonMode) {
  const config = await requireSignedUser();
  const topicId = options['topic-id'];
  if (!topicId) {
    throw new Error('Missing --topic-id');
  }
  const payload = getOutputPayload(await apiGet('/api/younews/subscription/content/topic/follow', {
    topic_id: topicId,
  }, { apiKey: config.apiKey }));
  printOutput(payload, _jsonMode);
}

async function topicsUnfollowCommand(options, _jsonMode) {
  const config = await requireSignedUser();
  const topicId = options['topic-id'];
  if (!topicId) {
    throw new Error('Missing --topic-id');
  }
  const payload = getOutputPayload(await apiGet('/api/younews/subscription/content/topic/unfollow', {
    topic_id: topicId,
  }, { apiKey: config.apiKey }));
  printOutput(payload, _jsonMode);
}

async function topicsSearchCommand(options, jsonMode) {
  const config = await requireSignedUser();
  const scope = options.scope;
  const query = options.query;
  if (!query) {
    throw new Error('Missing --query');
  }
  if (!scope || !['my', 'square'].includes(scope)) {
    throw new Error('Missing or invalid --scope, expected my or square');
  }

  const endpoint = scope === 'my'
    ? '/api/younews/subscription/content/topic/followed/search'
    : '/api/younews/subscription/content/topic/all/search';
  const sharedParams = {
    keyword: query,
    ...parsePaginationOptions(options),
  };

  const payload = getOutputPayload(await apiGet(endpoint, {
    ...sharedParams,
  }, { apiKey: config.apiKey }));

  printOutput(payload, jsonMode);
}

async function topicShowCommand(options, jsonMode) {
  const config = await requireSignedUser();
  const topicId = options['topic-id'];
  if (!topicId) {
    throw new Error('Missing --topic-id');
  }

  const pagination = parsePaginationOptions(options);

  const payload = getOutputPayload(await apiGet('/api/younews/subscription/content/topic/details', {
    topic_id: topicId,
    ...pagination,
  }, { apiKey: config.apiKey }));
  printOutput(payload, jsonMode);
}

async function newsCardsFeedCommand(options, jsonMode, mode = 'auto') {
  const config = await requireSignedUser();
  const explicitMyFeed = mode === 'my';
  const topicId = !explicitMyFeed && options['topic-id'];
  const pagination = parsePaginationOptions(options);

  const payload = topicId
    ? getOutputPayload(await apiGet('/api/younews/subscription/content/topic/details', {
      topic_id: topicId,
      ...pagination,
    }, { apiKey: config.apiKey }))
    : getOutputPayload(await apiGet('/api/younews/subscription/content/home/feed/cards', {
      ...pagination,
    }, { apiKey: config.apiKey }));

  printOutput(payload, jsonMode);
}

async function newsCardsGetCommand(options, jsonMode, positionalNewsId) {
  const config = await requireSignedUser();
  const newsId = options['news-id'] || positionalNewsId;
  if (!newsId) {
    throw new Error('Missing --news-id or positional news id');
  }
  const payload = getOutputPayload(await apiGet('/api/younews/subscription/content/cards/detail/extend', {
    immersive_type: 'single',
    news_id: newsId,
  }, { apiKey: config.apiKey }));

  if (!jsonMode && payload?.data?.cards) {
    const firstCard = payload.data.cards?.[0];
    if (firstCard) {
      printOutput(firstCard, false);
      return;
    }
  }

  printOutput(payload, jsonMode);
}

async function newsCardsSearchCommand(options, jsonMode) {
  const config = await requireSignedUser();
  const query = options.query;
  if (!query) {
    throw new Error('Missing --query');
  }
  const payload = getOutputPayload(await apiGet('/api/younews/subscription/content/cards/search', {
    keyword: query,
  }, { apiKey: config.apiKey }));
  printOutput(payload, jsonMode);
}

async function articlesContentCommand(options, jsonMode) {
  const config = await requireSignedUser();
  const articleId = options['article-id'];
  if (!articleId) {
    throw new Error('Missing --article-id');
  }
  const payload = getOutputPayload(await apiGet('/api/younews/subscription/content/cards/article/detail', {
    oid: articleId,
  }, { apiKey: config.apiKey }));
  printOutput(payload, jsonMode);
}

async function main() {
  const { positional, options } = parseArgs(process.argv.slice(2));
  const jsonMode = Boolean(options.json);
  const [root, sub, sub2] = positional;

  if (options.help || positional.length === 0) {
    process.stdout.write(`${usage()}\n`);
    return;
  }

  const route = `${root || ''} ${sub || ''} ${sub2 || ''}`.trim().replace(/\s+/g, ' ');

  try {
    if (root === 'login') {
      await loginCommand(options, jsonMode);
      return;
    }

    if (root === 'topics') {
      if (sub === 'my') {
        await topicsMyCommand(jsonMode);
      } else if (sub === 'list') {
        await topicsListCommand(jsonMode);
      } else if (sub === 'follow') {
        await topicsFollowCommand(options, jsonMode);
      } else if (sub === 'unfollow') {
        await topicsUnfollowCommand(options, jsonMode);
      } else if (sub === 'search') {
        await topicsSearchCommand(options, jsonMode);
      } else {
        throw new Error('Unknown topics command');
      }
      return;
    }

    if (root === 'topic') {
      if (sub === 'show') {
        await topicShowCommand(options, jsonMode);
      } else {
        throw new Error('Unknown topic command');
      }
      return;
    }

    if (root === 'news_cards') {
      if (sub === 'feed') {
        if (sub2 === 'my') {
          await newsCardsFeedCommand(options, jsonMode, 'my');
        } else if (options['topic-id']) {
          await newsCardsFeedCommand(options, jsonMode);
        } else if (!sub2) {
          await newsCardsFeedCommand(options, jsonMode, 'my');
        } else {
          throw new Error('Unknown news_cards feed command');
        }
        return;
      }
      if (sub === 'get') {
        await newsCardsGetCommand(options, jsonMode, sub2);
        return;
      }
      if (sub === 'search') {
        await newsCardsSearchCommand(options, jsonMode);
        return;
      }
      throw new Error('Unknown news_cards command');
    }

    if (root === 'articles' && sub === 'content') {
      await articlesContentCommand(options, jsonMode);
      return;
    }

    throw new Error(`Unsupported command: ${route}`);
  } catch (error) {
    const message = error?.message || 'Unknown error';
    process.stderr.write(`Error: ${message}\n`);
    process.stderr.write(`${usage()}\n`);
    process.exitCode = 1;
  }
}

main();
