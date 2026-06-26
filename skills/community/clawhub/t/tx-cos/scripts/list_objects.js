#!/usr/bin/env node
const { readJsonArg, createCos, getBucketConfig, print } = require('./lib');

function call(cos, params) {
  return new Promise((resolve, reject) => {
    cos.getBucket(params, (err, data) => {
      if (err) reject(err);
      else resolve(data);
    });
  });
}

async function main() {
  const input = readJsonArg(2, 'input');
  const cos = createCos();
  const { bucket, region } = getBucketConfig();
  const data = await call(cos, {
    Bucket: bucket,
    Region: region,
    Prefix: input.prefix || '',
    Delimiter: input.delimiter || '',
    MaxKeys: Number(input.max_keys || 100),
  });

  print({
    success: true,
    action: 'list_objects',
    prefix: input.prefix || '',
    files: data.Contents || [],
    folders: data.CommonPrefixes || [],
    truncated: Boolean(data.IsTruncated),
  });
}

main().catch((error) => {
  console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
  process.exit(1);
});
