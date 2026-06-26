import crypto from 'crypto';
import axios, { AxiosInstance } from 'axios';
import FormData from 'form-data';
import { createReadStream } from 'fs';
import { StardotsConfig, UploadResult, ListResult, FileInfo } from './types';

export class StardotsClient {
  private client: AxiosInstance;
  private config: StardotsConfig;
  private readonly baseURL = 'https://api.stardots.io';

  constructor(config: StardotsConfig) {
    this.config = config;
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: 60000,
    });
  }

  private generateNonce(length: number = 10): string {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let nonce = '';
    for (let i = 0; i < length; i++) {
      nonce += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return nonce;
  }

  private generateSign(timestamp: number, nonce: string): string {
    const needSignStr = `${timestamp}|${this.config.apiSecret}|${nonce}`;
    return crypto.createHash('md5').update(needSignStr).digest('hex').toUpperCase();
  }

  private getAuthHeaders(): Record<string, string> {
    const timestamp = Math.floor(Date.now() / 1000);
    const nonce = this.generateNonce();
    const sign = this.generateSign(timestamp, nonce);

    return {
      'x-stardots-timestamp': timestamp.toString(),
      'x-stardots-nonce': nonce,
      'x-stardots-key': this.config.apiKey,
      'x-stardots-sign': sign,
      'x-stardots-extensions': '{"via": "openclaw", "version": "1.0.0"}'
    };
  }

  async uploadImage(imagePath: string, space?: string, metadata?: Record<string, any>): Promise<UploadResult> {
    try {
      const formData = new FormData();
      formData.append('file', createReadStream(imagePath));
      formData.append('space', space || this.config.space);
      
      if (metadata) {
        formData.append('metadata', JSON.stringify(metadata));
      }

      const headers = {
        ...this.getAuthHeaders(),
        ...formData.getHeaders(),
      };

      const response = await this.client.put('/openapi/file/upload', formData, { headers });

      if (response.data?.success) {
        return {
          success: true,
          url: response.data.data.url,
          message: '上传成功',
        };
      }

      return {
        success: false,
        url: '',
        message: response.data?.message || '上传失败',
      };
    } catch (error: any) {
      return {
        success: false,
        url: '',
        message: error.response?.data?.message || error.message,
      };
    }
  }

  async listFiles(params: { page?: number; pageSize?: number; space?: string }): Promise<ListResult> {
    try {
      const response = await this.client.get('/openapi/file/list', {
        headers: this.getAuthHeaders(),
        params: {
          space: params.space || this.config.space,
          page: params.page || 1,
          pageSize: params.pageSize || 20,
        },
      });

      if (response.data?.success) {
        return {
          files: response.data.data.files || [],
          total: response.data.data.total || 0,
          page: params.page || 1,
          pageSize: params.pageSize || 20,
        };
      }

      throw new Error(response.data?.message || '获取文件列表失败');
    } catch (error: any) {
      throw new Error(`获取文件列表失败: ${error.message}`);
    }
  }

  async deleteFile(fileId: string, space?: string): Promise<boolean> {
    try {
      const response = await this.client.delete('/openapi/file/delete', {
        headers: this.getAuthHeaders(),
        data: {
          fileId,
          space: space || this.config.space,
        },
      });

      return response.data?.success || false;
    } catch (error) {
      return false;
    }
  }
}