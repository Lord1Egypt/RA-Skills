"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.StardotsClient = void 0;
const crypto_1 = __importDefault(require("crypto"));
const axios_1 = __importDefault(require("axios"));
const form_data_1 = __importDefault(require("form-data"));
const fs_1 = require("fs");
class StardotsClient {
    constructor(config) {
        this.baseURL = 'https://api.stardots.io';
        this.config = config;
        this.client = axios_1.default.create({
            baseURL: this.baseURL,
            timeout: 60000,
        });
    }
    generateNonce(length = 10) {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        let nonce = '';
        for (let i = 0; i < length; i++) {
            nonce += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return nonce;
    }
    generateSign(timestamp, nonce) {
        const needSignStr = `${timestamp}|${this.config.apiSecret}|${nonce}`;
        return crypto_1.default.createHash('md5').update(needSignStr).digest('hex').toUpperCase();
    }
    getAuthHeaders() {
        const timestamp = Math.floor(Date.now() / 1000);
        const nonce = this.generateNonce();
        const sign = this.generateSign(timestamp, nonce);
        return {
            'x-stardots-timestamp': timestamp.toString(),
            'x-stardots-nonce': nonce,
            'x-stardots-key': this.config.apiKey,
            'x-stardots-sign': sign,
            'x-stardots-extensions': '{"via": "openclaw", "version": "1.0.0"}'
        };
    }
    async uploadImage(imagePath, space, metadata) {
        try {
            const formData = new form_data_1.default();
            formData.append('file', (0, fs_1.createReadStream)(imagePath));
            formData.append('space', space || this.config.space);
            if (metadata) {
                formData.append('metadata', JSON.stringify(metadata));
            }
            const headers = {
                ...this.getAuthHeaders(),
                ...formData.getHeaders(),
            };
            const response = await this.client.put('/openapi/file/upload', formData, { headers });
            if (response.data?.success) {
                return {
                    success: true,
                    url: response.data.data.url,
                    message: '上传成功',
                };
            }
            return {
                success: false,
                url: '',
                message: response.data?.message || '上传失败',
            };
        }
        catch (error) {
            return {
                success: false,
                url: '',
                message: error.response?.data?.message || error.message,
            };
        }
    }
    async listFiles(params) {
        try {
            const response = await this.client.get('/openapi/file/list', {
                headers: this.getAuthHeaders(),
                params: {
                    space: params.space || this.config.space,
                    page: params.page || 1,
                    pageSize: params.pageSize || 20,
                },
            });
            if (response.data?.success) {
                return {
                    files: response.data.data.files || [],
                    total: response.data.data.total || 0,
                    page: params.page || 1,
                    pageSize: params.pageSize || 20,
                };
            }
            throw new Error(response.data?.message || '获取文件列表失败');
        }
        catch (error) {
            throw new Error(`获取文件列表失败: ${error.message}`);
        }
    }
    async deleteFile(fileId, space) {
        try {
            const response = await this.client.delete('/openapi/file/delete', {
                headers: this.getAuthHeaders(),
                data: {
                    fileId,
                    space: space || this.config.space,
                },
            });
            return response.data?.success || false;
        }
        catch (error) {
            return false;
        }
    }
}
exports.StardotsClient = StardotsClient;
//# sourceMappingURL=stardots-client.js.map