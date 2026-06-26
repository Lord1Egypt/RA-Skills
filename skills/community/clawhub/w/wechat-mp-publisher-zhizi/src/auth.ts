/**
 * AccessToken 管理模块
 * 负责获取和缓存微信公众号 AccessToken
 */

import axios from 'axios';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { AccessTokenResponse, AccessTokenCache, WeChatMPConfig } from './types';

const WECHAT_API_BASE = 'https://api.weixin.qq.com/cgi-bin';

export class AuthManager {
  private config: WeChatMPConfig;
  private cacheFile: string;
  private tokenPromise: Promise<string> | null = null;

  constructor(config: WeChatMPConfig) {
    this.config = config;
    this.cacheFile = config.access_token_cache_file || 
      path.join(os.homedir(), '.openclaw', '.wechat_mp_token.json');
    
    // 确保缓存目录存在（创建时限制权限）
    const cacheDir = path.dirname(this.cacheFile);
    if (!fs.existsSync(cacheDir)) {
      fs.mkdirSync(cacheDir, { recursive: true, mode: 0o700 });
    }
  }

  /**
   * 获取有效的 AccessToken
   * 优先从缓存读取，过期则重新获取
   * 使用锁机制防止并发重复获取
   */
  async getAccessToken(): Promise<string> {
    // 尝试从缓存读取
    const cached = this.readCachedToken();
    if (cached && cached.expires_at > Date.now() + 60000) {
      // 缓存还有效（预留1分钟缓冲）
      return cached.access_token;
    }

    // 如果正在获取中，复用现有的 Promise
    if (this.tokenPromise) {
      return this.tokenPromise;
    }

    // 创建新的获取 Promise
    this.tokenPromise = this.fetchAccessToken().finally(() => {
      this.tokenPromise = null;
    });

    return this.tokenPromise;
  }

  /**
   * 从微信服务器获取 AccessToken
   */
  private async fetchAccessToken(): Promise<string> {
    const url = `${WECHAT_API_BASE}/token?grant_type=client_credential&appid=${this.config.app_id}&secret=${this.config.app_secret}`;
    
    try {
      const response = await axios.get<AccessTokenResponse>(url);
      const data = response.data;

      if (data.errcode) {
        throw new Error(`获取 AccessToken 失败: [${data.errcode}] ${data.errmsg}`);
      }

      // 缓存 Token
      const cache: AccessTokenCache = {
        access_token: data.access_token,
        expires_at: Date.now() + (data.expires_in * 1000)
      };
      this.writeCachedToken(cache);

      return data.access_token;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(`请求 AccessToken 失败: ${error.message}`);
      }
      throw error;
    }
  }

  /**
   * 从缓存文件读取 Token
   */
  private readCachedToken(): AccessTokenCache | null {
    try {
      if (fs.existsSync(this.cacheFile)) {
        const content = fs.readFileSync(this.cacheFile, 'utf-8');
        return JSON.parse(content) as AccessTokenCache;
      }
    } catch (error) {
      console.warn('读取 AccessToken 缓存失败:', error);
    }
    return null;
  }

  /**
   * 写入 Token 到缓存文件
   * 使用 0o600 权限保护敏感信息
   */
  private writeCachedToken(cache: AccessTokenCache): void {
    try {
      fs.writeFileSync(this.cacheFile, JSON.stringify(cache, null, 2), { mode: 0o600 });
    } catch (error) {
      console.warn('写入 AccessToken 缓存失败:', error);
    }
  }

  /**
   * 清除缓存的 Token
   */
  clearCache(): void {
    try {
      if (fs.existsSync(this.cacheFile)) {
        fs.unlinkSync(this.cacheFile);
      }
    } catch (error) {
      console.warn('清除 AccessToken 缓存失败:', error);
    }
  }
}
