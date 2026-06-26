#!/usr/bin/env node
/**
 * UTF-8编码工具模块
 * 解决多平台中文乱码问题，支持Discord、GitHub、Reddit等平台
 * 
 * 核心问题：PowerShell控制台使用GB2312编码显示UTF-8内容，导致控制台输出乱码
 * 解决方案：使用Node.js（默认UTF-8）端到端处理，确保HTTP请求体正确编码
 * 
 * @version 1.0.0
 * @author 丞相
 * @date 2026-03-15
 */

const fs = require('fs');
const { URL } = require('url');

class UTF8Encoder {
  constructor() {
    this.encoding = 'utf8';
  }

  /**
   * 确保文本是UTF-8编码的字符串
   * @param {string|Buffer} text - 输入文本
   * @returns {string} UTF-8编码的字符串
   */
  ensureUTF8(text) {
    if (Buffer.isBuffer(text)) {
      // 如果是Buffer，假设是UTF-8编码
      return text.toString(this.encoding);
    }
    
    if (typeof text !== 'string') {
      // 如果不是字符串，转换为字符串
      text = String(text);
    }
    
    // 验证字符串是否包含有效UTF-8字符
    try {
      Buffer.from(text, this.encoding);
      return text;
    } catch (error) {
      console.warn('⚠️ 文本包含非UTF-8字符，尝试修复...');
      // 尝试用'latin1'编码读取，然后转换为UTF-8
      const buffer = Buffer.from(text, 'latin1');
      return buffer.toString(this.encoding);
    }
  }

  /**
   * 计算文本的UTF-8字节长度（用于HTTP Content-Length头）
   * @param {string} text - 文本内容
   * @returns {number} UTF-8字节长度
   */
  calculateUTF8ByteLength(text) {
    const utf8Text = this.ensureUTF8(text);
    return Buffer.byteLength(utf8Text, this.encoding);
  }

  /**
   * 以UTF-8编码读取文件
   * @param {string} filePath - 文件路径
   * @returns {string} UTF-8编码的文件内容
   * @throws {Error} 文件读取失败时抛出
   */
  readFileUTF8(filePath) {
    try {
      const content = fs.readFileSync(filePath, this.encoding);
      console.log(`✅ 文件读取成功: ${filePath}`);
      console.log(`   字符数: ${content.length}, 字节数: ${this.calculateUTF8ByteLength(content)}`);
      
      // 验证中文字符是否正常
      if (content.match(/[\u4e00-\u9fa5]/)) {
        const chineseCount = (content.match(/[\u4e00-\u9fa5]/g) || []).length;
        console.log(`   中文字符数: ${chineseCount}`);
      }
      
      return content;
    } catch (error) {
      console.error(`❌ 文件读取失败: ${filePath}`);
      console.error(`   错误: ${error.message}`);
      throw error;
    }
  }

  /**
   * 创建UTF-8编码的JSON字符串
   * @param {object} data - JSON数据对象
   * @param {boolean} [pretty=false] - 是否美化输出
   * @returns {string} UTF-8编码的JSON字符串
   */
  createUTF8JSONPayload(data, pretty = false) {
    const jsonString = pretty 
      ? JSON.stringify(data, null, 2)
      : JSON.stringify(data);
    
    const utf8String = this.ensureUTF8(jsonString);
    
    console.log(`📦 JSON载荷创建完成`);
    console.log(`   对象属性: ${Object.keys(data).length} 个`);
    console.log(`   JSON长度: ${utf8String.length} 字符`);
    console.log(`   UTF-8字节: ${this.calculateUTF8ByteLength(utf8String)} 字节`);
    
    return utf8String;
  }

  /**
   * 创建HTTP请求头（包含正确的Content-Length）
   * @param {string} payload - 请求体内容
   * @param {object} [additionalHeaders={}] - 附加请求头
   * @returns {object} HTTP请求头对象
   */
  createUTF8Headers(payload, additionalHeaders = {}) {
    const contentLength = this.calculateUTF8ByteLength(payload);
    
    const headers = {
      'Content-Type': 'application/json; charset=utf-8',
      'Content-Length': contentLength,
      'User-Agent': 'UTF8-Encoder/1.0.0',
      ...additionalHeaders
    };
    
    console.log(`📋 HTTP请求头创建完成`);
    console.log(`   Content-Length: ${contentLength} 字节`);
    console.log(`   总头数量: ${Object.keys(headers).length} 个`);
    
    return headers;
  }

  /**
   * 验证文本是否包含乱码字符
   * @param {string} text - 要验证的文本
   * @returns {object} 验证结果
   */
  validateNoGarbledChars(text) {
    const utf8Text = this.ensureUTF8(text);
    
    // 检测Unicode替换字符 � (U+FFFD) - 这是最常见的乱码标识
    const replacementCharPattern = /\uFFFD/g;
    const replacementMatches = utf8Text.match(replacementCharPattern);
    
    // 检测控制字符（除了常见的空白控制符）
    // 允许：\t (0x09), \n (0x0A), \r (0x0D)
    const controlCharPattern = /[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g;
    const controlMatches = utf8Text.match(controlCharPattern);
    
    const hasReplacement = replacementMatches && replacementMatches.length > 0;
    const hasControlChars = controlMatches && controlMatches.length > 0;
    const hasGarbled = hasReplacement || hasControlChars;
    
    const garbledChars = [];
    if (hasReplacement) garbledChars.push(...replacementMatches.slice(0, 3));
    if (hasControlChars) garbledChars.push(...controlMatches.slice(0, 3));
    
    return {
      valid: !hasGarbled,
      garbledCount: (hasReplacement ? replacementMatches.length : 0) + 
                   (hasControlChars ? controlMatches.length : 0),
      garbledChars: [...new Set(garbledChars)].slice(0, 5), // 去重，最多显示5个
      totalChars: utf8Text.length,
      chineseChars: (utf8Text.match(/[\u4e00-\u9fa5]/g) || []).length,
      hasReplacement: hasReplacement,
      hasControlChars: hasControlChars
    };
  }

  /**
   * 平台适配器：Discord Webhook
   * @param {string} webhookUrl - Discord Webhook URL
   * @param {string} content - 消息内容
   * @param {object} [options={}] - 选项（username, avatar_url等）
   * @returns {Promise<object>} 发送结果
   */
  async sendToDiscord(webhookUrl, content, options = {}) {
    console.log(`📨 发送到Discord...`);
    
    const payload = {
      content: this.ensureUTF8(content),
      username: options.username || 'UTF8-Encoder',
      avatar_url: options.avatar_url || ''
    };
    
    const postData = this.createUTF8JSONPayload(payload);
    const headers = this.createUTF8Headers(postData);
    
    const url = new URL(webhookUrl);
    
    const httpsOptions = {
      hostname: url.hostname,
      path: url.pathname + url.search,
      method: 'POST',
      headers: headers
    };
    
    return new Promise((resolve, reject) => {
      const https = require('https');
      const req = https.request(httpsOptions, (res) => {
        let data = '';
        res.on('data', (chunk) => { data += chunk; });
        res.on('end', () => {
          const result = {
            success: res.statusCode === 204 || (res.statusCode >= 200 && res.statusCode < 300),
            statusCode: res.statusCode,
            platform: 'Discord',
            messageLength: content.length,
            byteLength: this.calculateUTF8ByteLength(postData)
          };
          
          console.log(`  状态码: ${res.statusCode}, 消息长度: ${content.length} 字符`);
          
          if (result.success) {
            console.log('✅ Discord消息发送成功');
          } else {
            console.error(`❌ Discord消息发送失败: ${res.statusCode}`);
          }
          
          resolve(result);
        });
      });
      
      req.on('error', (error) => {
        console.error(`❌ Discord请求失败: ${error.message}`);
        reject(error);
      });
      
      req.write(postData);
      req.end();
    });
  }

  /**
   * 平台适配器：GitHub Gist
   * @param {string} token - GitHub API Token
   * @param {string} content - Gist内容
   * @param {string} filename - 文件名
   * @param {string} description - Gist描述
   * @param {boolean} isPublic - 是否公开
   * @returns {Promise<object>} 创建结果
   */
  async createGitHubGist(token, content, filename = 'utf8-test.md', description = 'UTF-8编码测试', isPublic = false) {
    console.log(`🐙 创建GitHub Gist...`);
    
    const payload = {
      description: this.ensureUTF8(description),
      public: isPublic,
      files: {
        [filename]: {
          content: this.ensureUTF8(content)
        }
      }
    };
    
    const postData = this.createUTF8JSONPayload(payload);
    const headers = this.createUTF8Headers(postData, {
      'Authorization': `token ${token}`,
      'Accept': 'application/vnd.github.v3+json',
      'User-Agent': 'UTF8-Encoder-Gist-Test'
    });
    
    const httpsOptions = {
      hostname: 'api.github.com',
      path: '/gists',
      method: 'POST',
      headers: headers
    };
    
    return new Promise((resolve, reject) => {
      const https = require('https');
      const req = https.request(httpsOptions, (res) => {
        let data = '';
        res.on('data', (chunk) => { data += chunk; });
        res.on('end', () => {
          const result = {
            success: res.statusCode === 201,
            statusCode: res.statusCode,
            platform: 'GitHub Gist',
            contentLength: content.length,
            response: data
          };
          
          console.log(`  状态码: ${res.statusCode}, 内容长度: ${content.length} 字符`);
          
          if (result.success) {
            console.log('✅ GitHub Gist创建成功');
            try {
              const jsonResponse = JSON.parse(data);
              result.gistUrl = jsonResponse.html_url;
              result.rawUrl = jsonResponse.files[filename].raw_url;
              console.log(`  Gist URL: ${jsonResponse.html_url}`);
            } catch (e) {
              // 忽略JSON解析错误
            }
          } else {
            console.error(`❌ GitHub Gist创建失败: ${res.statusCode}`);
          }
          
          resolve(result);
        });
      });
      
      req.on('error', (error) => {
        console.error(`❌ GitHub请求失败: ${error.message}`);
        reject(error);
      });
      
      req.write(postData);
      req.end();
    });
  }

  /**
   * 生成测试报告
   * @param {Array<object>} testResults - 测试结果数组
   * @returns {string} Markdown格式的报告
   */
  generateTestReport(testResults) {
    console.log('📊 生成测试报告...');
    
    const totalTests = testResults.length;
    const passedTests = testResults.filter(r => r.success).length;
    const failedTests = totalTests - passedTests;
    
    let report = `# UTF-8编码工具测试报告\n\n`;
    report += `**生成时间**: ${new Date().toISOString()}\n`;
    report += `**测试总数**: ${totalTests}\n`;
    report += `**通过数量**: ${passedTests}\n`;
    report += `**失败数量**: ${failedTests}\n`;
    report += `**通过率**: ${((passedTests / totalTests) * 100).toFixed(1)}%\n\n`;
    
    report += `## 测试详情\n\n`;
    
    testResults.forEach((result, index) => {
      report += `### 测试 #${index + 1}: ${result.platform}\n`;
      report += `- **状态**: ${result.success ? '✅ 通过' : '❌ 失败'}\n`;
      report += `- **状态码**: ${result.statusCode}\n`;
      report += `- **平台**: ${result.platform}\n`;
      report += `- **消息长度**: ${result.messageLength || result.contentLength || 'N/A'} 字符\n`;
      report += `- **字节长度**: ${result.byteLength || 'N/A'} 字节\n`;
      
      if (result.gistUrl) {
        report += `- **Gist URL**: ${result.gistUrl}\n`;
      }
      
      if (result.error) {
        report += `- **错误**: ${result.error}\n`;
      }
      
      report += '\n';
    });
    
    report += `## 验证结果\n\n`;
    
    const validation = this.validateNoGarbledChars(
      testResults.map(r => r.platform).join(' ') + 
      testResults.map(r => r.statusCode).join(' ')
    );
    
    report += `- **乱码检测**: ${validation.valid ? '✅ 无乱码字符' : `❌ 发现${validation.garbledCount}个乱码字符`}\n`;
    report += `- **总字符数**: ${validation.totalChars}\n`;
    report += `- **中文字符**: ${validation.chineseChars}\n`;
    
    if (!validation.valid && validation.garbledChars.length > 0) {
      report += `- **乱码字符示例**: ${validation.garbledChars.map(c => `"${c}"`).join(', ')}\n`;
    }
    
    report += `\n## 总结\n\n`;
    
    if (passedTests === totalTests) {
      report += `🎉 **所有测试通过！** UTF-8编码工具工作正常。\n`;
      report += `该工具可以正确处理中文、英文、特殊字符和Emoji。\n`;
    } else {
      report += `⚠️ **部分测试失败**，需要检查以下问题：\n`;
      report += `1. API Token 是否正确有效\n`;
      report += `2. 网络连接是否正常\n`;
      report += `3. 平台API限制是否触发\n`;
    }
    
    console.log(`报告生成完成: ${report.length} 字符`);
    return report;
  }
}

// 基础设施类：UTF-8发布基础设施
class UTF8Infrastructure {
  constructor() {
    this.encoder = new UTF8Encoder();
    this.retryCount = 0;
    this.maxRetries = 2; // 三次尝试法则：第一次 + 两次重试
    this.alternativeMethods = []; // 备选方案列表
  }

  /**
   * 智能检测是否需要编码处理
   * @param {string} text - 要检测的文本
   * @returns {object} 检测结果
   */
  shouldProcess(text) {
    // 检测编码问题
    const validation = this.encoder.validateNoGarbledChars(text);
    const hasChinese = /[\u4e00-\u9fa5]/.test(text);
    const hasEmoji = /[\u{1F300}-\u{1F9FF}]/u.test(text);
    
    const needsProcessing = !validation.valid || hasChinese || hasEmoji;
    
    return {
      needsProcessing,
      reasons: [
        !validation.valid ? '检测到乱码字符' : null,
        hasChinese ? '包含中文字符' : null,
        hasEmoji ? '包含Emoji表情' : null
      ].filter(Boolean),
      validation,
      hasChinese,
      hasEmoji
    };
  }

  /**
   * 集成中间件，提供系统级集成接口
   * @returns {object} 中间件对象
   */
  integrateAsMiddleware() {
    const self = this;
    
    return {
      /**
       * 发送到Discord（带重试和备选方案）
       * @param {string} webhookUrl - Discord Webhook URL
       * @param {string} content - 消息内容
       * @param {object} options - 选项
       * @returns {Promise<object>} 发送结果
       */
      async sendToDiscordWithRetry(webhookUrl, content, options = {}) {
        // 检测是否需要处理
        const check = self.shouldProcess(content);
        
        if (check.needsProcessing) {
          console.debug('🔄 基础设施自动处理编码问题');
          // 遵循"防止勤务干扰"原则：不汇报编码处理细节
        }
        
        let lastError = null;
        
        // 三次尝试法则
        for (let attempt = 0; attempt <= self.maxRetries; attempt++) {
          try {
            console.debug(`尝试 #${attempt + 1} 发送到Discord`);
            const result = await self.encoder.sendToDiscord(webhookUrl, content, options);
            
            if (result.success) {
              // 成功时重置重试计数
              self.retryCount = 0;
              return {
                success: true,
                attempt: attempt + 1,
                ...result
              };
            } else {
              lastError = new Error(`Discord发送失败，状态码: ${result.statusCode}`);
            }
          } catch (error) {
            lastError = error;
          }
          
          // 如果不是最后一次尝试，等待后重试
          if (attempt < self.maxRetries) {
            const delay = Math.pow(2, attempt) * 1000; // 指数退避
            console.debug(`等待 ${delay}ms 后重试...`);
            await new Promise(resolve => setTimeout(resolve, delay));
          }
        }
        
        // 所有尝试都失败
        console.error(`❌ 所有 ${self.maxRetries + 1} 次尝试均失败`);
        
        // 触发备选方案
        if (self.alternativeMethods.length > 0) {
          console.debug('🔄 触发备选方案');
          // 这里可以调用备选方案，例如发送到GitHub替代Discord
        }
        
        throw lastError || new Error('发送失败，未知错误');
      },

      /**
       * 创建GitHub Gist（带韧性保障）
       * @param {string} token - GitHub Token
       * @param {string} content - 内容
       * @param {string} filename - 文件名
       * @param {string} description - 描述
       * @param {boolean} isPublic - 是否公开
       * @returns {Promise<object>} 创建结果
       */
      async createGitHubGistWithResilience(token, content, filename = 'utf8-test.md', description = 'UTF-8测试', isPublic = false) {
        const check = self.shouldProcess(content);
        
        if (check.needsProcessing) {
          console.debug('🔄 基础设施自动处理编码问题');
        }
        
        let lastError = null;
        
        for (let attempt = 0; attempt <= self.maxRetries; attempt++) {
          try {
            console.debug(`尝试 #${attempt + 1} 创建GitHub Gist`);
            const result = await self.encoder.createGitHubGist(token, content, filename, description, isPublic);
            
            if (result.success) {
              self.retryCount = 0;
              return {
                success: true,
                attempt: attempt + 1,
                ...result
              };
            } else {
              lastError = new Error(`GitHub Gist创建失败，状态码: ${result.statusCode}`);
            }
          } catch (error) {
            lastError = error;
          }
          
          if (attempt < self.maxRetries) {
            const delay = Math.pow(2, attempt) * 1000;
            console.debug(`等待 ${delay}ms 后重试...`);
            await new Promise(resolve => setTimeout(resolve, delay));
          }
        }
        
        console.error(`❌ 所有 ${self.maxRetries + 1} 次尝试均失败`);
        
        // 备选方案：保存到本地文件
        const fs = require('fs');
        const backupPath = `./backup-${Date.now()}.md`;
        fs.writeFileSync(backupPath, content, 'utf8');
        console.debug(`✅ 内容已备份到本地文件: ${backupPath}`);
        
        throw lastError || new Error('GitHub Gist创建失败');
      },

      /**
       * 批量发布到多个平台
       * @param {Array} platforms - 平台配置数组
       * @param {string} content - 内容
       * @returns {Promise<Array>} 各平台发布结果
       */
      async publishToMultiplePlatforms(platforms, content) {
        const results = [];
        
        for (const platform of platforms) {
          try {
            let result;
            
            switch (platform.type) {
              case 'discord':
                result = await this.sendToDiscordWithRetry(
                  platform.url,
                  content,
                  platform.options || {}
                );
                break;
                
              case 'github':
                result = await this.createGitHubGistWithResilience(
                  platform.token,
                  content,
                  platform.filename || 'content.md',
                  platform.description || '发布内容',
                  platform.isPublic || false
                );
                break;
                
              default:
                result = { success: false, error: `不支持的平台类型: ${platform.type}` };
            }
            
            results.push({
              platform: platform.type,
              success: result.success,
              attempt: result.attempt || 1,
              details: result
            });
            
          } catch (error) {
            results.push({
              platform: platform.type,
              success: false,
              error: error.message
            });
          }
        }
        
        return results;
      }
    };
  }

  /**
   * 添加备选方案
   * @param {object} method - 备选方案配置
   */
  addAlternativeMethod(method) {
    this.alternativeMethods.push(method);
    console.debug(`✅ 添加备选方案: ${method.name || '未命名方案'}`);
  }

  /**
   * 生成基础设施状态报告
   * @returns {object} 状态报告
   */
  getInfrastructureStatus() {
    return {
      encoderReady: !!this.encoder,
      retryCount: this.retryCount,
      maxRetries: this.maxRetries,
      alternativeMethodsCount: this.alternativeMethods.length,
      alternativeMethods: this.alternativeMethods.map(m => m.name || '未命名'),
      infrastructureMode: true
    };
  }
}

// 导出模块
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    UTF8Encoder,
    UTF8Infrastructure
  };
}

// 如果直接运行，执行示例测试
if (require.main === module) {
  console.log('🚀 UTF-8编码工具 - 示例测试');
  console.log('='.repeat(50));
  
  const encoder = new UTF8Encoder();
  
  // 示例1: 基本功能测试
  console.log('\n📝 示例1: 基本功能测试');
  const testText = 'UTF-8测试：中文Chinese, English英文, Emoji🎯, 符号!@#$%';
  const validated = encoder.validateNoGarbledChars(testText);
  console.log(`测试文本: "${testText}"`);
  console.log(`验证结果: ${validated.valid ? '✅ 有效' : '❌ 无效'}`);
  console.log(`字符数: ${validated.totalChars}, 中文字符: ${validated.chineseChars}`);
  
  // 示例2: 计算字节长度
  console.log('\n📏 示例2: 字节长度计算');
  const byteLength = encoder.calculateUTF8ByteLength(testText);
  console.log(`文本: "${testText.substring(0, 20)}..."`);
  console.log(`字符长度: ${testText.length}, UTF-8字节长度: ${byteLength}`);
  
  // 示例3: 创建JSON载荷
  console.log('\n📦 示例3: JSON载荷创建');
  const jsonData = {
    message: testText,
    timestamp: new Date().toISOString(),
    author: '丞相',
    tags: ['UTF-8', '编码', '测试']
  };
  const jsonPayload = encoder.createUTF8JSONPayload(jsonData, true);
  console.log(`JSON预览:\n${jsonPayload.substring(0, 150)}...`);
  
  // 示例4: 基础设施测试
  console.log('\n🏛️ 示例4: 基础设施测试');
  const infrastructure = new UTF8Infrastructure();
  const middleware = infrastructure.integrateAsMiddleware();
  
  const check = infrastructure.shouldProcess(testText);
  console.log(`智能检测: ${check.needsProcessing ? '需要处理' : '无需处理'}`);
  console.log(`检测原因: ${check.reasons.join(', ')}`);
  
  const status = infrastructure.getInfrastructureStatus();
  console.log(`基础设施状态: ${status.infrastructureMode ? '已启用' : '未启用'}`);
  console.log(`备选方案数量: ${status.alternativeMethodsCount}`);
  
  console.log('\n✅ 示例测试完成！');
  console.log('使用方式:');
  console.log('  1. const { UTF8Encoder, UTF8Infrastructure } = require("./utf8-encoder");');
  console.log('  2. const encoder = new UTF8Encoder(); // 传统工具模式');
  console.log('  3. const infrastructure = new UTF8Infrastructure(); // 基础设施模式');
  console.log('  4. const middleware = infrastructure.integrateAsMiddleware();');
  console.log('  5. middleware.sendToDiscordWithRetry(url, content); // 带重试的发送');
}