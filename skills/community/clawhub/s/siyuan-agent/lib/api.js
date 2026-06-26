const BASE = process.env.SIYUAN_BASE || "http://127.0.0.1:6806";

if (!process.env.SIYUAN_TOKEN) {
  console.error("SIYUAN_TOKEN environment variable is not set");
  process.exit(1);
}

const TOKEN = process.env.SIYUAN_TOKEN;

export async function call(pathName, body = {}) {
  const res = await fetch(`${BASE}${pathName}`, {
    method: "POST",
    headers: {
      Authorization: `token ${TOKEN}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify(body)
  });
  const data = await res.json();
  return data;
}
