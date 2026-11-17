import { gunzipSync } from 'node:zlib';
import { mkdir, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fail } from './source.mjs';

// Parse a bounded regular-file ustar archive before creating any member. Links,
// device nodes, pax/long-name extensions and ambiguous paths are unsupported.
export function members(bytes) {
  let tar;
  try { tar = gunzipSync(bytes, { maxOutputLength: 2097152 }); } catch { throw fail('archive_oversized_or_invalid'); }
  const files = new Map(); let offset = 0; let count = 0;
  const string = b => b.toString('utf8').replace(/\0.*$/s, '');
  while (offset + 512 <= tar.length) {
    const header = tar.subarray(offset, offset + 512); offset += 512;
    if (header.every(b => b === 0)) {
      if (tar.subarray(offset).some(b => b !== 0)) throw fail('archive_trailing_bytes');
      return files;
    }
    if (++count > 128) throw fail('archive_member_limit');
    const checksum = string(header.subarray(148, 156)).trim();
    const sum = header.reduce((total, byte, i) => total + (i >= 148 && i < 156 ? 32 : byte), 0);
    if (!/^[0-7]+$/.test(checksum) || parseInt(checksum, 8) !== sum) throw fail('archive_checksum');
    const prefix = string(header.subarray(345, 500));
    const name = (prefix ? prefix + '/' : '') + string(header.subarray(0, 100));
    const sizeText = string(header.subarray(124, 136)).trim();
    if (!/^[0-7]+$/.test(sizeText)) throw fail('archive_size');
    const size = parseInt(sizeText, 8); const type = string(header.subarray(156, 157));
    const parts = name.replace(/\/$/, '').split('/');
    if (!['package', 'task-linked-delivery'].includes(parts[0]) || parts.some(p => !p || p === '.' || p === '..') || name.includes('\\') || !/^[a-zA-Z0-9_./\-]+$/.test(name)) throw fail('archive_path');
    if (!['', '0', '5'].includes(type) || (type === '5' && size !== 0)) throw fail('archive_member_type');
    if (size > 262144 || offset + size > tar.length) throw fail('archive_size');
    if (type !== '5') { if (files.has(name)) throw fail('archive_duplicate'); files.set(name, tar.subarray(offset, offset + size)); }
    offset += Math.ceil(size / 512) * 512;
  }
  throw fail('archive_truncated');
}
export async function extract(files, root, allowance) {
  for (const [name, bytes] of files) {
    allowance.left();
    await allowance.wait(mkdir(dirname(join(root, name)), { recursive: true }));
    await allowance.wait(writeFile(join(root, name), bytes, { flag: 'wx', mode: 0o600 }));
  }
}
