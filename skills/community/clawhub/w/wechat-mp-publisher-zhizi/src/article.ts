/**
 * 图文消息管理模块
 * 负责创建草稿、发布文章、查询状态
 */

import axios from 'axios';
import { AuthManager } from './auth';
import {
  NewsArticle,
  NewsUploadRequest,
  NewsUploadResponse,
  FreePublishRequest,
  FreePublishResponse,
  PublishStatusResponse,
  DraftListResponse
} from './types';

const WECHAT_API_BASE = 'https://api.weixin.qq.com/cgi-bin';

// 默认请求超时时间（毫秒）
const DEFAULT_TIMEOUT = 30000;

export interface CreateArticleOptions {
  title: string;
  content: string;
  coverMediaId: string;
  author?: string;
  digest?: string;
  contentSourceUrl?: string;
  showCoverPic?: boolean;
  needOpenComment?: boolean;
  onlyFansCanComment?: boolean;
}

export interface PublishOptions {
  mediaId: string;
}

export class ArticleManager {
  private authManager: AuthManager;

  constructor(authManager: AuthManager) {
    this.authManager = authManager;
  }

  /**
   * 创建图文消息草稿
   * @param articles 文章列表（单篇或多篇）
   * @returns media_id 草稿 ID
   */
  async createDraft(articles: NewsArticle[]): Promise<string> {
    const accessToken = await this.authManager.getAccessToken();
    const url = `${WECHAT_API_BASE}/draft/add?access_token=${accessToken}`;

    const request: NewsUploadRequest = { articles };

    try {
      const response = await axios.post<NewsUploadResponse>(url, request, {
        timeout: DEFAULT_TIMEOUT
      });
      const data = response.data;

      if (data.errcode) {
        throw new Error(`创建草稿失败: [${data.errcode}] ${data.errmsg}`);
      }

      return data.media_id;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(`创建草稿请求失败: ${error.message}`);
      }
      throw error;
    }
  }

  /**
   * 创建单篇图文消息草稿（简化版）
   */
  async createSingleDraft(options: CreateArticleOptions): Promise<string> {
    const article: NewsArticle = {
      title: options.title,
      thumb_media_id: options.coverMediaId,
      author: options.author,
      digest: options.digest,
      show_cover_pic: options.showCoverPic ? 1 : 0,
      content: options.content,
      content_source_url: options.contentSourceUrl,
      need_open_comment: options.needOpenComment ? 1 : 0,
      only_fans_can_comment: options.onlyFansCanComment ? 1 : 0
    };

    return this.createDraft([article]);
  }

  /**
   * 发布草稿（群发）
   * @param mediaId 草稿 media_id
   * @returns publish_id 发布任务 ID
   */
  async publishDraft(mediaId: string): Promise<string> {
    const accessToken = await this.authManager.getAccessToken();
    const url = `${WECHAT_API_BASE}/freepublish/submit?access_token=${accessToken}`;

    const request: FreePublishRequest = { media_id: mediaId };

    try {
      const response = await axios.post<FreePublishResponse>(url, request);
      const data = response.data;

      if (data.errcode) {
        throw new Error(`发布草稿失败: [${data.errcode}] ${data.errmsg}`);
      }

      return data.publish_id;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(`发布草稿请求失败: ${error.message}`);
      }
      throw error;
    }
  }

  /**
   * 查询发布状态
   * @param publishId 发布任务 ID
   */
  async getPublishStatus(publishId: string): Promise<PublishStatusResponse> {
    const accessToken = await this.authManager.getAccessToken();
    const url = `${WECHAT_API_BASE}/freepublish/get?access_token=${accessToken}`;

    try {
      const response = await axios.post<PublishStatusResponse>(url, {
        publish_id: publishId
      });
      const data = response.data;

      if (data.errcode) {
        throw new Error(`查询发布状态失败: [${data.errcode}] ${data.errmsg}`);
      }

      return data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(`查询发布状态请求失败: ${error.message}`);
      }
      throw error;
    }
  }

  /**
   * 获取草稿列表
   * @param offset 分页偏移量
   * @param count 每页数量（最大 20）
   */
  async getDraftList(offset: number = 0, count: number = 20): Promise<DraftListResponse> {
    const accessToken = await this.authManager.getAccessToken();
    const url = `${WECHAT_API_BASE}/draft/batchget?access_token=${accessToken}`;

    try {
      const response = await axios.post<DraftListResponse>(url, {
        offset,
        count: Math.min(count, 20)
      });
      const data = response.data;

      if (data.errcode) {
        throw new Error(`获取草稿列表失败: [${data.errcode}] ${data.errmsg}`);
      }

      return data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(`获取草稿列表请求失败: ${error.message}`);
      }
      throw error;
    }
  }

  /**
   * 删除草稿
   * @param mediaId 草稿 media_id
   */
  async deleteDraft(mediaId: string): Promise<void> {
    const accessToken = await this.authManager.getAccessToken();
    const url = `${WECHAT_API_BASE}/draft/delete?access_token=${accessToken}`;

    try {
      const response = await axios.post(url, { media_id: mediaId });
      const data = response.data;

      if (data.errcode) {
        throw new Error(`删除草稿失败: [${data.errcode}] ${data.errmsg}`);
      }
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(`删除草稿请求失败: ${error.message}`);
      }
      throw error;
    }
  }

  /**
   * 获取草稿详情
   * @param mediaId 草稿 media_id
   */
  async getDraftDetail(mediaId: string): Promise<NewsArticle[]> {
    const accessToken = await this.authManager.getAccessToken();
    const url = `${WECHAT_API_BASE}/draft/get?access_token=${accessToken}`;

    try {
      const response = await axios.post(url, { media_id: mediaId });
      const data = response.data;

      if (data.errcode) {
        throw new Error(`获取草稿详情失败: [${data.errcode}] ${data.errmsg}`);
      }

      return data.news_item || [];
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(`获取草稿详情请求失败: ${error.message}`);
      }
      throw error;
    }
  }

  /**
   * 发布文章（创建草稿并立即发布）
   * @param options 文章选项
   * @returns 包含 media_id 和 publish_id 的对象
   */
  async publishArticle(options: CreateArticleOptions): Promise<{ mediaId: string; publishId: string }> {
    // 创建草稿
    const mediaId = await this.createSingleDraft(options);
    
    // 立即发布
    const publishId = await this.publishDraft(mediaId);

    return { mediaId, publishId };
  }
}
