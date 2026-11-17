#!/usr/bin/env node
// 发布状态自检：仓库布局、frontmatter 要素、skills.sh 索引、clawhub 下载量。
//
//   node check.mjs <owner/repo> [skill-name]
//
// skill-name 省略时取仓库名。全部走公开 HTTP 接口，不读本地，换机器也能用。
import { t } from './lib-i18n.mjs';

const [repoArg, skillArg] = process.argv.slice(2);

if (!repoArg || !repoArg.includes('/')) {
  console.error(t('用法：node check.mjs <owner/repo> [skill-name]', 'Usage: node check.mjs <owner/repo> [skill-name]'));
  process.exit(2);
}

const [owner, repo] = repoArg.split('/');
const skill = skillArg || repo;

const ok = (s) => `  \x1b[32m✓\x1b[0m ${s}`;
const bad = (s) => `  \x1b[31m✗\x1b[0m ${s}`;
const info = (s) => `  · ${s}`;

async function getJson(url) {
  const r = await fetch(url, { headers: { 'User-Agent': 'ship-skill-check' } });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}

async function checkRepo() {
  console.log(`\n=== ${t('仓库','Repository')} ===`);
  const meta = await getJson(`https://api.github.com/repos/${owner}/${repo}`);
  console.log(`  ${meta.full_name}  ${meta.private ? t('私有','private') : t('公开','public')}  ${t('分支','branch')} ${meta.default_branch}  ★${meta.stargazers_count}`);
  if (meta.private) console.log(bad(t('私有仓库无法被任何目录收录','Private repos cannot be indexed by any directory')));
  return meta.default_branch;
}

async function checkLayout(branch) {
  console.log(`\n=== ${t('布局','Layout')} ===`);
  const base = `https://api.github.com/repos/${owner}/${repo}/contents`;
  const root = await getJson(`${base}?ref=${branch}`);
  const names = root.map((x) => x.name);

  if (!names.includes('skills')) {
    console.log(bad(t('根目录没有 skills/','No skills/ directory at repo root')));
    if (names.includes('SKILL.md')) {
      console.log(info(t('根目录有 SKILL.md，部分扫描逻辑会提前返回，导致子目录的 skill 扫不到','Root SKILL.md makes some scanners return early, hiding skills in subdirectories')));
      console.log(info(t('改成 skills/<name>/SKILL.md','Move it to skills/<name>/SKILL.md')));
    }
    return false;
  }

  const dirs = await getJson(`${base}/skills?ref=${branch}`);
  const targets = dirs.filter((d) => d.type === 'dir').map((d) => d.name);
  if (!targets.includes(skill)) {
    console.log(bad(t(`skills/ 下没有 ${skill}/`, `No ${skill}/ under skills/`)));
    console.log(info(t('现有：','Existing: ') + (targets.join(', ') || t('(空)','(none)'))));
    return false;
  }

  const files = await getJson(`${base}/skills/${skill}?ref=${branch}`);
  const hasSkillMd = files.some((f) => f.name === 'SKILL.md');
  console.log(hasSkillMd ? ok(`skills/${skill}/SKILL.md`) : bad(t(`skills/${skill}/ 下没有 SKILL.md`, `No SKILL.md in skills/${skill}/`)));
  return hasSkillMd;
}

async function checkFrontmatter(branch) {
  console.log(`\n=== frontmatter ===`);
  const url = `https://raw.githubusercontent.com/${owner}/${repo}/${branch}/skills/${skill}/SKILL.md`;
  const r = await fetch(url);
  if (!r.ok) {
    console.log(bad(t('取不到 SKILL.md','Cannot fetch SKILL.md')));
    return;
  }
  const text = await r.text();
  const m = text.match(/^---\n([\s\S]*?)\n---/);
  if (!m) {
    console.log(bad(t('没有 frontmatter 块','No frontmatter block')));
    return;
  }
  const fm = m[1];
  const field = (k) => {
    const line = fm.split('\n').find((l) => l.startsWith(k + ':'));
    return line ? line.slice(k.length + 1).trim() : '';
  };

  const name = field('name');
  const desc = field('description');
  const license = field('license');

  console.log(name === skill ? ok(t(`name: ${name}（与目录名一致）`, `name: ${name} (matches directory)`)) : bad(t(`name: ${name || '(缺失)'}，应等于目录名 ${skill}`, `name: ${name || '(missing)'} should equal directory ${skill}`)));
  if (desc) {
    const head = desc.slice(0, 40);
    console.log(desc.length > 20 ? ok(`description: ${head}…`) : bad(t('description 太短','description too short')));
    if (desc.length > 400) console.log(info(t(`描述 ${desc.length} 字，偏长，前 30 字才是 agent 最先读到的`, `description is ${desc.length} chars, long; agents read the first 30 first`)));
  } else {
    console.log(bad(t('缺 description','description missing')));
  }
  console.log(license ? ok(`license: ${license}`) : bad(t('缺 license，clawhub 会拒收','license missing, clawhub rejects it')));
}

async function checkSkillsSh() {
  console.log(`\n=== skills.sh ===`);
  try {
    const j = await getJson(`https://www.skills.sh/api/search?q=${encodeURIComponent(skill)}`);
    const hit = (j.skills || []).find((s) => s.id === `${owner}/${repo}/${skill}` || s.skillId === skill);
    if (hit) {
      console.log(ok(t(`已收录  ${hit.installs || 0} 次安装`, `indexed, ${hit.installs || 0} installs`)));
      console.log(info(`https://www.skills.sh/${hit.id}`));
    } else {
      console.log(bad(t(`未收录（搜索结果 ${j.count || 0} 条）`, `not indexed (${j.count || 0} results)`)));
      console.log(info(t('检查环境：env | grep -i disable_telemetry', 'check env: env | grep -i disable_telemetry')));
      console.log(info('值哪怕是 0 也会关闭遥测，要用 DISABLE_TELEMETRY= 覆盖成空'));
    }
  } catch (e) {
    console.log(bad(t('查询失败：','query failed: ') + e.message));
  }
}

async function checkClawhub() {
  console.log(`\n=== clawhub ===`);
  try {
    const j = await getJson(`https://clawhub.ai/api/search?q=${encodeURIComponent(skill)}`);
    const hit = (j.results || []).find((r) => r.displayName === skill);
    if (hit) {
      console.log(ok(t(`已发布  ${hit.downloads} 次下载`, `published, ${hit.downloads} downloads`)));
      console.log(info(`https://clawhub.ai${hit.canonicalUrl}`));
      console.log(info(t('安装：','install: ') + `openclaw skills install @${owner}/${skill}`));
    } else {
      console.log(bad(t('未找到', 'not found')));
      console.log(info(t('发布：','publish: ') + 'npx clawhub skill publish ./skills/' + skill + ' --slug ' + skill + ' --version 0.1.0'));
    }
  } catch (e) {
    console.log(bad(t('查询失败：','query failed: ') + e.message));
  }
}

try {
  const branch = await checkRepo();
  const layoutOk = await checkLayout(branch);
  if (layoutOk) await checkFrontmatter(branch);
  await checkSkillsSh();
  await checkClawhub();
  console.log('');
} catch (e) {
  console.error('检查中断：' + e.message);
  process.exit(1);
}
