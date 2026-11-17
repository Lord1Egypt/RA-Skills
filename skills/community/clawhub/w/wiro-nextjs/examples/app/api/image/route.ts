// app/api/image/route.ts
import { connection } from 'next/server';
import { getPrices, priceFor, priceLabel } from '../../../lib/models';
import { runModel } from '../../../lib/wiro';

// The server picks the model and its settings. The browser sends only the prompt.
const MODEL = 'pruna/p-image';
const SETTINGS = { aspectRatio: '1:1' };

/** The price the page shows before the run, such as "$0.005 per run". */
export async function GET() {
  await connection(); // answer per request, not once at build time
  const row = priceFor(await getPrices(MODEL), SETTINGS);
  return Response.json({ price: row ? priceLabel(row) : null });
}

export async function POST(request: Request) {
  const { prompt } = (await request.json().catch(() => ({}))) as { prompt?: unknown };
  if (typeof prompt !== 'string' || !prompt.trim() || prompt.length > 2000) {
    return Response.json({ error: 'Send a prompt of up to 2,000 characters.' }, { status: 400 });
  }
  try {
    const token = await runModel(MODEL, { prompt, ...SETTINGS });
    return Response.json({ token }); // the task token goes to the browser, the key never does
  } catch (error) {
    console.error(error);
    return Response.json({ error: 'Could not start the run.' }, { status: 502 });
  }
}
