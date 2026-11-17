#!/usr/bin/env node
// 名字可用性与候选生成。
//
//   node name-check.mjs <name> [更多候选...] [--owner <账号>]
//   node name-check.mjs --suggest "export chat history" [--owner <账号>]
//
// 检查模式：在 skills.sh、clawhub、GitHub 三处看候选名占用，判定 干净 / 拥挤 / 撞名。
// 建议模式：给一句描述，生成候选名并逐个检查，按可用度排序。
//
// 判定依据是撞名与命中密度。名字太泛会沉底，因为 clawhub 的搜索只匹配 displayName，
// skills.sh 的模糊搜索里同词越多，单个 skill 越难被点到。

const argv = process.argv.slice(2);
let selfOwner = '';
let suggestFrom = '';
const names = [];
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === '--owner') selfOwner = argv[++i] || '';
  else if (argv[i] === '--suggest') suggestFrom = argv[++i] || '';
  else names.push(argv[i]);
}

if (suggestFrom) names.push(...candidatesFrom(suggestFrom));
else if (!names.length) {
  console.error(
    '用法：\n' +
      '  node name-check.mjs <name> [更多候选...] [--owner <账号>]\n' +
      '  node name-check.mjs --suggest "<功能描述>" [--owner <账号>]'
  );
  process.exit(2);
}


import { execFileSync } from 'node:child_process';
import { t } from './lib-i18n.mjs';

const C = {
  ok: (s) => `\x1b[32m✓\x1b[0m ${s}`,
  warn: (s) => `\x1b[33m!\x1b[0m ${s}`,
  bad: (s) => `\x1b[31m✗\x1b[0m ${s}`,
  dim: (s) => `\x1b[2m${s}\x1b[0m`,
};

// 从描述里出候选名。三种形态：动词+宾语、宾语+动词、加限定词。
function candidatesFrom(text) {
  // 描述里的每个名词都当一次核心词，因为哪个是主语需要语义判断，脚本猜不准。
  // 只生成说得通的组合：核心词+动作、动作+核心词、修饰+核心词。
  const VERBS = ['export', 'backup', 'archive', 'publish', 'sync', 'search', 'reader', 'writer'];
  const words = String(text)
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, ' ')
    .split(/[\s-]+/)
    .filter((w) => w && w.length > 2 && !VERBS.includes(w) && !['the', 'and', 'for', 'from', 'with', 'into', 'all'].includes(w));
  const uniq = [...new Set(words)];
  if (!uniq.length) return [];

  const out = new Set();
  for (const core of uniq) {
    for (const v of VERBS) {
      out.add(core + '-' + v);
      out.add(v + '-' + core);
    }
    // 相邻修饰词 + 核心
    const idx = uniq.indexOf(core);
    if (idx > 0) out.add(uniq[idx - 1] + '-' + core);
    if (idx < uniq.length - 1) out.add(core + '-' + uniq[idx + 1]);
  }
  return [...out].filter((n) => n.length <= 32).slice(0, 12);
}

async function getJson(url) {
  const r = await fetch(url, { headers: { 'User-Agent': 'skill-registry-publish' } });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}

// skills.sh：模糊搜索，count 大说明这个词在生态里被大量使用，检索时会沉底
async function checkSkillsSh(name) {
  try {
    const j = await getJson(`https://www.skills.sh/api/search?q=${encodeURIComponent(name)}`);
    const list = j.skills || [];
    const exact = list.filter((s) => s.skillId === name || s.name === name);
    return { count: j.count || 0, exact, sample: list.slice(0, 3).map((s) => s.id) };
  } catch (e) {
    return { error: e.message };
  }
}

// clawhub：只匹配 displayName，有精确同名就是硬撞车
async function checkClawhub(name) {
  try {
    const j = await getJson(`https://clawhub.ai/api/search?q=${encodeURIComponent(name)}`);
    const list = j.results || [];
    const mine = (r) => selfOwner && String(r.install && r.install.reference || '').startsWith(selfOwner + '/');
    const exact = list.filter((r) => r.displayName === name && !mine(r));
    const own = list.filter((r) => r.displayName === name && mine(r));
    return { count: list.length, exact, own };
  } catch (e) {
    return { error: e.message };
  }
}

// GitHub：同名仓库多说明这个名字在别的语境里已被占用。
// 未认证的公开 API 限流是 10 次/分钟，批量查候选会撞上限，所以优先用 gh（带 token）。
async function checkGithub(name) {
  const q = `${encodeURIComponent('"' + name + '"')}+in:name&per_page=30`;
  try {
    const out = execFileSync('gh', ['api', `search/repositories?q=${q}`], {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
      timeout: 15000,
    });
    const j = JSON.parse(out);
    const exact = (j.items || []).filter((r) => r.name === name && !(selfOwner && r.owner.login === selfOwner));
    return { total: j.total_count || 0, exact: exact.map((r) => r.full_name) };
  } catch {
    // gh 不可用或未登录，退回公开接口
  }
  try {
    const r = await fetch(`https://api.github.com/search/repositories?q=${q}`, {
      headers: { 'User-Agent': 'skill-registry-publish' },
    });
    if (r.status === 403) return { error: '限流（未认证 10 次/分钟），用 gh 登录或稍后重试' };
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const j = await r.json();
    const exact = (j.items || []).filter((x) => x.name === name && !(selfOwner && x.owner.login === selfOwner));
    return { total: j.total_count || 0, exact: exact.map((x) => x.full_name) };
  } catch (e) {
    return { error: e.message };
  }
}

function verdict(ss, ch, gh) {
  if (ss.error || ch.error || gh.error) return { level: 'warn', text: t('部分查询失败，重跑一次', 'some queries failed, rerun') };
  // 只有 skill 生态里的同名才算硬撞车。GitHub 上不同领域的同名仓库很多，不构成冲突
  if (ch.exact.length) return { level: 'bad', text: t(`clawhub 已被占用：${ch.exact.map((x) => x.install && x.install.reference).join(', ')}`, `taken on clawhub: ${ch.exact.map((x) => x.install && x.install.reference).join(', ')}`) };
  if (ss.exact.length) return { level: 'bad', text: t(`skills.sh 有同名 skill：${ss.exact.map((x) => x.id).slice(0, 3).join(', ')}`, `same-name skill on skills.sh: ${ss.exact.map((x) => x.id).slice(0, 3).join(', ')}`) };
  // 没有同名时看密度：同词越多，用户搜的时候越难点到你
  if (ss.count > 50 || gh.total > 200) return { level: 'warn', text: t(`太泛（skills.sh ${ss.count} 条，GitHub ${gh.total} 个）`, `too generic (${ss.count} hits on skills.sh, ${gh.total} repos on GitHub)`) };
  if (ss.count > 10 || gh.total > 50) return { level: 'warn', text: t(`略拥挤（skills.sh ${ss.count} 条，GitHub ${gh.total} 个）`, `crowded (${ss.count} hits on skills.sh, ${gh.total} repos on GitHub)`) };
  return { level: 'ok', text: t('干净', 'clean') };
}

const results = [];

for (const name of names) {
  console.log(`\n=== ${name} ===`);
  if (results.length) await new Promise((r) => setTimeout(r, 250));
  const [ss, ch, gh] = await Promise.all([checkSkillsSh(name), checkClawhub(name), checkGithub(name)]);

  if (ss.error) console.log(C.bad(`skills.sh 查询失败：${ss.error}`));
  else {
    const tag = ss.exact.length ? C.bad(t('有同名', 'collision')) : ss.count > 50 ? C.warn(t('太泛', 'too generic')) : C.ok(t('无同名', 'no collision'));
    console.log(`skills.sh  ${String(ss.count).padStart(4)} ${t('条', 'hits')}  ${tag}`);
    if (ss.sample.length) console.log(C.dim('            ' + ss.sample.join(', ')));
  }

  if (ch.error) console.log(C.bad(`clawhub 查询失败：${ch.error}`));
  else {
    const ownNote = ch.own && ch.own.length ? C.dim(t('（自己已发布，不算占用）', ' (yours, not a conflict)')) : '';
    console.log(`clawhub    ${ch.exact.length ? C.bad(t('已占用', 'taken')) : C.ok(t('未占用', 'free'))} ${ownNote}`);
  }

  if (gh.error) console.log(C.bad(`GitHub 查询失败：${gh.error}`));
  else {
    console.log(`GitHub     ${String(gh.total).padStart(4)} ${t('个同名仓库', 'repos')}  ${gh.exact.length ? C.warn(t('存在同名', 'same-name repos exist')) : C.ok(t('无同名', 'no collision'))}`);
    if (gh.exact.length) console.log(C.dim('            ' + gh.exact.join(', ')));
  }

  const v = verdict(ss, ch, gh);
  const mark = v.level === 'ok' ? C.ok(v.text) : v.level === 'warn' ? C.warn(v.text) : C.bad(v.text);
  console.log(`${t('判定：', 'Verdict: ')}${mark}`);
  results.push({
    name,
    level: v.level,
    score: v.level === 'ok' ? 0 : v.level === 'warn' ? 1 : 2,
    hits: ss.count || 0,
    gh: gh.total || 0,
  });
}

if (results.length > 1) {
  // 按可用度排序：干净在前，撞名在后；同档看 skills.sh 命中数
  const sorted = [...results].sort((a, b) => a.score - b.score || a.hits - b.hits);
  console.log('\n=== 排序 ===');
  for (const r of sorted) {
    const mark = r.score === 0 ? C.ok(t('干净', 'clean')) : r.score === 1 ? C.warn(t('拥挤', 'crowded')) : C.bad(t('撞名', 'taken'));
    console.log(`  ${mark.padEnd(14)} ${r.name.padEnd(26)} skills.sh ${String(r.hits).padStart(4)} ${t('条', 'hits')}  GitHub ${String(r.gh).padStart(4)}`);
  }
  const clean = sorted.filter((r) => r.score === 0);
  if (clean.length) console.log('\n' + t('建议：', 'Pick: ') + clean.slice(0, 2).map((r) => r.name).join(t(' 或 ', ' or ')));
  else console.log(t('\n没有干净候选，换一组词再试，或者接受最靠前的那个。', '\nNo clean candidate. Try another word set, or take the top one.'));
  console.log(C.dim(t('高频词（export、publish、registry）能带来检索命中，但同词太多反而沉底。', 'High-frequency words (export, publish, registry) aid retrieval until the term gets crowded.')));
}
console.log('');
