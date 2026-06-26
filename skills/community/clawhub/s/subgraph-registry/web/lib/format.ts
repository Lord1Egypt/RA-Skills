export function fmtUSD(n: number, opts?: { precise?: boolean }): string {
  if (!Number.isFinite(n)) return "$0";
  if (opts?.precise) {
    return n.toLocaleString("en-US", {
      style: "currency",
      currency: "USD",
      minimumFractionDigits: 4,
      maximumFractionDigits: 4,
    });
  }
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(2)}M`;
  if (n >= 1_000) return `$${(n / 1_000).toFixed(2)}k`;
  return n.toLocaleString("en-US", { style: "currency", currency: "USD" });
}

export function fmtInt(n: number): string {
  if (!Number.isFinite(n)) return "0";
  return n.toLocaleString("en-US");
}

export function fmtPct(n: number, signed = false): string {
  if (!Number.isFinite(n)) return "0%";
  const sign = signed && n > 0 ? "+" : "";
  return `${sign}${n.toFixed(1)}%`;
}

export function shortAddr(addr: string | null | undefined, head = 6, tail = 4): string {
  if (!addr) return "";
  const a = String(addr).toLowerCase();
  if (a.length <= head + tail + 2) return a;
  return `${a.slice(0, head)}…${a.slice(-tail)}`;
}

export function timeAgo(iso: string | Date | number | null | undefined): string {
  if (!iso) return "never";
  const t = iso instanceof Date ? iso.getTime() : typeof iso === "number" ? iso : Date.parse(String(iso));
  if (!Number.isFinite(t)) return "?";
  const diff = Math.max(0, Date.now() - t);
  const s = Math.floor(diff / 1000);
  if (s < 60) return `${s}s ago`;
  const m = Math.floor(s / 60);
  if (m < 60) return `${m}m ago`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h}h ago`;
  const d = Math.floor(h / 24);
  if (d < 30) return `${d}d ago`;
  return new Date(t).toLocaleDateString();
}

// Deterministic HSL gradient avatar from a wallet — same wallet = same colors
export function walletGradient(wallet: string): { from: string; to: string } {
  const h1 = hashStr(wallet) % 360;
  const h2 = (h1 + 47) % 360;
  return {
    from: `hsl(${h1} 70% 55%)`,
    to: `hsl(${h2} 70% 45%)`,
  };
}

function hashStr(s: string): number {
  let h = 0;
  for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0;
  return Math.abs(h);
}
