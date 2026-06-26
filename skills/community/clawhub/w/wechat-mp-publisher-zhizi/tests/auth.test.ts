/**
 * AuthManager 单元测试
 * 测试 AccessToken 获取和缓存功能
 */

import { AuthManager } from '../src/auth';
import { WeChatMPConfig } from '../src/types';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import axios from 'axios';

// Mock axios
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

// Mock fs
jest.mock('fs');
const mockedFs = fs as jest.Mocked<typeof fs>;

describe('AuthManager', () => {
  const mockConfig: WeChatMPConfig = {
    app_id: 'test_app_id',
    app_secret: 'test_app_secret',
    access_token_cache_file: '/tmp/test_token.json'
  };

  let authManager: AuthManager;

  beforeEach(() => {
    jest.clearAllMocks();
    
    // 重置 fs mock
    mockedFs.existsSync = jest.fn();
    mockedFs.readFileSync = jest.fn();
    mockedFs.writeFileSync = jest.fn();
    mockedFs.unlinkSync = jest.fn();
    mockedFs.mkdirSync = jest.fn();
    
    // 默认目录存在
    mockedFs.existsSync.mockReturnValue(true);
    
    authManager = new AuthManager(mockConfig);
  });

  describe('构造函数', () => {
    it('应该使用自定义缓存文件路径', () => {
      const customPath = '/custom/path/token.json';
      const manager = new AuthManager({
        ...mockConfig,
        access_token_cache_file: customPath
      });
      expect(manager).toBeDefined();
    });

    it('应该在目录不存在时创建缓存目录', () => {
      mockedFs.existsSync.mockReturnValueOnce(false);
      const manager = new AuthManager(mockConfig);
      expect(mockedFs.mkdirSync).toHaveBeenCalledWith(
        path.dirname(mockConfig.access_token_cache_file!),
        { recursive: true }
      );
    });
  });

  describe('getAccessToken', () => {
    it('应该从缓存读取有效的 token', async () => {
      const cachedToken = {
        access_token: 'cached_token_123',
        expires_at: Date.now() + 600000 // 10分钟后过期
      };
      mockedFs.existsSync.mockReturnValueOnce(true);
      mockedFs.readFileSync.mockReturnValueOnce(JSON.stringify(cachedToken));

      const token = await authManager.getAccessToken();

      expect(token).toBe('cached_token_123');
      expect(mockedFs.readFileSync).toHaveBeenCalled();
      expect(mockedAxios.get).not.toHaveBeenCalled();
    });

    it('应该在缓存过期时重新获取 token', async () => {
      // 设置过期缓存
      const expiredToken = {
        access_token: 'expired_token',
        expires_at: Date.now() - 1000 // 已过期
      };
      mockedFs.existsSync.mockReturnValueOnce(true);
      mockedFs.readFileSync.mockReturnValueOnce(JSON.stringify(expiredToken));

      // 模拟 API 响应
      const apiResponse = {
        data: {
          access_token: 'new_token_123',
          expires_in: 7200
        }
      };
      mockedAxios.get.mockResolvedValueOnce(apiResponse);

      const token = await authManager.getAccessToken();

      expect(token).toBe('new_token_123');
      expect(mockedAxios.get).toHaveBeenCalled();
    });

    it('应该在缓存不存在时获取新 token', async () => {
      mockedFs.existsSync.mockReturnValueOnce(false);

      const apiResponse = {
        data: {
          access_token: 'fresh_token_123',
          expires_in: 7200
        }
      };
      mockedAxios.get.mockResolvedValueOnce(apiResponse);

      const token = await authManager.getAccessToken();

      expect(token).toBe('fresh_token_123');
    });

    it('应该在缓存即将过期时（1分钟内）重新获取 token', async () => {
      const nearExpiredToken = {
        access_token: 'near_expired',
        expires_at: Date.now() + 30000 // 30秒后过期
      };
      mockedFs.existsSync.mockReturnValueOnce(true);
      mockedFs.readFileSync.mockReturnValueOnce(JSON.stringify(nearExpiredToken));

      const apiResponse = {
        data: {
          access_token: 'fresh_token_123',
          expires_in: 7200
        }
      };
      mockedAxios.get.mockResolvedValueOnce(apiResponse);

      await authManager.getAccessToken();

      expect(mockedAxios.get).toHaveBeenCalled();
    });
  });

  describe('fetchAccessToken', () => {
    it('应该正确调用微信 API', async () => {
      const apiResponse = {
        data: {
          access_token: 'api_token_123',
          expires_in: 7200
        }
      };
      mockedAxios.get.mockResolvedValueOnce(apiResponse);

      await authManager.getAccessToken();

      expect(mockedAxios.get).toHaveBeenCalledWith(
        expect.stringContaining('https://api.weixin.qq.com/cgi-bin/token')
      );
      expect(mockedAxios.get).toHaveBeenCalledWith(
        expect.stringContaining('appid=test_app_id')
      );
      expect(mockedAxios.get).toHaveBeenCalledWith(
        expect.stringContaining('secret=test_app_secret')
      );
    });

    it('应该正确缓存获取的 token', async () => {
      const apiResponse = {
        data: {
          access_token: 'token_to_cache',
          expires_in: 7200
        }
      };
      mockedAxios.get.mockResolvedValueOnce(apiResponse);

      await authManager.getAccessToken();

      expect(mockedFs.writeFileSync).toHaveBeenCalled();
      const writeCall = mockedFs.writeFileSync.mock.calls[0];
      const cachedData = JSON.parse(writeCall[1] as string);
      expect(cachedData.access_token).toBe('token_to_cache');
      expect(cachedData.expires_at).toBeGreaterThan(Date.now());
    });

    it('应该在 API 返回错误时抛出异常', async () => {
      const errorResponse = {
        data: {
          errcode: 40001,
          errmsg: 'invalid credential'
        }
      };
      mockedAxios.get.mockResolvedValueOnce(errorResponse);
      mockedFs.existsSync.mockReturnValueOnce(false);

      await expect(authManager.getAccessToken()).rejects.toThrow('获取 AccessToken 失败');
    });

    it('应该在网络请求失败时抛出异常', async () => {
      mockedAxios.get.mockRejectedValueOnce(new Error('Network Error'));
      mockedFs.existsSync.mockReturnValueOnce(false);

      await expect(authManager.getAccessToken()).rejects.toThrow('请求 AccessToken 失败');
    });

    it('应该在 Axios 错误时正确处理', async () => {
      const axiosError = new Error('Request timeout');
      (axiosError as any).isAxiosError = true;
      mockedAxios.isAxiosError = jest.fn().mockReturnValue(true);
      mockedAxios.get.mockRejectedValueOnce(axiosError);
      mockedFs.existsSync.mockReturnValueOnce(false);

      await expect(authManager.getAccessToken()).rejects.toThrow('请求 AccessToken 失败');
    });
  });

  describe('readCachedToken', () => {
    it('应该处理读取缓存文件失败的情况', async () => {
      mockedFs.existsSync.mockReturnValueOnce(true);
      mockedFs.readFileSync.mockImplementationOnce(() => {
        throw new Error('Permission denied');
      });

      // 设置 API 响应以获取新 token
      const apiResponse = {
        data: {
          access_token: 'fallback_token',
          expires_in: 7200
        }
      };
      mockedAxios.get.mockResolvedValueOnce(apiResponse);

      const token = await authManager.getAccessToken();

      expect(token).toBe('fallback_token');
    });

    it('应该处理缓存文件不存在的情况', async () => {
      mockedFs.existsSync.mockReturnValueOnce(false);

      const apiResponse = {
        data: {
          access_token: 'new_token',
          expires_in: 7200
        }
      };
      mockedAxios.get.mockResolvedValueOnce(apiResponse);

      const token = await authManager.getAccessToken();

      expect(token).toBe('new_token');
    });
  });

  describe('writeCachedToken', () => {
    it('应该处理写入缓存文件失败的情况', async () => {
      mockedFs.existsSync.mockReturnValueOnce(false);
      mockedFs.writeFileSync.mockImplementationOnce(() => {
        throw new Error('Disk full');
      });

      const apiResponse = {
        data: {
          access_token: 'token_123',
          expires_in: 7200
        }
      };
      mockedAxios.get.mockResolvedValueOnce(apiResponse);

      // 应该不抛出异常，只是警告
      const token = await authManager.getAccessToken();
      expect(token).toBe('token_123');
    });
  });

  describe('clearCache', () => {
    it('应该成功清除缓存文件', () => {
      mockedFs.existsSync.mockReturnValueOnce(true);

      authManager.clearCache();

      expect(mockedFs.unlinkSync).toHaveBeenCalledWith(mockConfig.access_token_cache_file);
    });

    it('应该在缓存文件不存在时静默处理', () => {
      mockedFs.existsSync.mockReturnValueOnce(false);

      authManager.clearCache();

      expect(mockedFs.unlinkSync).not.toHaveBeenCalled();
    });

    it('应该在删除失败时警告但不抛出', () => {
      mockedFs.existsSync.mockReturnValueOnce(true);
      mockedFs.unlinkSync.mockImplementationOnce(() => {
        throw new Error('Permission denied');
      });

      expect(() => authManager.clearCache()).not.toThrow();
    });
  });
});
