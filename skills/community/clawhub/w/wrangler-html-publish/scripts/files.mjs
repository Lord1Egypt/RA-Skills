// 仅处理本地文件，不登录、不联网、不执行站点代码。
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

export function defaults(env = process.env, home = os.homedir()) {
  return {
    archive: path.join(home, 'Documents', 'published-html'),
    config: env.HTML_PUBLISH_CONFIG || path.join(env.XDG_CONFIG_HOME || path.join(home, '.config'), 'wrangler-html-publish', 'config.json'),
  };
}

function relative(value) {
  if (typeof value !== 'string' || !value || value.includes('\\') || value.includes(':') || value.includes('\0') || value.startsWith('/') || value.split('/').some(x => !x || x === '.' || x === '..')) throw new Error(`非法相对路径：${value}`);
  return value;
}

export function checkedFile(root, name) {
  relative(name);
  const base = path.resolve(root);
  if (fs.lstatSync(base).isSymbolicLink() || !fs.statSync(base).isDirectory()) throw new Error('源根目录必须是普通目录');
  let current = base;
  for (const part of name.split('/')) {
    current = path.join(current, part);
    if (fs.lstatSync(current).isSymbolicLink()) throw new Error(`拒绝符号链接：${name}`);
  }
  if (!fs.statSync(current).isFile()) throw new Error(`不是普通文件：${name}`);
  const blocked = name.split('/').some(x => x.startsWith('.') || ['functions', 'node_modules', '_worker.js', '_redirects', '_headers'].includes(x));
  if (blocked || /(?:\.map$|^|\/)wrangler\.(?:toml|jsonc?)$/.test(name) || !/\.(?:html?|css|js|mjs|json|png|jpe?g|gif|svg|webp|ico|woff2?|ttf|otf|txt|pdf|avif)$/i.test(name)) throw new Error(`不允许发布此文件：${name}`);
  return current;
}

const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');

// plan.files 是人工审核过的完整快照白名单；不遍历归档目录。
export function stage(plan, destination) {
  if (!plan.project || !plan.branch || !Array.isArray(plan.files) || !plan.files.length) throw new Error('缺少项目、分支或文件清单');
  if (fs.existsSync(destination)) throw new Error('staging 目标必须不存在');
  const seen = new Set();
  const files = plan.files.map(item => {
    const target = relative(item.target);
    const key = target.toLowerCase();
    if (seen.has(key)) throw new Error(`重复目标路径：${target}`);
    seen.add(key);
    // 对源路径和目标路径分别执行规则检查。
    const source = checkedFile(item.root, item.source);
    const targetParts = target.split('/');
    if (targetParts.some(x => x.startsWith('.') || ['functions', 'node_modules', '_worker.js', '_redirects', '_headers'].includes(x)) || /(?:^|\/)wrangler\.(?:toml|jsonc?)$/.test(target) || !/\.(?:html?|css|js|mjs|json|png|jpe?g|gif|svg|webp|ico|woff2?|ttf|otf|txt|pdf|avif)$/i.test(target)) throw new Error('目标路径包含配置、可执行后端或不支持的文件类型');
    const bytes = fs.readFileSync(source);
    if (!/^[a-f0-9]{64}$/.test(item.sha256 || '')) throw new Error(`缺少有效审核哈希：${target}`);
    if (item.sha256 !== hash(bytes)) throw new Error(`文件在审核后发生变化：${target}`);
    return { target, bytes, sha256: hash(bytes) };
  });
  // 全部检查通过后才创建目标；使用独占写入，拒绝覆盖。
  fs.mkdirSync(destination, { recursive: false, mode: 0o700 });
  for (const file of files) {
    const target = path.join(destination, ...file.target.split('/'));
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, file.bytes, { flag: 'wx' });
  }
  return { version: 1, project: plan.project, branch: plan.branch, files: files.map(({ target, sha256 }) => ({ target, sha256 })) };
}

export function archive(source, root, slug) {
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug)) throw new Error('slug 仅允许小写英文、数字与连字符');
  const src = path.resolve(source);
  if (fs.lstatSync(src).isSymbolicLink() || !fs.statSync(src).isFile()) throw new Error('输入必须是普通 HTML 文件');
  if (!/\.html?$/i.test(src)) throw new Error('输入必须是 HTML 文件');
  const bytes = fs.readFileSync(src);
  fs.mkdirSync(root, { recursive: true });
  const directory = path.join(root, slug);
  fs.mkdirSync(directory); // 同名即失败，不覆盖旧页面。
  fs.writeFileSync(path.join(directory, 'index.html'), bytes, { flag: 'wx' });
  return directory;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const [command, ...args] = process.argv.slice(2);
    if (command === 'defaults') console.log(JSON.stringify(defaults(), null, 2));
    else if (command === 'archive' && args.length === 3) console.log(archive(...args));
    else if (command === 'stage' && args.length === 2) console.log(JSON.stringify(stage(JSON.parse(fs.readFileSync(args[0], 'utf8')), args[1]), null, 2));
    else throw new Error('用法：files.mjs defaults | archive <HTML> <归档根目录> <slug> | stage <plan.json> <不存在的staging目录>');
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}
