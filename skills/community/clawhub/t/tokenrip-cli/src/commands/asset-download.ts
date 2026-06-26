import fs from 'node:fs';
import path from 'node:path';
import mime from 'mime-types';
import { optionalAuthClient } from '../auth-client.js';
import { outputSuccess } from '../output.js';
import { formatAssetDownloaded } from '../formatters.js';

export async function assetDownload(
  uuid: string,
  options: { output?: string; version?: string },
): Promise<void> {
  const { client } = optionalAuthClient();

  const endpoint = options.version
    ? `/v0/assets/${uuid}/versions/${options.version}/content`
    : `/v0/assets/${uuid}/content`;

  const response = await client.get(endpoint, { responseType: 'arraybuffer' });

  const contentType = response.headers['content-type'] || 'application/octet-stream';
  const ext = mime.extension(contentType) || 'bin';

  const outPath = path.resolve(options.output || `${uuid}.${ext}`);

  fs.writeFileSync(outPath, Buffer.from(response.data));

  outputSuccess(
    { file: outPath, sizeBytes: response.data.byteLength, mimeType: contentType },
    formatAssetDownloaded,
  );
}
