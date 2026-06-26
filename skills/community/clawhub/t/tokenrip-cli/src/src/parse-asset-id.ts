const ASSET_URL_RE = /\/s\/([^/?#\s]+)/i;

export function parseAssetId(input: string): string {
  const match = input.match(ASSET_URL_RE);
  if (match) return match[1];
  return input;
}
