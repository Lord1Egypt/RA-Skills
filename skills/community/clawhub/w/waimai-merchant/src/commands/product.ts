import { Command } from 'commander';
import chalk from 'chalk';
import * as productDb from '../db/product';
import * as merchantDb from '../db/merchant';

export function createProductCommands(): Command {
  const product = new Command('product').description('商品管理命令');

  // 添加新商品
  product
    .command('add')
    .description('添加新商品')
    .requiredOption('-m, --merchant <id>', '商家ID')
    .requiredOption('-n, --name <name>', '商品名称')
    .requiredOption('-p, --price <price>', '商品价格')
    .option('-d, --description <desc>', '商品描述')
    .option('-o, --original <price>', '原价')
    .option('-i, --image <url>', '商品图片URL')
    .option('-c, --category <category>', '商品分类')
    .option('-t, --time <minutes>', '配送时间（分钟）', '30')
    .option('-s, --stock <count>', '库存数量', '0')
    .action((options) => {
      try {
        const merchantId = parseInt(options.merchant);
        const merchant = merchantDb.getMerchantById(merchantId);
        if (!merchant) {
          console.log(chalk.red('❌ 商家不存在'));
          process.exit(1);
        }

        const price = parseFloat(options.price);
        if (isNaN(price) || price < 0) {
          console.log(chalk.red('❌ 价格必须是有效的正数'));
          process.exit(1);
        }

        const originalPrice = options.original ? parseFloat(options.original) : undefined;
        if (originalPrice !== undefined && (isNaN(originalPrice) || originalPrice < 0)) {
          console.log(chalk.red('❌ 原价必须是有效的正数'));
          process.exit(1);
        }

        const deliveryTime = parseInt(options.time);
        if (isNaN(deliveryTime) || deliveryTime < 0) {
          console.log(chalk.red('❌ 配送时间必须是有效的正整数'));
          process.exit(1);
        }

        const stock = parseInt(options.stock);
        if (isNaN(stock) || stock < 0) {
          console.log(chalk.red('❌ 库存必须是有效的正整数'));
          process.exit(1);
        }

        const prod = productDb.createProduct({
          merchant_id: merchantId,
          name: options.name,
          description: options.description,
          price: price,
          original_price: originalPrice,
          image_url: options.image,
          category: options.category,
          delivery_time: deliveryTime,
          stock: stock
        });

        console.log(chalk.green('✅ 商品添加成功！'));
        console.log(chalk.gray('─'.repeat(50)));
        console.log(`商品ID: ${chalk.cyan(prod.id)}`);
        console.log(`商品名称: ${chalk.bold(prod.name)}`);
        console.log(`所属商家: ${chalk.cyan(merchant.name)}`);
        console.log(`价格: ${chalk.green(`¥${prod.price.toFixed(2)}`)}`);
        if (prod.original_price) {
          console.log(`原价: ${chalk.strikethrough(`¥${prod.original_price.toFixed(2)}`)}`);
        }
        console.log(`配送时间: ${chalk.cyan(`${prod.delivery_time} 分钟`)}`);
        console.log(`库存: ${chalk.cyan(prod.stock)}`);
        console.log(`状态: ${chalk.yellow(prod.status)}`);
        console.log(chalk.gray('─'.repeat(50)));
      } catch (error) {
        console.error(chalk.red('❌ 添加失败:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  // 列出商品
  product
    .command('list')
    .description('列出商品')
    .option('-m, --merchant <id>', '按商家筛选')
    .option('-c, --category <category>', '按分类筛选')
    .option('-a, --active', '只显示上架商品')
    .action((options) => {
      try {
        let products;
        
        if (options.merchant) {
          const merchantId = parseInt(options.merchant);
          if (options.active) {
            products = productDb.getActiveProductsByMerchant(merchantId);
          } else {
            products = productDb.getProductsByMerchant(merchantId);
          }
        } else if (options.category) {
          products = productDb.getProductsByCategory(options.category);
        } else {
          products = productDb.getAllProducts();
        }

        if (products.length === 0) {
          console.log(chalk.yellow('暂无商品数据'));
          return;
        }

        console.log(chalk.bold('\n📦 商品列表\n'));
        console.log(chalk.gray('─'.repeat(80)));
        
        products.forEach((p: any) => {
          const statusColors: Record<string, (text: string) => string> = {
            active: chalk.green,
            inactive: chalk.gray,
            sold_out: chalk.red
          };
          const statusColor = statusColors[p.status] || chalk.white;

          const priceStr = p.original_price 
            ? `${chalk.green(`¥${p.price.toFixed(2)}`)} ${chalk.gray(`(原价 ¥${p.original_price.toFixed(2)})`)}`
            : chalk.green(`¥${p.price.toFixed(2)}`);

          console.log(`${chalk.cyan(p.id)}. ${chalk.bold(p.name)} ${statusColor(`[${p.status}]`)}`);
          console.log(`   💰 ${priceStr} | ⏱️ ${p.delivery_time}分钟 | 📦 库存: ${p.stock}`);
          if (p.merchant_name) console.log(`   🏪 ${p.merchant_name}`);
          if (p.category) console.log(`   🏷️ ${p.category}`);
          console.log(chalk.gray('─'.repeat(80)));
        });

        console.log(chalk.gray(`\n共 ${products.length} 件商品`));
      } catch (error) {
        console.error(chalk.red('❌ 查询失败:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  // 查看商品详情
  product
    .command('show <id>')
    .description('查看商品详情')
    .action((id) => {
      try {
        const prod = productDb.getProductById(parseInt(id));
        if (!prod) {
          console.log(chalk.red('❌ 商品不存在'));
          process.exit(1);
        }

        const merchant = merchantDb.getMerchantById(prod.merchant_id);

        const statusColor = {
          active: chalk.green,
          inactive: chalk.gray,
          sold_out: chalk.red
        }[prod.status];

        console.log(chalk.bold('\n📦 商品详情\n'));
        console.log(chalk.gray('─'.repeat(50)));
        console.log(`商品ID: ${chalk.cyan(prod.id)}`);
        console.log(`商品名称: ${chalk.bold(prod.name)}`);
        console.log(`销售状态: ${statusColor(prod.status)}`);
        console.log(chalk.gray('─'.repeat(50)));
        console.log(`价格: ${chalk.green(`¥${prod.price.toFixed(2)}`)}`);
        if (prod.original_price) {
          console.log(`原价: ${chalk.strikethrough(`¥${prod.original_price.toFixed(2)}`)}`);
        }
        console.log(`配送时间: ${chalk.cyan(`${prod.delivery_time} 分钟`)}`);
        console.log(`库存: ${chalk.cyan(prod.stock)}`);
        if (prod.category) console.log(`分类: ${chalk.cyan(prod.category)}`);
        console.log(chalk.gray('─'.repeat(50)));
        if (merchant) console.log(`所属商家: ${chalk.cyan(merchant.name)}`);
        if (prod.description) console.log(`描述: ${prod.description}`);
        if (prod.image_url) console.log(`图片: ${chalk.blue(prod.image_url)}`);
        console.log(chalk.gray('─'.repeat(50)));
        console.log(`创建时间: ${chalk.gray(prod.created_at)}`);
        console.log(`更新时间: ${chalk.gray(prod.updated_at)}`);
        console.log(chalk.gray('─'.repeat(50)));
      } catch (error) {
        console.error(chalk.red('❌ 查询失败:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  // 更新商品信息
  product
    .command('update <id>')
    .description('更新商品信息')
    .option('-n, --name <name>', '商品名称')
    .option('-d, --description <desc>', '商品描述')
    .option('-p, --price <price>', '商品价格')
    .option('-o, --original <price>', '原价')
    .option('-i, --image <url>', '商品图片URL')
    .option('-c, --category <category>', '商品分类')
    .option('-s, --stock <count>', '库存数量')
    .action((id, options) => {
      try {
        const productId = parseInt(id);
        const existing = productDb.getProductById(productId);
        if (!existing) {
          console.log(chalk.red('❌ 商品不存在'));
          process.exit(1);
        }

        const updateData: any = {};
        if (options.name) updateData.name = options.name;
        if (options.description !== undefined) updateData.description = options.description;
        if (options.price) updateData.price = parseFloat(options.price);
        if (options.original !== undefined) updateData.original_price = parseFloat(options.original);
        if (options.image !== undefined) updateData.image_url = options.image;
        if (options.category !== undefined) updateData.category = options.category;
        if (options.stock) updateData.stock = parseInt(options.stock);

        if (Object.keys(updateData).length === 0) {
          console.log(chalk.yellow('⚠️ 没有提供要更新的字段'));
          process.exit(1);
        }

        const prod = productDb.updateProduct(productId, updateData);
        console.log(chalk.green('✅ 商品信息更新成功！'));
        console.log(chalk.gray('─'.repeat(50)));
        console.log(`商品ID: ${chalk.cyan(prod!.id)}`);
        console.log(`商品名称: ${chalk.bold(prod!.name)}`);
        console.log(`价格: ${chalk.green(`¥${prod!.price.toFixed(2)}`)}`);
        console.log(`配送时间: ${chalk.cyan(`${prod!.delivery_time} 分钟`)}`);
        console.log(chalk.gray('─'.repeat(50)));
      } catch (error) {
        console.error(chalk.red('❌ 更新失败:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  // 修改商品价格
  product
    .command('price <id> <price>')
    .description('修改商品价格')
    .action((id, price) => {
      try {
        const productId = parseInt(id);
        const newPrice = parseFloat(price);

        if (isNaN(newPrice) || newPrice < 0) {
          console.log(chalk.red('❌ 价格必须是有效的正数'));
          process.exit(1);
        }

        const existing = productDb.getProductById(productId);
        if (!existing) {
          console.log(chalk.red('❌ 商品不存在'));
          process.exit(1);
        }

        const prod = productDb.updateProductPrice(productId, newPrice);
        console.log(chalk.green('✅ 价格修改成功！'));
        console.log(chalk.gray('─'.repeat(50)));
        console.log(`商品: ${chalk.bold(prod!.name)}`);
        console.log(`新价格: ${chalk.green(`¥${prod!.price.toFixed(2)}`)}`);
        console.log(chalk.gray('─'.repeat(50)));
      } catch (error) {
        console.error(chalk.red('❌ 修改失败:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  // 修改配送时间
  product
    .command('delivery <id> <minutes>')
    .description('修改商品配送承诺时间（分钟）')
    .action((id, minutes) => {
      try {
        const productId = parseInt(id);
        const deliveryTime = parseInt(minutes);

        if (isNaN(deliveryTime) || deliveryTime < 0) {
          console.log(chalk.red('❌ 配送时间必须是有效的正整数'));
          process.exit(1);
        }

        const existing = productDb.getProductById(productId);
        if (!existing) {
          console.log(chalk.red('❌ 商品不存在'));
          process.exit(1);
        }

        const prod = productDb.updateProductDeliveryTime(productId, deliveryTime);
        console.log(chalk.green('✅ 配送时间修改成功！'));
        console.log(chalk.gray('─'.repeat(50)));
        console.log(`商品: ${chalk.bold(prod!.name)}`);
        console.log(`配送承诺: ${chalk.cyan(`${prod!.delivery_time} 分钟`)}`);
        console.log(chalk.gray('─'.repeat(50)));
      } catch (error) {
        console.error(chalk.red('❌ 修改失败:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  // 上架商品
  product
    .command('activate <id>')
    .description('上架商品')
    .action((id) => {
      try {
        const prod = productDb.activateProduct(parseInt(id));
        if (!prod) {
          console.log(chalk.red('❌ 商品不存在'));
          process.exit(1);
        }
        console.log(chalk.green(`✅ 商品 "${prod.name}" 已上架`));
      } catch (error) {
        console.error(chalk.red('❌ 操作失败:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  // 下架商品
  product
    .command('deactivate <id>')
    .description('下架商品')
    .action((id) => {
      try {
        const prod = productDb.deactivateProduct(parseInt(id));
        if (!prod) {
          console.log(chalk.red('❌ 商品不存在'));
          process.exit(1);
        }
        console.log(chalk.yellow(`⏸️ 商品 "${prod.name}" 已下架`));
      } catch (error) {
        console.error(chalk.red('❌ 操作失败:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  // 标记售罄
  product
    .command('soldout <id>')
    .description('标记商品售罄')
    .action((id) => {
      try {
        const prod = productDb.markProductSoldOut(parseInt(id));
        if (!prod) {
          console.log(chalk.red('❌ 商品不存在'));
          process.exit(1);
        }
        console.log(chalk.red(`🚫 商品 "${prod.name}" 已标记为售罄`));
      } catch (error) {
        console.error(chalk.red('❌ 操作失败:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  // 删除商品
  product
    .command('delete <id>')
    .description('删除商品')
    .action((id) => {
      try {
        const prod = productDb.getProductById(parseInt(id));
        if (!prod) {
          console.log(chalk.red('❌ 商品不存在'));
          process.exit(1);
        }

        productDb.deleteProduct(parseInt(id));
        console.log(chalk.green(`✅ 商品 "${prod.name}" 已删除`));
      } catch (error) {
        console.error(chalk.red('❌ 删除失败:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  // 搜索商品
  product
    .command('search <keyword>')
    .description('搜索商品')
    .action((keyword) => {
      try {
        const products = productDb.searchProducts(keyword);
        if (products.length === 0) {
          console.log(chalk.yellow('未找到匹配的商品'));
          return;
        }

        console.log(chalk.bold(`\n🔍 搜索结果: "${keyword}"\n`));
        console.log(chalk.gray('─'.repeat(80)));
        
        products.forEach((p) => {
          console.log(`${chalk.cyan(p.id)}. ${chalk.bold(p.name)} ${chalk.green(`¥${p.price.toFixed(2)}`)}`);
          console.log(`   🏪 ${p.merchant_name}`);
          if (p.category) console.log(`   🏷️ ${p.category}`);
          console.log(chalk.gray('─'.repeat(80)));
        });

        console.log(chalk.gray(`\n共找到 ${products.length} 件商品`));
      } catch (error) {
        console.error(chalk.red('❌ 搜索失败:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  // 列出分类
  product
    .command('categories')
    .description('列出所有商品分类')
    .action(() => {
      try {
        const categories = productDb.getCategories();
        if (categories.length === 0) {
          console.log(chalk.yellow('暂无商品分类'));
          return;
        }

        console.log(chalk.bold('\n🏷️ 商品分类\n'));
        categories.forEach((cat, index) => {
          console.log(`${chalk.cyan(index + 1)}. ${cat}`);
        });
      } catch (error) {
        console.error(chalk.red('❌ 查询失败:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  return product;
}
