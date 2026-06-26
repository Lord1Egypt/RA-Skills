import { optionalAuthClient } from '../auth-client.js';
import { outputSuccess } from '../output.js';
import { formatVersionList, formatVersionMetadata } from '../formatters.js';
import { parseAssetId } from '../parse-asset-id.js';

export async function assetVersions(
  input: string,
  options: { version?: string },
): Promise<void> {
  const uuid = parseAssetId(input);
  const { client } = optionalAuthClient();

  if (options.version) {
    const { data } = await client.get(`/v0/assets/${uuid}/versions/${options.version}`);
    outputSuccess(data.data, formatVersionMetadata);
  } else {
    const { data } = await client.get(`/v0/assets/${uuid}/versions`);
    outputSuccess(data.data as unknown as Record<string, unknown>, formatVersionList);
  }
}
