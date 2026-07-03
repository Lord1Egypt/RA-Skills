/**
 * RealBrowser by Ceki — Node.js / TypeScript quickstart.
 *
 * Rent a real Chrome from the marketplace, navigate, stop.
 *
 * Requirements:
 *   npm install ceki
 *
 * Env:
 *   CEKI_API_KEY — your API key from https://ceki.me dashboard
 */

import { Browser } from 'ceki';

async function main() {
  const token = process.env.CEKI_API_KEY;
  if (!token) {
    throw new Error('Set CEKI_API_KEY env var (get one at https://ceki.me)');
  }

  const br = new Browser({
    token,
    relayUrl: 'wss://browser.ceki.me/ws/agent',
    apiUrl: 'https://api.ceki.me',
  });
  await br.connect();

  const options = await br.search({});
  if (options.length === 0) {
    console.log('No browsers online. Try again in a moment.');
    await br.close();
    return;
  }

  console.log(`Renting browser scheduleId=${options[0].scheduleId}...`);
  const session = await br.rent(options[0].scheduleId);

  try {
    await session.send({
      method: 'Page.navigate',
      params: { url: 'https://example.com' },
    });
    console.log('Navigated. Session id:', session.id);
  } finally {
    await session.close();
    await br.close();
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
