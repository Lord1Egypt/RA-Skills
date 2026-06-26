import axios from 'axios';

export function registerSlonAideTools(api) {
  let cachedToken = null;
  let tokenExpiry = null;
  let config = null;

  // 初始化配置
  function initConfig() {
    if (!config) {
      config = api.getConfig();
      if (!config) {
        throw new Error('SlonAide 插件配置未加载');
      }
    }
    return config;
  }

  // 获取认证令牌（带缓存）
  async function getToken() {
    // 检查缓存
    if (cachedToken && tokenExpiry && Date.now() < tokenExpiry) {
      return cachedToken;
    }

    const config = initConfig();
    const apiKey = config.apiKey;
    const baseUrl = config.baseUrl || 'https://api.aidenote.cn';

    if (!apiKey) {
      throw new Error('未配置 SlonAide API Key。请运行: openclaw config set slonaide.apiKey YOUR_API_KEY');
    }

    try {
      const response = await axios.post(
        `${baseUrl}/api/UserapikeyMstr/GetToken/${apiKey}`,
        {},
        {
          headers: { 'Content-Type': 'application/json' },
          timeout: 10000
        }
      );

      const data = response.data;

      if (data.code === 200) {
        cachedToken = data.result.token;
        // 令牌有效期6天，提前1小时刷新
        tokenExpiry = Date.now() + (6 * 24 - 1) * 60 * 60 * 1000;
        return cachedToken;
      } else {
        throw new Error(`获取令牌失败: ${data.message || '未知错误'}`);
      }
    } catch (error) {
      if (error.response) {
        throw new Error(`API 错误: ${error.response.data?.message || error.response.statusText}`);
      } else if (error.request) {
        throw new Error('网络连接失败，请检查网络设置');
      } else {
        throw new Error(`请求失败: ${error.message}`);
      }
    }
  }

  // 工具1: 获取录音笔记列表
  api.registerTool({
    name: 'slonaide_get_list',
    description: '获取 SlonAide 录音笔记列表',
    parameters: {
      type: 'object',
      properties: {
        page: {
          type: 'number',
          description: '页码（从1开始）',
          default: 1
        },
        pageSize: {
          type: 'number',
          description: '每页数量（1-50）',
          default: 10,
          minimum: 1,
          maximum: 50
        },
        keyword: {
          type: 'string',
          description: '搜索关键词（可选）'
        }
      }
    },
    async execute(_toolCallId, params) {
      try {
        const token = await getToken();
        const config = initConfig();
        const baseUrl = config.baseUrl || 'https://api.aidenote.cn';

        const response = await axios.post(
          `${baseUrl}/api/audiofileMstr/audiofileseleUserAllList`,
          {
            order: 'descending',
            orderField: 'createTime',
            page: params.page || 1,
            pageSize: params.pageSize || 10,
            selectValue: params.keyword || ''
          },
          {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            },
            timeout: 15000
          }
        );

        const data = response.data;

        if (data.code === 200) {
          const result = data.result;
          const records = result.records || result.items || [];
          const total = result.total || 0;

          if (records.length === 0) {
            return {
              content: [{ type: 'text', text: '📭 没有找到录音笔记记录' }]
            };
          }

          // 格式化输出
          let output = `📋 SlonAide 录音笔记列表\n`;
          output += `总计: ${total} 条记录\n`;
          output += `当前页: ${records.length} 条\n\n`;

          records.forEach((record, index) => {
            const title = record.audiofileTitle || record.audiofileFileName || '未命名';
            const fileId = record.id || '未知ID';
            
            // 格式化时间
            let timeStr = '未知时间';
            if (record.createTime) {
              try {
                const timestamp = parseInt(record.createTime) / 1000;
                const date = new Date(timestamp * 1000);
                timeStr = date.toLocaleString('zh-CN');
              } catch (e) {
                timeStr = record.createTime;
              }
            }

            // 格式化时长
            const durationMs = record.audiofileTimeLength || 0;
            const minutes = Math.floor(durationMs / 60000);
            const seconds = Math.floor((durationMs % 60000) / 1000);

            output += `${index + 1}. ${title}\n`;
            output += `   ID: ${fileId}\n`;
            output += `   时间: ${timeStr}\n`;
            output += `   时长: ${minutes}分${seconds}秒\n`;
            
            // 状态
            const transcriptStatus = record.transcriptStatus || 0;
            const summaryStatus = record.summaryStatus || 0;
            
            let status = [];
            if (transcriptStatus === 2) status.push('✅ 已转写');
            else if (transcriptStatus === 1) status.push('🔄 转写中');
            else status.push('⏳ 未转写');
            
            if (summaryStatus === 2) status.push('✅ 已总结');
            else if (summaryStatus === 1) status.push('🔄 总结中');
            else status.push('⏳ 未总结');
            
            output += `   状态: ${status.join(' | ')}\n\n`;
          });

          if (total > records.length) {
            output += `📄 提示: 还有更多记录，可以使用 page 参数查看下一页`;
          }

          return {
            content: [{ type: 'text', text: output }]
          };
        } else {
          throw new Error(`获取列表失败: ${data.message || '未知错误'}`);
        }
      } catch (error) {
        return {
          content: [{ type: 'text', text: `❌ 获取列表失败: ${error.message}` }]
        };
      }
    }
  });

  // 工具2: 获取录音笔记详情
  api.registerTool({
    name: 'slonaide_get_detail',
    description: '获取 SlonAide 录音笔记详情（转写文本和AI总结）',
    parameters: {
      type: 'object',
      properties: {
        fileId: {
          type: 'string',
          description: '录音笔记文件ID（必填）'
        }
      },
      required: ['fileId']
    },
    async execute(_toolCallId, params) {
      try {
        const token = await getToken();
        const config = initConfig();
        const baseUrl = config.baseUrl || 'https://api.aidenote.cn';

        // 获取笔记详情
        const response = await axios.get(
          `${baseUrl}/api/audiofileMstr/GetAudioFileDetail/${params.fileId}`,
          {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            },
            timeout: 15000
          }
        );

        const data = response.data;

        if (data.code === 200) {
          const detail = data.result;
          const title = detail.audiofileTitle || detail.audiofileFileName || '未命名';
          
          let output = `📝 SlonAide 录音笔记详情\n`;
          output += `标题: ${title}\n`;
          output += `文件ID: ${params.fileId}\n`;

          // 转写文本
          const transcript = detail.transcriptText || '';
          if (transcript) {
            output += `\n📄 转写文本 (${transcript.length} 字符):\n`;
            output += `${transcript.substring(0, 500)}`;
            if (transcript.length > 500) {
              output += `\n... (还有 ${transcript.length - 500} 字符)`;
            }
            output += `\n`;
          } else {
            output += `\n📄 转写文本: 暂无\n`;
          }

          // AI 总结
          const summary = detail.aiSummary || '';
          if (summary) {
            output += `\n🤖 AI 总结:\n`;
            output += `${summary}\n`;
          } else {
            output += `\n🤖 AI 总结: 暂无\n`;
          }

          // 标签
          const tags = detail.tags || [];
          if (tags.length > 0) {
            output += `\n🏷️ 标签: ${tags.join(', ')}\n`;
          }

          // 状态
          const transcriptStatus = detail.transcriptStatus || 0;
          const summaryStatus = detail.summaryStatus || 0;
          
          output += `\n📊 处理状态:\n`;
          output += `转写: ${transcriptStatus === 2 ? '✅ 已完成' : transcriptStatus === 1 ? '🔄 进行中' : '⏳ 未开始'}\n`;
          output += `总结: ${summaryStatus === 2 ? '✅ 已完成' : summaryStatus === 1 ? '🔄 进行中' : '⏳ 未开始'}\n`;

          return {
            content: [{ type: 'text', text: output }]
          };
        } else {
          throw new Error(`获取详情失败: ${data.message || '未知错误'}`);
        }
      } catch (error) {
        return {
          content: [{ type: 'text', text: `❌ 获取详情失败: ${error.message}` }]
        };
      }
    }
  });

  // 工具3: 获取最新笔记摘要
  api.registerTool({
    name: 'slonaide_get_summary',
    description: '获取最新录音笔记的摘要信息',
    parameters: {
      type: 'object',
      properties: {
        count: {
          type: 'number',
          description: '要获取的记录数量（1-10）',
          default: 3,
          minimum: 1,
          maximum: 10
        }
      }
    },
    async execute(_toolCallId, params) {
      try {
        const token = await getToken();
        const config = initConfig();
        const baseUrl = config.baseUrl || 'https://api.aidenote.cn';

        const response = await axios.post(
          `${baseUrl}/api/audiofileMstr/audiofileseleUserAllList`,
          {
            order: 'descending',
            orderField: 'createTime',
            page: 1,
            pageSize: params.count || 3
          },
          {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            },
            timeout: 15000
          }
        );

        const data = response.data;

        if (data.code === 200) {
          const result = data.result;
          const records = result.records || result.items || [];
          const total = result.total || 0;

          if (records.length === 0) {
            return {
              content: [{ type: 'text', text: '📭 没有找到录音笔记记录' }]
            };
          }

          let output = `📊 SlonAide 最新笔记摘要\n`;
          output += `总计记录: ${total} 条\n`;
          output += `最新 ${records.length} 条摘要:\n\n`;

          // 统计信息
          let completedTranscripts = 0;
          let completedSummaries = 0;
          const types = {};

          records.forEach((record, index) => {
            const title = record.audiofileTitle || record.audiofileFileName || '未命名';
            
            // 分析类型
            const titleLower = title.toLowerCase();
            let type = '其他';
            if (titleLower.includes('总结') || titleLower.includes('汇总')) type = '总结类';
            else if (titleLower.includes('异常') || titleLower.includes('错误') || titleLower.includes('失败')) type = '问题类';
            else if (titleLower.includes('系统') || titleLower.includes('行为') || titleLower.includes('参数')) type = '技术类';
            else if (titleLower.includes('信息') || titleLower.includes('需要') || titleLower.includes('补充')) type = '需求类';
            
            types[type] = (types[type] || 0) + 1;

            // 统计状态
            if (record.transcriptStatus === 2) completedTranscripts++;
            if (record.summaryStatus === 2) completedSummaries++;

            output += `${index + 1}. ${title}\n`;
            output += `   类型: ${type}\n`;
            
            // 状态简写
            let status = [];
            if (record.transcriptStatus === 2) status.push('已转写');
            else if (record.transcriptStatus === 1) status.push('转写中');
            
            if (record.summaryStatus === 2) status.push('已总结');
            else if (record.summaryStatus === 1) status.push('总结中');
            
            if (status.length > 0) {
              output += `   状态: ${status.join(' | ')}\n`;
            }
            output += `\n`;
          });

          // 添加统计信息
          output += `📈 统计信息:\n`;
          output += `转写完成率: ${completedTranscripts}/${records.length} (${Math.round(completedTranscripts/records.length*100)}%)\n`;
          output += `总结完成率: ${completedSummaries}/${records.length} (${Math.round(completedSummaries/records.length*100)}%)\n\n`;

          output += `🎯 内容类型分布:\n`;
          Object.entries(types).forEach(([type, count]) => {
            const percentage = Math.round(count / records.length * 100);
            output += `${type}: ${count} 条 (${percentage}%)\n`;
          });

          // 建议
          output += `\n💡 建议:\n`;
          if (completedTranscripts < records.length) {
            output += `• 部分笔记尚未转写，建议检查转写状态\n`;
          }
          if (completedSummaries < records.length) {
            output += `• 部分笔记尚未总结，可以等待或重新触发\n`;
          }

          const latestTitle = records[0]?.audiofileTitle || records[0]?.audiofileFileName || '';
          if (latestTitle.toLowerCase().includes('需要') || latestTitle.toLowerCase().includes('补充')) {
            output += `• 最新记录提示需要补充信息，建议优先处理\n`;
          }
          if (latestTitle.toLowerCase().includes('异常') || latestTitle.toLowerCase().includes('错误')) {
            output += `• 最新记录涉及异常情况，建议立即查看\n`;
          }

          return {
            content: [{ type: 'text', text: output }]
          };
        } else {
          throw new Error(`获取摘要失败: ${data.message || '未知错误'}`);
        }
      } catch (error) {
        return {
          content: [{ type: 'text', text: `❌ 获取摘要失败: ${error.message}` }]
        };
      }
    }
  });

  // 工具4: 测试连接
  api.registerTool({
    name: 'slonaide_test_connection',
    description: '测试 SlonAide API 连接和配置',
    parameters: {
      type: 'object',
      properties: {}
    },
    async execute(_toolCallId, _params) {
      try {
        const config = initConfig();
        const apiKey = config.apiKey;
        const baseUrl = config.baseUrl || 'https://api.aidenote.cn';

        if (!apiKey) {
          return {
            content: [{ type: 'text', text: '❌ 未配置 API Key\n请运行: openclaw config set slonaide.apiKey YOUR_API_KEY' }]
          };
        }

        let output = `🔍 SlonAide 连接测试\n`;
        output += `配置状态: ✅ 已配置\n`;
        output += `API Key: ${apiKey.substring(0, 10)}...${apiKey.substring(apiKey.length - 4)}\n`;
        output += `Base URL: ${baseUrl}\n\n`;

        output += `正在测试认证...\n`;

        try {
          const token = await getToken();
          output += `认证状态: ✅ 成功\n`;
          output += `令牌: ${token.substring(0, 20)}...\n\n`;

          // 测试获取列表
          output += `正在测试数据访问...\n`;
          const testResponse = await axios.post(
            `${baseUrl}/api/audiofileMstr/audiofileseleUserAllList`,
            {
              order: 'descending',
              orderField: 'createTime',
              page: 1,
              pageSize: 1
            },
            {
              headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
              },
              timeout: 10000
            }
          );

          const testData = testResponse.data;
          if (testData.code === 200) {
            const total = testData.result?.total || 0;
            output += `数据访问: ✅ 成功\n`;
            output += `总记录数: ${total} 条\n`;
            output += `服务状态: ✅ 正常\n`;
          } else {
            output += `数据访问: ⚠️ 部分成功\n`;
            output += `错误信息: ${testData.message || '未知错误'}\n`;
          }

        } catch (authError) {
          output += `认证状态: ❌ 失败\n`;
          output += `错误信息: ${authError.message}\n`;
          output += `\n💡 建议:\n`;
          output += `1. 检查 API Key 是否正确\n`;
          output += `2. 检查网络连接\n`;
          output += `3. 确认 API Key 是否有效\n`;
        }

        output += `\n✅ 测试完成`;

        return {
          content: [{ type: 'text', text: output }]
        };
      } catch (error) {
        return {
          content: [{ type: 'text', text: `❌ 连接测试失败: ${error.message}` }]
        };
      }
    }
  });
}

