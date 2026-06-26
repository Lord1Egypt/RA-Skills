import { optionalAuthClient } from '../auth-client.js';
import { outputSuccess } from '../output.js';
import { formatVersionList, formatVersionMetadata } from '../formatters.js';

export async function assetVersions(
  uuid: string,
  options: { version?: string },
): Promise<void> {
  const { client } = optionalAuthClient();

  if (options.version) {
    const { data } = await client.get(`/v0/assets/${uuid}/versions/${options.version}`);
    outputSuccess(data.data, formatVersionMetadata);
  } else {
    const { data } = await client.get(`/v0/assets/${uuid}/versions`);
    outputSuccess(data.data as unknown as Record<string, unknown>, formatVersionList);
  }
}
