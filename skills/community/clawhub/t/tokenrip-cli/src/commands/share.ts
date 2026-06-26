import { loadIdentity } from '../identity.js';
import { createCapabilityToken } from '../crypto.js';
import { getFrontendUrl, loadConfig } from '../config.js';
import { CliError } from '../errors.js';
import { outputSuccess } from '../output.js';
import { formatShareLink } from '../formatters.js';

export function parseDuration(s: string): number {
  const match = s.match(/^(\d+)(s|m|h|d)$/);
  if (!match) throw new CliError('INVALID_DURATION', `Invalid duration: ${s}. Use e.g. 1h, 7d, 30m`);
  const n = parseInt(match[1], 10);
  const unit = match[2];
  const multipliers: Record<string, number> = { s: 1, m: 60, h: 3600, d: 86400 };
  return Math.floor(Date.now() / 1000) + n * multipliers[unit];
}

export async function share(
  assetId: string,
  options: { commentOnly?: boolean; expires?: string; for?: string },
): Promise<void> {
  const identity = loadIdentity();
  if (!identity) {
    throw new CliError('NO_IDENTITY', 'No agent identity found. Run `rip auth register` first.');
  }

  const perm = options.commentOnly ? ['comment'] : ['comment', 'version:create'];
  const exp = options.expires ? parseDuration(options.expires) : undefined;
  const aud = options.for || undefined;

  const token = createCapabilityToken(
    { sub: `asset:${assetId}`, iss: identity.agentId, perm, exp, aud },
    identity.secretKey,
  );

  const frontendUrl = getFrontendUrl(loadConfig());
  const url = `${frontendUrl}/s/${assetId}?cap=${encodeURIComponent(token)}`;

  outputSuccess({ url, token, assetId, perm, exp: exp ?? null, aud: aud ?? null }, formatShareLink);
}
