import nodeFetch from 'node-fetch';

/**
 * GitHub site skill — API-first approach.
 *
 * Uses GitHub REST API (or gh CLI) instead of browser.
 * No browser needed — this is the Router's ideal: API layer.
 *
 * Auth: Uses GITHUB_TOKEN env var, or falls back to gh CLI auth.
 */

const API_BASE = 'https://api.github.com';

function getHeaders() {
  const token = process.env.GITHUB_TOKEN;
  const headers = {
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'reach-agent/0.1.0',
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}

async function apiRequest(path, options = {}) {
  const { method = 'GET', body, params } = options;

  let url = path.startsWith('http') ? path : `${API_BASE}${path}`;
  if (params) {
    const searchParams = new URLSearchParams(params);
    url += `?${searchParams.toString()}`;
  }

  const response = await nodeFetch(url, {
    method,
    headers: {
      ...getHeaders(),
      ...(body ? { 'Content-Type': 'application/json' } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`GitHub API ${response.status}: ${text.substring(0, 200)}`);
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return null;
  }

  return response.json();
}

/**
 * Read repository contents (file or directory listing).
 *
 * @param {string} owner - Repo owner
 * @param {string} repo - Repo name
 * @param {string} [path] - File or directory path (default: root)
 * @param {string} [ref] - Branch/tag/commit (default: default branch)
 * @returns {object} File content or directory listing
 */
export async function readRepo(owner, repo, path = '', ref) {
  const params = ref ? { ref } : {};
  const result = await apiRequest(`/repos/${owner}/${repo}/contents/${path}`, { params });

  // Single file — decode content
  if (!Array.isArray(result) && result.content) {
    const decoded = Buffer.from(result.content, 'base64').toString('utf-8');
    return {
      type: 'file',
      path: result.path,
      name: result.name,
      size: result.size,
      content: decoded,
      sha: result.sha,
      url: result.html_url,
    };
  }

  // Directory listing
  if (Array.isArray(result)) {
    return {
      type: 'directory',
      path: path || '/',
      entries: result.map(e => ({
        name: e.name,
        type: e.type, // 'file' or 'dir'
        size: e.size,
        path: e.path,
        sha: e.sha,
        url: e.html_url,
      })),
    };
  }

  return result;
}

/**
 * Get repository info.
 *
 * @param {string} owner
 * @param {string} repo
 * @returns {object} Repository metadata
 */
export async function getRepoInfo(owner, repo) {
  const result = await apiRequest(`/repos/${owner}/${repo}`);
  return {
    name: result.name,
    fullName: result.full_name,
    description: result.description,
    language: result.language,
    stars: result.stargazers_count,
    forks: result.forks_count,
    openIssues: result.open_issues_count,
    defaultBranch: result.default_branch,
    private: result.private,
    url: result.html_url,
    topics: result.topics,
    createdAt: result.created_at,
    updatedAt: result.updated_at,
  };
}

/**
 * List issues for a repository.
 *
 * @param {string} owner
 * @param {string} repo
 * @param {object} [options]
 * @param {string} [options.state] - 'open' | 'closed' | 'all' (default: 'open')
 * @param {string} [options.labels] - Comma-separated label names
 * @param {number} [options.per_page] - Results per page (default: 30)
 * @param {number} [options.page] - Page number (default: 1)
 * @returns {object} { issues }
 */
export async function listIssues(owner, repo, options = {}) {
  const { state = 'open', labels, per_page = 30, page = 1 } = options;
  const params = { state, per_page: String(per_page), page: String(page) };
  if (labels) params.labels = labels;

  const result = await apiRequest(`/repos/${owner}/${repo}/issues`, { params });

  const issues = result.map(i => ({
    number: i.number,
    title: i.title,
    state: i.state,
    author: i.user?.login,
    labels: i.labels?.map(l => l.name) || [],
    comments: i.comments,
    createdAt: i.created_at,
    updatedAt: i.updated_at,
    url: i.html_url,
    body: i.body?.substring(0, 500) || '',
    isPR: !!i.pull_request,
  }));

  return { issues, state, page, per_page };
}

/**
 * Read a specific issue or PR with full body and comments.
 *
 * @param {string} owner
 * @param {string} repo
 * @param {number} number - Issue/PR number
 * @returns {object} { issue, comments }
 */
export async function readIssue(owner, repo, number) {
  const [issue, comments] = await Promise.all([
    apiRequest(`/repos/${owner}/${repo}/issues/${number}`),
    apiRequest(`/repos/${owner}/${repo}/issues/${number}/comments`),
  ]);

  return {
    number: issue.number,
    title: issue.title,
    state: issue.state,
    author: issue.user?.login,
    labels: issue.labels?.map(l => l.name) || [],
    body: issue.body || '',
    createdAt: issue.created_at,
    url: issue.html_url,
    isPR: !!issue.pull_request,
    comments: comments.map(c => ({
      author: c.user?.login,
      body: c.body || '',
      createdAt: c.created_at,
    })),
  };
}

/**
 * List pull requests.
 *
 * @param {string} owner
 * @param {string} repo
 * @param {object} [options]
 * @param {string} [options.state] - 'open' | 'closed' | 'all'
 * @param {number} [options.per_page]
 * @returns {object} { pulls }
 */
export async function listPulls(owner, repo, options = {}) {
  const { state = 'open', per_page = 30 } = options;
  const result = await apiRequest(`/repos/${owner}/${repo}/pulls`, {
    params: { state, per_page: String(per_page) },
  });

  const pulls = result.map(pr => ({
    number: pr.number,
    title: pr.title,
    state: pr.state,
    author: pr.user?.login,
    branch: pr.head?.ref,
    baseBranch: pr.base?.ref,
    mergeable: pr.mergeable,
    createdAt: pr.created_at,
    url: pr.html_url,
    body: pr.body?.substring(0, 500) || '',
  }));

  return { pulls, state };
}

/**
 * Create a new issue.
 *
 * @param {string} owner
 * @param {string} repo
 * @param {object} issue
 * @param {string} issue.title
 * @param {string} issue.body
 * @param {string[]} [issue.labels]
 * @param {string[]} [issue.assignees]
 * @returns {object} Created issue
 */
export async function createIssue(owner, repo, issue) {
  const { title, body, labels, assignees } = issue;

  if (!title) {
    throw new Error('createIssue requires title');
  }

  const result = await apiRequest(`/repos/${owner}/${repo}/issues`, {
    method: 'POST',
    body: { title, body: body || '', labels: labels || [], assignees: assignees || [] },
  });

  return {
    number: result.number,
    title: result.title,
    url: result.html_url,
    state: result.state,
  };
}

/**
 * Search GitHub code, repos, or issues.
 *
 * @param {string} query - Search query
 * @param {string} [type] - 'repositories' | 'code' | 'issues' (default: 'repositories')
 * @param {number} [per_page] - Results per page
 * @returns {object} Search results
 */
export async function search(query, type = 'repositories', per_page = 10) {
  const result = await apiRequest(`/search/${type}`, {
    params: { q: query, per_page: String(per_page) },
  });

  return {
    totalCount: result.total_count,
    items: result.items?.map(item => ({
      name: item.name || item.full_name || item.title,
      url: item.html_url,
      description: item.description || item.body?.substring(0, 200) || '',
      ...(type === 'repositories' ? { stars: item.stargazers_count, language: item.language } : {}),
      ...(type === 'code' ? { path: item.path, repository: item.repository?.full_name } : {}),
      ...(type === 'issues' ? { number: item.number, state: item.state } : {}),
    })) || [],
  };
}

export default {
  readRepo,
  getRepoInfo,
  listIssues,
  readIssue,
  listPulls,
  createIssue,
  search,
};
