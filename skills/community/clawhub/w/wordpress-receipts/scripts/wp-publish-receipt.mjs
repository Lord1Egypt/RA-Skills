#!/usr/bin/env node
import fs from 'node:fs';

function parseArgs(argv) {
  const args = new Map();
  for (let i = 2; i < argv.length; i += 1) {
    const key = argv[i];
    if (!key.startsWith('--')) continue;
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) args.set(key.slice(2), 'true');
    else {
      args.set(key.slice(2), next);
      i += 1;
    }
  }
  return args;
}

function readEnvFile(file) {
  const env = {};
  if (!file) return env;
  for (const line of fs.readFileSync(file, 'utf8').split(/\r?\n/)) {
    if (!line.trim() || line.trim().startsWith('#')) continue;
    const i = line.indexOf('=');
    if (i < 0) continue;
    env[line.slice(0, i).trim()] = line.slice(i + 1).trim().replace(/^["']|["']$/g, '');
  }
  return env;
}

function value(args, env, key, fallback) {
  const flag = key.toLowerCase().replaceAll('_', '-');
  return args.get(flag) || env[key] || fallback;
}

function stripHtml(text) {
  return String(text || '').replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').trim();
}

function die(reason, details = {}) {
  console.error(JSON.stringify({ ok: false, reason, ...details }, null, 2));
  process.exit(2);
}

const args = parseArgs(process.argv);
const env = readEnvFile(args.get('env-file'));
const apiBase = value(args, env, 'WORDPRESS_API_BASE');
const username = value(args, env, 'WORDPRESS_USERNAME');
const password = value(args, env, 'WORDPRESS_APPLICATION_PASSWORD') || value(args, env, 'WORDPRESS_APP_PASSWORD');
const author = Number(args.get('author') || env.WORDPRESS_AUTHOR_ID || 0) || undefined;
const category = Number(args.get('category') || env.WORDPRESS_DEFAULT_CATEGORY_ID || 0) || undefined;
const title = args.get('title') || (args.get('title-file') ? fs.readFileSync(args.get('title-file'), 'utf8').trim() : '');
const content = args.get('content') || (args.get('content-file') ? fs.readFileSync(args.get('content-file'), 'utf8') : '');

if (!apiBase) die('missing_wordpress_api_base');
if (!username) die('missing_wordpress_username');
if (!password) die('missing_wordpress_application_password');
if (!title) die('missing_title');
if (!content) die('missing_content');

const auth = 'Basic ' + Buffer.from(`${username}:${password}`).toString('base64');

async function wp(path, options = {}) {
  const res = await fetch(`${apiBase}${path}`, {
    ...options,
    headers: {
      Authorization: auth,
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
  });
  const text = await res.text();
  let json = null;
  try {
    json = text ? JSON.parse(text) : null;
  } catch {
    json = { raw: text };
  }
  if (!res.ok) die('wordpress_api_error', { status: res.status, message: json?.message || json?.code || text.slice(0, 300) });
  return json;
}

const recent = await wp(`/posts?search=${encodeURIComponent(title)}&per_page=5&status=publish&_fields=id,date,link,status,title`);
const duplicate = recent.find((post) => stripHtml(post.title?.rendered) === title);
if (duplicate && args.get('allow-duplicate') !== 'true') {
  const publicRes = await fetch(duplicate.link, { method: 'GET' });
  console.log(JSON.stringify({ ok: true, action: 'duplicate-skip', id: duplicate.id, status: duplicate.status, title, link: duplicate.link, publicStatus: publicRes.status }, null, 2));
  process.exit(publicRes.status === 200 ? 0 : 2);
}

const payload = {
  title,
  content,
  status: args.get('status') || 'publish',
  comment_status: args.get('comment-status') || 'closed',
  ping_status: args.get('ping-status') || 'closed',
};
if (author) payload.author = author;
if (category) payload.categories = [category];

const post = await wp('/posts', { method: 'POST', body: JSON.stringify(payload) });
const verified = await wp(`/posts/${post.id}?context=edit&_fields=id,status,link,author,categories,title`);
const publicRes = await fetch(post.link, { method: 'GET' });
const ok = verified.status === payload.status && publicRes.status === 200;
console.log(JSON.stringify({ ok, action: 'published', id: post.id, status: verified.status, author: verified.author, categories: verified.categories, title, link: post.link, publicStatus: publicRes.status }, null, 2));
if (!ok) process.exit(2);
