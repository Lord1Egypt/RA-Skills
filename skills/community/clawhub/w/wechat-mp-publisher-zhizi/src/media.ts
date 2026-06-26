/**
 * 素材管理模块
 * 负责上传和管理微信素材
 */

import axios from 'axios';
import * as fs from 'fs';
import FormData from 'form-data';
import { AuthManager } from './auth';
import { MediaUploadResponse } from './types';

const WECHAT_API_BASE = 'https://api.weixin.qq.com/cgi-bin';

export type MediaType = 'image' | 'thumb' | 'voice' | 'video';

export class MediaManager {
  private authManager: AuthManager;

  constructor(authManager: AuthManager) {
    this.authManager = authManager;
  }

  /**
   * 上传图文消息内的图片（获取图片 URL）
   * 这种图片不会存入素材库，只能在正文中使用
   */
  async uploadArticleImage(imagePath: string): Promise<string> {
    const accessToken = await this.authManager.getAccessToken();
    const url = `${WECHAT_API_BASE}/media/uploadimg?access_token=${accessToken}`;

    const form = new FormData();
    form.append('media', fs.createReadStream(imagePath));

    try {
      const response = await axios.post<MediaUploadResponse>(url, form, {
        headers: form.getHeaders()
      });

      const data = response.data;
      if (data.errcode) {
        throw new Error(`上传图片失败: [${data.errcode}] ${data.errmsg}`);
      }

      return data.url!;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(`上传图片请求失败: ${error.message}`);
      }
      throw error;
    }
  }

  /**
   * 上传素材到微信服务器
   * @param filePath 本地文件路径
   * @param type 素材类型: image(图片), thumb(缩略图), voice(语音), video(视频)
   */
  async uploadMedia(filePath: string, type: MediaType): Promise<MediaUploadResponse> {
    const accessToken = await this.authManager.getAccessToken();
    const url = `${WECHAT_API_BASE}/media/upload?access_token=${accessToken}&type=${type}`;

    const form = new FormData();
    form.append('media', fs.createReadStream(filePath));

    try {
      const response = await axios.post<MediaUploadResponse>(url, form, {
        headers: form.getHeaders()
      });

      const data = response.data;
      if (data.errcode) {
        throw new Error(`上传素材失败: [${data.errcode}] ${data.errmsg}`);
      }

      return data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(`上传素材请求失败: ${error.message}`);
      }
      throw error;
    }
  }

  /**
   * 上传封面图片（自动裁剪为合适的尺寸）
   * 微信要求大图: 900*500, 小图: 200*200
   */
  async uploadCoverImage(imagePath: string): Promise<string> {
    // 封面图使用 thumb 类型（缩略图）
    const result = await this.uploadMedia(imagePath, 'thumb');
    return result.media_id;
  }

  /**
   * 上传正文中的图片（批量）
   */
  async uploadContentImages(imagePaths: string[]): Promise<Map<string, string>> {
    const result = new Map<string, string>();
    
    for (const path of imagePaths) {
      try {
        const url = await this.uploadArticleImage(path);
        result.set(path, url);
      } catch (error) {
        console.warn(`上传图片失败 ${path}:`, error);
        result.set(path, '');
      }
    }

    return result;
  }
}
