import { requireAuthClient } from '../auth-client.js';
import { outputSuccess } from '../output.js';
import { formatMessageSent, formatMessages } from '../formatters.js';

export async function assetComment(
  uuid: string,
  message: string,
  options: { intent?: string; type?: string },
): Promise<void> {
  const { client } = requireAuthClient();

  const payload: Record<string, unknown> = { body: message };
  if (options.intent) payload.intent = options.intent;
  if (options.type) payload.type = options.type;

  const { data } = await client.post(`/v0/assets/${uuid}/messages`, payload);
  outputSuccess(data.data, formatMessageSent);
}

export async function assetComments(
  uuid: string,
  options: { since?: string; limit?: string },
): Promise<void> {
  const { client } = requireAuthClient();

  const params: Record<string, string> = {};
  if (options.since) params.since_sequence = options.since;
  if (options.limit) params.limit = options.limit;

  const { data } = await client.get(`/v0/assets/${uuid}/messages`, { params });
  outputSuccess(data.data as unknown as Record<string, unknown>, formatMessages);
}
