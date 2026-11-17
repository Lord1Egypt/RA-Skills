/**
 * entitlement-key.mjs — 本地权益凭证的验签公钥（Ed25519）
 *
 * 设计要点：
 *   - 私钥只存在于服务端（rea402-gateway），永不下发；
 *   - 本文件只有【公钥】，因此技能包只能【验证】凭证真伪，无法【伪造】凭证；
 *   - 签名原文 = `${skill}\n${out_trade_no}\n${expires_at}`，
 *     改到期时间 / 换产品 / 复用他人订单号，任一篡改都会验签失败。
 *
 * 于是本地 `engine/.entitlement.json` 从「明文可手搓」升级为「服务端签发、本地可验不可伪造」。
 */
export const ENTITLEMENT_PUBLIC_KEY_PEM = `-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEAJ1sS5U8o6eSxv7cdP+tR+r6VIWqhaXC+ot8m3Fsdnp0=
-----END PUBLIC KEY-----
`;

export const ENTITLEMENT_SIG_ALG = "Ed25519";
export const ENTITLEMENT_SKILL_ID = "rea-cn-paid";
