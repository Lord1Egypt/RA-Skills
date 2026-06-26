export function getApiKey(): string {
  const key = process.env.STICKYHIVE_API_KEY;
  if (!key) {
    console.error(JSON.stringify({ error: 'STICKYHIVE_API_KEY environment variable is not set.' }));
    process.exit(1);
  }
  return key;
}

export function getBaseUrl(): string {
  return (process.env.STICKYHIVE_API_URL || 'https://app.stickyhive.com').replace(/\/+$/, '');
}
