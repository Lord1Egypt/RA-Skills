/**
 * 站点配置 + 本机状态（登录令牌、没走完的登录 / 订单）。
 *
 * 同一份脚本打成两个技能包（superx-studio、aihuihua-studio），区别只在包里的 site.json：
 * 网站地址、接口前缀、授权页、充值套餐接口、有哪些模型。
 * 本机状态放在 ~/.<技能名>/，两个站点互不干扰；文件权限 600，令牌就是用户的登录凭据。
 */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

/** 技能根目录：lib → scripts → 技能目录。装在哪儿由 AI 工具决定，别假设是 ~/.claude/skills */
export const SKILL_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

export const SITE = JSON.parse(fs.readFileSync(path.join(SKILL_ROOT, 'site.json'), 'utf8'));

// 调试用：STUDIO_BASE_URL 指到测试环境
export const BASE_URL = String(process.env.STUDIO_BASE_URL || SITE.baseUrl).replace(/\/+$/, '');

export const STATE_DIR = path.join(os.homedir(), `.${SITE.name}`);

function file(name) {
  return path.join(STATE_DIR, name);
}

export function readState(name) {
  try {
    return JSON.parse(fs.readFileSync(file(name), 'utf8'));
  } catch {
    return null;
  }
}

export function writeState(name, data) {
  fs.mkdirSync(STATE_DIR, { recursive: true, mode: 0o700 });
  const target = file(name);
  fs.writeFileSync(target, JSON.stringify(data, null, 2), { mode: 0o600 });
  try {
    fs.chmodSync(target, 0o600);
  } catch {
    /* Windows */
  }
}

export function removeState(name) {
  fs.rmSync(file(name), { force: true });
}

/** 当前令牌：环境变量优先（CI / 不想落盘时用），其次本机登录记录 */
export function currentToken() {
  if (process.env.STUDIO_TOKEN) return process.env.STUDIO_TOKEN;
  const cred = readState('credentials.json');
  return cred && cred.baseUrl === BASE_URL ? cred.token : '';
}

/** OSS 上的相对路径补成完整地址；MJ 一类的图在另一个域名 */
export function fullUrl(p, paintingType = '') {
  if (!p) return '';
  const s = String(p);
  if (/^https?:\/\//i.test(s)) return s;
  if (s.startsWith('//')) return `https:${s}`;
  const mj = (SITE.mjOssTypes || []).includes(String(paintingType).toLowerCase());
  const base = mj ? SITE.mjOssBase : SITE.ossBase;
  return `${base}${s.startsWith('/') ? '' : '/'}${s}`;
}

export const artApi = (p) => `${BASE_URL}${SITE.artPrefix}/${p.replace(/^\/+/, '')}`;
export const api = (p) => `${BASE_URL}/api/${p.replace(/^\/+/, '')}`;
