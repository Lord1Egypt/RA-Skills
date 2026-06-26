import { requireAuthClient } from '../auth-client.js';
import { outputSuccess } from '../output.js';
import { formatAssetDeleted } from '../formatters.js';
import { parseAssetId } from '../parse-asset-id.js';

export async function deleteAsset(identifier: string, options: { dryRun?: boolean } = {}): Promise<void> {
  const id = parseAssetId(identifier);
  if (options.dryRun) {
    outputSuccess({ dryRun: true, action: 'would delete', id }, formatAssetDeleted);
    return;
  }

  const { client } = requireAuthClient();
  await client.delete(`/v0/assets/${id}`);

  outputSuccess({ id, deleted: true }, formatAssetDeleted);
}
