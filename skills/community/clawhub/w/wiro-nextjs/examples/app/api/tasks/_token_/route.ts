// app/api/tasks/[token]/route.ts
import { getTask, isFinal, succeeded } from '../../../../lib/wiro';

/** The browser polls this with the task token every few seconds. */
export async function GET(_request: Request, { params }: { params: Promise<{ token: string }> }) {
  const { token } = await params;
  if (!/^[\w-]{8,200}$/.test(token)) return Response.json({ error: 'Not a task token.' }, { status: 400 });
  try {
    const task = await getTask({ tasktoken: token });
    if (!task) return Response.json({ error: 'There is no such task.' }, { status: 404 });
    const files = (task.outputs ?? []).flatMap((output) => (output.url ? [output.url] : []));
    return Response.json(
      {
        status: task.status,
        done: isFinal(task),
        ok: succeeded(task),
        files,
        // An LLM answers in debugoutput. For models that make files it only holds logs.
        text: files.length === 0 && task.debugoutput ? task.debugoutput : null,
        cost: isFinal(task) ? Number(task.totalcost ?? 0) : null,
      },
      { headers: { 'Cache-Control': 'no-store' } },
    );
  } catch (error) {
    console.error(error);
    return Response.json({ error: 'Could not read the task.' }, { status: 502 });
  }
}
