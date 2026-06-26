#!/usr/bin/env node
const { readJsonArg, createCos, getBucketConfig, print } = require('./lib');

async function main() {
  const input = readJsonArg(2, 'input');
  if (!input.object_key) throw new Error('object_key is required');

  const cos = createCos();
  const { bucket, region } = getBucketConfig();
  const expires = Number(input.expire_time || 3600);

  const url = cos.getObjectUrl({
    Bucket: bucket,
    Region: region,
    Key: input.object_key,
    Sign: true,
    Expires: expires,
  });

  print({
    success: true,
    action: 'generate_signed_url',
    key: input.object_key,
    expire_time: expires,
    url,
  });
}

main().catch((error) => {
  console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
  process.exit(1);
});
