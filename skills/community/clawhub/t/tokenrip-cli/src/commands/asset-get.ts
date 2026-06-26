import { optionalAuthClient } from '../auth-client.js';
import { outputSuccess } from '../output.js';
import { formatAssetMetadata } from '../formatters.js';

export async function assetGet(uuid: string): Promise<void> {
  const { client } = optionalAuthClient();
  const { data } = await client.get(`/v0/assets/${uuid}`);
  outputSuccess(data.data, formatAssetMetadata);
}
