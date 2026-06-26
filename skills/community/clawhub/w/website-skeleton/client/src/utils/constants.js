/**
 * constants — 全局常量
 */

/** API 基础路径（含代理前缀，生产环境可改为完整域名） */
export const BASE_URL = import.meta.env?.BASE_URL || '';

/** API 端点前缀 */
export const API_PREFIX = '/api';

/** 分页默认值 */
export const PAGE_SIZE = 20;
export const PAGE_SIZE_OPTIONS = [10, 20, 50, 100];

/** 主题色变量名 */
export const THEME = {
  LIGHT: 'light',
  DARK: 'dark',
};

/** 本地存储前缀 */
export const STORAGE_PREFIX = 'geekshop:';

/** Token 存储 Key */
export const TOKEN_KEY = `${STORAGE_PREFIX}token`;

/** 刷新 Token 存储 Key */
export const REFRESH_TOKEN_KEY = `${STORAGE_PREFIX}refresh_token`;

/** 用户信息存储 Key */
export const USER_KEY = `${STORAGE_PREFIX}user`;
