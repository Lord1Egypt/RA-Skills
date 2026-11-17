#!/usr/bin/env node
/**
 * install_skills.mjs — 吸星大法 / Skill Consolidator 安装器（可选，手动执行）
 *
 * 把整个 skill 包目录（含 scripts/）复制到各 Agent 的 skills 目录。
 * 替代旧版 package.json 中自动执行的 postinstall（副作用过强、且只复制了 SKILL.md）。
 * 现在改为显式手动运行，默认用户级安装。
 *
 * 用法：
 *   node skill-consolidator/scripts/install_skills.mjs
 *   node skill-consolidator/scripts/install_skills.mjs --agents claude,cursor
 *   node skill-consolidator/scripts/install_skills.mjs --project      # 安装到当前项目
 *   node skill-consolidator/scripts/install_skills.mjs --source ./skill-consolidator
 */
import { cpSync, existsSync, mkdirSync, copyFileSync, rmSync } from 'node:fs';
import { join, resolve, basename } from 'node:path';
import { homedir } from 'node:os';

const HOME = homedir();
const args = process.argv.slice(2);
const getArg = (name) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : undefined;
};
const hasFlag = (name) => args.includes(name);

const SOURCE = resolve(getArg('--source') ?? 'skill-consolidator');
const AGENTS = (getArg('--agents') ?? 'workbuddy,claude,cursor,trae').split(',').map((s) => s.trim()).filter(Boolean);
const PROJECT = hasFlag('--project');

// agent -> [userLevelDir, projectLevelDir, kind]
// kind: 'skills' 目录型（复制整个包目录）；'rules' 单文件型（仅复制 SKILL.md）
const AGENT_DIRS = {
  workbuddy: { user: '~/.workbuddy/skills', project: '.workbuddy/skills', kind: 'skills' },
  claude:    { user: '~/.claude/skills',    project: '.claude/skills',    kind: 'skills' },
  cursor:    { user: '~/.cursor/skills',    project: '.cursor/skills',    kind: 'skills' },
  trae:      { user: '~/.trae-cn/skills',   project: '.trae/skills',      kind: 'skills' },
  agents:    { user: '~/.agents/skills',    project: '.agents/skills',    kind: 'skills' },
  openclaw:  { user: '~/.openclaw/skills',  project: '.openclaw/skills',  kind: 'skills' },
  windsurf:  { user: '~/.windsurf/rules',   project: '.windsurf/rules',   kind: 'rules' },
};

if (!existsSync(join(SOURCE, 'SKILL.md'))) {
  console.error(`\u2717 ${SOURCE}/SKILL.md 不存在，请用 --source 指定 skill 包目录`);
  process.exit(1);
}
const skillName = basename(SOURCE);
const unknown = AGENTS.filter((a) => !AGENT_DIRS[a]);
if (unknown.length) {
  console.error(`\u2717 未知 agent: ${unknown.join(', ')}（可用: ${Object.keys(AGENT_DIRS).join(', ')}）`);
  process.exit(1);
}

let installed = 0;
for (const agent of AGENTS) {
  const cfg = AGENT_DIRS[agent];
  const base = PROJECT ? cfg.project : cfg.user;
  const targetRoot = base.replace(/^~(?=\/|$)/, HOME);
  if (!targetRoot) continue;

  try {
    if (cfg.kind === 'skills') {
      // 复制整个包目录（含 scripts/），目标已存在则先移除再复制，保证最新
      const dest = join(targetRoot, skillName);
      rmSync(dest, { recursive: true, force: true });
      mkdirSync(targetRoot, { recursive: true });
      cpSync(SOURCE, dest, { recursive: true });
      console.log(`\u2713 ${agent} (${PROJECT ? 'project' : 'user'}): ${dest}`);
    } else {
      // rules 布局：<root>/<name>/<name>.md，仅复制 SKILL.md（rules 模式不支持 scripts）
      const destDir = join(targetRoot, skillName);
      mkdirSync(destDir, { recursive: true });
      copyFileSync(join(SOURCE, 'SKILL.md'), join(destDir, `${skillName}.md`));
      console.log(`\u2713 ${agent} (${PROJECT ? 'project' : 'user'}): ${join(destDir, `${skillName}.md`)}（rules 模式仅支持单文件）`);
    }
    installed++;
  } catch (e) {
    console.error(`\u2717 ${agent} 安装失败: ${e.message}`);
  }
}

console.log(`\n完成：${installed}/${AGENTS.length} 个目标安装成功。重启对应 Agent / IDE 后生效。`);
