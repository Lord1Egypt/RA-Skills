/**
 * WeChat MP Publisher - OpenClaw Skill
 * 微信公众号文章自动发布工具
 */

import { AuthManager } from './auth';
import { MediaManager, MediaType } from './media';
import { ArticleManager, CreateArticleOptions } from './article';
import { WeChatMPConfig, NewsArticle } from './types';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

/**
 * 检查文件权限，返回其他用户是否可读
 */
function checkFilePermissions(filePath: string): { readableByOthers: boolean; mode?: number } {
  try {
    const stats = fs.statSync(filePath);
    const mode = stats.mode;
    // 检查其他用户是否有读权限 (0o044)
    const readableByOthers = (mode & 0o044) !== 0;
    return { readableByOthers, mode };
  } catch {
    return { readableByOthers: false };
  }
}

export { AuthManager, MediaManager, ArticleManager };
export * from './types';
export { MediaType } from './media';
export { CreateArticleOptions } from './article';

// 默认配置文件路径
const DEFAULT_CONFIG_PATH = path.join(os.homedir(), '.openclaw', 'config', 'wechat-mp.json');

/**
 * 加载配置文件
 * 检查文件权限，防止敏感信息泄露
 */
function loadConfig(configPath?: string): WeChatMPConfig {
  const targetPath = configPath || DEFAULT_CONFIG_PATH;

  // 首先尝试从环境变量读取
  const envAppId = process.env.WECHAT_MP_APP_ID;
  const envAppSecret = process.env.WECHAT_MP_APP_SECRET;

  if (envAppId && envAppSecret) {
    return {
      app_id: envAppId,
      app_secret: envAppSecret,
      default_author: process.env.WECHAT_MP_DEFAULT_AUTHOR,
      access_token_cache_file: process.env.WECHAT_MP_TOKEN_CACHE
    };
  }

  // 从配置文件读取
  if (!fs.existsSync(targetPath)) {
    throw new Error(
      `未找到配置文件: ${targetPath}\n` +
      `请创建配置文件或设置环境变量:\n` +
      `  WECHAT_MP_APP_ID - 微信公众号 AppID\n` +
      `  WECHAT_MP_APP_SECRET - 微信公众号 AppSecret`
    );
  }

  // 检查配置文件权限
  const permCheck = checkFilePermissions(targetPath);
  if (permCheck.readableByOthers) {
    console.warn(`警告: 配置文件 ${targetPath} 对其他用户可读，建议执行: chmod 600 ${targetPath}`);
  }

  try {
    const content = fs.readFileSync(targetPath, 'utf-8');
    const config = JSON.parse(content) as WeChatMPConfig;

    if (!config.app_id || !config.app_secret) {
      throw new Error('配置文件缺少必需的 app_id 或 app_secret');
    }

    return config;
  } catch (error) {
    if (error instanceof SyntaxError) {
      throw new Error(`配置文件 JSON 格式错误: ${targetPath}`);
    }
    // 脱敏处理：不暴露敏感路径或内部错误细节
    throw new Error('读取配置文件失败，请检查文件路径和权限');
  }
}

/**
 * 创建 WeChatMP 客户端
 */
export function createWeChatMPClient(config?: WeChatMPConfig, configPath?: string) {
  const cfg = config || loadConfig(configPath);
  
  const authManager = new AuthManager(cfg);
  const mediaManager = new MediaManager(authManager);
  const articleManager = new ArticleManager(authManager);

  return {
    auth: authManager,
    media: mediaManager,
    article: articleManager,
    config: cfg
  };
}

/**
 * OpenClaw Tool: 发布微信公众号文章
 * @param params 发布参数
 */
export async function wechatMpPublish(params: {
  title: string;
  content: string;
  cover_media_id?: string;
  author?: string;
  digest?: string;
  content_source_url?: string;
  publish?: boolean;
}): Promise<{ success: boolean; message: string; data?: any }> {
  try {
    const client = createWeChatMPClient();
    
    // 检查必需的封面图
    if (!params.cover_media_id) {
      return {
        success: false,
        message: '缺少必需参数: cover_media_id（封面图片素材 ID）'
      };
    }

    const options: CreateArticleOptions = {
      title: params.title,
      content: params.content,
      coverMediaId: params.cover_media_id,
      author: params.author || client.config.default_author,
      digest: params.digest,
      contentSourceUrl: params.content_source_url,
      showCoverPic: true
    };

    if (params.publish !== false) {
      // 立即发布
      const result = await client.article.publishArticle(options);
      return {
        success: true,
        message: '文章已创建并提交发布',
        data: {
          media_id: result.mediaId,
          publish_id: result.publishId
        }
      };
    } else {
      // 保存为草稿
      const mediaId = await client.article.createSingleDraft(options);
      return {
        success: true,
        message: '草稿创建成功',
        data: {
          media_id: mediaId
        }
      };
    }
  } catch (error: any) {
    // 错误信息脱敏：只返回用户友好的消息，不暴露内部细节
    const errorMessage = error.message?.includes('config') || error.message?.includes('path')
      ? '发布失败: 配置错误或文件访问问题'
      : `发布失败: ${error.message}`;
    return {
      success: false,
      message: errorMessage
    };
  }
}

/**
 * OpenClaw Tool: 上传素材到微信服务器
 * @param params 上传参数
 */
export async function wechatMpUploadMedia(params: {
  file_path: string;
  type?: MediaType;
}): Promise<{ success: boolean; message: string; data?: any }> {
  try {
    if (!params.file_path) {
      return {
        success: false,
        message: '缺少必需参数: file_path'
      };
    }

    if (!fs.existsSync(params.file_path)) {
      return {
        success: false,
        message: `文件不存在: ${params.file_path}`
      };
    }

    const client = createWeChatMPClient();
    const mediaType: MediaType = params.type || 'image';
    
    const result = await client.media.uploadMedia(params.file_path, mediaType);
    
    return {
      success: true,
      message: '素材上传成功',
      data: {
        media_id: result.media_id,
        type: result.type,
        created_at: result.created_at
      }
    };
  } catch (error: any) {
    // 错误信息脱敏
    const errorMessage = error.message?.includes('config') || error.message?.includes('path')
      ? '上传失败: 配置错误或文件访问问题'
      : `上传失败: ${error.message}`;
    return {
      success: false,
      message: errorMessage
    };
  }
}

/**
 * OpenClaw Tool: 上传封面图片
 * @param params 上传参数
 */
export async function wechatMpUploadCover(params: {
  file_path: string;
}): Promise<{ success: boolean; message: string; data?: any }> {
  try {
    if (!params.file_path) {
      return {
        success: false,
        message: '缺少必需参数: file_path'
      };
    }

    if (!fs.existsSync(params.file_path)) {
      return {
        success: false,
        message: `文件不存在: ${params.file_path}`
      };
    }

    const client = createWeChatMPClient();
    const mediaId = await client.media.uploadCoverImage(params.file_path);

    return {
      success: true,
      message: '封面上传成功',
      data: {
        media_id: mediaId
      }
    };
  } catch (error: any) {
    // 错误信息脱敏
    const errorMessage = error.message?.includes('config') || error.message?.includes('path')
      ? '上传封面失败: 配置错误或文件访问问题'
      : `上传封面失败: ${error.message}`;
    return {
      success: false,
      message: errorMessage
    };
  }
}

/**
 * OpenClaw Tool: 查询草稿列表
 * @param params 查询参数
 */
export async function wechatMpQueryDrafts(params: {
  offset?: number;
  count?: number;
} = {}): Promise<{ success: boolean; message: string; data?: any }> {
  try {
    const client = createWeChatMPClient();
    const result = await client.article.getDraftList(
      params.offset || 0,
      params.count || 10
    );
    
    return {
      success: true,
      message: `获取草稿列表成功，共 ${result.total_count} 条`,
      data: {
        total_count: result.total_count,
        item_count: result.item_count,
        items: result.item
      }
    };
  } catch (error: any) {
    // 错误信息脱敏
    const errorMessage = error.message?.includes('config') || error.message?.includes('path')
      ? '查询草稿列表失败: 配置错误或文件访问问题'
      : `查询草稿列表失败: ${error.message}`;
    return {
      success: false,
      message: errorMessage
    };
  }
}

/**
 * OpenClaw Tool: 查询发布状态
 * @param params 查询参数
 */
export async function wechatMpQueryPublishStatus(params: {
  publish_id: string;
}): Promise<{ success: boolean; message: string; data?: any }> {
  try {
    if (!params.publish_id) {
      return {
        success: false,
        message: '缺少必需参数: publish_id'
      };
    }

    const client = createWeChatMPClient();
    const result = await client.article.getPublishStatus(params.publish_id);
    
    const statusMap: Record<number, string> = {
      0: '成功',
      1: '发布中',
      2: '原创审核失败',
      3: '失败'
    };
    
    return {
      success: true,
      message: `发布状态: ${statusMap[result.publish_status] || '未知'}`,
      data: {
        publish_id: result.publish_id,
        publish_status: result.publish_status,
        status_text: statusMap[result.publish_status] || '未知',
        article_id: result.article_id,
        article_detail: result.article_detail,
        fail_idx: result.fail_idx
      }
    };
  } catch (error: any) {
    // 错误信息脱敏
    const errorMessage = error.message?.includes('config') || error.message?.includes('path')
      ? '查询发布状态失败: 配置错误或文件访问问题'
      : `查询发布状态失败: ${error.message}`;
    return {
      success: false,
      message: errorMessage
    };
  }
}

/**
 * OpenClaw Tool: 删除草稿
 * @param params 删除参数
 */
export async function wechatMpDeleteDraft(params: {
  media_id: string;
}): Promise<{ success: boolean; message: string }> {
  try {
    if (!params.media_id) {
      return {
        success: false,
        message: '缺少必需参数: media_id'
      };
    }

    const client = createWeChatMPClient();
    await client.article.deleteDraft(params.media_id);
    
    return {
      success: true,
      message: '草稿删除成功'
    };
  } catch (error: any) {
    // 错误信息脱敏
    const errorMessage = error.message?.includes('config') || error.message?.includes('path')
      ? '删除草稿失败: 配置错误或文件访问问题'
      : `删除草稿失败: ${error.message}`;
    return {
      success: false,
      message: errorMessage
    };
  }
}

// 默认导出
export default {
  createWeChatMPClient,
  wechatMpPublish,
  wechatMpUploadMedia,
  wechatMpUploadCover,
  wechatMpQueryDrafts,
  wechatMpQueryPublishStatus,
  wechatMpDeleteDraft
};
