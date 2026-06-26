import { requireAuthClient } from '../auth-client.js';
import { outputSuccess } from '../output.js';
import { parseAssetId } from '../parse-asset-id.js';

export async function archiveAsset(identifier: string): Promise<void> {
  const id = parseAssetId(identifier);
  const { client } = requireAuthClient();
  await client.post(`/v0/assets/${id}/archive`);
  outputSuccess({ id, state: 'archived' });
}

export async function unarchiveAsset(identifier: string): Promise<void> {
  const id = parseAssetId(identifier);
  const { client } = requireAuthClient();
  await client.post(`/v0/assets/${id}/unarchive`);
  outputSuccess({ id, state: 'published' });
}
