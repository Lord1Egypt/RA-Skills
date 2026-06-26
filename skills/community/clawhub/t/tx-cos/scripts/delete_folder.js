#!/usr/bin/env node
const { readJsonArg, createCos, getBucketConfig, print } = require('./lib');

function call(cos, method, params) {
  return new Promise((resolve, reject) => {
    cos[method](params, (err, data) => {
      if (err) reject(err);
      else resolve(data);
    });
  });
}

async function listAll(cos, bucket, region, prefix) {
  const data = await call(cos, 'getBucket', {
    Bucket: bucket,
    Region: region,
    Prefix: prefix,
    MaxKeys: 1000,
  });
  return data.Contents || [];
}

async function main() {
  const input = readJsonArg(2, 'input');
  if (!input.folder_path) throw new Error('folder_path is required');

  const cos = createCos();
  const { bucket, region } = getBucketConfig();
  const folderKey = input.folder_path.endsWith('/') ? input.folder_path : `${input.folder_path}/`;

  if (input.recursive) {
    const files = await listAll(cos, bucket, region, folderKey);
    const keys = files.map((item) => ({ Key: item.Key }));
    if (keys.length) {
      await call(cos, 'deleteMultipleObject', {
        Bucket: bucket,
        Region: region,
        Delete: { Objects: keys, Quiet: false },
      });
    } else {
      await call(cos, 'deleteObject', { Bucket: bucket, Region: region, Key: folderKey }).catch(() => null);
    }
    return print({ success: true, action: 'delete_folder', folder_path: folderKey, recursive: true, deleted_count: keys.length });
  }

  await call(cos, 'deleteObject', { Bucket: bucket, Region: region, Key: folderKey });
  print({ success: true, action: 'delete_folder', folder_path: folderKey, recursive: false });
}

main().catch((error) => {
  console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
  process.exit(1);
});
