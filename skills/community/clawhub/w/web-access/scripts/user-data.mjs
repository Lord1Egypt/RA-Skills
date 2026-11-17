// 用户数据位置 + 旧版本数据一次性迁移 - 单一职责模块
// 被 check-deps.mjs、browser-discovery.mjs、match-site.mjs、cdp-proxy.mjs 共享。
//
// 用户数据（浏览器偏好 config.env、站点经验 site-patterns/）放在 ~/.web-access/，
// 不在 Skill 目录内：整目录替换（npx skills update）或按版本分目录（Claude Code 插件）升级都不会带走它。
//
// 迁移规则（新目录没有 .migrated 标记时执行一次，之后不再扫描，避免已删除的文件被旧副本复活）：
//   来源 1：当前 Skill 根目录下的 config.env 与 references/site-patterns/（git 安装升级后旧文件仍在原处）
//   来源 2：插件缓存按版本分目录（<…>/web-access/<版本>/）时，相邻兄弟目录中 SKILL.md frontmatter
//           name 为 web-access 的旧版本，只取含用户数据且修改时间最新的一个。只有父目录名为 web-access
//           才扫描，Skill 直接放在 HOME 等普通目录下时不去读 ~/Desktop 等兄弟目录
//   只复制不删除；目标已存在的文件不覆盖；来源 1 优先。

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const SKILL_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SKILL_NAME = 'web-access';

// 调用时按 HOME 计算（Windows 为 C:\Users\<用户>\.web-access\）
export function userDataPaths(home = os.homedir()) {
  const dir = path.join(home, '.web-access');
  return {
    dir,
    config: path.join(dir, 'config.env'),
    sitePatterns: path.join(dir, 'site-patterns'),
    marker: path.join(dir, '.migrated'),
  };
}

// 旧版本在 Skill 根目录内的用户数据位置
function legacyPaths(root) {
  return {
    config: path.join(root, 'config.env'),
    sitePatterns: path.join(root, 'references', 'site-patterns'),
  };
}

// 递归列出普通文件的相对路径；跳过占位 .gitkeep 和符号链接
function listFiles(base, rel = '') {
  let entries;
  try { entries = fs.readdirSync(path.join(base, rel), { withFileTypes: true }); }
  catch (error) {
    if (error.code === 'ENOENT' || error.code === 'ENOTDIR') return [];
    throw error;
  }
  const files = [];
  for (const entry of entries) {
    const child = path.join(rel, entry.name);
    if (entry.isDirectory()) files.push(...listFiles(base, child));
    else if (entry.isFile() && entry.name !== '.gitkeep') files.push(child);
  }
  return files;
}

// 该目录下的旧用户数据；没有则返回 null
function legacyData(root) {
  const legacy = legacyPaths(root);
  const hasConfig = fs.statSync(legacy.config, { throwIfNoEntry: false })?.isFile() === true;
  const patterns = listFiles(legacy.sitePatterns);
  if (!hasConfig && !patterns.length) return null;
  const files = [...(hasConfig ? [legacy.config] : []), ...patterns.map(file => path.join(legacy.sitePatterns, file))];
  const mtime = Math.max(...files.map(file => fs.statSync(file).mtimeMs));
  return { root, hasConfig, patterns, mtime };
}

// 保守识别：目录内 SKILL.md 的 frontmatter 明确写着 name: web-access
function isWebAccessSkill(dir) {
  let text;
  try { text = fs.readFileSync(path.join(dir, 'SKILL.md'), 'utf8'); }
  catch { return false; }
  const front = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  return !!front && new RegExp(`^name:\\s*["']?${SKILL_NAME}["']?\\s*$`, 'm').test(front[1]);
}

// 相邻目录中含用户数据且最新的 web-access 旧版本（不跟随符号链接）。
// 只认插件缓存的 <plugin>/<version>/ 布局（父目录名为 web-access），其他位置不扫描兄弟目录。
function newestSibling(root) {
  const parent = path.dirname(root);
  if (path.basename(parent) !== SKILL_NAME) return null;
  let newest = null;
  for (const entry of fs.readdirSync(parent, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const dir = path.join(parent, entry.name);
    if (dir === root || !isWebAccessSkill(dir)) continue;
    const data = legacyData(dir);
    if (data && (!newest || data.mtime > newest.mtime)) newest = data;
  }
  return newest;
}

// 目标已存在则跳过（原子判断），返回是否真正复制
function copyIfAbsent(from, to) {
  fs.mkdirSync(path.dirname(to), { recursive: true });
  try {
    fs.copyFileSync(from, to, fs.constants.COPYFILE_EXCL);
    return true;
  } catch (error) {
    if (error.code === 'EEXIST') return false;
    throw error;
  }
}

// 执行一次性迁移。返回 { dir, sources: [{ from, config, patterns }] }，已迁移过则返回 null。
// 出错直接抛出且不写标记，由调用方提示，下次运行重试（只复制不覆盖，重试安全）。
export function migrateLegacyData({ root = SKILL_ROOT, home = os.homedir() } = {}) {
  root = path.resolve(root);
  const target = userDataPaths(home);
  if (fs.existsSync(target.marker)) return null;

  const sources = [];
  for (const data of [legacyData(root), newestSibling(root)]) {
    if (!data) continue;
    const legacy = legacyPaths(data.root);
    const config = data.hasConfig && copyIfAbsent(legacy.config, target.config);
    let patterns = 0;
    for (const file of data.patterns) {
      if (copyIfAbsent(path.join(legacy.sitePatterns, file), path.join(target.sitePatterns, file))) patterns++;
    }
    if (config || patterns) sources.push({ from: data.root, config, patterns });
  }

  fs.mkdirSync(target.dir, { recursive: true });
  const note = sources.map(source => `${source.from}: config.env=${source.config}, site-patterns=${source.patterns}`);
  fs.writeFileSync(target.marker, [`migrated ${new Date().toISOString()}`, ...note].join('\n') + '\n');
  return { dir: target.dir, sources };
}
