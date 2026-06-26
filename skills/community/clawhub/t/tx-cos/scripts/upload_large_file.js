#!/usr/bin/env node
const { readJsonArg, createCos, getBucketConfig, buildUrl, print } = require('./lib');

async function main() {
  const input = readJsonArg(2, 'input');
  if (!input.file_path) throw new Error('file_path is required');

  const cos = createCos();
  const { bucket, region } = getBucketConfig();
  const chunkSize = Math.max(1024 * 1024, Number(input.chunk_size || 1024 * 1024));
  const concurrency = Math.max(1, Math.min(10, Number(input.concurrency || 3)));
  const key = input.object_key || require('path').basename(input.file_path);

  const result = await new Promise((resolve, reject) => {
    let latest = null;
    cos.sliceUploadFile({
      Bucket: bucket,
      Region: region,
      Key: key,
      FilePath: input.file_path,
      ChunkSize: chunkSize,
      AsyncLimit: concurrency,
      onTaskReady(taskId) {
        latest = { task_id: taskId };
      },
      onProgress(progress) {
        latest = {
          ...(latest || {}),
          percent: progress.percent,
          speed: progress.speed || 0,
        };
      },
    }, (err, data) => {
      if (err) reject(err);
      else resolve({ data, latest });
    });
  });

  print({
    success: true,
    action: 'upload_large_file',
    key,
    chunk_size: chunkSize,
    concurrency,
    url: buildUrl(key, input.custom_domain),
    progress: result.latest,
    data: result.data,
  });
}

main().catch((error) => {
  console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
  process.exit(1);
});
