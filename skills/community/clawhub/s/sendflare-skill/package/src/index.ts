/**
 * Sendflare Skill
 * 
 * 通过 Sendflare SDK 发送电子邮件和管理联系人
 */
import { SendflareClient } from './Sendflare-client';
import type { SendflareConfig, SkillContext, SkillResult, SendEmailRequest } from './types';

export class SendflareSkill {
  public name: string = 'Sendflare-email';
  public description: string = '通过 Sendflare 发送电子邮件和管理联系人';
  public version: string = '1.0.0';

  private client: SendflareClient | null = null;
  private config: SendflareConfig | null = null;

  /**
   * 初始化方法（OpenClaw 会在加载时调用）
   */
  async initialize(config: SendflareConfig): Promise<void> {
    this.config = {
      apiToken: config.apiToken,
    };
    this.client = new SendflareClient(this.config);
  }

  /**
   * 核心执行方法
   */
  async execute(context: SkillContext): Promise<SkillResult> {
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
      } else if (this.matchGetContactsIntent(message)) {
        return await this.handleGetContacts(message);
      } else if (this.matchSaveContactIntent(message)) {
        return await this.handleSaveContact(message);
      } else if (this.matchDeleteContactIntent(message)) {
        return await this.handleDeleteContact(message);
      } else {
        return this.getHelpMessage();
      }
    } catch (error: any) {
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
  private matchSendEmailIntent(message: string): boolean {
    const lowerMsg = message.toLowerCase();
    return (
      lowerMsg.includes('发送邮件') ||
      lowerMsg.includes('发邮件') ||
      lowerMsg.includes('send email') ||
      lowerMsg.includes('email to')
    );
  }

  /**
   * 匹配获取联系人意图
   */
  private matchGetContactsIntent(message: string): boolean {
    const lowerMsg = message.toLowerCase();
    return (
      lowerMsg.includes('联系人列表') ||
      lowerMsg.includes('列出联系人') ||
      lowerMsg.includes('显示联系人') ||
      lowerMsg.includes('get contacts') ||
      lowerMsg.includes('list contacts')
    );
  }

  /**
   * 匹配保存联系人意图
   */
  private matchSaveContactIntent(message: string): boolean {
    const lowerMsg = message.toLowerCase();
    return (
      lowerMsg.includes('保存联系人') ||
      lowerMsg.includes('添加联系人') ||
      lowerMsg.includes('save contact') ||
      lowerMsg.includes('add contact')
    );
  }

  /**
   * 匹配删除联系人意图
   */
  private matchDeleteContactIntent(message: string): boolean {
    const lowerMsg = message.toLowerCase();
    return (
      lowerMsg.includes('删除联系人') ||
      lowerMsg.includes('remove contact') ||
      lowerMsg.includes('delete contact')
    );
  }

  /**
   * 处理发送邮件
   */
  private async handleSendEmail(message: string): Promise<SkillResult> {
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
  private async performSendEmail(to: string, subject: string, body: string): Promise<SkillResult> {
    if (!this.client) {
      throw new Error('客户端未初始化');
    }

    // 构建发送请求
    const emailReq: SendEmailRequest = {
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
        message: `✅ 邮件发送成功！\n收件人：${to}\n主题：${subject}\n邮件 ID: ${(result as any).messageId || 'N/A'}`,
        data: result,
      };
    } else {
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
  private async handleGetContacts(message: string): Promise<SkillResult> {
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
  private async handleSaveContact(message: string): Promise<SkillResult> {
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
  private async handleDeleteContact(message: string): Promise<SkillResult> {
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
  private getHelpMessage(): SkillResult {
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

// 导出单例
export default new SendflareSkill();
