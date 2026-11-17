#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { promises as fs } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const RENDERER_VERSION = '0.1.0';

const REQUIRED_FIELDS = [
  'spec', 'task_id', 'revision', 'title', 'objective', 'scope',
  'definition_of_done', 'constraints', 'permissions', 'deliverables',
  'next_steps', 'open_questions',
];

const REQUIRED_PACKAGE_FILES = [
  'AI任务说明.md',
  'MANIFEST.json',
  '任务合同.json',
  '任务说明.md',
];

function fail(message) {
  throw new Error(message);
}

function sha256(data) {
  return createHash('sha256').update(data).digest('hex');
}

function canonicalize(value) {
  if (Array.isArray(value)) return value.map(canonicalize);
  if (value && typeof value === 'object') {
    return Object.fromEntries(Object.keys(value).sort().map((key) => [key, canonicalize(value[key])]));
  }
  return value;
}

export function canonicalJson(value) {
  return `${JSON.stringify(canonicalize(value), null, 2)}\n`;
}

function assertText(value, field) {
  if (typeof value !== 'string' || value.trim() === '') fail(`${field} 必须是非空文本`);
}

function assertTextArray(value, field, { nonEmpty = false } = {}) {
  if (!Array.isArray(value) || (nonEmpty && value.length === 0)) fail(`${field} 必须是${nonEmpty ? '非空' : ''}文本数组`);
  value.forEach((item, index) => assertText(item, `${field}[${index}]`));
}

export function validateContract(contract) {
  if (!contract || typeof contract !== 'object' || Array.isArray(contract)) fail('任务合同必须是 JSON 对象');
  const unexpected = Object.keys(contract).filter((key) => ![...REQUIRED_FIELDS, 'references'].includes(key));
  if (unexpected.length) fail(`任务合同含有未定义字段：${unexpected.join(', ')}`);
  const missing = REQUIRED_FIELDS.filter((key) => !(key in contract));
  if (missing.length) fail(`任务合同缺少字段：${missing.join(', ')}`);
  if (contract.spec !== 'task-sync/1') fail('spec 必须是 task-sync/1');
  if (typeof contract.task_id !== 'string' || !/^[A-Za-z0-9][A-Za-z0-9._-]{2,63}$/.test(contract.task_id)) {
    fail('task_id 必须为 3–64 位字母、数字、点、下划线或连字符');
  }
  if (!Number.isInteger(contract.revision) || contract.revision < 1) fail('revision 必须是大于等于 1 的整数');
  assertText(contract.title, 'title');
  assertText(contract.objective, 'objective');
  if (!contract.scope || typeof contract.scope !== 'object' || Array.isArray(contract.scope)) fail('scope 必须是对象');
  if (Object.keys(contract.scope).some((key) => !['include', 'exclude'].includes(key))) fail('scope 只能含 include 和 exclude');
  assertTextArray(contract.scope.include, 'scope.include');
  assertTextArray(contract.scope.exclude, 'scope.exclude');
  assertTextArray(contract.definition_of_done, 'definition_of_done', { nonEmpty: true });
  assertTextArray(contract.constraints, 'constraints');
  assertTextArray(contract.permissions, 'permissions');
  assertTextArray(contract.next_steps, 'next_steps');
  assertTextArray(contract.open_questions, 'open_questions');
  if (!Array.isArray(contract.deliverables)) fail('deliverables 必须是数组');
  contract.deliverables.forEach((deliverable, index) => {
    if (!deliverable || typeof deliverable !== 'object' || Array.isArray(deliverable)) fail(`deliverables[${index}] 必须是对象`);
    const keys = Object.keys(deliverable).sort();
    if (keys.join(',') !== 'accept,name') fail(`deliverables[${index}] 只能含 name 和 accept`);
    assertText(deliverable.name, `deliverables[${index}].name`);
    assertText(deliverable.accept, `deliverables[${index}].accept`);
  });
  if (contract.references !== undefined) {
    if (!Array.isArray(contract.references)) fail('references 必须是数组');
    contract.references.forEach((reference, index) => {
      if (!reference || typeof reference !== 'object' || Array.isArray(reference)) fail(`references[${index}] 必须是对象`);
      const keys = Object.keys(reference).sort();
      if (!['label,ref', 'label,ref,sha256'].includes(keys.join(','))) fail(`references[${index}] 字段不合法`);
      assertText(reference.label, `references[${index}].label`);
      assertText(reference.ref, `references[${index}].ref`);
      if (reference.sha256 !== undefined && !/^[a-f0-9]{64}$/.test(reference.sha256)) fail(`references[${index}].sha256 必须是小写 SHA-256`);
    });
  }
  return contract;
}

function markdownList(items) {
  return items.length ? items.map((item) => `- ${item}`).join('\n') : '- （无）';
}

function numberedList(items) {
  return items.length ? items.map((item, index) => `${index + 1}. ${item}`).join('\n') : '（无）';
}

function deliverableTable(deliverables) {
  if (!deliverables.length) return '（无）';
  return ['| 交付物 | 验收方式 |', '| --- | --- |', ...deliverables.map(({ name, accept }) => `| ${name} | ${accept} |`)].join('\n');
}

function referenceList(references = []) {
  return references.length
    ? references.map(({ label, ref, sha256: digest }) => `- ${label}：${ref}${digest ? `（SHA-256: ${digest}）` : ''}`).join('\n')
    : '- （无）';
}

function humanProjection(contract, contractHash) {
  return `# ${contract.title}\n\n` +
    `> **任务身份**：${contract.task_id} · r${contract.revision}  \n` +
    `> **同一合同校验值**：\`${contractHash}\`  \n` +
    `> 本文件由 \`任务合同.json\` 生成，供人确认；不得手改。异议请回到合同修订并提升 revision。\n\n` +
    `## 要达成什么\n\n${contract.objective}\n\n` +
    `## 范围\n\n### 做\n\n${markdownList(contract.scope.include)}\n\n### 不做\n\n${markdownList(contract.scope.exclude)}\n\n` +
    `## 怎样算完成\n\n${numberedList(contract.definition_of_done)}\n\n` +
    `## 交付物与验收\n\n${deliverableTable(contract.deliverables)}\n\n` +
    `## 约束与授权\n\n### 约束\n\n${markdownList(contract.constraints)}\n\n### 当前授权\n\n${markdownList(contract.permissions)}\n\n` +
    `## 下一步\n\n${numberedList(contract.next_steps)}\n\n` +
    `## 待确认\n\n${numberedList(contract.open_questions)}\n\n` +
    `## 参考\n\n${referenceList(contract.references)}\n`;
}

function aiProjection(contract, contractHash, contractJson) {
  return `# AI 执行说明：${contract.title}\n\n` +
    `- 任务身份：\`${contract.task_id}\`，revision \`${contract.revision}\`\n` +
    `- 唯一真相源：\`任务合同.json\`\n` +
    `- 任务合同 SHA-256：\`${contractHash}\`\n` +
    `- 本说明只由任务合同确定性生成；如与其他聊天、邮件或附件相冲突，向用户指出冲突并要求以新 revision 处理。\n\n` +
    `## 开始前\n\n` +
    `1. 先运行包校验器；失败时不要执行任务。\n` +
    `2. 以 \`definition_of_done\` 作为完成判据；不要用“看起来完成”替代。\n` +
    `3. \`open_questions\` 未关闭时，只能推进不依赖它们的部分；不能自行臆断。\n` +
    `4. \`permissions\` 不是永久或泛化授权。任何外部发送、发布、收费或不可逆动作仍须获得当前用户授权。\n` +
    `5. 不把完整聊天、凭据或大文件复制进任务包；把可复验的引用和结果写入任务系统或 Task Passport。\n\n` +
    `## 同一任务合同（机器可读）\n\n\`\`\`json\n${contractJson}\`\`\`\n\n` +
    `## 执行停点\n\n` +
    `- 合同校验不通过、包内容被篡改，或合同 SHA-256 不一致：停止。\n` +
    `- 需要超出当前 \`permissions\` 的动作：停止并请求授权。\n` +
    `- 无法满足任一 \`definition_of_done\`：报告缺口，不宣称完成。\n`;
}

function createManifest(contract, contractHash, renderedFiles) {
  return {
    spec: 'task-sync-manifest/1',
    renderer_version: RENDERER_VERSION,
    task_id: contract.task_id,
    revision: contract.revision,
    task_contract_sha256: contractHash,
    files: [...renderedFiles.entries()]
      .map(([name, content]) => ({ name, sha256: sha256(content), bytes: Buffer.byteLength(content) }))
      .sort((left, right) => left.name.localeCompare(right.name, 'en')),
  };
}

export function renderPackage(contractInput) {
  const contract = validateContract(canonicalize(contractInput));
  const contractJson = canonicalJson(contract);
  const contractHash = sha256(contractJson);
  const withoutManifest = new Map([
    ['AI任务说明.md', aiProjection(contract, contractHash, contractJson)],
    ['任务合同.json', contractJson],
    ['任务说明.md', humanProjection(contract, contractHash)],
  ]);
  const manifest = createManifest(contract, contractHash, withoutManifest);
  const files = new Map([...withoutManifest, ['MANIFEST.json', canonicalJson(manifest)]]);
  return { contract, contractHash, files };
}

const CRC_TABLE = (() => {
  const table = new Uint32Array(256);
  for (let index = 0; index < 256; index += 1) {
    let value = index;
    for (let bit = 0; bit < 8; bit += 1) value = (value >>> 1) ^ ((value & 1) ? 0xedb88320 : 0);
    table[index] = value >>> 0;
  }
  return table;
})();

function crc32(data) {
  let value = 0xffffffff;
  for (const byte of data) value = CRC_TABLE[(value ^ byte) & 0xff] ^ (value >>> 8);
  return (value ^ 0xffffffff) >>> 0;
}

function u16(value) {
  const buffer = Buffer.alloc(2);
  buffer.writeUInt16LE(value, 0);
  return buffer;
}

function u32(value) {
  const buffer = Buffer.alloc(4);
  buffer.writeUInt32LE(value >>> 0, 0);
  return buffer;
}

// Store-only ZIP avoids runtime dependencies and uses a fixed DOS timestamp for reproducibility.
export function createDeterministicZip(files) {
  const entries = [...files.entries()]
    .map(([name, content]) => ({ name, nameBytes: Buffer.from(name, 'utf8'), data: Buffer.from(content, 'utf8') }))
    .sort((left, right) => left.name.localeCompare(right.name, 'en'));
  const localParts = [];
  const centralParts = [];
  let offset = 0;
  for (const entry of entries) {
    const checksum = crc32(entry.data);
    const local = Buffer.concat([
      u32(0x04034b50), u16(20), u16(0x0800), u16(0), u16(0), u16(0),
      u32(checksum), u32(entry.data.length), u32(entry.data.length),
      u16(entry.nameBytes.length), u16(0), entry.nameBytes, entry.data,
    ]);
    localParts.push(local);
    const central = Buffer.concat([
      u32(0x02014b50), u16(0x0314), u16(20), u16(0x0800), u16(0), u16(0), u16(0),
      u32(checksum), u32(entry.data.length), u32(entry.data.length),
      u16(entry.nameBytes.length), u16(0), u16(0), u16(0), u16(0), u32(0), u32(offset), entry.nameBytes,
    ]);
    centralParts.push(central);
    offset += local.length;
  }
  const central = Buffer.concat(centralParts);
  const end = Buffer.concat([
    u32(0x06054b50), u16(0), u16(0), u16(entries.length), u16(entries.length),
    u32(central.length), u32(offset), u16(0),
  ]);
  return Buffer.concat([...localParts, central, end]);
}

export function readDeterministicZip(zip) {
  let endOffset = -1;
  const lowerBound = Math.max(0, zip.length - 0xffff - 22);
  for (let offset = zip.length - 22; offset >= lowerBound; offset -= 1) {
    if (zip.readUInt32LE(offset) === 0x06054b50) { endOffset = offset; break; }
  }
  if (endOffset === -1) fail('不是有效 ZIP：未找到结束记录');
  const entries = zip.readUInt16LE(endOffset + 10);
  const centralOffset = zip.readUInt32LE(endOffset + 16);
  const files = new Map();
  let cursor = centralOffset;
  for (let index = 0; index < entries; index += 1) {
    if (cursor + 46 > zip.length || zip.readUInt32LE(cursor) !== 0x02014b50) fail('ZIP 中央目录损坏');
    const flags = zip.readUInt16LE(cursor + 8);
    const method = zip.readUInt16LE(cursor + 10);
    const checksum = zip.readUInt32LE(cursor + 16);
    const compressedSize = zip.readUInt32LE(cursor + 20);
    const uncompressedSize = zip.readUInt32LE(cursor + 24);
    const nameLength = zip.readUInt16LE(cursor + 28);
    const extraLength = zip.readUInt16LE(cursor + 30);
    const commentLength = zip.readUInt16LE(cursor + 32);
    const localOffset = zip.readUInt32LE(cursor + 42);
    if (!(flags & 0x0800) || method !== 0 || compressedSize !== uncompressedSize) fail('只接受本工具生成的 UTF-8、无压缩 ZIP');
    const name = zip.subarray(cursor + 46, cursor + 46 + nameLength).toString('utf8');
    if (!name || name.includes('/') || name.includes('\\') || name === '.' || name === '..' || files.has(name)) fail(`ZIP 文件名不安全或重复：${name}`);
    if (localOffset + 30 > zip.length || zip.readUInt32LE(localOffset) !== 0x04034b50) fail(`ZIP 本地文件头损坏：${name}`);
    const localNameLength = zip.readUInt16LE(localOffset + 26);
    const localExtraLength = zip.readUInt16LE(localOffset + 28);
    const start = localOffset + 30 + localNameLength + localExtraLength;
    const data = zip.subarray(start, start + compressedSize);
    if (data.length !== compressedSize || crc32(data) !== checksum) fail(`ZIP 文件校验失败：${name}`);
    files.set(name, data.toString('utf8'));
    cursor += 46 + nameLength + extraLength + commentLength;
  }
  return files;
}

function sameBytes(left, right) {
  return left.length === right.length && left.equals(right);
}

export async function build({ inputPath, outputPath, replace = false }) {
  const contract = JSON.parse(await fs.readFile(inputPath, 'utf8'));
  const rendered = renderPackage(contract);
  const zip = createDeterministicZip(rendered.files);
  await fs.mkdir(path.dirname(outputPath), { recursive: true });
  try {
    const existing = await fs.readFile(outputPath);
    if (sameBytes(existing, zip)) {
      return { ok: true, changed: false, output: outputPath, task_id: rendered.contract.task_id, revision: rendered.contract.revision, sha256: sha256(zip) };
    }
    if (!replace) fail(`目标文件已存在但内容不同：${outputPath}；如确认替换，请显式传 --replace`);
  } catch (error) {
    if (error.code !== 'ENOENT') throw error;
  }
  await fs.writeFile(outputPath, zip);
  return { ok: true, changed: true, output: outputPath, task_id: rendered.contract.task_id, revision: rendered.contract.revision, sha256: sha256(zip) };
}

export async function verify(zipPath) {
  const files = readDeterministicZip(await fs.readFile(zipPath));
  const names = [...files.keys()].sort((left, right) => left.localeCompare(right, 'en'));
  const expectedNames = [...REQUIRED_PACKAGE_FILES].sort((left, right) => left.localeCompare(right, 'en'));
  if (names.join('\0') !== expectedNames.join('\0')) fail(`包文件列表不一致：应为 ${expectedNames.join(', ')}`);
  let contract;
  let manifest;
  try {
    contract = JSON.parse(files.get('任务合同.json'));
    manifest = JSON.parse(files.get('MANIFEST.json'));
  } catch {
    fail('任务合同或清单不是有效 JSON');
  }
  const expected = renderPackage(contract);
  if (manifest.spec !== 'task-sync-manifest/1' || manifest.renderer_version !== RENDERER_VERSION) fail('清单版本不受支持');
  if (manifest.task_contract_sha256 !== expected.contractHash) fail('任务合同哈希不一致');
  const expectedManifest = JSON.parse(expected.files.get('MANIFEST.json'));
  if (canonicalJson(manifest) !== canonicalJson(expectedManifest)) fail('清单内容与合同投影不一致');
  for (const [name, content] of expected.files) {
    if (files.get(name) !== content) fail(`投影与任务合同发生漂移：${name}`);
  }
  return { ok: true, task_id: expected.contract.task_id, revision: expected.contract.revision, contract_sha256: expected.contractHash, files: names };
}

function parseArgs(argv) {
  const [command, ...rest] = argv;
  const options = { command, replace: false };
  for (let index = 0; index < rest.length; index += 1) {
    const item = rest[index];
    if (item === '--replace') options.replace = true;
    else if (item === '--input' || item === '--out') {
      if (!rest[index + 1]) fail(`${item} 缺少参数`);
      options[item.slice(2)] = rest[index + 1];
      index += 1;
    } else fail(`未知参数：${item}`);
  }
  return options;
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.command !== 'build' || !options.input || !options.out) {
    fail('用法：node scripts/task-sync-pack.mjs build --input <任务合同.json> --out <任务.task-sync.zip> [--replace]');
  }
  process.stdout.write(`${JSON.stringify(await build({ inputPath: options.input, outputPath: options.out, replace: options.replace }))}\n`);
}

const invokedPath = process.argv[1] && path.resolve(process.argv[1]);
if (invokedPath === fileURLToPath(import.meta.url)) {
  main().catch((error) => {
    process.stderr.write(`task-sync-pack: ${error.message}\n`);
    process.exitCode = 1;
  });
}
