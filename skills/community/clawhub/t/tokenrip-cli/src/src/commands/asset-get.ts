import { optionalAuthClient } from '../auth-client.js';
import { outputSuccess } from '../output.js';
import { formatAssetMetadata } from '../formatters.js';
import { parseAssetId } from '../parse-asset-id.js';

export async function assetGet(input: string): Promise<void> {
  const uuid = parseAssetId(input);
  const { client } = optionalAuthClient();
  const { data } = await client.get(`/v0/assets/${uuid}`);
  outputSuccess(data.data, formatAssetMetadata);
}
