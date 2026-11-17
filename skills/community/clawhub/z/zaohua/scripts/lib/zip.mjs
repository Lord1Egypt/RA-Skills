import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { listFilesRecursive, portableRelativePath } from "./files.mjs";

const CRC_TABLE = Array.from({ length: 256 }, (_, index) => {
  let value = index;
  for (let bit = 0; bit < 8; bit += 1) value = (value & 1) ? (0xedb88320 ^ (value >>> 1)) : (value >>> 1);
  return value >>> 0;
});

function crc32(buffer) {
  let crc = 0xffffffff;
  for (const byte of buffer) crc = CRC_TABLE[(crc ^ byte) & 0xff] ^ (crc >>> 8);
  return (crc ^ 0xffffffff) >>> 0;
}

function localHeader(name, data, crc) {
  const header = Buffer.alloc(30);
  header.writeUInt32LE(0x04034b50, 0);
  header.writeUInt16LE(20, 4);
  header.writeUInt16LE(0x0800, 6);
  header.writeUInt16LE(0, 8);
  header.writeUInt16LE(0, 10);
  header.writeUInt16LE(33, 12);
  header.writeUInt32LE(crc, 14);
  header.writeUInt32LE(data.length, 18);
  header.writeUInt32LE(data.length, 22);
  header.writeUInt16LE(name.length, 26);
  header.writeUInt16LE(0, 28);
  return header;
}

function centralHeader(name, data, crc, offset) {
  const header = Buffer.alloc(46);
  header.writeUInt32LE(0x02014b50, 0);
  header.writeUInt16LE(20, 4);
  header.writeUInt16LE(20, 6);
  header.writeUInt16LE(0x0800, 8);
  header.writeUInt16LE(0, 10);
  header.writeUInt16LE(0, 12);
  header.writeUInt16LE(33, 14);
  header.writeUInt32LE(crc, 16);
  header.writeUInt32LE(data.length, 20);
  header.writeUInt32LE(data.length, 24);
  header.writeUInt16LE(name.length, 28);
  header.writeUInt16LE(0, 30);
  header.writeUInt16LE(0, 32);
  header.writeUInt16LE(0, 34);
  header.writeUInt16LE(0, 36);
  header.writeUInt32LE(0, 38);
  header.writeUInt32LE(offset, 42);
  return header;
}

function endRecord(fileCount, centralSize, centralOffset) {
  const record = Buffer.alloc(22);
  record.writeUInt32LE(0x06054b50, 0);
  record.writeUInt16LE(0, 4);
  record.writeUInt16LE(0, 6);
  record.writeUInt16LE(fileCount, 8);
  record.writeUInt16LE(fileCount, 10);
  record.writeUInt32LE(centralSize, 12);
  record.writeUInt32LE(centralOffset, 16);
  record.writeUInt16LE(0, 20);
  return record;
}

export async function createZipFromDirectory(sourceDirectory, outputFile, rootName) {
  const outputAbsolute = path.resolve(outputFile);
  const files = (await listFilesRecursive(sourceDirectory))
    .filter((file) => path.resolve(file.absolute) !== outputAbsolute);
  if (files.length === 0) throw new Error(`Cannot package an empty directory: ${sourceDirectory}`);
  if (files.length > 65535) throw new Error("ZIP64 is not supported; the package contains too many files.");
  const root = portableRelativePath(rootName);
  const localParts = [];
  const centralParts = [];
  let localOffset = 0;

  for (const file of files) {
    const data = await readFile(file.absolute);
    if (data.length > 0xffffffff) throw new Error(`ZIP64 is not supported for ${file.relative}.`);
    const name = Buffer.from(`${root}/${portableRelativePath(file.relative)}`, "utf8");
    const crc = crc32(data);
    const local = localHeader(name, data, crc);
    localParts.push(local, name, data);
    const central = centralHeader(name, data, crc, localOffset);
    centralParts.push(central, name);
    localOffset += local.length + name.length + data.length;
  }

  const localData = Buffer.concat(localParts);
  const centralData = Buffer.concat(centralParts);
  const archive = Buffer.concat([localData, centralData, endRecord(files.length, centralData.length, localData.length)]);
  await mkdir(path.dirname(outputFile), { recursive: true });
  await writeFile(outputFile, archive);
  return { outputFile, bytes: archive.length, files: files.length };
}
