/**
 * 文件系统接口 - File System Interface
 * 借鉴 OpenViking 的文件系统范式
 */

import { logger } from '../utils/logger.js';
import { VikingURI } from '../core/viking_uri.js';

/**
 * 文件系统接口
 */
export class FileSystemInterface {
  constructor(options = {}) {
    this.storage = options.storage;
    this.vectorStore = options.vectorStore;
    this.cache = new Map();
    this.cacheMaxSize = options.cacheMaxSize || 1000;
  }
  
  /**
   * 列出目录内容
   */
  async ls(uri, options = {}) {
    const vikingUri = new VikingURI(uri);
    
    logger.debug(`[FileSystem] ls: ${uri}`);
    
    if (!this.storage) {
      logger.warn('[FileSystem] 存储未配置');
      return [];
    }
    
    try {
      const entries = await this.storage.ls(vikingUri.fullPath);
      
      return entries.map(entry => ({
        name: entry.name,
        uri: `viking://${entry.path}`,
        isDirectory: entry.isDirectory,
        size: entry.size || 0,
        modifiedAt: entry.modifiedAt || Date.now()
      }));
      
    } catch (error) {
      logger.error(`[FileSystem] ls 失败: ${uri}`, error);
      return [];
    }
  }
  
  /**
   * 创建目录
   */
  async mkdir(uri) {
    const vikingUri = new VikingURI(uri);
    
    logger.debug(`[FileSystem] mkdir: ${uri}`);
    
    if (!this.storage) {
      throw new Error('存储未配置');
    }
    
    await this.storage.mkdir(vikingUri.fullPath);
    
    return { uri: uri, created: true };
  }
  
  /**
   * 删除文件或目录
   */
  async rm(uri, options = {}) {
    const vikingUri = new VikingURI(uri);
    
    logger.debug(`[FileSystem] rm: ${uri}`);
    
    if (!this.storage) {
      throw new Error('存储未配置');
    }
    
    await this.storage.rm(vikingUri.fullPath, { recursive: options.recursive });
    
    // 清除缓存
    this.cache.delete(uri);
    
    return { uri: uri, deleted: true };
  }
  
  /**
   * 移动文件或目录
   */
  async mv(sourceUri, targetUri) {
    const source = new VikingURI(sourceUri);
    const target = new VikingURI(targetUri);
    
    logger.debug(`[FileSystem] mv: ${sourceUri} -> ${targetUri}`);
    
    if (!this.storage) {
      throw new Error('存储未配置');
    }
    
    await this.storage.mv(source.fullPath, target.fullPath);
    
    // 清除缓存
    this.cache.delete(sourceUri);
    
    return { source: sourceUri, target: targetUri, moved: true };
  }
  
  /**
   * 读取文件
   */
  async read(uri, options = {}) {
    const vikingUri = new VikingURI(uri);
    
    logger.debug(`[FileSystem] read: ${uri}`);
    
    // 检查缓存
    if (this.cache.has(uri)) {
      return this.cache.get(uri);
    }
    
    if (!this.storage) {
      throw new Error('存储未配置');
    }
    
    const content = await this.storage.read(vikingUri.fullPath);
    
    // 缓存
    if (options.cache !== false) {
      this.cache.set(uri, content);
      
      // 限制缓存大小
      if (this.cache.size > this.cacheMaxSize) {
        const firstKey = this.cache.keys().next().value;
        this.cache.delete(firstKey);
      }
    }
    
    return content;
  }
  
  /**
   * 写入文件
   */
  async write(uri, content, options = {}) {
    const vikingUri = new VikingURI(uri);
    
    logger.debug(`[FileSystem] write: ${uri}`);
    
    if (!this.storage) {
      throw new Error('存储未配置');
    }
    
    await this.storage.write(vikingUri.fullPath, content);
    
    // 更新缓存
    this.cache.set(uri, content);
    
    return { uri: uri, written: true };
  }
  
  /**
   * 获取抽象层 (L0)
   */
  async abstract(uri) {
    const vikingUri = new VikingURI(uri);
    
    logger.debug(`[FileSystem] abstract: ${uri}`);
    
    // 尝试读取 .abstract.md
    const abstractUri = vikingUri.isDirectory ? 
      vikingUri.join('.abstract.md') : 
      new VikingURI(uri.replace(/\.[^.]+$/, '.abstract.md'));
    
    try {
      const content = await this.read(abstractUri.uri);
      return content;
    } catch (error) {
      // 如果不存在，生成抽象
      if (this.vectorStore) {
        const metadata = await this.vectorStore.getMetadata(uri);
        return metadata?.abstract || '';
      }
      return '';
    }
  }
  
  /**
   * 获取概览层 (L1)
   */
  async overview(uri) {
    const vikingUri = new VikingURI(uri);
    
    logger.debug(`[FileSystem] overview: ${uri}`);
    
    // 尝试读取 .overview.md
    const overviewUri = vikingUri.isDirectory ? 
      vikingUri.join('.overview.md') : 
      new VikingURI(uri.replace(/\.[^.]+$/, '.overview.md'));
    
    try {
      const content = await this.read(overviewUri.uri);
      return content;
    } catch (error) {
      // 如果不存在，返回完整内容的前 2000 字符
      try {
        const content = await this.read(uri);
        const text = typeof content === 'string' ? content : JSON.stringify(content);
        return text.substring(0, 2000);
      } catch (e) {
        return '';
      }
    }
  }
  
  /**
   * 获取文件树
   */
  async tree(uri, options = {}) {
    const vikingUri = new VikingURI(uri);
    const depth = options.depth || 3;
    
    logger.debug(`[FileSystem] tree: ${uri}, depth: ${depth}`);
    
    const result = {
      uri: uri,
      name: vikingUri.name || vikingUri.scope,
      isDirectory: true,
      children: []
    };
    
    await this.buildTree(result, depth - 1);
    
    return result;
  }
  
  /**
   * 构建文件树
   */
  async buildTree(node, remainingDepth) {
    if (remainingDepth <= 0) return;
    
    try {
      const entries = await this.ls(node.uri);
      
      for (const entry of entries) {
        const child = {
          uri: entry.uri,
          name: entry.name,
          isDirectory: entry.isDirectory,
          size: entry.size,
          modifiedAt: entry.modifiedAt,
          children: entry.isDirectory ? [] : undefined
        };
        
        node.children.push(child);
        
        if (entry.isDirectory && remainingDepth > 1) {
          await this.buildTree(child, remainingDepth - 1);
        }
      }
      
    } catch (error) {
      logger.error(`[FileSystem] 构建文件树失败: ${node.uri}`, error);
    }
  }
  
  /**
   * 获取文件状态
   */
  async stat(uri) {
    const vikingUri = new VikingURI(uri);
    
    logger.debug(`[FileSystem] stat: ${uri}`);
    
    if (!this.storage) {
      throw new Error('存储未配置');
    }
    
    const stat = await this.storage.stat(vikingUri.fullPath);
    
    return {
      uri: uri,
      isDirectory: stat.isDirectory,
      size: stat.size,
      createdAt: stat.createdAt,
      modifiedAt: stat.modifiedAt
    };
  }
  
  /**
   * 搜索文件内容
   */
  async grep(uri, pattern, options = {}) {
    const vikingUri = new VikingURI(uri);
    
    logger.debug(`[FileSystem] grep: ${pattern} in ${uri}`);
    
    const results = [];
    const regex = new RegExp(pattern, options.ignoreCase ? 'gi' : 'g');
    
    // 递归搜索
    await this.grepRecursive(vikingUri, regex, results, options);
    
    return results;
  }
  
  /**
   * 递归搜索
   */
  async grepRecursive(vikingUri, regex, results, options) {
    try {
      const entries = await this.ls(vikingUri.uri);
      
      for (const entry of entries) {
        if (entry.isDirectory) {
          await this.grepRecursive(new VikingURI(entry.uri), regex, results, options);
        } else {
          try {
            const content = await this.read(entry.uri);
            const text = typeof content === 'string' ? content : JSON.stringify(content);
            
            const matches = text.match(regex);
            
            if (matches) {
              results.push({
                uri: entry.uri,
                matches: matches.length,
                preview: text.substring(0, 200)
              });
            }
            
          } catch (error) {
            // 忽略读取错误
          }
        }
      }
      
    } catch (error) {
      logger.error(`[FileSystem] grep 递归搜索失败: ${vikingUri.uri}`, error);
    }
  }
  
  /**
   * Glob 模式匹配
   */
  async glob(uri, pattern) {
    const vikingUri = new VikingURI(uri);
    
    logger.debug(`[FileSystem] glob: ${pattern} in ${uri}`);
    
    const results = [];
    const regex = this.globToRegex(pattern);
    
    await this.globRecursive(vikingUri, regex, results);
    
    return results;
  }
  
  /**
   * 递归 glob
   */
  async globRecursive(vikingUri, regex, results) {
    try {
      const entries = await this.ls(vikingUri.uri);
      
      for (const entry of entries) {
        if (regex.test(entry.name)) {
          results.push({
            uri: entry.uri,
            name: entry.name,
            isDirectory: entry.isDirectory
          });
        }
        
        if (entry.isDirectory) {
          await this.globRecursive(new VikingURI(entry.uri), regex, results);
        }
      }
      
    } catch (error) {
      logger.error(`[FileSystem] glob 递归搜索失败: ${vikingUri.uri}`, error);
    }
  }
  
  /**
   * Glob 模式转正则表达式
   */
  globToRegex(pattern) {
    const escaped = pattern
      .replace(/[.+^${}()|[\]\\]/g, '\\$&')
      .replace(/\*/g, '.*')
      .replace(/\?/g, '.');
    
    return new RegExp(`^${escaped}$`);
  }
  
  /**
   * 清除缓存
   */
  clearCache() {
    this.cache.clear();
  }
  
  /**
   * 获取缓存统计
   */
  getCacheStats() {
    return {
      size: this.cache.size,
      maxSize: this.cacheMaxSize
    };
  }
}

/**
 * 获取文件系统接口实例
 */
let defaultFS = null;

export function getFileSystem(options = {}) {
  if (!defaultFS) {
    defaultFS = new FileSystemInterface(options);
  }
  return defaultFS;
}

export default FileSystemInterface;
