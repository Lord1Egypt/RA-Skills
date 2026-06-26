import { requireAuthClient } from '../auth-client.js';
import { outputSuccess } from '../output.js';
import { formatAssetDeleted } from '../formatters.js';

export async function deleteAsset(uuid: string, options: { dryRun?: boolean } = {}): Promise<void> {
  if (options.dryRun) {
    outputSuccess({ dryRun: true, action: 'would delete', id: uuid }, formatAssetDeleted);
    return;
  }

  const { client } = requireAuthClient();
  await client.delete(`/v0/assets/${uuid}`);

  outputSuccess({ id: uuid, deleted: true }, formatAssetDeleted);
}
