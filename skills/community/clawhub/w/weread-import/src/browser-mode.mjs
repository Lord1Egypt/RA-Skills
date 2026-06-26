export function normalizeCookieSource(cookieFrom = 'manual') {
  const value = String(cookieFrom || 'manual').trim().toLowerCase();
  if (value === 'browser') return 'browser-managed';
  if (value === 'browser-live') return 'browser-live';
  if (value === 'browser-managed') return 'browser-managed';
  return 'manual';
}

export function isBrowserCookieMode(cookieFrom) {
  return normalizeCookieSource(cookieFrom) !== 'manual';
}

export function isManagedBrowserMode(cookieFrom) {
  return normalizeCookieSource(cookieFrom) === 'browser-managed';
}

export function isLiveBrowserMode(cookieFrom) {
  return normalizeCookieSource(cookieFrom) === 'browser-live';
}
