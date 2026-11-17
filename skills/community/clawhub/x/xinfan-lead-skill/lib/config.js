// 环境配置
// ─────────────────────────────────────────────────────────────────────────────
// 域名：接口服务已正式上线，默认指向生产域名。如需临时指向其他环境，用
// XINFAN_LEAD_DOMAIN 环境变量覆盖即可，不用改代码。
export const DOMAIN =
  process.env.XINFAN_LEAD_DOMAIN || "hawkeye.devops.xiaohongshu.com";

export const BASE_URL = `https://${DOMAIN}`;

// ─────────────────────────────────────────────────────────────────────────────
// 鉴权说明（重要，实测结论 2026-08-05）
//
// 本 skill 采用「浏览器会话通道」鉴权：请求通过当前登录用户本人已登录新帆的浏览器
// 页面发出（见 lib/browserSession.js），身份天然携带。不再依赖任何可搬运的 token/cookie。
//
// 为什么放弃了旧的「token/cookie 搬运」方案（历史踩坑，勿再走回头路）：
//   1) agent 环境自带的 ambient token（~/.token/sso_token.json 里的
//      common-internal-access-token-<tier>）——merchant_lead 接口的 edith 网关
//      SSO 插件不认，无论 beta 还是正式生产域名，均已实测确认不生效。
//   2) 传说中的 access-token-<域名> cookie——在真实环境（beta/prod）里根本不存在。
//      真实登录态是 HttpOnly / localStorage，由前端运行时注入请求头，无法搬运。
//   因此「拼 Cookie 头用 Node fetch 直发」这条路走不通，已彻底移除。
//
// COOKIE_NAME 仅保留给 set-token 兜底路径（极端场景手动注入 cookie 时用），非主路径。
export const COOKIE_NAME =
  process.env.XINFAN_LEAD_COOKIE_NAME || `access-token-${DOMAIN}`;
