/**
 * 技能自己更新自己。
 *
 * 技能是一次性装到用户机器上的，之后网站加了模型、改了价格、修了问题，用户手里那份都不会动。
 * 所以每条命令运行前问一下 OSS 上的 latest.json（一小时最多问一次，结果记在本机），
 * 有新版就下载、核对 sha256、解到技能目录旁边、整个换过去，再用新脚本把这条命令重跑一遍。
 *
 * 任何一步出问题都只是退回「打一行提示、接着用旧版跑」，更新失败绝不能挡住生图。
 */
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { request } from './http.mjs';
import { SITE, SKILL_ROOT, readState, writeState } from './store.mjs';

const CHECK_EVERY_MS = 60 * 60 * 1000;
const RETRY_FAILED_MS = 10 * 60 * 1000;
// 先走 CDN，连不上（有的网络到 CDN 不通）再直连 OSS 源站
const BASES = () => [process.env.STUDIO_SKILL_BASE || SITE.skillBase, SITE.skillBaseFallback].filter(Boolean);

/** 版本号只认 SKILL.md 的 frontmatter，发布脚本也是从那里读的 */
export function localVersion(root = SKILL_ROOT) {
  try {
    const text = fs.readFileSync(path.join(root, 'SKILL.md'), 'utf8');
    const front = /^---\r?\n([\s\S]*?)\r?\n---/.exec(text);
    return /^version:\s*(\S+)/m.exec(front?.[1] ?? '')?.[1] ?? '0.0.0';
  } catch {
    return '0.0.0';
  }
}

/** 只比 x.y.z 三段数字；解析不了的一律当 0，不会误判成「有新版」 */
export function isNewer(remote, local) {
  const parse = (v) => String(v || '').split('.').map((n) => Number.parseInt(n, 10) || 0);
  const a = parse(remote);
  const b = parse(local);
  for (let i = 0; i < 3; i += 1) {
    if ((a[i] ?? 0) !== (b[i] ?? 0)) return (a[i] ?? 0) > (b[i] ?? 0);
  }
  return false;
}

/** OSS 上的发布清单 { version, tarball, sha256, notes }；拿不到返回 null */
export async function latestManifest({ force = false } = {}) {
  const cache = readState('update-check.json');
  const ttl = cache?.manifest ? CHECK_EVERY_MS : RETRY_FAILED_MS;
  if (!force && cache && Date.now() - Number(cache.checkedAt || 0) < ttl) return cache.manifest || null;
  let manifest = null;
  for (const base of BASES()) {
    try {
      // 带上时间戳绕开 CDN 缓存，清单本身很小
      const res = await request(`${base}/${SITE.name}/latest.json?t=${Date.now()}`, { timeout: 4000 });
      if (res.ok) {
        const json = await res.json();
        if (json && json.version && json.tarball) {
          manifest = { ...json, base };
          break;
        }
      }
    } catch {
      /* 换下一个地址；都不通就算了，后面的命令自己会报错 */
    }
  }
  // 没问到也记一笔：连不上的这段时间里，每条命令都白等几秒不划算（失败的 10 分钟后再问）
  try {
    writeState('update-check.json', { checkedAt: Date.now(), manifest });
  } catch {
    /* 记不下来就下次再问 */
  }
  return manifest;
}

/** 这份技能能不能被自动替换。返回空串表示可以，否则是原因 */
export function cannotSelfUpdate(root = SKILL_ROOT) {
  if (process.env.STUDIO_NO_AUTO_UPDATE) return '设置了 STUDIO_NO_AUTO_UPDATE';
  // 源码仓库里构建出来的那份是开发者在改的东西，不能被线上旧版覆盖
  if (fs.existsSync(path.join(root, '..', '..', 'build.mjs'))) return '这是技能源码仓库里的构建目录';
  if (!fs.existsSync(path.join(root, 'SKILL.md'))) return `${root} 不像是技能目录`;
  try {
    fs.accessSync(path.dirname(root), fs.constants.W_OK);
    fs.accessSync(root, fs.constants.W_OK);
  } catch {
    return `${root} 没有写权限`;
  }
  return '';
}

/**
 * 下载新版并整个换掉技能目录，成功返回新版本号，失败抛错。
 * 解到技能目录旁边：最后一步是 rename，同一个文件系统上才是原子的。
 */
export async function installLatest(manifest, root = SKILL_ROOT) {
  const parent = path.dirname(root);
  const stamp = `${process.pid}-${Date.now()}`;
  const work = path.join(parent, `.${SITE.name}-update-${stamp}`);
  const backup = path.join(parent, `.${SITE.name}-old-${stamp}`);
  fs.mkdirSync(work, { recursive: true });
  try {
    // 清单从哪个地址拿到的，包就先从哪儿下；版本包不可变，换个源下到的内容一样（sha256 兜底）
    const urls = [...new Set([manifest.base, ...BASES()].filter(Boolean)
      .map((b) => manifest.tarball.replace(SITE.skillBase, b)))];
    let buf = null;
    let lastError = '';
    for (const url of urls) {
      try {
        const res = await request(url, { timeout: 60_000 });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        buf = Buffer.from(await res.arrayBuffer());
        break;
      } catch (e) {
        lastError = e.message;
      }
    }
    if (!buf) throw new Error(`下载技能包失败（${lastError}）`);
    if (manifest.sha256) {
      const got = crypto.createHash('sha256').update(buf).digest('hex');
      if (got !== manifest.sha256) throw new Error('技能包校验失败（sha256 不一致）');
    }
    const archive = path.join(work, 'skill.tar.gz');
    fs.writeFileSync(archive, buf);
    // macOS / Linux / Windows 10 以上都自带 tar
    const r = spawnSync('tar', ['xzf', archive, '-C', work], { encoding: 'utf8' });
    if (r.error || r.status !== 0) throw new Error(`解压技能包失败：${r.error?.message || r.stderr || `退出码 ${r.status}`}`);

    const fresh = path.join(work, SITE.name);
    if (!fs.existsSync(path.join(fresh, 'SKILL.md')) || !fs.existsSync(path.join(fresh, 'scripts', 'studio.mjs'))) {
      throw new Error('技能包不完整');
    }
    const version = localVersion(fresh);

    fs.renameSync(root, backup);
    try {
      fs.renameSync(fresh, root);
    } catch (e) {
      fs.renameSync(backup, root);
      throw e;
    }
    return version;
  } finally {
    fs.rmSync(work, { recursive: true, force: true });
    fs.rmSync(backup, { recursive: true, force: true });
  }
}
