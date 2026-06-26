#!/usr/bin/env node
const { readJsonArg, createCos, getBucketConfig, buildUrl, print } = require('./lib');

function call(cos, method, params) {
  return new Promise((resolve, reject) => {
    cos[method](params, (err, data) => {
      if (err) reject(err);
      else resolve(data);
    });
  });
}

async function main() {
  const input = readJsonArg(2, 'input');
  if (!input.action) throw new Error('action is required');

  const cos = createCos();
  const { bucket, region } = getBucketConfig();

  if (input.action === 'delete') {
    if (!input.object_key) throw new Error('object_key is required');
    const data = await call(cos, 'deleteObject', {
      Bucket: bucket,
      Region: region,
      Key: input.object_key,
    });
    return print({ success: true, action: 'delete', key: input.object_key, data });
  }

  if (input.action === 'delete_multiple') {
    if (!Array.isArray(input.object_keys) || !input.object_keys.length) {
      throw new Error('object_keys is required');
    }
    const data = await call(cos, 'deleteMultipleObject', {
      Bucket: bucket,
      Region: region,
      Objects: input.object_keys.map((Key) => ({ Key })),
    });
    return print({ success: true, action: 'delete_multiple', total: input.object_keys.length, data });
  }

  if (input.action === 'copy' || input.action === 'move' || input.action === 'rename') {
    const sourceKey = input.source_key || input.old_key;
    const targetKey = input.target_key || input.new_key;
    if (!sourceKey || !targetKey) throw new Error('source/target key is required');
    const sourceBucket = input.target_bucket || bucket;
    const copySource = `${sourceBucket}.cos.${region}.myqcloud.com/${encodeURI(sourceKey).replace(/#/g, '%23')}`;
    const copyData = await call(cos, 'putObjectCopy', {
      Bucket: bucket,
      Region: region,
      Key: targetKey,
      CopySource: copySource,
    });
    if (input.action === 'move' || input.action === 'rename') {
      await call(cos, 'deleteObject', { Bucket: bucket, Region: region, Key: sourceKey });
    }
    return print({
      success: true,
      action: input.action,
      source_key: sourceKey,
      target_key: targetKey,
      url: buildUrl(targetKey),
      data: copyData,
    });
  }

  if (input.action === 'create_folder') {
    if (!input.folder_path) throw new Error('folder_path is required');
    const key = input.folder_path.endsWith('/') ? input.folder_path : `${input.folder_path}/`;
    const data = await call(cos, 'putObject', {
      Bucket: bucket,
      Region: region,
      Key: key,
      Body: '',
    });
    return print({ success: true, action: 'create_folder', key, data });
  }

  throw new Error(`Unsupported action: ${input.action}`);
}

main().catch((error) => {
  console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
  process.exit(1);
});
