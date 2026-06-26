#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const {
  readJsonArg,
  ensureFile,
  createCos,
  getBucketConfig,
  buildUrl,
  print,
} = require('./lib');

async function main() {
  const input = readJsonArg(2, 'input');
  if (!input.file_path) throw new Error('file_path is required');

  ensureFile(input.file_path);
  const cos = createCos();
  const { bucket, region } = getBucketConfig();
  const key = input.object_key || path.basename(input.file_path);
  const body = fs.readFileSync(input.file_path);

  const response = await cos.putObject({
    Bucket: bucket,
    Region: region,
    Key: key,
    Body: body,
  });

  print({
    success: true,
    action: 'upload_file',
    key,
    size: body.length,
    etag: response.ETag,
    location: response.Location,
    url: buildUrl(key, input.custom_domain),
  });
}

main().catch((error) => {
  console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
  process.exit(1);
});
