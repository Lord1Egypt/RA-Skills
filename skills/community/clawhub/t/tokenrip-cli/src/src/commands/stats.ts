import { requireAuthClient } from '../auth-client.js';
import { outputSuccess } from '../output.js';
import { formatStats } from '../formatters.js';

export async function stats(): Promise<void> {
  const { client } = requireAuthClient();
  const { data } = await client.get('/v0/assets/stats');

  outputSuccess(data.data, formatStats);
}
