#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const {
  readJsonArg,
  ensureFile,
  walkFiles,
  createCos,
  getBucketConfig,
  buildUrl,
  print,
} = require('./lib');

async function uploadOne(cos, bucket, region, filePath, key, customDomain) {
  const body = fs.readFileSync(filePath);
  const response = await cos.putObject({ Bucket: bucket, Region: region, Key: key, Body: body });
  return {
    file_path: filePath,
    key,
    size: body.length,
    etag: response.ETag,
    url: buildUrl(key, customDomain),
  };
}

async function main() {
  const input = readJsonArg(2, 'input');
  const cos = createCos();
  const { bucket, region } = getBucketConfig();
  const concurrency = Math.max(1, Math.min(10, Number(input.concurrency || 3)));

  let items = [];
  if (Array.isArray(input.files) && input.files.length) {
    items = input.files.map((item) => ({
      file_path: item.file_path,
      object_key: item.object_key,
    }));
  } else if (input.dir_path) {
    const baseDir = path.resolve(input.dir_path);
    items = walkFiles(baseDir).map((filePath) => ({
      file_path: filePath,
      object_key: path.posix.join(input.prefix || '', path.relative(baseDir, filePath).split(path.sep).join('/')),
    }));
  } else {
    throw new Error('files or dir_path is required');
  }

  const queue = items.map((item) => {
    ensureFile(item.file_path);
    return item;
  });

  const results = [];
  const errors = [];
  let index = 0;

  async function worker() {
    while (index < queue.length) {
      const current = queue[index++];
      const key = current.object_key || path.basename(current.file_path);
      try {
        const result = await uploadOne(cos, bucket, region, current.file_path, key, input.custom_domain);
        results.push(result);
      } catch (error) {
        errors.push({ file_path: current.file_path, key, error: error.message });
      }
    }
  }

  await Promise.all(Array.from({ length: Math.min(concurrency, queue.length || 1) }, worker));

  print({
    success: errors.length === 0,
    action: 'upload_batch',
    total: queue.length,
    succeeded: results.length,
    failed: errors.length,
    results,
    errors,
  });
}

main().catch((error) => {
  console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
  process.exit(1);
});
