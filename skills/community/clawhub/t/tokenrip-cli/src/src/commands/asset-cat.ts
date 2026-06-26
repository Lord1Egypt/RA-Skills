import { optionalAuthClient } from '../auth-client.js';
import { parseAssetId } from '../parse-asset-id.js';

export async function assetCat(
  input: string,
  options: { version?: string },
): Promise<void> {
  const identifier = parseAssetId(input);
  const { client } = optionalAuthClient();

  const endpoint = options.version
    ? `/v0/assets/${identifier}/versions/${options.version}/content`
    : `/v0/assets/${identifier}/content`;

  const response = await client.get(endpoint, { responseType: 'arraybuffer' });

  process.stdout.write(Buffer.from(response.data));
}
