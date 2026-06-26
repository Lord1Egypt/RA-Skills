import type { SendflareConfig, SendEmailRequest, SendEmailResponse, SaveContactRequest, DeleteContactRequest, GetContactListRequest, GetContactListResponse } from './types';
export declare class SendflareClient {
    private client;
    private config;
    constructor(config: SendflareConfig);
    /**
     * 发送邮件
     */
    sendEmail(req: SendEmailRequest): Promise<SendEmailResponse>;
    /**
     * 获取联系人列表
     */
    getContactList(req: GetContactListRequest): Promise<GetContactListResponse>;
    /**
     * 保存联系人
     */
    saveContact(req: SaveContactRequest): Promise<{
        success: boolean;
        message: string;
    }>;
    /**
     * 删除联系人
     */
    deleteContact(req: DeleteContactRequest): Promise<{
        success: boolean;
        message: string;
    }>;
}
