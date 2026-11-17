'use strict';
/**
 * lib/untar.js —— 零依赖内置解包（元阁 0.24.0，方案 A.2）。
 *
 * 只服务 npm 包形态的 tar.gz：必须 `package/` 前缀、拒绝链接条目与路径越界、
 * 支持 ustar prefix / pax 扩展头 / GNU 长名；产出与 bin 的 extractTarball 相同契约
 * （`{ pkgDir }` 或 `{ error }`）。
 */

const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

/** 与 lib/install-pipeline.js 的 isSafeTarEntry 同口径（测试有 parity 断言）。 */
function isSafeTarEntry(entry) {
  const value = String(entry || '').replace(/\\/g, '/');
  if (value !== 'package' && !value.startsWith('package/')) return false;
  if (value.startsWith('/') || /^[A-Za-z]:\//.test(value)) return false;
  return !value.split('/').includes('..');
}

function cstring(buf, start, length) {
  const slice = buf.subarray(start, start + length);
  const end = slice.indexOf(0);
  return slice.subarray(0, end === -1 ? slice.length : end).toString('utf8').trim();
}

function parseOctal(buf, start, length) {
  const raw = cstring(buf, start, length).replace(/\0/g, '').trim();
  if (!raw) return 0;
  const value = parseInt(raw, 8);
  return Number.isFinite(value) ? value : 0;
}

function parsePaxRecords(data) {
  const map = {};
  let offset = 0;
  while (offset < data.length) {
    const space = data.indexOf(0x20, offset);
    if (space === -1) break;
    const length = parseInt(data.subarray(offset, space).toString('utf8'), 10);
    if (!Number.isFinite(length) || length <= 0 || offset + length > data.length) break;
    const record = data.subarray(space + 1, offset + length).toString('utf8');
    const eq = record.indexOf('=');
    if (eq !== -1) map[record.slice(0, eq)] = record.slice(eq + 1).replace(/\n$/, '');
    offset += length;
  }
  return map;
}

/**
 * 解析 tar（不含 gzip）为条目数组。
 * 返回 { entries } 或 { error }；条目形如 { name, mode, type, data }。
 */
function parseEntries(buffer) {
  const entries = [];
  let offset = 0;
  let pendingPax = {};
  let pendingLongName = null;
  while (offset + 512 <= buffer.length) {
    const header = buffer.subarray(offset, offset + 512);
    let allZero = true;
    for (const byte of header) {
      if (byte !== 0) {
        allZero = false;
        break;
      }
    }
    if (allZero) break;

    let name = cstring(header, 0, 100);
    const prefix = cstring(header, 345, 155);
    const mode = parseOctal(header, 100, 8);
    const size = parseOctal(header, 124, 12);
    const type = String.fromCharCode(header[156] || 0x30);
    const dataStart = offset + 512;
    const dataEnd = dataStart + size;
    if (size < 0 || dataEnd > buffer.length) {
      return { error: 'tar 结构损坏：条目数据越界（' + (name || '未命名') + '）' };
    }
    const data = buffer.subarray(dataStart, dataEnd);

    if (type === 'x' || type === 'g') {
      const records = parsePaxRecords(data);
      if (type === 'x') pendingPax = Object.assign(pendingPax, records);
      offset = dataStart + Math.ceil(size / 512) * 512;
      continue;
    }
    if (type === 'L') {
      pendingLongName = cstring(data, 0, data.length);
      offset = dataStart + Math.ceil(size / 512) * 512;
      continue;
    }
    if (prefix && type !== 'x' && type !== 'g') name = prefix + '/' + name;
    if (pendingLongName) {
      name = pendingLongName;
      pendingLongName = null;
    }
    if (pendingPax.path) name = pendingPax.path;
    if (pendingPax.size !== undefined && Number(pendingPax.size) !== size) {
      return { error: 'tar 结构不支持：pax size 覆盖（' + name + '）' };
    }
    const entryMode = pendingPax.mode !== undefined ? parseInt(pendingPax.mode, 8) : mode;
    pendingPax = {};

    entries.push({ name, mode: Number.isFinite(entryMode) ? entryMode : mode, type, size, data: Buffer.from(data) });
    offset = dataStart + Math.ceil(size / 512) * 512;
  }
  return { entries };
}

function extractTarballBuiltin(tarball, extractDir) {
  let compressed;
  try {
    compressed = fs.readFileSync(tarball);
  } catch (error) {
    return { error: '读取压缩包失败: ' + error.message };
  }
  let buffer;
  try {
    buffer = zlib.gunzipSync(compressed);
  } catch (error) {
    return { error: 'gzip 解压失败: ' + error.message };
  }

  const parsed = parseEntries(buffer);
  if (parsed.error) return { error: parsed.error };

  // fail-closed：先整体校验，再落盘（不允许部分写入）。
  const root = path.resolve(extractDir);
  for (const entry of parsed.entries) {
    if (!isSafeTarEntry(entry.name)) return { error: '压缩包包含不安全路径: ' + entry.name };
    if (entry.type === '1' || entry.type === '2') {
      return { error: '压缩包包含链接条目（fail-closed 拒绝）: ' + entry.name };
    }
    if (!['0', '7', '5'].includes(entry.type)) {
      return { error: '压缩包包含不支持的 tar 条目类型（' + entry.type + '）: ' + entry.name };
    }
    const target = path.resolve(extractDir, entry.name);
    if (target !== root && !target.startsWith(root + path.sep)) {
      return { error: '压缩包路径越界: ' + entry.name };
    }
  }

  fs.mkdirSync(extractDir, { recursive: true });
  try {
    for (const entry of parsed.entries) {
      const target = path.resolve(extractDir, entry.name);
      if (entry.type === '5') {
        fs.mkdirSync(target, { recursive: true });
        continue;
      }
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.writeFileSync(target, entry.data);
      if (entry.mode & 0o111) {
        try {
          fs.chmodSync(target, 0o755);
        } catch (_) {
          // Windows 上 chmod 基本无效；忽略即可，不阻断解包。
        }
      }
    }
  } catch (error) {
    return { error: '写入解包产物失败: ' + error.message };
  }

  const pkgDir = path.join(extractDir, 'package');
  if (!fs.existsSync(path.join(pkgDir, 'SKILL.md'))) {
    return { error: '解压产物缺少 SKILL.md（' + tarball + '）' };
  }
  return { pkgDir, channel: 'builtin' };
}

module.exports = {
  isSafeTarEntry,
  parseEntries,
  parsePaxRecords,
  extractTarballBuiltin,
};
