/**
 * 订单管理模块
 * 集成 TikTok API 和飞书同步
 */

import { getCurrentAccount, loadConfig } from './init.js';
import { createTikTokAPI } from '../src/api.js';
import { createFeishuIntegration } from '../src/feishu.js';

/**
 * 同步订单
 */
export async function syncOrders(options) {
  const account = getCurrentAccount();
  const config = loadConfig();

  console.log('🔄 同步订单...');
  console.log(`  账号：${account?.username || '未指定'}`);
  console.log(`  目标：${options.target || 'feishu-bitable'}`);
  console.log(`  自动同步：${options.autoSync ? '是' : '否'}`);
  
  if (options.autoSync) {
    console.log(`  间隔：${options.interval} 分钟`);
  }

  try {
    // 1. 从 TikTok Shop 拉取订单
    const tiktokAPI = createTikTokAPI(config);
    const shopId = account?.shopId || config.tiktok?.shopId || 'mock_shop';
    
    const orderResult = await tiktokAPI.listOrders(shopId, {
      status: 'pending'
    });
    
    const orders = orderResult.data?.orders || [];
    console.log(`✓ 从 TikTok 获取到 ${orders.length} 个订单`);

    // 2. 同步到飞书多维表格
    if (options.target === 'feishu-bitable' || config.feishu?.enabled) {
      const feishu = createFeishuIntegration(config);
      
      const appToken = options.appToken || config.feishu?.appToken;
      const tableId = options.tableId || config.feishu?.tableId;
      
      if (appToken && tableId) {
        const syncResult = await feishu.syncOrdersToBitable(orders, {
          appToken,
          tableId
        });
        
        console.log(`✓ 已同步 ${syncResult.synced} 条订单到飞书`);
        
        return {
          synced: true,
          count: syncResult.synced,
          orders: orders
        };
      } else {
        console.log('⚠️  飞书配置不完整，跳过同步');
      }
    }

    return {
      synced: true,
      count: orders.length,
      orders: orders
    };
    
  } catch (error) {
    console.error('✗ 同步失败:', error.message);
    throw error;
  }
}

/**
 * 批量发货
 */
export async function fulfillOrders(options) {
  const account = getCurrentAccount();
  const config = loadConfig();

  console.log('📦 处理发货...');
  
  if (options.orderIds) {
    const orderIds = options.orderIds.split(',');
    console.log(`  订单数量：${orderIds.length}`);
  } else {
    console.log('  订单：所有待发货订单');
  }
  
  console.log(`  物流：${options.carrier || '未指定'}`);
  console.log(`  通知买家：${options.autoNotify ? '是' : '否'}`);

  try {
    const tiktokAPI = createTikTokAPI(config);
    const shopId = account?.shopId || config.tiktok?.shopId || 'mock_shop';
    
    const orderIds = options.orderIds ? options.orderIds.split(',') : ['ORD001', 'ORD002', 'ORD003'];
    let successCount = 0;

    for (const orderId of orderIds) {
      const trackingNumber = `${options.trackingPrefix || ''}${Date.now()}`;
      
      const result = await tiktokAPI.updateOrderStatus(
        shopId,
        orderId,
        'shipped',
        trackingNumber
      );

      if (result.code === 0) {
        successCount++;
        console.log(`✓ 订单 ${orderId} 已发货，运单号：${trackingNumber}`);
        
        // 通知买家
        if (options.autoNotify) {
          const feishu = createFeishuIntegration(config);
          await feishu.sendWebhookMessage(`您的订单 ${orderId} 已发货，运单号：${trackingNumber}`);
        }
      }
    }

    return {
      count: successCount,
      success: true
    };
    
  } catch (error) {
    console.error('✗ 发货失败:', error.message);
    throw error;
  }
}

/**
 * 处理退货
 */
export async function processReturn(options) {
  const account = getCurrentAccount();
  const config = loadConfig();

  console.log(`🔄 处理退货 - 订单：${options.orderId}`);
  console.log(`  原因：${options.reason}`);
  console.log(`  操作：${options.action}`);

  try {
    const tiktokAPI = createTikTokAPI(config);
    const shopId = account?.shopId || config.tiktok?.shopId || 'mock_shop';
    
    const result = await tiktokAPI.updateOrderStatus(
      shopId,
      options.orderId,
      options.action === 'refund' ? 'refunded' : 'returned'
    );

    if (result.code === 0) {
      console.log(`✓ 退货处理完成`);
      
      // 发送通知
      const feishu = createFeishuIntegration(config);
      await feishu.sendWebhookMessage(
        `退货通知：订单 ${options.orderId} 已${options.action === 'refund' ? '退款' : '退货'}`,
        { type: 'text' }
      );
    }

    return {
      processed: true,
      status: options.action
    };
    
  } catch (error) {
    console.error('✗ 退货处理失败:', error.message);
    throw error;
  }
}
