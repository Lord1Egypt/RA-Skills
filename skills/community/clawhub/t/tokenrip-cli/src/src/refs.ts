import { CliError } from './errors.js';

const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export interface CliRefInput {
  type: 'asset' | 'url';
  target_id: string;
}

export function parseRefList(refs: string): CliRefInput[] {
  const values = refs
    .split(',')
    .map((value) => value.trim())
    .filter(Boolean);

  return values.map((value) => {
    if (UUID_RE.test(value)) {
      return { type: 'asset', target_id: value };
    }
    if (/^https?:\/\//i.test(value)) {
      return { type: 'url', target_id: value };
    }
    throw new CliError(
      'INVALID_REF',
      `Invalid ref "${value}". Use a full URL or an asset UUID.`,
    );
  });
}
