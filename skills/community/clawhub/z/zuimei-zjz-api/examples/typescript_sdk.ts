/**
 * 最美证件照 API TypeScript SDK
 *
 * 安装依赖：npm install axios form-data
 *
 * 环境变量：
 * export ZUIMEI_API_KEY="your_api_key"
 * export ZUIMEI_SECRET_KEY="your_secret_key"
 */

import * as crypto from 'crypto';
import * as fs from 'fs';
import axios from 'axios';
import FormData from 'form-data';

const BASE_URL = 'https://idphoto.huipai.vip';

/** API 响应格式 */
interface ApiResponse<T = unknown> {
  code: number;
  message: string;
  data: T | null;
}

/** 证件照响应数据 */
interface IdPhotoData {
  image_url: string;
  hd_transparent_url?: string;
  width: number;
  height: number;
  dpi: number;
  size_kb: number;
  output_format: string;
}

/** 抠图响应数据 */
interface SegmentData {
  image_url: string;
}

/** 换背景响应数据 */
interface BackgroundData {
  image_url: string;
  images?: Array<{ background_color: string; image_url: string }>;
  dpi: number;
  output_format: string;
}

/** 增强响应数据 */
interface EnhanceData {
  original_url: string;
  enhanced_url: string;
  width: number;
  height: number;
  dpi: number;
  enhance_time: number;
  face_count: number;
}

/** 排版响应数据 */
interface LayoutData {
  image_url: string;
  width: number;
  height: number;
  dpi: number;
  photo_count: number;
  layout_type: string;
}

/** 编辑响应数据 */
interface EditData {
  image_url: string;
  width: number;
  height: number;
  dpi: number;
  size_kb: number;
  output_format: string;
}

/** API 错误类 */
class ZuimeiApiError extends Error {
  constructor(public code: number, message: string) {
    super(`[${code}] ${message}`);
    this.name = 'ZuimeiApiError';
  }
}

class ZuimeiZjzClient {
  private apiKey: string;
  private secretKey: string;

  constructor() {
    this.apiKey = process.env.ZUIMEI_API_KEY || '';
    this.secretKey = process.env.ZUIMEI_SECRET_KEY || '';
    if (!this.apiKey || !this.secretKey) {
      throw new Error('请设置 ZUIMEI_API_KEY 和 ZUIMEI_SECRET_KEY');
    }
  }

  private buildContentSha256(fields: Record<string, any>): string {
    const lines: string[] = [];
    for (const key of Object.keys(fields).sort()) {
      const value = fields[key];
      if (value === null || value === undefined) continue;
      lines.push(`${key}=${typeof value === 'boolean' ? (value ? 'true' : 'false') : value}`);
    }
    return crypto.createHash('sha256').update(lines.join('\n')).digest('hex');
  }

  private generateSignature(url: string, timestamp: string, nonce: string, contentSha256: string): string {
    const signStr = `POST\n${url}\n${timestamp}\n${nonce}\n${contentSha256}`;
    return crypto.createHmac('sha256', this.secretKey).update(signStr).digest('hex');
  }

  private async callApi<T>(endpoint: string, buffer: Buffer, data: Record<string, unknown> = {}): Promise<ApiResponse<T>> {
    const timestamp = Math.floor(Date.now() / 1000).toString();
    const nonce = crypto.randomBytes(16).toString('hex');

    const fields = { image: crypto.createHash('sha256').update(buffer).digest('hex'), ...data };
    const contentSha256 = this.buildContentSha256(fields);
    const signature = this.generateSignature(endpoint, timestamp, nonce, contentSha256);

    const formData = new FormData();
    formData.append('image', buffer, { filename: 'image.jpg' });
    for (const [key, value] of Object.entries(data)) {
      formData.append(key, String(value));
    }

    const response = await axios.post<ApiResponse<T>>(`${BASE_URL}${endpoint}`, formData, {
      headers: {
        ...formData.getHeaders(),
        'X-API-Key': this.apiKey,
        'X-Timestamp': timestamp,
        'X-Nonce': nonce,
        'X-Signature': signature,
        'X-Content-SHA256': contentSha256,
        'X-Sign-Version': 'v2',
      },
    });

    const result = response.data;
    if (result.code !== 0) {
      throw new ZuimeiApiError(result.code, result.message);
    }

    return result;
  }

  /** 一键证件照 */
  async idPhoto(
    imagePath: string,
    options: { width?: number; height?: number; backgroundColor?: string; beautify?: boolean } = {}
  ): Promise<ApiResponse<IdPhotoData>> {
    const buffer = fs.readFileSync(imagePath);
    return this.callApi<IdPhotoData>('/api/v1/photo/id-photo', buffer, {
      width: options.width || 295,
      height: options.height || 413,
      background_color: options.backgroundColor || '#FFFFFF',
      beautify_flag: options.beautify || false,
    });
  }

  /** 智能抠图 */
  async segmentPortrait(imagePath: string): Promise<ApiResponse<SegmentData>> {
    const buffer = fs.readFileSync(imagePath);
    return this.callApi<SegmentData>('/api/v1/segment/portrait', buffer);
  }

  /** 换背景色 */
  async segmentBackground(
    imagePath: string,
    options: { backgroundColor?: string; quality?: string } = {}
  ): Promise<ApiResponse<BackgroundData>> {
    const buffer = fs.readFileSync(imagePath);
    const data: Record<string, unknown> = { background_color: options.backgroundColor || '#FFFFFF' };
    if (options.quality) data.quality = options.quality;
    return this.callApi<BackgroundData>('/api/v1/segment/background', buffer, data);
  }

  /** 人脸增强 */
  async enhance(
    imagePath: string,
    options: { fidelity?: number; useSr?: boolean } = {}
  ): Promise<ApiResponse<EnhanceData>> {
    const buffer = fs.readFileSync(imagePath);
    return this.callApi<EnhanceData>('/api/v1/photo/enhance', buffer, {
      fidelity: options.fidelity || 0.3,
      use_sr: options.useSr || false,
    });
  }

  /** 排版照 */
  async layout(
    imagePath: string,
    options: { layoutType?: string; cropLine?: boolean } = {}
  ): Promise<ApiResponse<LayoutData>> {
    const buffer = fs.readFileSync(imagePath);
    return this.callApi<LayoutData>('/api/v1/photo/layout', buffer, {
      layout_type: options.layoutType || '6inch',
      crop_line: options.cropLine || false,
    });
  }

  /** 图片编辑 */
  async edit(
    imagePath: string,
    options: { width?: number; height?: number; dpi?: number; outputFormat?: string } = {}
  ): Promise<ApiResponse<EditData>> {
    const buffer = fs.readFileSync(imagePath);
    const data: Record<string, unknown> = { dpi: options.dpi || 300, output_format: options.outputFormat || 'jpeg' };
    if (options.width) data.width = options.width;
    if (options.height) data.height = options.height;
    return this.callApi<EditData>('/api/v1/photo/edit', buffer, data);
  }
}

export { ZuimeiZjzClient, ZuimeiApiError };
export type { ApiResponse, IdPhotoData, SegmentData, BackgroundData, EnhanceData, LayoutData, EditData };
