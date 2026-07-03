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

function localDate(timeZone) {
  const parts = new Intl.DateTimeFormat('en-CA', { timeZone, year: 'numeric', month: '2-digit', day: '2-digit' }).formatToParts(new Date());
  const get = (type) => parts.find((p) => p.type === type)?.value;
  return `${get('year')}-${get('month')}-${get('day')}`;
}

function die(reason, details = {}) {
  console.error(JSON.stringify({ ok: false, reason, ...details }, null, 2));
  process.exit(2);
}

const args = parseArgs(process.argv);
const env = readEnvFile(args.get('env-file'));
const apiBase = args.get('api-base') || env.WORDPRESS_API_BASE;
const username = args.get('username') || env.WORDPRESS_USERNAME;
const password = args.get('application-password') || env.WORDPRESS_APPLICATION_PASSWORD || env.WORDPRESS_APP_PASSWORD;
const auth = username && password ? 'Basic ' + Buffer.from(`${username}:${password}`).toString('base64') : null;

if (!apiBase && !args.get('url')) die('missing_wordpress_api_base');

async function wp(path) {
  const res = await fetch(`${apiBase}${path}`, { headers: auth ? { Authorization: auth } : {} });
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

let post = null;
if (args.get('id')) {
  post = await wp(`/posts/${encodeURIComponent(args.get('id'))}?_fields=id,date,link,status,title,author,categories`);
} else if (args.get('date')) {
  const date = args.get('date');
  const posts = await wp('/posts?per_page=10&status=publish&_fields=id,date,link,status,title,author,categories');
  post = posts.find((item) => String(item.date || '').startsWith(date));
  if (!post) die('no_published_post_for_date', { date, latest: posts[0] ? { id: posts[0].id, date: posts[0].date, link: posts[0].link, title: posts[0].title?.rendered } : null });
} else if (!args.get('url')) {
  const timeZone = args.get('tz') || 'UTC';
  const date = localDate(timeZone);
  const posts = await wp('/posts?per_page=10&status=publish&_fields=id,date,link,status,title,author,categories');
  post = posts.find((item) => String(item.date || '').startsWith(date));
  if (!post) die('no_published_post_for_local_date', { date, timeZone });
}

const url = args.get('url') || post.link;
const publicRes = await fetch(url, { method: 'GET' });
const ok = publicRes.status === 200 && (!post || post.status === 'publish');
console.log(JSON.stringify({ ok, id: post?.id, date: post?.date, status: post?.status, title: post?.title?.rendered, link: url, publicStatus: publicRes.status }, null, 2));
if (!ok) process.exit(2);
