// 输出语言。判定顺序与 chat-share-reader 一致：
//   REG_LANG 环境变量 → 系统 locale → 回落到中文。
//
// 只影响脚本的终端输出，不影响 SKILL.md 和 README，那两份各语言独立成文。

const explicit = (process.env.REG_LANG || '').toLowerCase().trim();
const sysLocale = (
  process.env.LC_ALL ||
  process.env.LC_MESSAGES ||
  process.env.LANG ||
  process.env.LANGUAGE ||
  ''
).toLowerCase();

function resolve() {
  if (explicit) return explicit.startsWith('zh') ? 'zh' : 'en';
  if (sysLocale) return sysLocale.startsWith('zh') ? 'zh' : 'en';
  return 'zh';
}

export const isZh = resolve() === 'zh';

export function t(zh, en) {
  return isZh ? zh : en;
}
