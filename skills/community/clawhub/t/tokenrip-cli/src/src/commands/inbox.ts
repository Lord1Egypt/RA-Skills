import { requireAuthClient } from '../auth-client.js';
import { CliError } from '../errors.js';
import { outputSuccess } from '../output.js';
import { formatInbox } from '../formatters.js';
import { loadState, saveState } from '../state.js';
import { resolveTeam } from '../teams.js';

function parseSince(value: string): string {
  const num = Number(value);
  if (!isNaN(num) && num > 0 && Number.isInteger(num)) {
    return new Date(Date.now() - num * 86400000).toISOString();
  }
  return value;
}

export async function inbox(options: {
  since?: string;
  types?: string;
  limit?: string;
  clear?: boolean;
  human?: boolean;
  team?: string;
}): Promise<void> {
  const { client } = requireAuthClient();
  const state = loadState();

  const sinceOverride = options.since ? parseSince(options.since) : undefined;
  const since = sinceOverride
    ?? state.lastInboxPoll
    ?? new Date(Date.now() - 86400000).toISOString();

  const params: Record<string, string> = { since };
  if (options.types) params.types = options.types;
  if (options.limit) params.limit = options.limit;
  if (options.team) params.team = resolveTeam(options.team);

  try {
    const { data } = await client.get('/v0/inbox', { params });
    const result = data.data;

    if (options.clear) {
      saveState({ ...state, lastInboxPoll: new Date().toISOString() });
    }

    outputSuccess(result, formatInbox);
  } catch (error) {
    if (error instanceof CliError) throw error;
    throw new CliError('INBOX_FAILED', 'Failed to fetch inbox. Is the server running?');
  }
}
