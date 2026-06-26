import { Command } from 'commander';
import chalk from 'chalk';
import * as merchantDb from '../db/merchant';

export function createMerchantCommands(): Command {
  const merchant = new Command('merchant').description('商家管理命令');

  // 注册新商家
  merchant
    .command('register')
    .description('注册新商家')
    .requiredOption('-n, --name <name>', '商家名称')
    .requiredOption('-p, --phone <phone>', '联系电话')
    .requiredOption('-a, --address <address>', '商家地址')
    .option('-e, --email <email>', '电子邮箱')
    .option('-l, --license <license>', '营业执照号')
    .option('-c, --contact <contact>', '联系人姓名')
    .action((options) => {
      try {
        // 检查手机号是否已存在
        const existing = merchantDb.getMerchantByPhone(options.phone);
        if (existing) {
          console.log(chalk.red('❌ 该手机号已被注册'));
          process.exit(1);
        }

        const merchant = merchantDb.createMerchant({
          name: options.name,
          phone: options.phone,
          email: options.email,
          address: options.address,
          business_license: options.license,
          contact_person: options.contact
        });

        console.log(chalk.green('✅ 商家注册成功！'));
        console.log(chalk.gray('─'.repeat(50)));
        console.log(`商家ID: ${chalk.cyan(merchant.id)}`);
        console.log(`商家名称: ${chalk.cyan(merchant.name)}`);
        console.log(`联系电话: ${chalk.cyan(merchant.phone)}`);
        console.log(`商家地址: ${chalk.cyan(merchant.address)}`);
        if (merchant.email) console.log(`电子邮箱: ${chalk.cyan(merchant.email)}`);
        if (merchant.contact_person) console.log(`联系人: ${chalk.cyan(merchant.contact_person)}`);
        console.log(`认证状态: ${chalk.yellow(merchant.status)}`);
        console.log(chalk.gray('─'.repeat(50)));
      } catch (error) {
        console.error(chalk.red('❌ 注册失败:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  // 列出所有商家
  merchant
    .command('list')
    .description('列出所有商家')
    .option('-s, --status <status>', '按状态筛选 (pending/approved/rejected/suspended)')
    .action((options) => {
      try {
        let merchants;
        if (options.status) {
          merchants = merchantDb.getMerchantsByStatus(options.status);
        } else {
          merchants = merchantDb.getAllMerchants();
        }

        if (merchants.length === 0) {
          console.log(chalk.yellow('暂无商家数据'));
          return;
        }

        console.log(chalk.bold('\n📋 商家列表\n'));
        console.log(chalk.gray('─'.repeat(80)));
        
        merchants.forEach((m) => {
          const statusColor = {
            pending: chalk.yellow,
            approved: chalk.green,
            rejected: chalk.red,
            suspended: chalk.gray
          }[m.status];

          console.log(`${chalk.cyan(m.id)}. ${chalk.bold(m.name)} ${statusColor(`[${m.status}]`)}`);
          console.log(`   📞 ${m.phone} | 📍 ${m.address}`);
          if (m.contact_person) console.log(`   👤 ${m.contact_person}`);
          console.log(`   🕐 ${m.created_at}`);
          console.log(chalk.gray('─'.repeat(80)));
        });

        console.log(chalk.gray(`\n共 ${merchants.length} 家商家`));
      } catch (error) {
        console.error(chalk.red('❌ 查询失败:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  // 查看商家详情
  merchant
    .command('show <id>')
    .description('查看商家详情')
    .action((id) => {
      try {
        const merchant = merchantDb.getMerchantById(parseInt(id));
        if (!merchant) {
          console.log(chalk.red('❌ 商家不存在'));
          process.exit(1);
        }

        const statusColor = {
          pending: chalk.yellow,
          approved: chalk.green,
          rejected: chalk.red,
          suspended: chalk.gray
        }[merchant.status];

        console.log(chalk.bold('\n🏪 商家详情\n'));
        console.log(chalk.gray('─'.repeat(50)));
        console.log(`商家ID: ${chalk.cyan(merchant.id)}`);
        console.log(`商家名称: ${chalk.bold(merchant.name)}`);
        console.log(`认证状态: ${statusColor(merchant.status)}`);
        console.log(chalk.gray('─'.repeat(50)));
        console.log(`联系电话: ${chalk.cyan(merchant.phone)}`);
        console.log(`商家地址: ${chalk.cyan(merchant.address)}`);
        if (merchant.email) console.log(`电子邮箱: ${chalk.cyan(merchant.email)}`);
        if (merchant.contact_person) console.log(`联系人: ${chalk.cyan(merchant.contact_person)}`);
        if (merchant.business_license) console.log(`营业执照: ${chalk.cyan(merchant.business_license)}`);
        console.log(chalk.gray('─'.repeat(50)));
        console.log(`创建时间: ${chalk.gray(merchant.created_at)}`);
        console.log(`更新时间: ${chalk.gray(merchant.updated_at)}`);
        console.log(chalk.gray('─'.repeat(50)));
      } catch (error) {
        console.error(chalk.red('❌ 查询失败:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  // 更新商家信息
  merchant
    .command('update <id>')
    .description('更新商家信息')
    .option('-n, --name <name>', '商家名称')
    .option('-p, --phone <phone>', '联系电话')
    .option('-a, --address <address>', '商家地址')
    .option('-e, --email <email>', '电子邮箱')
    .option('-l, --license <license>', '营业执照号')
    .option('-c, --contact <contact>', '联系人姓名')
    .action((id, options) => {
      try {
        const merchantId = parseInt(id);
        const existing = merchantDb.getMerchantById(merchantId);
        if (!existing) {
          console.log(chalk.red('❌ 商家不存在'));
          process.exit(1);
        }

        const updateData: any = {};
        if (options.name) updateData.name = options.name;
        if (options.phone) updateData.phone = options.phone;
        if (options.address) updateData.address = options.address;
        if (options.email !== undefined) updateData.email = options.email;
        if (options.license !== undefined) updateData.business_license = options.license;
        if (options.contact !== undefined) updateData.contact_person = options.contact;

        if (Object.keys(updateData).length === 0) {
          console.log(chalk.yellow('⚠️ 没有提供要更新的字段'));
          process.exit(1);
        }

        const merchant = merchantDb.updateMerchant(merchantId, updateData);
        console.log(chalk.green('✅ 商家信息更新成功！'));
        console.log(chalk.gray('─'.repeat(50)));
        console.log(`商家ID: ${chalk.cyan(merchant!.id)}`);
        console.log(`商家名称: ${chalk.cyan(merchant!.name)}`);
        console.log(`联系电话: ${chalk.cyan(merchant!.phone)}`);
        console.log(`商家地址: ${chalk.cyan(merchant!.address)}`);
        console.log(chalk.gray('─'.repeat(50)));
      } catch (error) {
        console.error(chalk.red('❌ 更新失败:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  // 认证商家
  merchant
    .command('approve <id>')
    .description('认证通过商家')
    .action((id) => {
      try {
        const merchant = merchantDb.approveMerchant(parseInt(id));
        if (!merchant) {
          console.log(chalk.red('❌ 商家不存在'));
          process.exit(1);
        }
        console.log(chalk.green(`✅ 商家 "${merchant.name}" 已通过认证`));
      } catch (error) {
        console.error(chalk.red('❌ 操作失败:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  // 拒绝商家
  merchant
    .command('reject <id>')
    .description('拒绝商家认证')
    .action((id) => {
      try {
        const merchant = merchantDb.rejectMerchant(parseInt(id));
        if (!merchant) {
          console.log(chalk.red('❌ 商家不存在'));
          process.exit(1);
        }
        console.log(chalk.red(`❌ 商家 "${merchant.name}" 已被拒绝`));
      } catch (error) {
        console.error(chalk.red('❌ 操作失败:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  // 暂停商家
  merchant
    .command('suspend <id>')
    .description('暂停商家营业')
    .action((id) => {
      try {
        const merchant = merchantDb.suspendMerchant(parseInt(id));
        if (!merchant) {
          console.log(chalk.red('❌ 商家不存在'));
          process.exit(1);
        }
        console.log(chalk.yellow(`⏸️ 商家 "${merchant.name}" 已被暂停`));
      } catch (error) {
        console.error(chalk.red('❌ 操作失败:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  // 删除商家
  merchant
    .command('delete <id>')
    .description('删除商家')
    .action((id) => {
      try {
        const merchant = merchantDb.getMerchantById(parseInt(id));
        if (!merchant) {
          console.log(chalk.red('❌ 商家不存在'));
          process.exit(1);
        }

        merchantDb.deleteMerchant(parseInt(id));
        console.log(chalk.green(`✅ 商家 "${merchant.name}" 已删除`));
      } catch (error) {
        console.error(chalk.red('❌ 删除失败:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  // 搜索商家
  merchant
    .command('search <keyword>')
    .description('搜索商家')
    .action((keyword) => {
      try {
        const merchants = merchantDb.searchMerchants(keyword);
        if (merchants.length === 0) {
          console.log(chalk.yellow('未找到匹配的商家'));
          return;
        }

        console.log(chalk.bold(`\n🔍 搜索结果: "${keyword}"\n`));
        console.log(chalk.gray('─'.repeat(80)));
        
        merchants.forEach((m) => {
          console.log(`${chalk.cyan(m.id)}. ${chalk.bold(m.name)}`);
          console.log(`   📞 ${m.phone} | 📍 ${m.address}`);
          console.log(chalk.gray('─'.repeat(80)));
        });

        console.log(chalk.gray(`\n共找到 ${merchants.length} 家商家`));
      } catch (error) {
        console.error(chalk.red('❌ 搜索失败:'), error instanceof Error ? error.message : error);
        process.exit(1);
      }
    });

  return merchant;
}
