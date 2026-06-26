"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const stardots_client_1 = require("./stardots-client");
const promises_1 = __importDefault(require("fs/promises"));
const path_1 = __importDefault(require("path"));
class StardotsBackupSkill {
    constructor() {
        this.name = 'stardots-backup';
        this.description = '自动将图像备份到 Stardots.io 平台';
        this.version = '1.0.0';
        this.client = null;
        this.config = null;
    }
    // 初始化方法（OpenClaw 会在加载时调用）
    async initialize(config) {
        this.config = {
            apiKey: config.apiKey,
            apiSecret: config.apiSecret,
            space: config.space || 'default',
        };
        this.client = new stardots_client_1.StardotsClient(this.config);
    }
    // 核心执行方法
    async execute(context) {
        try {
            // 如果还没初始化，先初始化
            if (!this.client) {
                await this.initialize(context.config);
            }
            const { userMessage } = context;
            const message = userMessage.content;
            // 解析用户意图
            if (this.matchUploadIntent(message)) {
                return await this.handleUpload(message);
            }
            else if (this.matchListIntent(message)) {
                return await this.handleList();
            }
            else {
                return this.getHelpMessage();
            }
        }
        catch (error) {
            return {
                success: false,
                message: `执行失败: ${error.message}`,
                error: error.stack
            };
        }
    }
    matchUploadIntent(message) {
        const lowerMsg = message.toLowerCase();
        return lowerMsg.includes('上传') ||
            lowerMsg.includes('备份') ||
            lowerMsg.includes('upload') ||
            lowerMsg.includes('backup');
    }
    matchListIntent(message) {
        const lowerMsg = message.toLowerCase();
        return lowerMsg.includes('列出') ||
            lowerMsg.includes('列表') ||
            lowerMsg.includes('list') ||
            lowerMsg.includes('show');
    }
    async handleUpload(message) {
        if (!this.client || !this.config) {
            throw new Error('技能未初始化');
        }
        // 尝试提取文件路径
        const filePathMatch = message.match(/(?:上传|备份|upload|backup)\s+([^\s]+\.(jpg|jpeg|png|gif|bmp|svg|avif|webp))/i);
        if (!filePathMatch) {
            return {
                success: false,
                message: '请指定要上传的图像路径，例如：上传 /path/to/image.jpg',
                suggestActions: ['上传 ~/Pictures/photo.jpg']
            };
        }
        const imagePath = filePathMatch[1];
        // 检查文件是否存在
        try {
            await promises_1.default.access(imagePath);
        }
        catch {
            return {
                success: false,
                message: `文件不存在: ${imagePath}`,
            };
        }
        // 获取文件信息
        const stats = await promises_1.default.stat(imagePath);
        const fileSize = (stats.size / 1024 / 1024).toFixed(2); // MB
        // 执行上传
        const result = await this.client.uploadImage(imagePath);
        if (result.success) {
            return {
                success: true,
                message: `✅ 图像上传成功！\n文件: ${path_1.default.basename(imagePath)}\n大小: ${fileSize} MB\nURL: ${result.url}`,
                data: {
                    url: result.url,
                    fileName: path_1.default.basename(imagePath),
                    fileSize: stats.size,
                    space: this.config.space,
                },
            };
        }
        else {
            return {
                success: false,
                message: `❌ 上传失败: ${result.message}`,
            };
        }
    }
    async handleList() {
        if (!this.client) {
            throw new Error('技能未初始化');
        }
        try {
            const result = await this.client.listFiles({ page: 1, pageSize: 10 });
            if (result.files.length === 0) {
                return {
                    success: true,
                    message: '📁 当前空间没有文件',
                };
            }
            const fileList = result.files.map(file => `- ${file.name} (${(file.size / 1024).toFixed(2)} KB) [${new Date(file.createdAt).toLocaleString()}]`).join('\n');
            return {
                success: true,
                message: `📁 文件列表 (共${result.total}个文件):\n\n${fileList}`,
                data: result,
            };
        }
        catch (error) {
            return {
                success: false,
                message: `获取文件列表失败: ${error.message}`,
            };
        }
    }
    getHelpMessage() {
        const helpText = `📚 Stardots.io 备份技能使用说明

可用命令：
• 上传 [文件路径] - 上传图像到Stardots
• 列出文件 - 查看已上传的文件列表
• 帮助 - 显示此帮助信息

配置要求：
需要在技能设置中配置以下参数：
- apiKey: 你的API密钥
- apiSecret: 你的API密钥
- space: 目标空间名称

示例：
"上传 /home/user/photos/vacation.jpg"
"列出文件"`;
        return {
            success: true,
            message: helpText,
        };
    }
}
exports.default = StardotsBackupSkill;
//# sourceMappingURL=index.js.map