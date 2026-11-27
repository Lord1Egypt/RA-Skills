// Central network/path policy. Only operator-configured Theta HTTPS origins;
// redirects are separately disabled at every transport boundary.
export function thetaUrl(raw: string, kind: 'ondemand' | 'dedicated'): string {
  let u: URL;
  try { u = new URL(raw); } catch { throw new Error('Invalid Theta endpoint URL'); }
  const allowed = kind === 'ondemand'
    ? u.hostname === 'ondemand.thetaedgecloud.com'
    : u.hostname.endsWith('.thetaedgecloud.com') || u.hostname.endsWith('.onthetaedgecloud.com');
  if (u.protocol !== 'https:' || !allowed || u.username || u.password || (u.port && u.port !== '443') || u.search || u.hash || (u.pathname !== '/' && u.pathname !== '')) {
    throw new Error('Theta endpoint must be an approved HTTPS origin without credentials, path, query, or fragment');
  }
  return u.origin;
}

// Runtime enum check: a TypeScript cast is not validation. Anything other than the exact strings
// 'openai' or 'gradio' (or undefined -> 'openai') is refused before any request is made.
export type ReadyProbe = 'openai' | 'gradio';
export function validateProbe(value: unknown): ReadyProbe {
  if (value === undefined) return 'openai';
  if (value === 'openai' || value === 'gradio') return value;
  throw new Error('probe must be exactly "openai" or "gradio"');
}

export function pathSegment(value: string, label: string): string {
  if (typeof value !== 'string' || !value.trim() || value.trim() === '.' || value.trim() === '..' || /[\x00-\x1f\x7f]/.test(value)) throw new Error(('' + String(label) + ' must be a non-empty string and safe identifier'));
  return encodeURIComponent(value.trim());
}
