"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.SendflareSkill = void 0;
/**
 * Sendflare Skill
 *
 * 通过 Sendflare SDK 发送电子邮件和管理联系人
 */
const Sendflare_client_1 = require("./Sendflare-client");
class SendflareSkill {
    constructor() {
        this.name = 'Sendflare-email';
        this.description = '通过 Sendflare 发送电子邮件和管理联系人';
        this.version = '1.0.0';
        this.client = null;
        this.config = null;
    }
    /**
     * 初始化方法（OpenClaw 会在加载时调用）
     */
    async initialize(config) {
        this.config = {
            apiToken: config.apiToken,
        };
        this.client = new Sendflare_client_1.SendflareClient(this.config);
    }
    /**
     * 核心执行方法
     */
    async execute(context) {
        try {
            // 如果还没初始化，先初始化
            if (!this.client && context.config) {
                await this.initialize(context.config);
            }
            if (!this.client || !this.config) {
                return {
                    success: false,
                    message: '技能未初始化，请配置 Sendflare API Token',
                    suggestActions: ['配置 Sendflare API Token'],
                };
            }
            const { userMessage } = context;
            const message = userMessage.content;
            // 解析用户意图
            if (this.matchSendEmailIntent(message)) {
                return await this.handleSendEmail(message);
            }
            else if (this.matchGetContactsIntent(message)) {
                return await this.handleGetContacts(message);
            }
            else if (this.matchSaveContactIntent(message)) {
                return await this.handleSaveContact(message);
            }
            else if (this.matchDeleteContactIntent(message)) {
                return await this.handleDeleteContact(message);
            }
            else {
                return this.getHelpMessage();
            }
        }
        catch (error) {
            return {
                success: false,
                message: `执行失败：${error.message}`,
                error: error.stack,
            };
        }
    }
    /**
     * 匹配发送邮件意图
     */
    matchSendEmailIntent(message) {
        const lowerMsg = message.toLowerCase();
        return (lowerMsg.includes('发送邮件') ||
            lowerMsg.includes('发邮件') ||
            lowerMsg.includes('send email') ||
            lowerMsg.includes('email to'));
    }
    /**
     * 匹配获取联系人意图
     */
    matchGetContactsIntent(message) {
        const lowerMsg = message.toLowerCase();
        return (lowerMsg.includes('联系人列表') ||
            lowerMsg.includes('列出联系人') ||
            lowerMsg.includes('显示联系人') ||
            lowerMsg.includes('get contacts') ||
            lowerMsg.includes('list contacts'));
    }
    /**
     * 匹配保存联系人意图
     */
    matchSaveContactIntent(message) {
        const lowerMsg = message.toLowerCase();
        return (lowerMsg.includes('保存联系人') ||
            lowerMsg.includes('添加联系人') ||
            lowerMsg.includes('save contact') ||
            lowerMsg.includes('add contact'));
    }
    /**
     * 匹配删除联系人意图
     */
    matchDeleteContactIntent(message) {
        const lowerMsg = message.toLowerCase();
        return (lowerMsg.includes('删除联系人') ||
            lowerMsg.includes('remove contact') ||
            lowerMsg.includes('delete contact'));
    }
    /**
     * 处理发送邮件
     */
    async handleSendEmail(message) {
        if (!this.client) {
            throw new Error('客户端未初始化');
        }
        // 尝试提取邮件信息
        // 格式：发送邮件给 xxx@example.com，主题：xxx，内容：xxx
        let emailMatch = message.match(/发送邮件给 ([^\s,]+)，主题：([^,，]+)，内容：(.+)/);
        if (!emailMatch) {
            // 尝试简化格式：发邮件到 xxx@example.com 主题 xxx 内容 xxx
            const simpleMatch = message.match(/发邮件 (?:到 | 给) ([^\s,]+)\s*(?:主题 | 标题)[:：]?\s*([^\s,]+)\s*(?:内容 | 正文)[:：]?\s*(.+)/);
            if (!simpleMatch) {
                return {
                    success: false,
                    message: '请指定收件人、主题和内容，例如：发送邮件给 test@example.com，主题：测试，内容：这是一封测试邮件',
                    suggestActions: [
                        '发送邮件给 test@example.com，主题：会议通知，内容：明天下午 3 点开会',
                        '发邮件到 john@example.com 主题：问候 内容：你好！',
                    ],
                };
            }
            const [, to, subject, body] = simpleMatch;
            return this.performSendEmail(to.trim(), subject.trim(), body.trim());
        }
        const [, to, subject, body] = emailMatch;
        return this.performSendEmail(to.trim(), subject.trim(), body.trim());
    }
    /**
     * 执行邮件发送
     */
    async performSendEmail(to, subject, body) {
        if (!this.client) {
            throw new Error('客户端未初始化');
        }
        // 构建发送请求
        const emailReq = {
            from: 'noreply@yourdomain.com', // TODO: 从配置读取
            to: to,
            subject: subject,
            body: body,
        };
        // 执行发送
        const result = await this.client.sendEmail(emailReq);
        if (result.success) {
            return {
                success: true,
                message: `✅ 邮件发送成功！\n收件人：${to}\n主题：${subject}\n邮件 ID: ${result.messageId || 'N/A'}`,
                data: result,
            };
        }
        else {
            return {
                success: false,
                message: `❌ 邮件发送失败：${result.message}`,
                error: result.message,
            };
        }
    }
    /**
     * 处理获取联系人
     */
    async handleGetContacts(message) {
        if (!this.client) {
            throw new Error('客户端未初始化');
        }
        // TODO: 需要从配置读取 appId
        return {
            success: false,
            message: '请先配置 App ID 才能获取联系人列表',
            suggestActions: ['配置 App ID'],
        };
    }
    /**
     * 处理保存联系人
     */
    async handleSaveContact(message) {
        if (!this.client) {
            throw new Error('客户端未初始化');
        }
        // 提取联系人信息
        // 格式：保存联系人 xxx@example.com，姓名：xxx
        const contactMatch = message.match(/保存联系人 ([^\s,]+)，姓名：(.+)/);
        if (!contactMatch) {
            return {
                success: false,
                message: '请指定联系人邮箱和姓名，例如：保存联系人 john@example.com，姓名：John Doe',
                suggestActions: ['保存联系人 john@example.com，姓名：John Doe'],
            };
        }
        const [, email, name] = contactMatch;
        // TODO: 需要从配置读取 appId
        return {
            success: false,
            message: '请先配置 App ID 才能保存联系人',
            suggestActions: ['配置 App ID'],
        };
    }
    /**
     * 处理删除联系人
     */
    async handleDeleteContact(message) {
        if (!this.client) {
            throw new Error('客户端未初始化');
        }
        // 提取联系人邮箱
        const emailMatch = message.match(/删除联系人 ([^\s,]+)/);
        if (!emailMatch) {
            return {
                success: false,
                message: '请指定要删除的联系人邮箱，例如：删除联系人 john@example.com',
                suggestActions: ['删除联系人 john@example.com'],
            };
        }
        const [, email] = emailMatch;
        // TODO: 需要从配置读取 appId
        return {
            success: false,
            message: '请先配置 App ID 才能删除联系人',
            suggestActions: ['配置 App ID'],
        };
    }
    /**
     * 获取帮助信息
     */
    getHelpMessage() {
        return {
            success: true,
            message: `📧 Sendflare Skill 帮助

可用命令：
1. 发送邮件：发送邮件给 xxx@example.com，主题：xxx，内容：xxx
2. 获取联系人：获取联系人列表
3. 保存联系人：保存联系人 xxx@example.com，姓名：xxx
4. 删除联系人：删除联系人 xxx@example.com

示例：
- 发送邮件给 test@example.com，主题：会议通知，内容：明天下午 3 点开会
- 获取联系人列表
- 保存联系人 john@example.com，姓名：John Doe
- 删除联系人 john@example.com`,
            suggestActions: [
                '发送邮件给 test@example.com，主题：测试，内容：这是一封测试邮件',
                '获取联系人列表',
                '保存联系人 john@example.com，姓名：John Doe',
            ],
        };
    }
}
exports.SendflareSkill = SendflareSkill;
// 导出单例
exports.default = new SendflareSkill();
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiaW5kZXguanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyIuLi9zcmMvaW5kZXgudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7O0FBQUE7Ozs7R0FJRztBQUNILHlEQUFxRDtBQUdyRCxNQUFhLGNBQWM7SUFBM0I7UUFDUyxTQUFJLEdBQVcsaUJBQWlCLENBQUM7UUFDakMsZ0JBQVcsR0FBVywyQkFBMkIsQ0FBQztRQUNsRCxZQUFPLEdBQVcsT0FBTyxDQUFDO1FBRXpCLFdBQU0sR0FBMkIsSUFBSSxDQUFDO1FBQ3RDLFdBQU0sR0FBMkIsSUFBSSxDQUFDO0lBb1JoRCxDQUFDO0lBbFJDOztPQUVHO0lBQ0gsS0FBSyxDQUFDLFVBQVUsQ0FBQyxNQUF1QjtRQUN0QyxJQUFJLENBQUMsTUFBTSxHQUFHO1lBQ1osUUFBUSxFQUFFLE1BQU0sQ0FBQyxRQUFRO1NBQzFCLENBQUM7UUFDRixJQUFJLENBQUMsTUFBTSxHQUFHLElBQUksa0NBQWUsQ0FBQyxJQUFJLENBQUMsTUFBTSxDQUFDLENBQUM7SUFDakQsQ0FBQztJQUVEOztPQUVHO0lBQ0gsS0FBSyxDQUFDLE9BQU8sQ0FBQyxPQUFxQjtRQUNqQyxJQUFJLENBQUM7WUFDSCxlQUFlO1lBQ2YsSUFBSSxDQUFDLElBQUksQ0FBQyxNQUFNLElBQUksT0FBTyxDQUFDLE1BQU0sRUFBRSxDQUFDO2dCQUNuQyxNQUFNLElBQUksQ0FBQyxVQUFVLENBQUMsT0FBTyxDQUFDLE1BQU0sQ0FBQyxDQUFDO1lBQ3hDLENBQUM7WUFFRCxJQUFJLENBQUMsSUFBSSxDQUFDLE1BQU0sSUFBSSxDQUFDLElBQUksQ0FBQyxNQUFNLEVBQUUsQ0FBQztnQkFDakMsT0FBTztvQkFDTCxPQUFPLEVBQUUsS0FBSztvQkFDZCxPQUFPLEVBQUUsZ0NBQWdDO29CQUN6QyxjQUFjLEVBQUUsQ0FBQyx3QkFBd0IsQ0FBQztpQkFDM0MsQ0FBQztZQUNKLENBQUM7WUFFRCxNQUFNLEVBQUUsV0FBVyxFQUFFLEdBQUcsT0FBTyxDQUFDO1lB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QkFBc0I7UUFDdEIsT0FBTztZQUNMLE9BQU8sRUFBRSxLQUFLO1lBQ2QsT0FBTyxFQUFFLHFCQUFxQjtZQUM5QixjQUFjLEVBQUUsQ0FBQyxXQUFXLENBQUM7U0FDOUIsQ0FBQztJQUNKLENBQUM7SUFFRDs7T0FFRztJQUNLLGNBQWM7UUFDcEIsT0FBTztZQUNMLE9BQU8sRUFBRSxJQUFJO1lBQ2IsT0FBTyxFQUFFOzs7Ozs7Ozs7Ozs7eUJBWVU7WUFDbkIsY0FBYyxFQUFFO2dCQUNkLDBDQUEwQztnQkFDMUMsU0FBUztnQkFDVCxvQ0FBb0M7YUFDckM7U0FDRixDQUFDO0lBQ0osQ0FBQztDQUNGO0FBMVJELHdDQTBSQztBQUVELE9BQU87QUFDUCxrQkFBZSxJQUFJLGNBQWMsRUFBRSxDQUFDIiwic291cmNlc0NvbnRlbnQiOlsiLyoqXG4gKiBTZW5kRmxhcmUgRW1haWwgU2tpbGxcbiAqIFxuICog6YCa6L+HIFNlbmRGbGFyZSBTREsg5Y+R6YCB55S15a2Q6YKu5Lu25ZKM566h55CG6IGU57O75Lq6XG4gKi9cbmltcG9ydCB7IFNlbmRmbGFyZUNsaWVudCB9IGZyb20gJy4vc2VuZGZsYXJlLWNsaWVudCc7XG5pbXBvcnQgdHlwZSB7IFNlbmRmbGFyZUNvbmZpZywgU2tpbGxDb250ZXh0LCBTa2lsbFJlc3VsdCwgU2VuZEVtYWlsUmVxdWVzdCB9IGZyb20gJy4vdHlwZXMnO1xuXG5leHBvcnQgY2xhc3MgU2VuZGZsYXJlU2tpbGwge1xuICBwdWJsaWMgbmFtZTogc3RyaW5nID0gJ3NlbmRmbGFyZS1lbWFpbCc7XG4gIHB1YmxpYyBkZXNjcmlwdGlvbjogc3RyaW5nID0gJ+mAmui/hyBTZW5kRmxhcmUg5Y+R6YCB55S15a2Q6YKu5Lu25ZKM566h55CG6IGU57O75Lq6JztcbiAgcHVibGljIHZlcnNpb246IHN0cmluZyA9ICcxLjAuMCc7XG5cbiAgcHJpdmF0ZSBjbGllbnQ6IFNlbmRmbGFyZUNsaWVudCB8IG51bGwgPSBudWxsO1xuICBwcml2YXRlIGNvbmZpZzogU2VuZGZsYXJlQ29uZmlnIHwgbnVsbCA9IG51bGw7XG5cbiAgLyoqXG4gICAqIOWIneWni+WMluaWueazle+8iE9wZW5DbGF3IOS8muWcqOWKoOi9veaXtuiwg+eUqO+8iVxuICAgKi9cbiAgYXN5bmMgaW5pdGlhbGl6ZShjb25maWc6IFNlbmRmbGFyZUNvbmZpZyk6IFByb21pc2U8dm9pZD4ge1xuICAgIHRoaXMuY29uZmlnID0ge1xuICAgICAgYXBpVG9rZW46IGNvbmZpZy5hcGlUb2tlbixcbiAgICB9O1xuICAgIHRoaXMuY2xpZW50ID0gbmV3IFNlbmRmbGFyZUNsaWVudCh0aGlzLmNvbmZpZyk7XG4gIH1cblxuICAvKipcbiAgICog5qC45b+D5omn6KGM5pa55rOVXG4gICAqL1xuICBhc3luYyBleGVjdXRlKGNvbnRleHQ6IFNraWxsQ29udGV4dCk6IFByb21pc2U8U2tpbGxSZXN1bHQ+IHtcbiAgICB0cnkge1xuICAgICAgLy8g5aaC5p6c6L+Y5rKh5Yid5aeL5YyW77yM5YWI5Yid5aeL5YyWXG4gICAgICBpZiAoIXRoaXMuY2xpZW50ICYmIGNvbnRleHQuY29uZmlnKSB7XG4gICAgICAgIGF3YWl0IHRoaXMuaW5pdGlhbGl6ZShjb250ZXh0LmNvbmZpZyk7XG4gICAgICB9XG5cbiAgICAgIGlmICghdGhpcy5jbGllbnQgfHwgIXRoaXMuY29uZmlnKSB7XG4gICAgICAgIHJldHVybiB7XG4gICAgICAgICAgc3VjY2VzczogZmFsc2UsXG4gICAgICAgICAgbWVzc2FnZTogJ+aKgOiDveacquWIneWni+WMlu+8jOivt+mFjee9riBTZW5kRmxhcmUgQVBJIFRva2VuJyxcbiAgICAgICAgICBzdWdnZXN0QWN0aW9uczogWyfphY3nva4gU2VuZEZsYXJlIEFQSSBUb2tlbiddLFxuICAgICAgICB9O1xuICAgICAgfVxuXG4gICAgICBjb25zdCB7IHVzZXJNZXNzYWdlIH0gPSBjb250ZXh0O1xuICAgICAgY29uc3QgbWVzc2FnZSA9IHVzZXJNZXNzYWdlLmNvbnRlbnQ7XG5cbiAgICAgIC8vIOino+aekOeUqOaIt+aEj+WbvlxuICAgICAgaWYgKHRoaXMubWF0Y2hTZW5kRW1haWxJbnRlbnQobWVzc2FnZSkpIHtcbiAgICAgICAgcmV0dXJuIGF3YWl0IHRoaXMuaGFuZGxlU2VuZEVtYWlsKG1lc3NhZ2UpO1xuICAgICAgfSBlbHNlIGlmICh0aGlzLm1hdGNoR2V0Q29udGFjdHNJbnRlbnQobWVzc2FnZSkpIHtcbiAgICAgICAgcmV0dXJuIGF3YWl0IHRoaXMuaGFuZGxlR2V0Q29udGFjdHMobWVzc2FnZSk7XG4gICAgICB9IGVsc2UgaWYgKHRoaXMubWF0Y2hTYXZlQ29udGFjdEludGVudChtZXNzYWdlKSkge1xuICAgICAgICByZXR1cm4gYXdhaXQgdGhpcy5oYW5kbGVTYXZlQ29udGFjdChtZXNzYWdlKTtcbiAgICAgIH0gZWxzZSBpZiAodGhpcy5tYXRjaERlbGV0ZUNvbnRhY3RJbnRlbnQobWVzc2FnZSkpIHtcbiAgICAgICAgcmV0dXJuIGF3YWl0IHRoaXMuaGFuZGxlRGVsZXRlQ29udGFjdChtZXNzYWdlKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHJldHVybiB0aGlzLmdldEhlbHBNZXNzYWdlKCk7XG4gICAgICB9XG4gICAgfSBjYXRjaCAoZXJyb3I6IGFueSkge1xuICAgICAgcmV0dXJuIHtcbiAgICAgICAgc3VjY2VzczogZmFsc2UsXG4gICAgICAgIG1lc3NhZ2U6IGDmiafooYzlpLHotKXvvJoke2Vycm9yLm1lc3NhZ2V9YCxcbiAgICAgICAgZXJyb3I6IGVycm9yLnN0YWNrLFxuICAgICAgfTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICog5Yy56YWN5Y+R6YCB6YKu5Lu25oSP5Zu+XG4gICAqL1xuICBwcml2YXRlIG1hdGNoU2VuZEVtYWlsSW50ZW50KG1lc3NhZ2U6IHN0cmluZyk6IGJvb2xlYW4ge1xuICAgIGNvbnN0IGxvd2VyTXNnID0gbWVzc2FnZS50b0xvd2VyQ2FzZSgpO1xuICAgIHJldHVybiAoXG4gICAgICBsb3dlck1zZy5pbmNsdWRlcygn5Y+R6YCB6YKu5Lu2JykgfHxcbiAgICAgIGxvd2VyTXNnLmluY2x1ZGVzKCflj5Hpgq7ku7YnKSB8fFxuICAgICAgbG93ZXJNc2cuaW5jbHVkZXMoJ3NlbmQgZW1haWwnKSB8fFxuICAgICAgbG93ZXJNc2cuaW5jbHVkZXMoJ2VtYWlsIHRvJylcbiAgICApO1xuICB9XG5cbiAgLyoqXG4gICAqIOWMuemFjeiOt+WPluiBlOezu+S6uuaEj+WbvlxuICAgKi9cbiAgcHJpdmF0ZSBtYXRjaEdldENvbnRhY3RzSW50ZW50KG1lc3NhZ2U6IHN0cmluZyk6IGJvb2xlYW4ge1xuICAgIGNvbnN0IGxvd2VyTXNnID0gbWVzc2FnZS50b0xvd2VyQ2FzZSgpO1xuICAgIHJldHVybiAoXG4gICAgICBsb3dlck1zZy5pbmNsdWRlcygn6IGU57O75Lq65YiX6KGoJykgfHxcbiAgICAgIGxvd2VyTXNnLmluY2x1ZGVzKCfliJflh7rogZTns7vkuronKSB8fFxuICAgICAgbG93ZXJNc2cuaW5jbHVkZXMoJ+aYvuekuuiBlOezu+S6uicpIHx8XG4gICAgICBsb3dlck1zZy5pbmNsdWRlcygnZ2V0IGNvbnRhY3RzJykgfHxcbiAgICAgIGxvd2VyTXNnLmluY2x1ZGVzKCdsaXN0IGNvbnRhY3RzJylcbiAgICApO1xuICB9XG5cbiAgLyoqXG4gICAqIOWMuemFjeS/neWtmOiBlOezu+S6uuaEj+WbvlxuICAgKi9cbiAgcHJpdmF0ZSBtYXRjaFNhdmVDb250YWN0SW50ZW50KG1lc3NhZ2U6IHN0cmluZyk6IGJvb2xlYW4ge1xuICAgIGNvbnN0IGxvd2VyTXNnID0gbWVzc2FnZS50b0xvd2VyQ2FzZSgpO1xuICAgIHJldHVybiAoXG4gICAgICBsb3dlck1zZy5pbmNsdWRlcygn5L+d5a2Y6IGU57O75Lq6JykgfHxcbiAgICAgIGxvd2VyTXNnLmluY2x1ZGVzKCfmt7vliqDogZTns7vkuronKSB8fFxuICAgICAgbG93ZXJNc2cuaW5jbHVkZXMoJ3NhdmUgY29udGFjdCcpIHx8XG4gICAgICBsb3dlck1zZy5pbmNsdWRlcygnYWRkIGNvbnRhY3QnKVxuICAgICk7XG4gIH1cblxuICAvKipcbiAgICog5Yy56YWN5Yig6Zmk6IGU57O75Lq65oSP5Zu+XG4gICAqL1xuICBwcml2YXRlIG1hdGNoRGVsZXRlQ29udGFjdEludGVudChtZXNzYWdlOiBzdHJpbmcpOiBib29sZWFuIHtcbiAgICBjb25zdCBsb3dlck1zZyA9IG1lc3NhZ2UudG9Mb3dlckNhc2UoKTtcbiAgICByZXR1cm4gKFxuICAgICAgbG93ZXJNc2cuaW5jbHVkZXMoJ+WIoOmZpOiBlOezu+S6uicpIHx8XG4gICAgICBsb3dlck1zZy5pbmNsdWRlcygncmVtb3ZlIGNvbnRhY3QnKSB8fFxuICAgICAgbG93ZXJNc2cuaW5jbHVkZXMoJ2RlbGV0ZSBjb250YWN0JylcbiAgICApO1xuICB9XG5cbiAgLyoqXG4gICAqIOWkhOeQhuWPkemAgemCruS7tlxuICAgKi9cbiAgcHJpdmF0ZSBhc3luYyBoYW5kbGVTZW5kRW1haWwobWVzc2FnZTogc3RyaW5nKTogUHJvbWlzZTxTa2lsbFJlc3VsdD4ge1xuICAgIGlmICghdGhpcy5jbGllbnQpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcign5a6i5oi356uv5pyq5Yid5aeL5YyWJyk7XG4gICAgfVxuXG4gICAgLy8g5bCd6K+V5o+Q5Y+W6YKu5Lu25L+h5oGvXG4gICAgLy8g5qC85byP77ya5Y+R6YCB6YKu5Lu257uZIHh4eEBleGFtcGxlLmNvbe+8jOS4u+mimO+8mnh4eO+8jOWGheWuue+8mnh4eFxuICAgIGxldCBlbWFpbE1hdGNoID0gbWVzc2FnZS5tYXRjaCgv5Y+R6YCB6YKu5Lu257uZIChbXlxccyxdKynvvIzkuLvpopjvvJooW14s77yMXSsp77yM5YaF5a6577yaKC4rKS8pO1xuICAgIFxuICAgIGlmICghZW1haWxNYXRjaCkge1xuICAgICAgLy8g5bCd6K+V566A5YyW5qC85byP77ya5Y+R6YKu5Lu25YiwIHh4eEBleGFtcGxlLmNvbSDkuLvpopggeHh4IOWGheWuuSB4eHhcbiAgICAgIGNvbnN0IHNpbXBsZU1hdGNoID0gbWVzc2FnZS5tYXRjaCgv5Y+R6YKu5Lu2ICg/OuWIsCB8IOe7mSkgKFteXFxzLF0rKVxccyooPzrkuLvpopggfCDmoIfpopgpWzrvvJpdP1xccyooW15cXHMsXSspXFxzKig/OuWGheWuuSB8IOato+aWhylbOu+8ml0/XFxzKiguKykvKTtcbiAgICAgIFxuICAgICAgaWYgKCFzaW1wbGVNYXRjaCkge1xuICAgICAgICByZXR1cm4ge1xuICAgICAgICAgIHN1Y2Nlc3M6IGZhbHNlLFxuICAgICAgICAgIG1lc3NhZ2U6ICfor7fmjIflrprmlLbku7bkurrjgIHkuLvpopjlkozlhoXlrrnvvIzkvovlpoLvvJrlj5HpgIHpgq7ku7bnu5kgdGVzdEBleGFtcGxlLmNvbe+8jOS4u+mimO+8mua1i+ivle+8jOWGheWuue+8mui/meaYr+S4gOWwgea1i+ivlemCruS7ticsXG4gICAgICAgICAgc3VnZ2VzdEFjdGlvbnM6IFtcbiAgICAgICAgICAgICflj5HpgIHpgq7ku7bnu5kgdGVzdEBleGFtcGxlLmNvbe+8jOS4u+mimO+8muS8muiurumAmuefpe+8jOWGheWuue+8muaYjuWkqeS4i+WNiCAzIOeCueW8gOS8micsXG4gICAgICAgICAgICAn5Y+R6YKu5Lu25YiwIGpvaG5AZXhhbXBsZS5jb20g5Li76aKY77ya6Zeu5YCZIOWGheWuue+8muS9oOWlve+8gScsXG4gICAgICAgICAgXSxcbiAgICAgICAgfTtcbiAgICAgIH1cblxuICAgICAgY29uc3QgWywgdG8sIHN1YmplY3QsIGJvZHldID0gc2ltcGxlTWF0Y2g7XG4gICAgICByZXR1cm4gdGhpcy5wZXJmb3JtU2VuZEVtYWlsKHRvLnRyaW0oKSwgc3ViamVjdC50cmltKCksIGJvZHkudHJpbSgpKTtcbiAgICB9XG5cbiAgICBjb25zdCBbLCB0bywgc3ViamVjdCwgYm9keV0gPSBlbWFpbE1hdGNoO1xuICAgIHJldHVybiB0aGlzLnBlcmZvcm1TZW5kRW1haWwodG8udHJpbSgpLCBzdWJqZWN0LnRyaW0oKSwgYm9keS50cmltKCkpO1xuICB9XG5cbiAgLyoqXG4gICAqIOaJp+ihjOmCruS7tuWPkemAgVxuICAgKi9cbiAgcHJpdmF0ZSBhc3luYyBwZXJmb3JtU2VuZEVtYWlsKHRvOiBzdHJpbmcsIHN1YmplY3Q6IHN0cmluZywgYm9keTogc3RyaW5nKTogUHJvbWlzZTxTa2lsbFJlc3VsdD4ge1xuICAgIGlmICghdGhpcy5jbGllbnQpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcign5a6i5oi356uv5pyq5Yid5aeL5YyWJyk7XG4gICAgfVxuXG4gICAgLy8g5p6E5bu65Y+R6YCB6K+35rGCXG4gICAgY29uc3QgZW1haWxSZXE6IFNlbmRFbWFpbFJlcXVlc3QgPSB7XG4gICAgICBmcm9tOiAnbm9yZXBseUB5b3VyZG9tYWluLmNvbScsIC8vIFRPRE86IOS7jumFjee9ruivu+WPllxuICAgICAgdG86IHRvLFxuICAgICAgc3ViamVjdDogc3ViamVjdCxcbiAgICAgIGJvZHk6IGJvZHksXG4gICAgfTtcblxuICAgIC8vIOaJp+ihjOWPkemAgVxuICAgIGNvbnN0IHJlc3VsdCA9IGF3YWl0IHRoaXMuY2xpZW50LnNlbmRFbWFpbChlbWFpbFJlcSk7XG5cbiAgICBpZiAocmVzdWx0LnN1Y2Nlc3MpIHtcbiAgICAgIHJldHVybiB7XG4gICAgICAgIHN1Y2Nlc3M6IHRydWUsXG4gICAgICAgIG1lc3NhZ2U6IGDinIUg6YKu5Lu25Y+R6YCB5oiQ5Yqf77yBXFxu5pS25Lu25Lq677yaJHt0b31cXG7kuLvpopjvvJoke3N1YmplY3R9XFxu6YKu5Lu2IElEOiAkeyhyZXN1bHQgYXMgYW55KS5tZXNzYWdlSWQgfHwgJ04vQSd9YCxcbiAgICAgICAgZGF0YTogcmVzdWx0LFxuICAgICAgfTtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIHtcbiAgICAgICAgc3VjY2VzczogZmFsc2UsXG4gICAgICAgIG1lc3NhZ2U6IGDinYwg6YKu5Lu25Y+R6YCB5aSx6LSl77yaJHtyZXN1bHQubWVzc2FnZX1gLFxuICAgICAgICBlcnJvcjogcmVzdWx0Lm1lc3NhZ2UsXG4gICAgICB9O1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiDlpITnkIbojrflj5bogZTns7vkurpcbiAgICovXG4gIHByaXZhdGUgYXN5bmMgaGFuZGxlR2V0Q29udGFjdHMobWVzc2FnZTogc3RyaW5nKTogUHJvbWlzZTxTa2lsbFJlc3VsdD4ge1xuICAgIGlmICghdGhpcy5jbGllbnQpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcign5a6i5oi356uv5pyq5Yid5aeL5YyWJyk7XG4gICAgfVxuXG4gICAgLy8gVE9ETzog6ZyA6KaB5LuO6YWN572u6K+75Y+WIGFwcElkXG4gICAgcmV0dXJuIHtcbiAgICAgIHN1Y2Nlc3M6IGZhbHNlLFxuICAgICAgbWVzc2FnZTogJ+ivt+WFiOmFjee9riBBcHAgSUQg5omN6IO96I635Y+W6IGU57O75Lq65YiX6KGoJyxcbiAgICAgIHN1Z2dlc3RBY3Rpb25zOiBbJ+mFjee9riBBcHAgSUQnXSxcbiAgICB9O1xuICB9XG5cbiAgLyoqXG4gICAqIOWkhOeQhuS/neWtmOiBlOezu+S6ulxuICAgKi9cbiAgcHJpdmF0ZSBhc3luYyBoYW5kbGVTYXZlQ29udGFjdChtZXNzYWdlOiBzdHJpbmcpOiBQcm9taXNlPFNraWxsUmVzdWx0PiB7XG4gICAgaWYgKCF0aGlzLmNsaWVudCkge1xuICAgICAgdGhyb3cgbmV3IEVycm9yKCflrqLmiLfnq6/mnKrliJ3lp4vljJYnKTtcbiAgICB9XG5cbiAgICAvLyDmj5Dlj5bogZTns7vkurrkv6Hmga9cbiAgICAvLyDmoLzlvI/vvJrkv53lrZjogZTns7vkurogeHh4QGV4YW1wbGUuY29t77yM5aeT5ZCN77yaeHh4XG4gICAgY29uc3QgY29udGFjdE1hdGNoID0gbWVzc2FnZS5tYXRjaCgv5L+d5a2Y6IGU57O75Lq6IChbXlxccyxdKynvvIzlp5PlkI3vvJooLispLyk7XG4gICAgXG4gICAgaWYgKCFjb250YWN0TWF0Y2gpIHtcbiAgICAgIHJldHVybiB7XG4gICAgICAgIHN1Y2Nlc3M6IGZhbHNlLFxuICAgICAgICBtZXNzYWdlOiAn6K+35oyH5a6a6IGU57O75Lq66YKu566x5ZKM5aeT5ZCN77yM5L6L5aaC77ya5L+d5a2Y6IGU57O75Lq6IGpvaG5AZXhhbXBsZS5jb23vvIzlp5PlkI3vvJpKb2huIERvZScsXG4gICAgICAgIHN1Z2dlc3RBY3Rpb25zOiBbJ+S/neWtmOiBlOezu+S6uiBqb2huQGV4YW1wbGUuY29t77yM5aeT5ZCN77yaSm9obiBEb2UnXSxcbiAgICAgIH07XG4gICAgfVxuXG4gICAgY29uc3QgWywgZW1haWwsIG5hbWVdID0gY29udGFjdE1hdGNoO1xuXG4gICAgLy8gVE9ETzog6ZyA6KaB5LuO6YWN572u6K+75Y+WIGFwcElkXG4gICAgcmV0dXJuIHtcbiAgICAgIHN1Y2Nlc3M6IGZhbHNlLFxuICAgICAgbWVzc2FnZTogJ+ivt+WFiOmFjee9riBBcHAgSUQg5omN6IO95L+d5a2Y6IGU57O75Lq6JyxcbiAgICAgIHN1Z2dlc3RBY3Rpb25zOiBbJ+mFjee9riBBcHAgSUQnXSxcbiAgICB9O1xuICB9XG5cbiAgLyoqXG4gICAqIOWkhOeQhuWIoOmZpOiBlOezu+S6ulxuICAgKi9cbiAgcHJpdmF0ZSBhc3luYyBoYW5kbGVEZWxldGVDb250YWN0KG1lc3NhZ2U6IHN0cmluZyk6IFByb21pc2U8U2tpbGxSZXN1bHQ+IHtcbiAgICBpZiAoIXRoaXMuY2xpZW50KSB7XG4gICAgICB0aHJvdyBuZXcgRXJyb3IoJ+WuouaIt+err+acquWIneWni+WMlicpO1xuICAgIH1cblxuICAgIC8vIOaPkOWPluiBlOezu+S6uumCrueusVxuICAgIGNvbnN0IGVtYWlsTWF0Y2ggPSBtZXNzYWdlLm1hdGNoKC/liKDpmaTogZTns7vkurogKFteXFxzLF0rKS8pO1xuICAgIFxuICAgIGlmICghZW1haWxNYXRjaCkge1xuICAgICAgcmV0dXJuIHtcbiAgICAgICAgc3VjY2VzczogZmFsc2UsXG4gICAgICAgIG1lc3NhZ2U6ICfor7fmjIflrpropoHliKDpmaTnmoTogZTns7vkurrpgq7nrrHvvIzkvovlpoLvvJrliKDpmaTogZTns7vkurogam9obkBleGFtcGxlLmNvbScsXG4gICAgICAgIHN1Z2dlc3RBY3Rpb25zOiBbJ+WIoOmZpOiBlOezu+S6uiBqb2huQGV4YW1wbGUuY29tJ10sXG4gICAgICB9O1xuICAgIH1cblxuICAgIGNvbnN0IFssIGVtYWlsXSA9IGVtYWlsTWF0Y2g7XG5cbiAgICAvLyBUT0RPOiDpnIDopoHku47phY3nva7or7vlj5YgYXBwSWRcbiAgICByZXR1cm4ge1xuICAgICAgc3VjY2VzczogZmFsc2UsXG4gICAgICBtZXNzYWdlOiAn6K+35YWI6YWN572uIEFwcCBJRCDmiY3og73liKDpmaTogZTns7vkuronLFxuICAgICAgc3VnZ2VzdEFjdGlvbnM6IFsn6YWN572uIEFwcCBJRCddLFxuICAgIH07XG4gIH1cblxuICAvKipcbiAgICog6I635Y+W5biu5Yqp5L+h5oGvXG4gICAqL1xuICBwcml2YXRlIGdldEhlbHBNZXNzYWdlKCk6IFNraWxsUmVzdWx0IHtcbiAgICByZXR1cm4ge1xuICAgICAgc3VjY2VzczogdHJ1ZSxcbiAgICAgIG1lc3NhZ2U6IGDwn5OnIFNlbmRGbGFyZSBFbWFpbCBTa2lsbCDluK7liqlcblxu5Y+v55So5ZG95Luk77yaXG4xLiDlj5HpgIHpgq7ku7bvvJrlj5HpgIHpgq7ku7bnu5kgeHh4QGV4YW1wbGUuY29t77yM5Li76aKY77yaeHh477yM5YaF5a6577yaeHh4XG4yLiDojrflj5bogZTns7vkurrvvJrojrflj5bogZTns7vkurrliJfooahcbjMuIOS/neWtmOiBlOezu+S6uu+8muS/neWtmOiBlOezu+S6uiB4eHhAZXhhbXBsZS5jb23vvIzlp5PlkI3vvJp4eHhcbjQuIOWIoOmZpOiBlOezu+S6uu+8muWIoOmZpOiBlOezu+S6uiB4eHhAZXhhbXBsZS5jb21cblxu56S65L6L77yaXG4tIOWPkemAgemCruS7tue7mSB0ZXN0QGV4YW1wbGUuY29t77yM5Li76aKY77ya5Lya6K6u6YCa55+l77yM5YaF5a6577ya5piO5aSp5LiL5Y2IIDMg54K55byA5LyaXG4tIOiOt+WPluiBlOezu+S6uuWIl+ihqFxuLSDkv53lrZjogZTns7vkurogam9obkBleGFtcGxlLmNvbe+8jOWnk+WQje+8mkpvaG4gRG9lXG4tIOWIoOmZpOiBlOezu+S6uiBqb2huQGV4YW1wbGUuY29tYCxcbiAgICAgIHN1Z2dlc3RBY3Rpb25zOiBbXG4gICAgICAgICflj5HpgIHpgq7ku7bnu5kgdGVzdEBleGFtcGxlLmNvbe+8jOS4u+mimO+8mua1i+ivle+8jOWGheWuue+8mui/meaYr+S4gOWwgea1i+ivlemCruS7ticsXG4gICAgICAgICfojrflj5bogZTns7vkurrliJfooagnLFxuICAgICAgICAn5L+d5a2Y6IGU57O75Lq6IGpvaG5AZXhhbXBsZS5jb23vvIzlp5PlkI3vvJpKb2huIERvZScsXG4gICAgICBdLFxuICAgIH07XG4gIH1cbn1cblxuLy8g5a+85Ye65Y2V5L6LXG5leHBvcnQgZGVmYXVsdCBuZXcgU2VuZGZsYXJlU2tpbGwoKTtcbiJdfQ==