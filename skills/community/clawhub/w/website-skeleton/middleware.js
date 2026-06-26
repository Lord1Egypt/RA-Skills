/**
 * Platform Middleware — 支付回调路径放行
 *
 * EdgeOne Pages 自动识别此文件并作为 Platform Middleware 运行。
 */

export async function onRequest(context) {
  try {
    const { request, next } = context;
    const url = new URL(request.url);

    // 支付回调独立路径放行（没有 JWT，不能进 Edge Middleware）
    if (url.pathname === '/api/pay/wx-notify' || url.pathname === '/api/pay/ali-notify') {
      return await next();
    }

    // 其他路径正常传递
    return await next();
  } catch (err) {
    console.error('[Middleware] Error:', err);
    return await context.next();
  }
}
