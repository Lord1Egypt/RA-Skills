import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, isAbsolute, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

/** 26-沙雕漫剧 根目录 */
export const SKILL_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../../../..');
export const PROJECTS_ROOT = join(SKILL_ROOT, '99-项目');

/** 剧名 / 角色名这类会拼进路径的字段：不许带路径分隔符，不许是 . 或 .. */
const SAFE_NAME = /^[^\\/:*?"<>|\x00-\x1f]{1,64}$/;

export function assertSafeName(name, what = '名称') {
  const s = String(name ?? '').trim();
  if (!s || !SAFE_NAME.test(s) || s === '.' || s === '..') {
    throw new Error(
      `${what}不合法：${JSON.stringify(name)}（不能为空，不能含 / \\ : * ? " < > |，不能是 . 或 ..）`,
    );
  }
  return s;
}

/** 把相对路径拼到 base 下，并保证结果跑不出 base（防 ../../ 读到季目录外） */
export function safeJoin(base, ...parts) {
  const root = resolve(base);
  const target = resolve(root, ...parts);
  const rel = relative(root, target);
  if (!rel || rel.startsWith('..') || isAbsolute(rel)) {
    throw new Error(`路径越界：${target} 不在 ${root} 内`);
  }
  return target;
}

export function seasonDir(project, season = 1) {
  if (!project) throw new Error('缺少 --project（剧名）');
  const name = assertSafeName(project, '剧名');
  if (!Number.isInteger(season) || season < 1 || season > 99) {
    throw new Error(`--season 必须是 1–99 的整数，实际是 ${season}`);
  }
  const dir = join(PROJECTS_ROOT, name, `第${String(season).padStart(2, '0')}季`);
  if (!existsSync(dir)) throw new Error(`季目录不存在：${dir}`);
  return dir;
}

export function readJson(path) {
  if (!existsSync(path)) throw new Error(`找不到文件：${path}`);
  return JSON.parse(readFileSync(path, 'utf8'));
}

export function writeJson(path, data) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, JSON.stringify(data, null, 2) + '\n', 'utf8');
}

export function ensureDir(dir) {
  mkdirSync(dir, { recursive: true });
  return dir;
}

export function relPath(fromDir, target) {
  return relative(fromDir, target).split('\\').join('/');
}

export function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const token = argv[i];
    if (token.startsWith('--')) {
      const key = token.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) {
        args[key] = true;
      } else {
        args[key] = next;
        i++;
      }
    } else {
      args._.push(token);
    }
  }
  return args;
}
