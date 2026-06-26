/**
 * 飞书集成模块
 * 实现订单同步、通知发送等功能
 * 不依赖 TikTok API，可独立使用
 */

import { loadConfig } from './config.js';

/**
 * 飞书 API 基础 URL
 */
const FEISHU_API_BASE = 'https://open.feishu.cn/open-apis';

/**
 * 飞书集成类
 */
export class FeishuIntegration {
  constructor(config = null) {
    this.config = config || loadConfig();
    this.appToken = this.config.feishu.appToken;
    this.tableId = this.config.feishu.tableId;
    this.webhookUrl = this.config.feishu.webhookUrl || this.config.notifications.feishuWebhook;
  }

  /**
   * 发送 HTTP 请求
   */
  async request(endpoint, options = {}) {
    const url = `${FEISHU_API_BASE}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };

    if (options.accessToken) {
      headers['Authorization'] = `Bearer ${options.accessToken}`;
    }

    const response = await fetch(url, {
      method: options.method || 'GET',
      headers,
      body: options.body ? JSON.stringify(options.body) : null
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(`飞书 API 请求失败：${result.msg || response.statusText}`);
    }

    return result;
  }

  /**
   * 获取飞书访问令牌（租户级别）
   * 实际使用时需要通过应用凭证获取
   */
  async getTenantAccessToken(appId, appSecret) {
    console.log('🔐 获取飞书访问令牌...');
    
    // 这里使用 Mock 模式，实际使用需要调用飞书 OAuth API
    // const result = await this.request('/auth/v3/tenant_access_token/internal', {
    //   method: 'POST',
    //   body: { app_id: appId, app_secret: appSecret }
    // });
    
    return {
      tenant_access_token: 'mock_feishu_token_' + Date.now(),
      expire: 7200
    };
  }

  /**
   * 同步订单到飞书多维表格
   * @param {Array} orders - 订单列表
   * @param {Object} options - 选项
   */
  async syncOrdersToBitable(orders, options = {}) {
    console.log('📊 同步订单到飞书多维表格...');
    
    if (!this.appToken || !this.tableId) {
      throw new Error('飞书多维表格配置不完整，请先配置 App Token 和 Table ID');
    }

    const appToken = options.appToken || this.appToken;
    const tableId = options.tableId || this.tableId;

    console.log(`  目标多维表格：${appToken}`);
    console.log(`  数据表 ID: ${tableId}`);
    console.log(`  订单数量：${orders.length}`);

    // 准备数据
    const records = orders.map(order => ({
      fields: {
        '订单 ID': order.order_id,
        '订单状态': this._translateOrderStatus(order.status),
        '订单金额': order.amount,
        '下单时间': order.created_at,
        '客户姓名': order.customer?.name || '',
        '客户邮箱': order.customer?.email || '',
        '商品数量': order.items?.reduce((sum, item) => sum + item.quantity, 0) || 0,
        '物流单号': order.tracking_number || '',
        '同步时间': new Date().toISOString()
      }
    }));

    // Mock 模式：模拟 API 调用
    if (this.config.tiktok?.useMock) {
      console.log('✓ [Mock] 订单同步成功');
      console.log(`  已同步 ${records.length} 条记录`);
      
      return {
        success: true,
        synced: records.length,
        records: records.map((r, i) => ({ record_id: `rec_mock_${i}`, fields: r.fields }))
      };
    }

    // 实际 API 调用（分批写入，每批最多 500 条）
    const batchSize = 500;
    const results = [];

    for (let i = 0; i < records.length; i += batchSize) {
      const batch = records.slice(i, i + batchSize);
      
      const result = await this.request(
        `/bitable/v1/apps/${appToken}/tables/${tableId}/records/batch_create`,
        {
          method: 'POST',
          body: { records: batch }
        }
      );

      results.push(result);
    }

    const totalSynced = results.reduce((sum, r) => sum + (r.data?.records?.length || 0), 0);
    console.log(`✓ 订单同步完成，共 ${totalSynced} 条记录`);

    return {
      success: true,
      synced: totalSynced,
      results
    };
  }

  /**
   * 更新飞书多维表格记录
   * @param {Array} records - 记录列表
   */
  async updateBitableRecords(records, options = {}) {
    console.log('📝 更新飞书多维表格记录...');

    const appToken = options.appToken || this.appToken;
    const tableId = options.tableId || this.tableId;

    // Mock 模式
    if (this.config.tiktok?.useMock) {
      console.log('✓ [Mock] 记录更新成功');
      return {
        success: true,
        updated: records.length
      };
    }

    const result = await this.request(
      `/bitable/v1/apps/${appToken}/tables/${tableId}/records/batch_update`,
      {
        method: 'PUT',
        body: { records }
      }
    );

    console.log(`✓ 更新完成，共 ${result.data?.records?.length || 0} 条记录`);

    return result;
  }

  /**
   * 查询飞书多维表格记录
   * @param {Object} options - 查询选项
   */
  async queryBitableRecords(options = {}) {
    console.log('🔍 查询飞书多维表格记录...');

    const appToken = options.appToken || this.appToken;
    const tableId = options.tableId || this.tableId;
    const filter = options.filter || {};

    // Mock 模式
    if (this.config.tiktok?.useMock) {
      console.log('✓ [Mock] 查询成功');
      return {
        success: true,
        records: [
          {
            record_id: 'rec_mock_1',
            fields: {
              '订单 ID': 'ORD001',
              '订单状态': '待发货',
              '订单金额': 29.99
            }
          }
        ],
        total: 1
      };
    }

    const queryParams = new URLSearchParams();
    if (filter.field_name) {
      queryParams.append('field_name', filter.field_name);
    }
    if (filter.value) {
      queryParams.append('value', filter.value);
    }

    const result = await this.request(
      `/bitable/v1/apps/${appToken}/tables/${tableId}/records?${queryParams}`
    );

    return {
      success: true,
      records: result.data?.items || [],
      total: result.data?.total || 0
    };
  }

  /**
   * 发送飞书消息（通过机器人 Webhook）
   * @param {string} message - 消息内容
   * @param {Object} options - 选项
   */
  async sendWebhookMessage(message, options = {}) {
    console.log('📤 发送飞书消息...');

    const webhookUrl = options.webhookUrl || this.webhookUrl;

    if (!webhookUrl) {
      throw new Error('飞书 Webhook URL 未配置');
    }

    const messageType = options.type || 'text';
    let content;

    if (messageType === 'text') {
      content = {
        msg_type: 'text',
        content: {
          text: message
        }
      };
    } else if (messageType === 'post') {
      content = {
        msg_type: 'post',
        content: {
          post: {
            zh_cn: {
              title: options.title || '通知',
              content: [
                [
                  {
                    tag: 'text',
                    text: message
                  }
                ]
              ]
            }
          }
        }
      };
    } else if (messageType === 'interactive') {
      content = {
        msg_type: 'interactive',
        card: options.card
      };
    }

    // Mock 模式
    if (this.config.tiktok?.useMock) {
      console.log('✓ [Mock] 消息发送成功');
      console.log(`  内容：${message.substring(0, 50)}...`);
      
      return {
        success: true,
        messageId: 'mock_msg_' + Date.now()
      };
    }

    const response = await fetch(webhookUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(content)
    });

    const result = await response.json();

    if (result.StatusCode !== 0 && result.code !== 0) {
      throw new Error(`飞书消息发送失败：${result.msg || result.StatusMessage}`);
    }

    console.log('✓ 消息发送成功');

    return {
      success: true,
      messageId: result.data?.message_id || result.message_id
    };
  }

  /**
   * 发送订单通知
   * @param {Object} order - 订单信息
   */
  async sendOrderNotification(order) {
    const message = `📦 新订单通知

订单 ID: ${order.order_id}
订单金额：¥${order.amount}
下单时间：${new Date(order.created_at).toLocaleString('zh-CN')}
客户：${order.customer?.name || '未知'}
状态：${this._translateOrderStatus(order.status)}

商品:
${order.items?.map(item => `  - ${item.product_id} x ${item.quantity}`).join('\n') || '无'}`;

    return await this.sendWebhookMessage(message, {
      type: 'text'
    });
  }

  /**
   * 发送库存预警通知
   * @param {Object} product - 商品信息
   * @param {number} threshold - 预警阈值
   */
  async sendStockAlert(product, threshold) {
    const message = `⚠️ 库存预警

商品：${product.title}
当前库存：${product.stock}
预警阈值：${threshold}

请及时补货！`;

    return await this.sendWebhookMessage(message, {
      type: 'text'
    });
  }

  /**
   * 发送日报通知
   * @param {Object} report - 日报数据
   */
  async sendDailyReport(report) {
    const message = `📊 每日销售日报

日期：${report.date}
总销售额：¥${report.totalSales}
总订单数：${report.totalOrders}
转化率：${report.conversionRate}%

详细报告请查看附件或登录后台查看。`;

    return await this.sendWebhookMessage(message, {
      type: 'text'
    });
  }

  /**
   * 翻译订单状态
   */
  _translateOrderStatus(status) {
    const statusMap = {
      'pending': '待处理',
      'processing': '处理中',
      'shipped': '已发货',
      'delivered': '已送达',
      'cancelled': '已取消',
      'refunded': '已退款'
    };
    return statusMap[status] || status;
  }

  /**
   * 测试飞书连接
   */
  async testConnection() {
    console.log('🔌 测试飞书连接...');

    try {
      // Mock 模式直接返回成功
      if (this.config.tiktok?.useMock) {
        console.log('✓ [Mock] 飞书连接测试成功');
        return { success: true, message: 'Mock 模式' };
      }

      // 实际连接测试
      if (this.webhookUrl) {
        await this.sendWebhookMessage('TikTok Shop Automation 连接测试', {
          type: 'text'
        });
        console.log('✓ 飞书连接测试成功');
        return { success: true, message: '连接正常' };
      } else {
        console.log('⚠️  未配置 Webhook URL');
        return { success: false, message: '未配置 Webhook URL' };
      }
    } catch (error) {
      console.error('✗ 飞书连接测试失败:', error.message);
      return { success: false, message: error.message };
    }
  }
}

/**
 * 创建飞书集成实例
 */
export function createFeishuIntegration(config) {
  return new FeishuIntegration(config);
}

export default FeishuIntegration;
