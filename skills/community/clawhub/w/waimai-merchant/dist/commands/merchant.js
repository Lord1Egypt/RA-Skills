"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.createMerchantCommands = createMerchantCommands;
const commander_1 = require("commander");
const chalk_1 = __importDefault(require("chalk"));
const merchantDb = __importStar(require("../db/merchant"));
function createMerchantCommands() {
    const merchant = new commander_1.Command('merchant').description('商家管理命令');
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
                console.log(chalk_1.default.red('❌ 该手机号已被注册'));
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
            console.log(chalk_1.default.green('✅ 商家注册成功！'));
            console.log(chalk_1.default.gray('─'.repeat(50)));
            console.log(`商家ID: ${chalk_1.default.cyan(merchant.id)}`);
            console.log(`商家名称: ${chalk_1.default.cyan(merchant.name)}`);
            console.log(`联系电话: ${chalk_1.default.cyan(merchant.phone)}`);
            console.log(`商家地址: ${chalk_1.default.cyan(merchant.address)}`);
            if (merchant.email)
                console.log(`电子邮箱: ${chalk_1.default.cyan(merchant.email)}`);
            if (merchant.contact_person)
                console.log(`联系人: ${chalk_1.default.cyan(merchant.contact_person)}`);
            console.log(`认证状态: ${chalk_1.default.yellow(merchant.status)}`);
            console.log(chalk_1.default.gray('─'.repeat(50)));
        }
        catch (error) {
            console.error(chalk_1.default.red('❌ 注册失败:'), error instanceof Error ? error.message : error);
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
            }
            else {
                merchants = merchantDb.getAllMerchants();
            }
            if (merchants.length === 0) {
                console.log(chalk_1.default.yellow('暂无商家数据'));
                return;
            }
            console.log(chalk_1.default.bold('\n📋 商家列表\n'));
            console.log(chalk_1.default.gray('─'.repeat(80)));
            merchants.forEach((m) => {
                const statusColor = {
                    pending: chalk_1.default.yellow,
                    approved: chalk_1.default.green,
                    rejected: chalk_1.default.red,
                    suspended: chalk_1.default.gray
                }[m.status];
                console.log(`${chalk_1.default.cyan(m.id)}. ${chalk_1.default.bold(m.name)} ${statusColor(`[${m.status}]`)}`);
                console.log(`   📞 ${m.phone} | 📍 ${m.address}`);
                if (m.contact_person)
                    console.log(`   👤 ${m.contact_person}`);
                console.log(`   🕐 ${m.created_at}`);
                console.log(chalk_1.default.gray('─'.repeat(80)));
            });
            console.log(chalk_1.default.gray(`\n共 ${merchants.length} 家商家`));
        }
        catch (error) {
            console.error(chalk_1.default.red('❌ 查询失败:'), error instanceof Error ? error.message : error);
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
                console.log(chalk_1.default.red('❌ 商家不存在'));
                process.exit(1);
            }
            const statusColor = {
                pending: chalk_1.default.yellow,
                approved: chalk_1.default.green,
                rejected: chalk_1.default.red,
                suspended: chalk_1.default.gray
            }[merchant.status];
            console.log(chalk_1.default.bold('\n🏪 商家详情\n'));
            console.log(chalk_1.default.gray('─'.repeat(50)));
            console.log(`商家ID: ${chalk_1.default.cyan(merchant.id)}`);
            console.log(`商家名称: ${chalk_1.default.bold(merchant.name)}`);
            console.log(`认证状态: ${statusColor(merchant.status)}`);
            console.log(chalk_1.default.gray('─'.repeat(50)));
            console.log(`联系电话: ${chalk_1.default.cyan(merchant.phone)}`);
            console.log(`商家地址: ${chalk_1.default.cyan(merchant.address)}`);
            if (merchant.email)
                console.log(`电子邮箱: ${chalk_1.default.cyan(merchant.email)}`);
            if (merchant.contact_person)
                console.log(`联系人: ${chalk_1.default.cyan(merchant.contact_person)}`);
            if (merchant.business_license)
                console.log(`营业执照: ${chalk_1.default.cyan(merchant.business_license)}`);
            console.log(chalk_1.default.gray('─'.repeat(50)));
            console.log(`创建时间: ${chalk_1.default.gray(merchant.created_at)}`);
            console.log(`更新时间: ${chalk_1.default.gray(merchant.updated_at)}`);
            console.log(chalk_1.default.gray('─'.repeat(50)));
        }
        catch (error) {
            console.error(chalk_1.default.red('❌ 查询失败:'), error instanceof Error ? error.message : error);
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
                console.log(chalk_1.default.red('❌ 商家不存在'));
                process.exit(1);
            }
            const updateData = {};
            if (options.name)
                updateData.name = options.name;
            if (options.phone)
                updateData.phone = options.phone;
            if (options.address)
                updateData.address = options.address;
            if (options.email !== undefined)
                updateData.email = options.email;
            if (options.license !== undefined)
                updateData.business_license = options.license;
            if (options.contact !== undefined)
                updateData.contact_person = options.contact;
            if (Object.keys(updateData).length === 0) {
                console.log(chalk_1.default.yellow('⚠️ 没有提供要更新的字段'));
                process.exit(1);
            }
            const merchant = merchantDb.updateMerchant(merchantId, updateData);
            console.log(chalk_1.default.green('✅ 商家信息更新成功！'));
            console.log(chalk_1.default.gray('─'.repeat(50)));
            console.log(`商家ID: ${chalk_1.default.cyan(merchant.id)}`);
            console.log(`商家名称: ${chalk_1.default.cyan(merchant.name)}`);
            console.log(`联系电话: ${chalk_1.default.cyan(merchant.phone)}`);
            console.log(`商家地址: ${chalk_1.default.cyan(merchant.address)}`);
            console.log(chalk_1.default.gray('─'.repeat(50)));
        }
        catch (error) {
            console.error(chalk_1.default.red('❌ 更新失败:'), error instanceof Error ? error.message : error);
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
                console.log(chalk_1.default.red('❌ 商家不存在'));
                process.exit(1);
            }
            console.log(chalk_1.default.green(`✅ 商家 "${merchant.name}" 已通过认证`));
        }
        catch (error) {
            console.error(chalk_1.default.red('❌ 操作失败:'), error instanceof Error ? error.message : error);
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
                console.log(chalk_1.default.red('❌ 商家不存在'));
                process.exit(1);
            }
            console.log(chalk_1.default.red(`❌ 商家 "${merchant.name}" 已被拒绝`));
        }
        catch (error) {
            console.error(chalk_1.default.red('❌ 操作失败:'), error instanceof Error ? error.message : error);
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
                console.log(chalk_1.default.red('❌ 商家不存在'));
                process.exit(1);
            }
            console.log(chalk_1.default.yellow(`⏸️ 商家 "${merchant.name}" 已被暂停`));
        }
        catch (error) {
            console.error(chalk_1.default.red('❌ 操作失败:'), error instanceof Error ? error.message : error);
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
                console.log(chalk_1.default.red('❌ 商家不存在'));
                process.exit(1);
            }
            merchantDb.deleteMerchant(parseInt(id));
            console.log(chalk_1.default.green(`✅ 商家 "${merchant.name}" 已删除`));
        }
        catch (error) {
            console.error(chalk_1.default.red('❌ 删除失败:'), error instanceof Error ? error.message : error);
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
                console.log(chalk_1.default.yellow('未找到匹配的商家'));
                return;
            }
            console.log(chalk_1.default.bold(`\n🔍 搜索结果: "${keyword}"\n`));
            console.log(chalk_1.default.gray('─'.repeat(80)));
            merchants.forEach((m) => {
                console.log(`${chalk_1.default.cyan(m.id)}. ${chalk_1.default.bold(m.name)}`);
                console.log(`   📞 ${m.phone} | 📍 ${m.address}`);
                console.log(chalk_1.default.gray('─'.repeat(80)));
            });
            console.log(chalk_1.default.gray(`\n共找到 ${merchants.length} 家商家`));
        }
        catch (error) {
            console.error(chalk_1.default.red('❌ 搜索失败:'), error instanceof Error ? error.message : error);
            process.exit(1);
        }
    });
    return merchant;
}
//# sourceMappingURL=merchant.js.map