const FIGMA_HOSTS = new Set(['figma.com', 'www.figma.com']);

const ISSUE_URL_SOURCES = [
  {
    path: ['figma_urls'],
    source: 'figma_urls',
    inputShape: 'top-level',
  },
  {
    path: ['issue', 'figma_urls'],
    source: 'issue.figma_urls',
    inputShape: 'issue-field',
  },
  {
    path: ['data', 'figma_urls'],
    source: 'data.figma_urls',
    inputShape: 'data-field',
  },
];

function readPath(value, path) {
  let current = value;
  for (const segment of path) {
    if (current === null || typeof current !== 'object') {
      return undefined;
    }
    current = current[segment];
  }
  return current;
}

function normalizeUrlInput(url) {
  if (typeof url !== 'string') {
    return '';
  }
  return url.trim();
}

function canonicalizeNodeId(nodeId) {
  return nodeId.replaceAll('-', ':');
}

function parseKind(url) {
  const [kind = null] = url.pathname.split('/').filter(Boolean);
  return kind;
}

export function parseFigmaDesignUrl(url) {
  const input = normalizeUrlInput(url);
  if (input.length === 0) {
    return {
      ok: false,
      errorCode: 'malformed_url',
      url,
    };
  }

  let parsed;
  try {
    parsed = new URL(input);
  } catch {
    return {
      ok: false,
      errorCode: 'malformed_url',
      url: input,
    };
  }

  if (!FIGMA_HOSTS.has(parsed.hostname.toLowerCase())) {
    return {
      ok: false,
      errorCode: 'non_figma_host',
      url: input,
      host: parsed.hostname,
    };
  }

  const kind = parseKind(parsed);
  if (kind !== 'design') {
    return {
      ok: false,
      errorCode: 'unsupported_figma_url_kind',
      url: input,
      kind,
    };
  }

  const [, fileKey = null] = parsed.pathname.split('/').filter(Boolean);
  if (!fileKey) {
    return {
      ok: false,
      errorCode: 'missing_file_key',
      url: input,
      kind,
    };
  }

  const originalNodeId = parsed.searchParams.get('node-id');
  if (!originalNodeId || originalNodeId.trim().length === 0) {
    return {
      ok: false,
      errorCode: 'missing_node_id',
      url: input,
      kind,
      fileKey,
    };
  }

  return {
    ok: true,
    url: input,
    kind,
    fileKey,
    originalNodeId,
    nodeId: canonicalizeNodeId(originalNodeId),
  };
}

export function extractFigmaUrlsFromIssue(issueJson) {
  for (const source of ISSUE_URL_SOURCES) {
    const rawUrls = readPath(issueJson, source.path);
    if (!Array.isArray(rawUrls)) {
      continue;
    }

    const urls = rawUrls
      .filter((url) => typeof url === 'string')
      .map((url) => url.trim())
      .filter((url) => url.length > 0);

    if (urls.length > 0) {
      return {
        ok: true,
        source: source.source,
        inputShape: source.inputShape,
        urls,
      };
    }
  }

  return {
    ok: false,
    errorCode: 'figma_urls_empty',
    source: null,
    inputShape: null,
    urls: [],
  };
}

export function dedupeParsedUrls(parsedUrls) {
  const seen = new Map();

  return parsedUrls.map((parsedUrl, index) => {
    const ordinal = index + 1;
    const entry = {
      ...parsedUrl,
      ordinal,
      duplicateOf: null,
    };

    if (parsedUrl?.ok === true) {
      const key = `${parsedUrl.fileKey}:${parsedUrl.nodeId}`;
      if (seen.has(key)) {
        entry.duplicateOf = seen.get(key);
      } else {
        seen.set(key, ordinal);
      }
    }

    return entry;
  });
}
