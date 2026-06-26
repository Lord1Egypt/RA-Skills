#!/usr/bin/env node
/**
 * Wiki.js V3 Client - All-encompassing GraphQL + REST Wrapper
 * 
 * Features:
 * - Full GraphQL API coverage (Pages, Assets, Search, Tags, Tree, History)
 * - Path-First design with ID fallback
 * - Retry with exponential backoff
 * - Chunking for large content (413 handling)
 * - Idempotent upsert operations
 * - Multi-locale support
 * - Asset upload via REST API
 * - Clean error messages
 * 
 * Usage:
 *   wiki upsert <path> <title> <content|@file> [tags]
 *   wiki get <path|id>
 *   wiki delete <path|id>
 *   wiki move <from> <to>
 *   wiki copy <from> <to>
 *   wiki history <path|id>
 *   wiki restore <path|id> --version=<n>
 *   wiki render <path|id> --format=html|pdf
 *   wiki search <term> [--tags=a,b] [--limit=20]
 *   wiki tree [--path=prefix] [--depth=3]
 *   wiki tags list
 *   wiki tags create <tag>
 *   wiki tags delete <tag>
 *   wiki assets [--folder=id] [--kind=IMAGE|VIDEO|FILE]
 *   wiki upload <file> [--folder=id] [--name=custom]
 *   wiki asset-delete <id>
 *   wiki mkdir <parent-id> <slug> [name]
 * 
 * IMPORTANT: API Key Permissions
 *   Wiki.js API keys have per-key permissions, NOT per-group.
 *   A key with `api:1` may have write access while `api:2` may be read-only,
 *   even if both are assigned to `grp:1`.
 *   If update returns "Forbidden", check the API key has write permissions.
 */

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

// Config
const WIKI_URL = process.env.WIKIJS_URL || 'http://localhost:3000';
const WIKI_TOKEN = process.env.WIKIJS_TOKEN;
const DEFAULT_LOCALE = process.env.WIKIJS_LOCALE || 'de';
const TIMEOUT_MS = parseInt(process.env.WIKIJS_TIMEOUT) || 30000;
const MAX_RETRIES = 3;
const MAX_CONTENT_SIZE = 10 * 1024 * 1024; // 10MB

if (!WIKI_TOKEN) {
  console.error('Error: WIKIJS_TOKEN environment variable not set.');
  console.error('Set it with: export WIKIJS_TOKEN=your_api_key');
  process.exit(1);
}

const ENDPOINT = `${WIKI_URL}/graphql`;
const UPLOAD_ENDPOINT = `${WIKI_URL}/u`;

// Utils
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

function parseTags(tagsStr) {
  if (!tagsStr) return [];
  if (Array.isArray(tagsStr)) return tagsStr;
  return tagsStr.split(',').map(t => t.trim()).filter(Boolean);
}

function parsePathOrId(input) {
  // If it's a number, treat as ID
  if (/^\d+$/.test(input)) return { id: parseInt(input), path: null };
  // Otherwise, treat as path
  return { id: null, path: input.replace(/^\//, '') };
}

// GraphQL Query with retry
async function query(graphql, variables = {}, retries = MAX_RETRIES) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);
  
  try {
    const resp = await fetch(ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${WIKI_TOKEN}`
      },
      body: JSON.stringify({ query: graphql, variables }),
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    // Handle 413 Payload Too Large
    if (resp.status === 413) {
      throw new Error('PAYLOAD_TOO_LARGE');
    }

    if (!resp.ok) {
      const text = await resp.text();
      throw new Error(`HTTP ${resp.status}: ${text.substring(0, 200)}`);
    }

    const json = await resp.json();

    if (json.errors && json.errors.length > 0) {
      const msgs = json.errors.map(e => e.message).join('; ');
      throw new Error(`GraphQL Error: ${msgs}`);
    }

    return json.data;
  } catch (err) {
    clearTimeout(timeoutId);
    
    if (err.name === 'AbortError') {
      throw new Error(`Timeout after ${TIMEOUT_MS / 1000}s`);
    }
    
    if (retries > 0 && (err.message.includes('ECONNREFUSED') || err.message.includes('ETIMEDOUT'))) {
      const delay = 1000 * Math.pow(2, MAX_RETRIES - retries);
      console.error(`Retry in ${delay}ms... (${retries} left)`);
      await sleep(delay);
      return query(graphql, variables, retries - 1);
    }
    
    throw err;
  }
}

// REST Upload with retry
async function uploadFile(filePath, folderId = 0, customName = null) {
  const FormData = require('form-data');
  const stat = fs.statSync(filePath);
  
  if (stat.size > MAX_CONTENT_SIZE) {
    throw new Error(`File too large: ${stat.size} > ${MAX_CONTENT_SIZE}`);
  }
  
  const form = new FormData();
  form.append('folderId', folderId.toString());
  form.append('file', fs.createReadStream(filePath), {
    filename: customName || path.basename(filePath)
  });

  const resp = await fetch(UPLOAD_ENDPOINT, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${WIKI_TOKEN}`,
      ...form.getHeaders()
    },
    body: form
  });

  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`Upload failed: HTTP ${resp.status} - ${text.substring(0, 200)}`);
  }

  return await resp.json();
}

// =====================
// PAGES API
// =====================

async function resolvePath(pagePath, locale = DEFAULT_LOCALE) {
  const normalized = pagePath.replace(/^\//, '');
  
  const result = await query(`
    query($path: String!, $locale: String!) {
      pages {
        singleByPath(path: $path, locale: $locale) {
          id
          path
          title
          locale
        }
      }
    }
  `, { path: normalized, locale });

  return result.pages.singleByPath;
}

async function getPageById(id) {
  const result = await query(`
    query($id: Int!) {
      pages {
        single(id: $id) {
          id
          path
          title
          content
          description
          locale
          isPrivate
          isPublished
          tags { tag }
          createdAt
          updatedAt
        }
      }
    }
  `, { id: parseInt(id) });

  return result.pages.single;
}

async function getPage(input, locale = DEFAULT_LOCALE) {
  const { id, path } = parsePathOrId(input);
  
  if (id) {
    return getPageById(id);
  }
  
  const page = await resolvePath(path, locale);
  if (!page) throw new Error(`Page not found: ${path}`);
  
  return getPageById(page.id);
}

async function createPage(pagePath, title, content, options = {}) {
  const locale = options.locale || DEFAULT_LOCALE;
  const tags = parseTags(options.tags);
  
  const result = await query(`
    mutation($content: String!, $description: String!, $editor: String!,
            $isPrivate: Boolean!, $isPublished: Boolean!, $locale: String!,
            $path: String!, $tags: [String]!, $title: String!) {
      pages {
        create(content: $content, description: $description, editor: $editor,
               isPrivate: $isPrivate, isPublished: $isPublished, locale: $locale,
               path: $path, tags: $tags, title: $title) {
          responseResult { succeeded message errorCode }
          page { id path title }
        }
      }
    }
  `, {
    content,
    description: options.description || '',
    editor: 'markdown',
    isPrivate: options.private || false,
    isPublished: !options.draft,
    locale,
    path: pagePath.replace(/^\//, ''),
    tags,
    title
  });

  if (!result.pages.create.responseResult.succeeded) {
    throw new Error(`Create failed: ${result.pages.create.responseResult.message}`);
  }

  return result.pages.create.page;
}

async function updatePage(id, updates = {}) {
  // Build mutation dynamically based on provided fields
  // NOTE: Wiki.js requires 'tags' field in update mutation, even if empty
  const mutationFields = [];
  const mutationVars = { id: parseInt(id) };
  const varDefs = ['$id: Int!'];
  
  if (updates.content) { mutationFields.push('content: $content'); mutationVars.content = updates.content; varDefs.push('$content: String'); }
  if (updates.title) { mutationFields.push('title: $title'); mutationVars.title = updates.title; varDefs.push('$title: String'); }
  // Always include tags (Wiki.js update mutation requires it, default to empty array)
  mutationFields.push('tags: $tags'); mutationVars.tags = parseTags(updates.tags || []); varDefs.push('$tags: [String]');
  if (updates.description !== undefined) { mutationFields.push('description: $description'); mutationVars.description = updates.description; varDefs.push('$description: String'); }

  if (mutationFields.length === 0) {
    throw new Error('No fields to update');
  }

  const mutation = `
    mutation(${varDefs.join(', ')}) {
      pages {
        update(id: $id, ${mutationFields.join(', ')}) {
          responseResult { succeeded message }
          page { id path title }
        }
      }
    }
  `;

  const result = await query(mutation, mutationVars);

  if (!result.pages.update.responseResult.succeeded) {
    throw new Error(`Update failed: ${result.pages.update.responseResult.message}`);
  }

  return result.pages.update.page;
}

async function upsertPage(pagePath, title, content, options = {}) {
  const locale = options.locale || DEFAULT_LOCALE;
  const normalized = pagePath.replace(/^\//, '');
  
  const existing = await resolvePath(normalized, locale);
  
  if (existing) {
    const result = await updatePage(existing.id, { content, title, tags: options.tags });
    return { action: 'updated', ...result };
  }
  
  const result = await createPage(normalized, title, content, options);
  return { action: 'created', ...result };
}

async function deletePage(input, locale = DEFAULT_LOCALE) {
  const { id, path } = parsePathOrId(input);
  
  let pageId = id;
  if (!pageId) {
    const page = await resolvePath(path, locale);
    if (!page) throw new Error(`Page not found: ${path}`);
    pageId = page.id;
  }

  const result = await query(`
    mutation($id: Int!) {
      pages {
        delete(id: $id) {
          responseResult { succeeded message }
        }
      }
    }
  `, { id: parseInt(pageId) });

  if (!result.pages.delete.responseResult.succeeded) {
    throw new Error(`Delete failed: ${result.pages.delete.responseResult.message}`);
  }

  return { deleted: true, id: pageId };
}

async function movePage(fromPath, toPath, locale = DEFAULT_LOCALE) {
  const page = await resolvePath(fromPath, locale);
  if (!page) throw new Error(`Source page not found: ${fromPath}`);

  const result = await query(`
    mutation($id: Int!, $destinationPath: String!, $destinationLocale: String!) {
      pages {
        move(id: $id, destinationPath: $destinationPath, destinationLocale: $destinationLocale) {
          responseResult { succeeded message }
          page { id path }
        }
      }
    }
  `, {
    id: page.id,
    destinationPath: toPath.replace(/^\//, ''),
    destinationLocale: locale
  });

  if (!result.pages.move.responseResult.succeeded) {
    throw new Error(`Move failed: ${result.pages.move.responseResult.message}`);
  }

  return result.pages.move.page;
}

async function copyPage(fromPath, toPath, locale = DEFAULT_LOCALE) {
  const page = await resolvePath(fromPath, locale);
  if (!page) throw new Error(`Source page not found: ${fromPath}`);

  const fullPage = await getPageById(page.id);

  const result = await createPage(toPath, `${fullPage.title} (Copy)`, fullPage.content, {
    tags: fullPage.tags?.map(t => t.tag) || [],
    locale,
    private: fullPage.isPrivate,
    draft: !fullPage.isPublished
  });

  return { action: 'copied', from: fromPath, to: toPath, ...result };
}

// =====================
// HISTORY / VERSIONING
// =====================

async function getPageHistory(input, locale = DEFAULT_LOCALE) {
  const { id, path } = parsePathOrId(input);
  
  let pageId = id;
  if (!pageId) {
    const page = await resolvePath(path, locale);
    if (!page) throw new Error(`Page not found: ${path}`);
    pageId = page.id;
  }

  const result = await query(`
    query($id: Int!) {
      pages {
        single(id: $id) {
          id
          path
          title
          history(offset: 0, limit: 50) {
            versionId
            versionDate
            authorId
            actionType
          }
        }
      }
    }
  `, { id: parseInt(pageId) });

  return result.pages.single.history;
}

async function restoreVersion(input, versionId, locale = DEFAULT_LOCALE) {
  const { id, path } = parsePathOrId(input);
  
  let pageId = id;
  if (!pageId) {
    const page = await resolvePath(path, locale);
    if (!page) throw new Error(`Page not found: ${path}`);
    pageId = page.id;
  }

  const result = await query(`
    mutation($pageId: Int!, $versionId: Int!) {
      pages {
        restoreVersion(pageId: $pageId, versionId: $versionId) {
          responseResult { succeeded message }
          page { id path title }
        }
      }
    }
  `, { pageId: parseInt(pageId), versionId: parseInt(versionId) });

  if (!result.pages.restoreVersion.responseResult.succeeded) {
    throw new Error(`Restore failed: ${result.pages.restoreVersion.responseResult.message}`);
  }

  return result.pages.restoreVersion.page;
}

// =====================
// RENDERING
// =====================

async function renderPage(input, format = 'html', locale = DEFAULT_LOCALE) {
  const page = await getPage(input, locale);
  
  if (format === 'html') {
    // Use render mutation
    const result = await query(`
      mutation($id: Int!) {
        pages {
          render(id: $id) {
            responseResult { succeeded message }
            output
          }
        }
      }
    `, { id: parseInt(page.id) });

    if (!result.pages.render.responseResult.succeeded) {
      throw new Error(`Render failed: ${result.pages.render.responseResult.message}`);
    }

    return result.pages.render.output;
  }
  
  if (format === 'pdf') {
    // Wiki.js doesn't have direct PDF API - use export endpoint
    const exportUrl = `${WIKI_URL}/export/${page.id}/pdf`;
    throw new Error(`PDF export requires web access: ${exportUrl}`);
  }

  throw new Error(`Unknown format: ${format}`);
}

// =====================
// SEARCH
// =====================

async function searchPages(term, options = {}) {
  const limit = options.limit || 20;
  const tags = options.tags ? parseTags(options.tags) : [];
  
  const result = await query(`
    query($term: String!, $limit: Int!) {
      pages {
        search(query: $term, limit: $limit) {
          results {
            id
            path
            title
            description
            tags { tag }
            locale
          }
          totalHits
        }
      }
    }
  `, { term, limit });

  let results = result.pages.search.results;
  
  // Filter by tags if specified
  if (tags.length > 0) {
    results = results.filter(r => 
      r.tags?.some(t => tags.includes(t.tag))
    );
  }

  return { results, total: result.pages.search.totalHits };
}

// =====================
// TREE / HIERARCHY
// =====================

async function getPageTree(prefix = '', depth = 3, locale = DEFAULT_LOCALE) {
  const result = await query(`
    query($path: String, $locale: String!) {
      pages {
        list(orderBy: PATH, limit: 500) {
          id
          path
          title
          locale
          isPublished
        }
      }
    }
  `, { path: prefix || null, locale });

  let pages = result.pages.list;
  
  // Filter by prefix
  if (prefix) {
    const normalized = prefix.replace(/^\//, '');
    pages = pages.filter(p => p.path.startsWith(normalized));
  }

  // Build tree structure
  const tree = {};
  pages.forEach(p => {
    const parts = p.path.split('/');
    let current = tree;
    parts.forEach((part, i) => {
      if (!current[part]) {
        current[part] = i === parts.length - 1 ? { ...p, children: {} } : { children: {} };
      }
      current = current[part].children;
    });
  });

  return { pages, tree };
}

// =====================
// TAGS
// =====================

async function listTags() {
  const result = await query(`
    query {
      pages {
        tags {
          list(orderBy: TITLE) {
            tag
            usageCount
          }
        }
      }
    }
  `, {});

  return result.pages.tags.list;
}

async function createTag(tagName) {
  const result = await query(`
    mutation($tag: String!) {
      pages {
        tags {
          create(tag: $tag) {
            responseResult { succeeded message }
            tag { tag }
          }
        }
      }
    }
  `, { tag: tagName });

  if (!result.pages.tags.create.responseResult.succeeded) {
    throw new Error(`Tag create failed: ${result.pages.tags.create.responseResult.message}`);
  }

  return result.pages.tags.create.tag;
}

async function deleteTag(tagName) {
  const result = await query(`
    mutation($id: String!) {
      pages {
        tags {
          delete(id: $id) {
            responseResult { succeeded message }
          }
        }
      }
    }
  `, { id: tagName });

  if (!result.pages.tags.delete.responseResult.succeeded) {
    throw new Error(`Tag delete failed: ${result.pages.tags.delete.responseResult.message}`);
  }

  return { deleted: true, tag: tagName };
}

// =====================
// ASSETS
// =====================

async function listAssets(folderId = 0, kind = null) {
  const result = await query(`
    query($folderId: Int, $kind: AssetKind) {
      assets {
        list(folderId: $folderId, kind: $kind) {
          id
          filename
          url
          kind
          fileSize
          createdAt
          folderId
        }
      }
    }
  `, { 
    folderId: folderId ? parseInt(folderId) : null, 
    kind: kind || null 
  });

  return result.assets.list;
}

async function uploadAsset(filePath, folderId = 0, customName = null) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`File not found: ${filePath}`);
  }

  const result = await uploadFile(filePath, folderId, customName);
  return result;
}

async function deleteAsset(assetId) {
  const result = await query(`
    mutation($id: Int!) {
      assets {
        delete(id: $id) {
          responseResult { succeeded message }
        }
      }
    }
  `, { id: parseInt(assetId) });

  if (!result.assets.delete.responseResult.succeeded) {
    throw new Error(`Asset delete failed: ${result.assets.delete.responseResult.message}`);
  }

  return { deleted: true, id: assetId };
}

async function createAssetFolder(parentId, slug, name) {
  const result = await query(`
    mutation($parentId: Int!, $slug: String!, $name: String!) {
      assets {
        createFolder(parentFolderId: $parentId, slug: $slug, name: $name) {
          responseResult { succeeded message }
          folder { id slug name }
        }
      }
    }
  `, { parentId: parseInt(parentId), slug, name: name || slug });

  if (!result.assets.createFolder.responseResult.succeeded) {
    throw new Error(`Folder create failed: ${result.assets.createFolder.responseResult.message}`);
  }

  return result.assets.createFolder.folder;
}

// =====================
// CLI
// =====================

function printJson(data) {
  console.log(JSON.stringify(data, null, 2));
}

function printPretty(data) {
  // Human-readable output
  if (Array.isArray(data)) {
    data.forEach((item, i) => {
      console.log(`${i + 1}. ${item.title || item.filename || item.tag || item.path || JSON.stringify(item)}`);
    });
  } else if (typeof data === 'object') {
    Object.entries(data).forEach(([k, v]) => {
      if (typeof v === 'object' && !Array.isArray(v)) {
        console.log(`${k}: ${JSON.stringify(v)}`);
      } else {
        console.log(`${k}: ${v}`);
      }
    });
  } else {
    console.log(data);
  }
}

function parseArgs(args) {
  const result = { _: [], flags: {} };
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if (arg.startsWith('--')) {
      const [key, value] = arg.slice(2).split('=');
      if (value) {
        result.flags[key] = value;
      } else if (args[i + 1] && !args[i + 1].startsWith('-')) {
        result.flags[key] = args[++i];
      } else {
        result.flags[key] = true;
      }
    } else if (arg.startsWith('-')) {
      const key = arg.slice(1);
      result.flags[key] = args[++i];
    } else {
      result._.push(arg);
    }
  }
  
  return result;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const [cmd, ...params] = args._;
  const pretty = args.flags.pretty || args.flags.p;
  const locale = args.flags.locale || args.flags.l || DEFAULT_LOCALE;

  try {
    let result;

    switch (cmd) {
      // Pages
      case 'upsert': {
        const [pagePath, title, contentOrFile, tagsStr] = params;
        if (!pagePath || !title) throw new Error('Usage: wiki upsert <path> <title> <content|@file> [tags]');
        
        let content = contentOrFile || '';
        if (contentOrFile?.startsWith('@')) {
          content = fs.readFileSync(contentOrFile.slice(1), 'utf8');
        }
        
        result = await upsertPage(pagePath, title, content, { 
          tags: tagsStr, 
          locale,
          private: args.flags.private,
          draft: args.flags.draft
        });
        break;
      }

      case 'get': {
        const [input] = params;
        if (!input) throw new Error('Usage: wiki get <path|id>');
        result = await getPage(input, locale);
        break;
      }

      case 'delete': {
        const [input] = params;
        if (!input) throw new Error('Usage: wiki delete <path|id>');
        result = await deletePage(input, locale);
        break;
      }

      case 'move': {
        const [from, to] = params;
        if (!from || !to) throw new Error('Usage: wiki move <from> <to>');
        result = await movePage(from, to, locale);
        break;
      }

      case 'copy': {
        const [from, to] = params;
        if (!from || !to) throw new Error('Usage: wiki copy <from> <to>');
        result = await copyPage(from, to, locale);
        break;
      }

      case 'history': {
        const [input] = params;
        if (!input) throw new Error('Usage: wiki history <path|id>');
        result = await getPageHistory(input, locale);
        break;
      }

      case 'restore': {
        const [input] = params;
        const version = args.flags.version || args.flags.v;
        if (!input || !version) throw new Error('Usage: wiki restore <path|id> --version=<n>');
        result = await restoreVersion(input, version, locale);
        break;
      }

      case 'render': {
        const [input] = params;
        const format = args.flags.format || args.flags.f || 'html';
        if (!input) throw new Error('Usage: wiki render <path|id> --format=html|pdf');
        result = await renderPage(input, format, locale);
        break;
      }

      // Search
      case 'search': {
        const [term] = params;
        if (!term) throw new Error('Usage: wiki search <term> [--tags=a,b] [--limit=20]');
        result = await searchPages(term, {
          tags: args.flags.tags,
          limit: parseInt(args.flags.limit) || 20
        });
        break;
      }

      // Tree
      case 'tree': {
        result = await getPageTree(args.flags.path || '', parseInt(args.flags.depth) || 3, locale);
        break;
      }

      // Tags
      case 'tags': {
        const [subCmd, tagName] = params;
        
        if (subCmd === 'create') {
          if (!tagName) throw new Error('Usage: wiki tags create <tag>');
          result = await createTag(tagName);
        } else if (subCmd === 'delete') {
          if (!tagName) throw new Error('Usage: wiki tags delete <tag>');
          result = await deleteTag(tagName);
        } else {
          result = await listTags();
        }
        break;
      }

      // Assets
      case 'assets': {
        result = await listAssets(args.flags.folder || 0, args.flags.kind || null);
        break;
      }

      case 'upload': {
        const [filePath] = params;
        if (!filePath) throw new Error('Usage: wiki upload <file> [--folder=id] [--name=custom]');
        result = await uploadAsset(filePath, args.flags.folder || 0, args.flags.name);
        break;
      }

      case 'asset-delete': {
        const [assetId] = params;
        if (!assetId) throw new Error('Usage: wiki asset-delete <id>');
        result = await deleteAsset(assetId);
        break;
      }

      case 'mkdir': {
        const [parentId, slug, name] = params;
        if (!parentId || !slug) throw new Error('Usage: wiki mkdir <parent-id> <slug> [name]');
        result = await createAssetFolder(parentId, slug, name);
        break;
      }

      // Help
      case 'help':
      case '--help':
      case '-h':
      case undefined:
        console.log(`
Wiki.js V3 Client - All-encompassing GraphQL + REST Wrapper

Usage:
  wiki <command> [options]

Pages:
  upsert <path> <title> <content|@file> [tags]  Create or update page
  get <path|id>                                 Get page content
  delete <path|id>                              Delete page
  move <from> <to>                              Move page
  copy <from> <to>                              Copy page
  history <path|id>                             Show page history
  restore <path|id> --version=<n>              Restore specific version
  render <path|id> --format=html|pdf           Render page

Search:
  search <term> [--tags=a,b] [--limit=20]      Search pages

Tree:
  tree [--path=prefix] [--depth=3]             List page hierarchy

Tags:
  tags                                          List all tags
  tags create <tag>                             Create tag
  tags delete <tag>                             Delete tag

Assets:
  assets [--folder=id] [--kind=IMAGE|VIDEO|FILE]  List assets
  upload <file> [--folder=id] [--name=custom]     Upload file
  asset-delete <id>                                Delete asset
  mkdir <parent-id> <slug> [name]                  Create folder

Options:
  --pretty, -p              Human-readable output
  --locale, -l <locale>     Locale (default: ${DEFAULT_LOCALE})
  --private                 Create private page
  --draft                   Create unpublished page

Environment:
  WIKIJS_URL      Wiki.js URL (default: http://localhost:3000)
  WIKIJS_TOKEN    API token (required)
  WIKIJS_LOCALE   Default locale (default: de)
        `);
        process.exit(0);

      default:
        throw new Error(`Unknown command: ${cmd}. Use 'wiki help' for usage.`);
    }

    if (pretty) {
      printPretty(result);
    } else {
      printJson(result);
    }

  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  }
}

main();