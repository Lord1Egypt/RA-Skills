/**
 * Sendflare SDK Client
 */
import { Sendflare } from 'Sendflare-sdk-ts';
import type {
  SendflareConfig,
  SendEmailRequest,
  SendEmailResponse,
  SaveContactRequest,
  DeleteContactRequest,
  GetContactListRequest,
  Contact,
  GetContactListResponse,
  ContactData,
} from './types';

export class SendflareClient {
  private client: Sendflare;
  private config: SendflareConfig;

  constructor(config: SendflareConfig) {
    this.config = config;
    this.client = new Sendflare(config.apiToken);
  }

  /**
   * 发送邮件
   */
  async sendEmail(req: SendEmailRequest): Promise<SendEmailResponse> {
    try {
      const emailReq: any = {
        from: req.from,
        to: req.to,
        subject: req.subject,
        body: req.body,
        cc: req.cc || [],
        bcc: req.bcc || [],
      };

      const response: any = await this.client.sendEmail(emailReq);

      return {
        success: true,
        messageId: (response as any).messageId,
        message: '邮件发送成功',
      };
    } catch (error: any) {
      return {
        success: false,
        message: error.message || '发送邮件失败',
      };
    }
  }

  /**
   * 获取联系人列表
   */
  async getContactList(req: GetContactListRequest): Promise<GetContactListResponse> {
    try {
      const response: any = await this.client.getContactList({
        appId: req.appId,
        page: req.page || 1,
        pageSize: req.pageSize || 20,
      });

      return {
        contacts: (response as any).contacts || [],
        total: (response as any).total || 0,
        page: req.page || 1,
        pageSize: req.pageSize || 20,
      };
    } catch (error: any) {
      throw new Error(`获取联系人列表失败：${error.message}`);
    }
  }

  /**
   * 保存联系人
   */
  async saveContact(req: SaveContactRequest): Promise<{ success: boolean; message: string }> {
    try {
      // 清理 undefined 值
      const cleanData: Record<string, string> = {};
      if (req.data) {
        Object.keys(req.data).forEach(key => {
          const value = (req.data as any)[key];
          if (value !== undefined && value !== null) {
            cleanData[key] = String(value);
          }
        });
      }

      await this.client.saveContact({
        appId: req.appId,
        emailAddress: req.emailAddress,
        data: Object.keys(cleanData).length > 0 ? cleanData : undefined,
      });

      return {
        success: true,
        message: `联系人 ${req.emailAddress} 保存成功`,
      };
    } catch (error: any) {
      return {
        success: false,
        message: `保存联系人失败：${error.message}`,
      };
    }
  }

  /**
   * 删除联系人
   */
  async deleteContact(req: DeleteContactRequest): Promise<{ success: boolean; message: string }> {
    try {
      await this.client.deleteContact({
        appId: req.appId,
        emailAddress: req.emailAddress,
      });

      return {
        success: true,
        message: `联系人 ${req.emailAddress} 删除成功`,
      };
    } catch (error: any) {
      return {
        success: false,
        message: `删除联系人失败：${error.message}`,
      };
    }
  }
}
