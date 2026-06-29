// ===== PWA Generator — Workers API Template =====
// Replace __TABLE__ and __FIELDS__ with actual values
// This file goes to: functions/api/__TABLE__.js

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET,POST,DELETE,OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

export async function onRequestOptions() {
  return new Response(null, { headers: CORS });
}

export async function onRequestGet({ env }) {
  const { results } = await env.DB.prepare('SELECT * FROM __TABLE__ ORDER BY updatedAt DESC').all();
  return Response.json(results, { headers: CORS });
}

export async function onRequestPost({ request, env }) {
  const item = await request.json();
  if (!item.id) item.id = 'id-' + Date.now();

  // __INSERT_STATEMENT__
  // Example:
  // await env.DB.prepare(`
  //   INSERT OR REPLACE INTO __TABLE__ (id, name, status, ..., updatedAt)
  //   VALUES (?, ?, ?, ..., unixepoch())
  // `).bind(item.id, item.name||'', item.status||'', ...).run();

  return Response.json({ ok: true, id: item.id }, { headers: CORS });
}

export async function onRequestDelete({ request, env }) {
  const url = new URL(request.url);
  const id = url.searchParams.get('id');
  if (!id) return Response.json({ error: 'missing id' }, { status: 400, headers: CORS });

  await env.DB.prepare('DELETE FROM __TABLE__ WHERE id = ?').bind(id).run();
  return Response.json({ ok: true }, { headers: CORS });
}
