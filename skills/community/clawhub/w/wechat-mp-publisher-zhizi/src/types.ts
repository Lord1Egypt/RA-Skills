/**
 * 微信公众号 API 类型定义
 */

// AccessToken 响应
export interface AccessTokenResponse {
  access_token: string;
  expires_in: number;
  errcode?: number;
  errmsg?: string;
}

// AccessToken 缓存
export interface AccessTokenCache {
  access_token: string;
  expires_at: number;
}

// 素材上传响应
export interface MediaUploadResponse {
  type: string;
  media_id: string;
  created_at: number;
  url?: string; // 图文消息内图片返回的 URL
  errcode?: number;
  errmsg?: string;
}

// 图文消息文章
export interface NewsArticle {
  title: string;
  thumb_media_id: string;
  author?: string;
  digest?: string;
  show_cover_pic?: number; // 0 or 1
  content: string;
  content_source_url?: string;
  need_open_comment?: number; // 0 or 1
  only_fans_can_comment?: number; // 0 or 1
}

// 图文消息素材上传请求
export interface NewsUploadRequest {
  articles: NewsArticle[];
}

// 图文消息素材上传响应
export interface NewsUploadResponse {
  type: string;
  media_id: string;
  created_at: number;
  errcode?: number;
  errmsg?: string;
}

// 发布草稿请求
export interface FreePublishRequest {
  media_id: string;
}

// 发布草稿响应
export interface FreePublishResponse {
  publish_id: string;
  errcode?: number;
  errmsg?: string;
}

// 发布状态查询响应
export interface PublishStatusResponse {
  publish_id: string;
  publish_status: number; // 0:成功, 1:发布中, 2:原创审核失败, 3:失败
  article_id?: string;
  article_detail?: {
    count: number;
    item: Array<{
      idx: number;
      article_url: string;
    }>;
  };
  fail_idx?: number[];
  errcode?: number;
  errmsg?: string;
}

// 草稿列表响应
export interface DraftListResponse {
  total_count: number;
  item_count: number;
  item: Array<{
    media_id: string;
    content: {
      news_item: NewsArticle[];
    };
    update_time: number;
  }>;
  errcode?: number;
  errmsg?: string;
}

// 微信错误响应
export interface WeChatError {
  errcode: number;
  errmsg: string;
}

// 配置类型
export interface WeChatMPConfig {
  app_id: string;
  app_secret: string;
  default_author?: string;
  access_token_cache_file?: string;
}
