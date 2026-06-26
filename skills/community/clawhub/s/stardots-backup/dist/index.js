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
Object.defineProperty(exports, "__esModule", { value: true });
const crypto = __importStar(require("crypto"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const os = __importStar(require("os"));
class StardotsBackupSkill {
    constructor() {
        this.name = 'stardots-backup';
        this.description = 'Upload images to stardots.io cloud storage platform';
    }
    async execute(context) {
        const { userMessage, config, tools } = context;
        // 获取配置
        const stardotsConfig = this.getConfig(config);
        if (!stardotsConfig) {
            return {
                message: '请配置 Stardots API 凭证。需要在 config.schema.json 中设置 apiKey, apiSecret 和 space。',
                data: { error: 'missing_config' }
            };
        }
        // 检查是否有文件需要上传
        const attachments = userMessage.attachments || [];
        const imageAttachments = attachments.filter(att => att.type?.startsWith('image/'));
        if (imageAttachments.length === 0) {
            return {
                message: '请发送一张图片，我会帮你上传到 stardots.io',
                data: { error: 'no_image' }
            };
        }
        const results = [];
        for (const attachment of imageAttachments) {
            try {
                const url = await this.uploadImage(attachment.path, stardotsConfig, tools);
                if (url) {
                    results.push(`✅ 上传成功: ${url}`);
                }
                else {
                    results.push(`❌ 上传失败: ${attachment.filename || 'unknown'}`);
                }
            }
            catch (error) {
                results.push(`❌ 错误: ${error instanceof Error ? error.message : 'unknown error'}`);
            }
        }
        return {
            message: results.join('\n'),
            data: { uploaded: results.length }
        };
    }
    getConfig(config) {
        // 优先从 skill 配置读取
        if (config?.apiKey && config?.apiSecret) {
            return {
                apiKey: config.apiKey,
                apiSecret: config.apiSecret,
                space: config.space || 'default'
            };
        }
        // 尝试从环境变量读取
        const apiKey = process.env.STARDOTS_API_KEY;
        const apiSecret = process.env.STARDOTS_API_SECRET;
        const space = process.env.STARDOTS_SPACE || 'default';
        if (apiKey && apiSecret) {
            return { apiKey, apiSecret, space };
        }
        // 尝试从配置文件读取
        const configPath = path.join(os.homedir(), '.config', 'stardots', 'config.json');
        if (fs.existsSync(configPath)) {
            try {
                const fileConfig = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
                if (fileConfig.apiKey && fileConfig.apiSecret) {
                    return {
                        apiKey: fileConfig.apiKey,
                        apiSecret: fileConfig.apiSecret,
                        space: fileConfig.space || 'default'
                    };
                }
            }
            catch (e) {
                console.error('读取配置文件失败:', e);
            }
        }
        return null;
    }
    generateSign(timestamp, nonce, secret) {
        const needSignStr = `${timestamp}|${secret}|${nonce}`;
        return crypto.createHash('md5').update(needSignStr).digest('hex').toUpperCase();
    }
    generateNonce(length = 10) {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        let result = '';
        for (let i = 0; i < length; i++) {
            result += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return result;
    }
    async uploadImage(imagePath, config, tools) {
        const timestamp = Math.floor(Date.now() / 1000);
        const nonce = this.generateNonce();
        const sign = this.generateSign(timestamp, nonce, config.apiSecret);
        // 使用 exec 工具调用 curl 上传
        const command = `curl -s -X PUT "https://api.stardots.io/openapi/file/upload" \
      -H "x-stardots-timestamp: ${timestamp}" \
      -H "x-stardots-nonce: ${nonce}" \
      -H "x-stardots-key: ${config.apiKey}" \
      -H "x-stardots-sign: ${sign}" \
      -F "space=${config.space}" \
      -F "file=@${imagePath}"`;
        try {
            const result = await tools.exec({ command, timeout: 60000 });
            const response = JSON.parse(result.stdout || '{}');
            if (response.success && response.data?.url) {
                return response.data.url;
            }
            return null;
        }
        catch (error) {
            console.error('上传失败:', error);
            return null;
        }
    }
}
exports.default = StardotsBackupSkill;
//# sourceMappingURL=index.js.map