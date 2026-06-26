#!/usr/bin/env node
const { readJsonArg, createCos, getBucketConfig, print, formatBytes } = require('./lib');

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
  const prefix = input.folder_path ? (input.folder_path.endsWith('/') ? input.folder_path : `${input.folder_path}/`) : '';

  const data = await call(cos, {
    Bucket: bucket,
    Region: region,
    Prefix: prefix,
    MaxKeys: Number(input.max_keys || 1000),
  });

  const files = (data.Contents || []).filter((item) => !String(item.Key).endsWith('/'));
  const totalSize = files.reduce((sum, item) => sum + Number(item.Size || 0), 0);
  const fileTypes = {};
  for (const item of files) {
    const ext = String(item.Key).includes('.') ? String(item.Key).split('.').pop().toLowerCase() : 'unknown';
    fileTypes[ext] = (fileTypes[ext] || 0) + 1;
  }

  print({
    success: true,
    action: 'get_folder_stats',
    folder_path: prefix,
    file_count: files.length,
    total_size: totalSize,
    total_size_formatted: formatBytes(totalSize),
    average_file_size: files.length ? Math.round(totalSize / files.length) : 0,
    file_types: fileTypes,
  });
}

main().catch((error) => {
  console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
  process.exit(1);
});
