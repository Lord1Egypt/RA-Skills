#!/usr/bin/env node
"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const commander_1 = require("commander");
const chalk_1 = __importDefault(require("chalk"));
const commands_1 = require("./commands");
const db_1 = require("./db");
const program = new commander_1.Command();
program
    .name('waimai-merchant')
    .description('外卖商家管理 CLI - 支持商家注册、商品管理、价格修改和配送时间设置')
    .version('1.0.0');
// 注册所有命令
(0, commands_1.registerCommands)(program);
// 数据目录命令
program
    .command('data')
    .description('查看数据存储位置')
    .action(() => {
    console.log(chalk_1.default.bold('\n📁 数据存储位置\n'));
    console.log(chalk_1.default.gray('─'.repeat(50)));
    console.log((0, db_1.getDataDir)());
    console.log(chalk_1.default.gray('─'.repeat(50)));
});
// 处理未捕获的错误
process.on('exit', () => {
    (0, db_1.closeDatabase)();
});
process.on('SIGINT', () => {
    (0, db_1.closeDatabase)();
    process.exit(0);
});
process.on('SIGTERM', () => {
    (0, db_1.closeDatabase)();
    process.exit(0);
});
// 解析命令行参数
program.parse();
// 如果没有提供命令，显示帮助
if (!process.argv.slice(2).length) {
    program.outputHelp();
}
//# sourceMappingURL=index.js.map