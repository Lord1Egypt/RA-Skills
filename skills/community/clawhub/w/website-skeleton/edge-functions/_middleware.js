/**
 * Edge Functions Middleware — JWT 校验 + 支付回调放行
 */

export async function onRequest(context) {
  const { request } = context;
  const url = new URL(request.url);

  // 公开路径 + Auth + 支付回调放行
  const publicPaths = [
    '/api/products', '/api/categories',
    '/api/auth/login', '/api/auth/register', '/api/auth/refresh',
    '/api/pay/wx-notify', '/api/pay/ali-notify',
  ];
  if (publicPaths.some(p => url.pathname.startsWith(p))) {
    return context.next();
  }

  // 其他路径需要 JWT（由下游 Edge Function 自行校验）
  return context.next();
}
