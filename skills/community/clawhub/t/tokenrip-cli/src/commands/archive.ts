import { requireAuthClient } from '../auth-client.js';
import { outputSuccess } from '../output.js';

export async function archiveAsset(uuid: string): Promise<void> {
  const { client } = requireAuthClient();
  await client.post(`/v0/assets/${uuid}/archive`);
  outputSuccess({ id: uuid, state: 'archived' });
}

export async function unarchiveAsset(uuid: string): Promise<void> {
  const { client } = requireAuthClient();
  await client.post(`/v0/assets/${uuid}/unarchive`);
  outputSuccess({ id: uuid, state: 'published' });
}
