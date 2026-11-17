'use strict';
const fs = require('fs');
const MAX_INPUT_BYTES = 50 * 1024 * 1024;
function checkSize(size) {
  if (!Number.isSafeInteger(size) || size < 0 || size > MAX_INPUT_BYTES) {
    throw new Error('本地文件超过 50 MiB 限制或大小无效');
  }
}
function readClassifiedFileBuffer(classified) {
  if (!classified || classified.kind !== 'file' || typeof classified.path !== 'string') {
    throw new Error('readClassifiedFileBuffer: expected a classifyInput()-vetted file descriptor');
  }
  checkSize(classified.sizeBytes);
  // Validate the opened descriptor, not just earlier path metadata. Nonblocking
  // prevents a file replaced with a FIFO from hanging before fstat can reject it.
  const fd = fs.openSync(classified.path, fs.constants.O_RDONLY | (fs.constants.O_NONBLOCK || 0));
  try {
    const stat = fs.fstatSync(fd);
    if (!stat.isFile()) throw new Error('只支持普通文件');
    checkSize(stat.size);
    const buffer = Buffer.alloc(stat.size);
    let offset = 0;
    while (offset < buffer.length) {
      const n = fs.readSync(fd, buffer, offset, buffer.length - offset, null);
      if (!n) throw new Error('文件在读取期间发生变化，请重试');
      offset += n;
    }
    // Never grow the allocation even if the source grows after fstat.
    if (fs.readSync(fd, Buffer.alloc(1), 0, 1, null) !== 0) {
      throw new Error('文件在读取期间发生变化，请重试');
    }
    return buffer;
  } finally {
    fs.closeSync(fd);
  }
}
module.exports = { MAX_INPUT_BYTES, readClassifiedFileBuffer };
