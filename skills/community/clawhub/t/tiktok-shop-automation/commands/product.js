/**
 * 商品管理模块
 * 集成 TikTok Shop 商品 API
 */

import { getCurrentAccount, loadConfig } from './init.js';
import { createTikTokAPI } from '../src/api.js';
import fs from 'fs';
import csv from 'csv-parser';
import { createFeishuIntegration } from '../src/feishu.js';

/**
 * 批量导入商品
 */
export async function importProducts(options) {
  const account = getCurrentAccount();
  const config = loadConfig();

  console.log('📦 批量导入商品...');
  console.log(`  文件：${options.file}`);
  console.log(`  店铺：${options.shop || account?.shopId || '默认店铺'}`);
  console.log(`  自动上架：${options.autoPublish ? '是' : '否'}`);

  try {
    // 读取 CSV 文件
    const products = await readCSV(options.file);
    console.log(`✓ 读取到 ${products.length} 个商品`);

    const tiktokAPI = createTikTokAPI(config);
    const shopId = options.shop || account?.shopId || config.tiktok?.shopId || 'mock_shop';
    
    let successCount = 0;
    const createdProducts = [];

    for (const product of products) {
      const result = await tiktokAPI.createProduct(shopId, {
        title: product.title,
        price: parseFloat(product.price),
        stock: parseInt(product.stock) || 100,
        description: product.description || '',
        images: product.images ? product.images.split(',') : []
      });

      if (result.code === 0) {
        successCount++;
        createdProducts.push({
          ...product,
          product_id: result.data.product_id
        });
        console.log(`✓ 商品创建成功：${product.title}`);
      }
    }

    console.log(`\n✓ 导入完成，成功 ${successCount}/${products.length} 个商品`);

    return {
      count: successCount,
      total: products.length,
      products: createdProducts
    };
    
  } catch (error) {
    console.error('✗ 导入失败:', error.message);
    throw error;
  }
}

/**
 * 创建单个商品
 */
export async function createProduct(options) {
  const account = getCurrentAccount();
  const config = loadConfig();

  console.log('📦 创建商品...');
  console.log(`  标题：${options.title}`);
  console.log(`  价格：$${options.price}`);
  console.log(`  库存：${options.stock}`);

  try {
    const tiktokAPI = createTikTokAPI(config);
    const shopId = account?.shopId || config.tiktok?.shopId || 'mock_shop';
    
    const result = await tiktokAPI.createProduct(shopId, {
      title: options.title,
      price: parseFloat(options.price),
      stock: parseInt(options.stock),
      description: options.description || '',
      images: options.images ? [options.images] : []
    });

    if (result.code === 0) {
      console.log('✓ 商品创建成功');
      
      return {
        productId: result.data.product_id,
        success: true
      };
    } else {
      throw new Error(result.message || '创建失败');
    }
    
  } catch (error) {
    console.error('✗ 创建失败:', error.message);
    throw error;
  }
}

/**
 * 同步库存
 */
export async function syncInventory(options) {
  const account = getCurrentAccount();
  const config = loadConfig();

  console.log('🔄 同步库存...');
  console.log(`  ERP 系统：${options.erpSystem || '未指定'}`);
  console.log(`  自动更新：${options.autoUpdate ? '是' : '否'}`);

  try {
    const tiktokAPI = createTikTokAPI(config);
    const shopId = account?.shopId || config.tiktok?.shopId || 'mock_shop';
    
    // 获取当前商品列表
    const productResult = await tiktokAPI.listProducts(shopId);
    const products = productResult.data?.products || [];
    
    console.log(`✓ 获取到 ${products.length} 个商品`);

    // Mock ERP 库存数据
    const erpInventory = {};
    products.forEach(p => {
      erpInventory[p.product_id] = Math.floor(Math.random() * 200);
    });

    // 更新库存
    if (options.autoUpdate) {
      let updateCount = 0;
      
      for (const [productId, quantity] of Object.entries(erpInventory)) {
        const result = await tiktokAPI.updateStock(shopId, productId, quantity);
        
        if (result.code === 0) {
          updateCount++;
          console.log(`✓ 更新库存：${productId} -> ${quantity}`);
        }
      }
      
      console.log(`\n✓ 库存同步完成，更新 ${updateCount} 个商品`);
    }

    return {
      synced: true,
      count: products.length,
      inventory: erpInventory
    };
    
  } catch (error) {
    console.error('✗ 同步失败:', error.message);
    throw error;
  }
}

/**
 * 设置库存预警
 */
export async function setStockAlert(options) {
  const config = loadConfig();

  console.log('⚠️  设置库存预警...');
  console.log(`  阈值：${options.threshold}`);
  console.log(`  通知邮箱：${options.notifyEmail}`);

  try {
    const tiktokAPI = createTikTokAPI(config);
    const shopId = config.tiktok?.shopId || 'mock_shop';
    
    // 获取商品列表
    const productResult = await tiktokAPI.listProducts(shopId);
    const products = productResult.data?.products || [];
    
    // 检查库存预警
    const lowStockProducts = products.filter(p => p.stock < options.threshold);
    
    if (lowStockProducts.length > 0) {
      console.log(`\n⚠️  发现 ${lowStockProducts.length} 个商品库存不足:`);
      lowStockProducts.forEach(p => {
        console.log(`  - ${p.title}: ${p.stock} (阈值：${options.threshold})`);
      });

      // 发送飞书通知
      if (config.feishu?.enabled || options.notifyEmail) {
        const feishu = createFeishuIntegration(config);
        
        for (const product of lowStockProducts) {
          await feishu.sendStockAlert(product, options.threshold);
        }
        
        console.log('✓ 已发送库存预警通知');
      }
    } else {
      console.log('✓ 所有商品库存充足');
    }

    return {
      checked: products.length,
      alerts: lowStockProducts.length,
      products: lowStockProducts
    };
    
  } catch (error) {
    console.error('✗ 设置预警失败:', error.message);
    throw error;
  }
}

/**
 * 读取 CSV 文件
 */
function readCSV(filePath) {
  return new Promise((resolve, reject) => {
    const results = [];
    
    if (!fs.existsSync(filePath)) {
      reject(new Error(`文件不存在：${filePath}`));
      return;
    }

    fs.createReadStream(filePath)
      .pipe(csv())
      .on('data', (data) => results.push(data))
      .on('end', () => resolve(results))
      .on('error', (error) => reject(error));
  });
}
