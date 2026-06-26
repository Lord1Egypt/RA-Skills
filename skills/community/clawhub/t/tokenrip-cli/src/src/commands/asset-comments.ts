import { requireAuthClient } from '../auth-client.js';
import { outputSuccess } from '../output.js';
import { formatMessageSent, formatMessages } from '../formatters.js';
import { parseAssetId } from '../parse-asset-id.js';

export async function assetComment(
  input: string,
  message: string,
  options: { intent?: string; type?: string; versionId?: string },
): Promise<void> {
  const uuid = parseAssetId(input);
  const { client } = requireAuthClient();

  const payload: Record<string, unknown> = { body: message };
  if (options.intent) payload.intent = options.intent;
  if (options.type) payload.type = options.type;
  if (options.versionId) payload.on_version_id = options.versionId;

  const { data } = await client.post(`/v0/assets/${uuid}/messages`, payload);
  outputSuccess(data.data, formatMessageSent);
}

export async function assetComments(
  input: string,
  options: { since?: string; limit?: string },
): Promise<void> {
  const uuid = parseAssetId(input);
  const { client } = requireAuthClient();

  const params: Record<string, string> = {};
  if (options.since) params.since_sequence = options.since;
  if (options.limit) params.limit = options.limit;

  const { data } = await client.get(`/v0/assets/${uuid}/messages`, { params });
  outputSuccess(data.data as unknown as Record<string, unknown>, formatMessages);
}
