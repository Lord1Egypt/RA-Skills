import type { SendflareConfig, SkillContext, SkillResult } from './types';
export declare class SendflareSkill {
    name: string;
    description: string;
    version: string;
    private client;
    private config;
    /**
     * 初始化方法（OpenClaw 会在加载时调用）
     */
    initialize(config: SendflareConfig): Promise<void>;
    /**
     * 核心执行方法
     */
    execute(context: SkillContext): Promise<SkillResult>;
    /**
     * 匹配发送邮件意图
     */
    private matchSendEmailIntent;
    /**
     * 匹配获取联系人意图
     */
    private matchGetContactsIntent;
    /**
     * 匹配保存联系人意图
     */
    private matchSaveContactIntent;
    /**
     * 匹配删除联系人意图
     */
    private matchDeleteContactIntent;
    /**
     * 处理发送邮件
     */
    private handleSendEmail;
    /**
     * 执行邮件发送
     */
    private performSendEmail;
    /**
     * 处理获取联系人
     */
    private handleGetContacts;
    /**
     * 处理保存联系人
     */
    private handleSaveContact;
    /**
     * 处理删除联系人
     */
    private handleDeleteContact;
    /**
     * 获取帮助信息
     */
    private getHelpMessage;
}
declare const _default: SendflareSkill;
export default _default;
