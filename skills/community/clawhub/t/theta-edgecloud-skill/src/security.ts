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

export function pathSegment(value: string, label: string): string {
  if (typeof value !== 'string' || !value.trim() || value.trim() === '.' || value.trim() === '..' || /[\x00-\x1f\x7f]/.test(value)) throw new Error(`${label} must be a non-empty string and safe identifier`);
  return encodeURIComponent(value.trim());
}
