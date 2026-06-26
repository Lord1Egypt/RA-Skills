import { requireAuthClient } from '../auth-client.js';
import { outputSuccess } from '../output.js';
import { formatSearchResults } from '../formatters.js';

export async function search(
  query: string,
  options: {
    type?: string;
    since?: string;
    limit?: string;
    offset?: string;
    state?: string;
    intent?: string;
    ref?: string;
    assetType?: string;
    archived?: boolean;
    includeArchived?: boolean;
  },
): Promise<void> {
  const { client } = requireAuthClient();
  const params: Record<string, string> = { q: query };
  if (options.type) params.type = options.type;
  if (options.since) params.since = options.since;
  if (options.limit) params.limit = options.limit;
  if (options.offset) params.offset = options.offset;
  if (options.state) params.state = options.state;
  if (options.intent) params.intent = options.intent;
  if (options.ref) params.ref = options.ref;
  if (options.assetType) params.asset_type = options.assetType;
  if (options.archived) params.archived = 'true';
  if (options.includeArchived) params.include_archived = 'true';

  const { data } = await client.get('/v0/search', { params });
  outputSuccess(data.data, formatSearchResults);
}
