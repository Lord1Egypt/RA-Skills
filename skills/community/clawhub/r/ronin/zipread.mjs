// A small, strict zip reader shared by the hub (scanning skill bundles) and the worker
// (unpacking them). Reads the central directory, so zips written by Windows, macOS and
// most tools (data descriptors, extra fields) work. Refuses what a skill bundle has no
// business containing: encrypted entries, paths that escape the folder, absolute paths,
// symlinks, and anything that inflates past the limits (a zip bomb).
//
//   readZip(buffer, {maxFiles, maxTotal, maxFile}) -> Map(name -> Buffer)   or throws ZipError

import { inflateRawSync } from 'node:zlib';

export class ZipError extends Error {
  constructor(code, message) { super(message); this.code = code; }
}

export const LIMITS = { maxFiles: 300, maxTotal: 25 * 1024 * 1024, maxFile: 5 * 1024 * 1024 };

export function isZip(buf) {
  return Buffer.isBuffer(buf) && buf.length >= 4 && buf.readUInt32LE(0) === 0x04034b50;
}

export function readZip(buf, limits = LIMITS) {
  const { maxFiles, maxTotal, maxFile } = { ...LIMITS, ...limits };
  // End of central directory: the last 22 bytes, or up to 64 KB further back with a comment.
  let eocd = -1;
  for (let i = buf.length - 22; i >= Math.max(0, buf.length - 22 - 65535); i--) {
    if (buf.readUInt32LE(i) === 0x06054b50) { eocd = i; break; }
  }
  if (eocd < 0) throw new ZipError('not-zip', 'not a zip file (no central directory)');
  const count = buf.readUInt16LE(eocd + 10);
  const cdOffset = buf.readUInt32LE(eocd + 16);
  if (count === 0xffff || cdOffset === 0xffffffff) throw new ZipError('zip64', 'zip64 archives are not supported');
  if (count > maxFiles) throw new ZipError('too-many', `more than ${maxFiles} files`);
  const out = new Map();
  let p = cdOffset, total = 0;
  for (let n = 0; n < count; n++) {
    if (buf.readUInt32LE(p) !== 0x02014b50) throw new ZipError('corrupt', 'central directory is corrupt');
    const flags = buf.readUInt16LE(p + 8), method = buf.readUInt16LE(p + 10);
    const csize = buf.readUInt32LE(p + 20), usize = buf.readUInt32LE(p + 24);
    const nlen = buf.readUInt16LE(p + 28), xlen = buf.readUInt16LE(p + 30), clen = buf.readUInt16LE(p + 32);
    const extAttr = buf.readUInt32LE(p + 38), local = buf.readUInt32LE(p + 42);
    const name = buf.subarray(p + 46, p + 46 + nlen).toString('utf8');
    p += 46 + nlen + xlen + clen;
    if (flags & 1) throw new ZipError('encrypted', `password-protected entry: ${name}`);
    if (name.endsWith('/')) continue; // a directory entry
    if (name.startsWith('/') || name.includes('\\') || /^[a-zA-Z]:/.test(name) || name.split('/').some((s) => s === '..' || s === '')) throw new ZipError('bad-path', `unsafe path in zip: ${name}`);
    if (((extAttr >>> 16) & 0o170000) === 0o120000) throw new ZipError('symlink', `symlink in zip: ${name}`);
    if (usize > maxFile) throw new ZipError('too-big', `${name} is over ${maxFile} bytes`);
    total += usize;
    if (total > maxTotal) throw new ZipError('too-big', `the files add up to more than ${maxTotal} bytes`);
    if (buf.readUInt32LE(local) !== 0x04034b50) throw new ZipError('corrupt', `bad local header for ${name}`);
    const start = local + 30 + buf.readUInt16LE(local + 26) + buf.readUInt16LE(local + 28);
    const body = buf.subarray(start, start + csize);
    let data;
    if (method === 0) data = Buffer.from(body);
    else if (method === 8) {
      try { data = inflateRawSync(body, { maxOutputLength: maxFile + 1 }); } catch { throw new ZipError('corrupt', `could not inflate ${name}`); }
    } else throw new ZipError('method', `unsupported compression in ${name}`);
    if (data.length !== usize) throw new ZipError('corrupt', `${name} is not the size the zip says`);
    if (out.has(name)) throw new ZipError('duplicate', `duplicate entry: ${name}`);
    out.set(name, data);
  }
  return out;
}

/**
 * A skill bundle: a zip with SKILL.md at its root, or inside one top folder. Returns
 * {files: Map(relative name -> Buffer), prefix} with the top folder stripped.
 */
export function readBundle(buf, limits) {
  const all = readZip(buf, limits);
  const names = [...all.keys()];
  let prefix = '';
  if (!all.has('SKILL.md')) {
    const tops = new Set(names.map((n) => n.split('/')[0]));
    const top = tops.size === 1 ? [...tops][0] : null;
    if (!top || !all.has(`${top}/SKILL.md`)) throw new ZipError('no-skill-md', 'a skill bundle needs SKILL.md at its root (or inside one top folder)');
    prefix = top + '/';
  }
  const files = new Map();
  for (const [n, b] of all) files.set(n.slice(prefix.length), b);
  return { files, prefix };
}
