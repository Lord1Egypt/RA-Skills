#!/usr/bin/env node
// 发布状态自检：仓库布局、frontmatter 要素、skills.sh 索引、clawhub 下载量。
//
//   node check.mjs <owner/repo> [skill-name]
//
// skill-name 省略时取仓库名。全部走公开 HTTP 接口，不读本地，换机器也能用。

const [repoArg, skillArg] = process.argv.slice(2);

if (!repoArg || !repoArg.includes('/')) {
  console.error('用法：node check.mjs <owner/repo> [skill-name]');
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
  console.log('\n=== 仓库 ===');
  const meta = await getJson(`https://api.github.com/repos/${owner}/${repo}`);
  console.log(`  ${meta.full_name}  ${meta.private ? '私有' : '公开'}  分支 ${meta.default_branch}  ★${meta.stargazers_count}`);
  if (meta.private) console.log(bad('私有仓库无法被任何目录收录'));
  return meta.default_branch;
}

async function checkLayout(branch) {
  console.log('\n=== 布局 ===');
  const base = `https://api.github.com/repos/${owner}/${repo}/contents`;
  const root = await getJson(`${base}?ref=${branch}`);
  const names = root.map((x) => x.name);

  if (!names.includes('skills')) {
    console.log(bad('根目录没有 skills/'));
    if (names.includes('SKILL.md')) {
      console.log(info('根目录有 SKILL.md，部分扫描逻辑会提前返回，导致子目录的 skill 扫不到'));
      console.log(info('改成 skills/<name>/SKILL.md'));
    }
    return false;
  }

  const dirs = await getJson(`${base}/skills?ref=${branch}`);
  const targets = dirs.filter((d) => d.type === 'dir').map((d) => d.name);
  if (!targets.includes(skill)) {
    console.log(bad(`skills/ 下没有 ${skill}/`));
    console.log(info('现有：' + (targets.join(', ') || '(空)')));
    return false;
  }

  const files = await getJson(`${base}/skills/${skill}?ref=${branch}`);
  const hasSkillMd = files.some((f) => f.name === 'SKILL.md');
  console.log(hasSkillMd ? ok(`skills/${skill}/SKILL.md`) : bad(`skills/${skill}/ 下没有 SKILL.md`));
  return hasSkillMd;
}

async function checkFrontmatter(branch) {
  console.log('\n=== frontmatter ===');
  const url = `https://raw.githubusercontent.com/${owner}/${repo}/${branch}/skills/${skill}/SKILL.md`;
  const r = await fetch(url);
  if (!r.ok) {
    console.log(bad('取不到 SKILL.md'));
    return;
  }
  const text = await r.text();
  const m = text.match(/^---\n([\s\S]*?)\n---/);
  if (!m) {
    console.log(bad('没有 frontmatter 块'));
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

  console.log(name === skill ? ok(`name: ${name}（与目录名一致）`) : bad(`name: ${name || '(缺失)'}，应等于目录名 ${skill}`));
  if (desc) {
    const head = desc.slice(0, 40);
    console.log(desc.length > 20 ? ok(`description: ${head}…`) : bad('description 太短'));
    if (desc.length > 400) console.log(info(`描述 ${desc.length} 字，偏长，前 30 字才是 agent 最先读到的`));
  } else {
    console.log(bad('缺 description'));
  }
  console.log(license ? ok(`license: ${license}`) : bad('缺 license，clawhub 会拒收'));
}

async function checkSkillsSh() {
  console.log('\n=== skills.sh ===');
  try {
    const j = await getJson(`https://www.skills.sh/api/search?q=${encodeURIComponent(skill)}`);
    const hit = (j.skills || []).find((s) => s.id === `${owner}/${repo}/${skill}` || s.skillId === skill);
    if (hit) {
      console.log(ok(`已收录  ${hit.installs || 0} 次安装`));
      console.log(info(`https://www.skills.sh/${hit.id}`));
    } else {
      console.log(bad(`未收录（搜索结果 ${j.count || 0} 条）`));
      console.log(info('检查环境：env | grep -i disable_telemetry'));
      console.log(info('值哪怕是 0 也会关闭遥测，要用 DISABLE_TELEMETRY= 覆盖成空'));
    }
  } catch (e) {
    console.log(bad('查询失败：' + e.message));
  }
}

async function checkClawhub() {
  console.log('\n=== clawhub ===');
  try {
    const j = await getJson(`https://clawhub.ai/api/search?q=${encodeURIComponent(skill)}`);
    const hit = (j.results || []).find((r) => r.displayName === skill);
    if (hit) {
      console.log(ok(`已发布  ${hit.downloads} 次下载`));
      console.log(info(`https://clawhub.ai${hit.canonicalUrl}`));
      console.log(info(`安装：openclaw skills install @${owner}/${skill}`));
    } else {
      console.log(bad('未找到'));
      console.log(info('发布：npx clawhub skill publish ./skills/' + skill + ' --slug ' + skill + ' --version 0.1.0'));
    }
  } catch (e) {
    console.log(bad('查询失败：' + e.message));
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
