export async function fetchStats(indexerUrl) {
  const res = await fetch(`${indexerUrl}/api/v1/stats`);
  if (!res.ok) throw new Error(`stats ${res.status}: ${await res.text()}`);
  return res.json();
}

export async function fetchPortfolio(indexerUrl, wallet) {
  const res = await fetch(`${indexerUrl}/api/v1/chibis/by-owner/${wallet}`);
  if (!res.ok) throw new Error(`portfolio ${res.status}: ${await res.text()}`);
  const body = await res.json();
  if (Array.isArray(body)) return body;
  if (Array.isArray(body.chibis)) return body.chibis;
  return [];
}
