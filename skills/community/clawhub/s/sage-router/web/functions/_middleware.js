const MARKETING_HOSTS = new Set(['sagerouter.dev', 'www.sagerouter.dev']);
const APP_HOST = 'app.sagerouter.dev';
const APP_ONLY_PATHS = new Set([
  '/account',
  '/account.html',
  '/login',
  '/login.html',
  '/analytics',
  '/analytics.html',
  '/launch-funnel',
  '/launch-funnel.html',
]);

export async function onRequest(context) {
  const url = new URL(context.request.url);
  if (MARKETING_HOSTS.has(url.hostname) && APP_ONLY_PATHS.has(url.pathname)) {
    url.hostname = APP_HOST;
    return Response.redirect(url.toString(), 308);
  }
  return context.next();
}
