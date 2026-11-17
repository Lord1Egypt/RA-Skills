// app/api/wiro-webhook/route.ts
import { after } from 'next/server';
import { getTask, succeeded } from '../../../lib/wiro';

/**
 * Wiro POSTs the task here when a run started with `callbackUrl` ends, whether
 * it succeeded or failed. The request is not signed, so treat the body as a
 * hint: match the task id with your own records and read the task again.
 */
export async function POST(request: Request) {
  const body = (await request.json().catch(() => null)) as { id?: unknown } | null;
  const taskid = typeof body?.id === 'string' || typeof body?.id === 'number' ? String(body.id) : null;
  if (taskid && /^\d{1,20}$/.test(taskid)) {
    after(async () => {
      const task = await getTask({ taskid });
      if (task && succeeded(task)) {
        // Find the run you saved for this task id, then store task.outputs and task.totalcost.
      }
    });
  }
  // Answer with a 2xx at once. Anything else makes Wiro try again, up to 3 tries, 2 seconds apart.
  return new Response(null, { status: 204 });
}
