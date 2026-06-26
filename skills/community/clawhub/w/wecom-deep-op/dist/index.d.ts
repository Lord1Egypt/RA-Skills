/**
 * wecom-deep-op - Enterprise WeChat All-in-One Skill
 *
 * This skill provides a unified interface to all WeCom (Enterprise WeChat)
 * MCP capabilities: documents, calendar/schedule, meetings, todos, and contacts.
 *
 * @package wecom-deep-op
 * @author 白小圈
 * @license MIT
 */
/**
 * 企业微信API错误类
 * 封装企业微信返回的错误信息，提供更清晰的错误消息
 */
export declare class WeComError extends Error {
    readonly errcode: number;
    readonly errmsg: string;
    readonly data?: any;
    constructor(message: string, errcode: number, errmsg: string, data?: any);
    toString(): string;
}
/**
 * 简单日志工具
 * 支持 debug/info/error 级别，可通过环境变量控制
 */
export declare class Logger {
    private prefix;
    private level;
    constructor(service: string);
    debug(message: string, meta?: any): void;
    info(message: string, meta?: any): void;
    warn(message: string, meta?: any): void;
    error(message: string, error?: any): void;
}
/**
 * 实现说明：
 * - 本 Skill 作为 OpenClaw 的技能插件，会被 OpenClaw 自动加载
 * - OpenClaw 会调用 skill.exportedTools 中注册的工具函数
 * - 所有工具函数都是异步的，返回标准 JSON 对象
 *
 * 配置要求：
 * - 用户需要在自己的 mcporter.json 中配置 wecom-doc / wecom-schedule / wecom-meeting / wecom-todo / wecom-contact 五个端点
 * - 或使用本 Skill 提供的统一配置端点 wecom-deep-op（如果配置了代理模式）
 *
 * 安全原则：
 * - 绝不硬编码任何 uaKey 或凭证
 * - 从环境变量或用户配置读取 endpoint 信息
 * - 所有敏感配置必须由用户自己管理
 */
export declare const skillMetadata: {
    name: string;
    version: string;
    description: string;
    author: string;
    license: string;
};
/**
 * 导出/获取文档内容
 * @param docid - 文档ID，或提供 url
 * @param type - 导出类型，固定为 2 (Markdown)
 * @param task_id - 如果有，表示轮询
 */
export declare function doc_get(docid?: string, url?: string, task_id?: string): Promise<Record<string, any>>;
/**
 * 创建文档
 * @param doc_type - 文档类型：3=文档，10=智能表格
 * @param doc_name - 文档名称
 */
export declare function doc_create(doc_type: number, doc_name: string): Promise<Record<string, any>>;
/**
 * 编辑/覆写文档内容
 * @param docid - 文档ID
 * @param content - Markdown内容
 * @param content_type - 内容类型，固定为 1 (Markdown)
 */
export declare function doc_edit(docid: string, content: string, content_type?: number): Promise<Record<string, any>>;
/**
 * 创建日程
 */
export declare function schedule_create(params: {
    summary: string;
    start_time: string;
    end_time: string;
    location?: string;
    description?: string;
    attendees?: string[];
    reminders?: Array<{
        type: number;
        minutes: number;
    }>;
}): Promise<Record<string, any>>;
/**
 * 查询日程
 */
export declare function schedule_list(start_time: string, end_time: string, params?: Record<string, any>): Promise<Record<string, any>>;
/**
 * 获取日程详情
 */
export declare function schedule_get(schedule_id: string): Promise<Record<string, any>>;
/**
 * 更新日程
 */
export declare function schedule_update(schedule_id: string, updates: Partial<{
    summary: string;
    start_time: string;
    end_time: string;
    location: string;
    description: string;
}>): Promise<Record<string, any>>;
/**
 * 取消日程
 */
export declare function schedule_cancel(schedule_id: string): Promise<Record<string, any>>;
/**
 * 添加参会人
 */
export declare function schedule_add_attendee(schedule_id: string, attendee_userids: string[]): Promise<Record<string, any>>;
/**
 * 移除参会人
 */
export declare function schedule_remove_attendee(schedule_id: string, attendee_userids: string[]): Promise<Record<string, any>>;
/**
 * 创建/预约会议
 */
export declare function meeting_create(params: {
    subject: string;
    start_time: string;
    end_time: string;
    type?: number;
    attendees?: string[];
    agenda?: string;
    media_conf_id?: string;
    meeting_room_id?: string;
}): Promise<Record<string, any>>;
/**
 * 查询会议列表
 */
export declare function meeting_list(start_time: string, end_time: string, params?: Record<string, any>): Promise<Record<string, any>>;
/**
 * 获取会议详情
 */
export declare function meeting_get(meeting_id: string): Promise<Record<string, any>>;
/**
 * 取消会议
 */
export declare function meeting_cancel(meeting_id: string): Promise<Record<string, any>>;
/**
 * 更新会议参会人
 */
export declare function meeting_update_attendees(meeting_id: string, add_attendees?: string[], remove_attendees?: string[]): Promise<Record<string, any>>;
/**
 * 创建待办
 */
export declare function todo_create(params: {
    title: string;
    due_time?: string;
    priority?: number;
    desc?: string;
    receivers?: string[];
    creator?: string;
}): Promise<Record<string, any>>;
/**
 * 获取待办列表
 */
export declare function todo_list(status?: number, // 0=未开始, 1=进行中, 2=完成
limit?: number, offset?: number): Promise<Record<string, any>>;
/**
 * 获取待办详情
 */
export declare function todo_get(todo_id: string): Promise<Record<string, any>>;
/**
 * 更新待办状态
 */
export declare function todo_update_status(todo_id: string, status: 0 | 1 | 2): Promise<Record<string, any>>;
/**
 * 更新待办内容
 */
export declare function todo_update(todo_id: string, updates: Partial<{
    title: string;
    due_time: string;
    priority: number;
    desc: string;
}>): Promise<Record<string, any>>;
/**
 * 删除待办
 */
export declare function todo_delete(todo_id: string): Promise<Record<string, any>>;
/**
 * 接收待办
 */
export declare function todo_accept(todo_id: string): Promise<Record<string, any>>;
/**
 * 拒绝待办
 */
export declare function todo_refuse(todo_id: string, reason?: string): Promise<Record<string, any>>;
/**
 * 获取通讯录成员列表（当前用户可见范围）
 * ⚠️ 限制：只返回当前用户**可见范围内**的成员（通常≤100人，建议≤10人使用）
 */
export declare function contact_get_userlist(): Promise<Record<string, any>>;
/**
 * 搜索成员（本地筛选）
 * 说明：企业微信MCP不支持服务端搜索，本函数获取全量后本地过滤
 */
export declare function contact_search(keyword: string): Promise<Record<string, any>>;
/**
 * 健康检查/就绪探测（Ping）
 * 用于验证 skill 加载、插件版本和配置是否正确
 *
 * 新增：检查企业微信官方插件版本是否 ≥ 1.0.13
 */
export declare function ping(): Promise<Record<string, any>>;
/**
 * 前置条件检查（Preflight）
 * 验证配置是否完整，如缺失则提供修复建议
 *
 * 新增：检查企业微信官方插件版本
 */
export declare function preflight_check(): Promise<Record<string, any>>;
/**
 * OpenClaw 加载 Skill 时调用，返回所有可用工具
 */
export declare const exportedTools: {
    doc_get: typeof doc_get;
    doc_create: typeof doc_create;
    doc_edit: typeof doc_edit;
    schedule_create: typeof schedule_create;
    schedule_list: typeof schedule_list;
    schedule_get: typeof schedule_get;
    schedule_update: typeof schedule_update;
    schedule_cancel: typeof schedule_cancel;
    schedule_add_attendee: typeof schedule_add_attendee;
    schedule_remove_attendee: typeof schedule_remove_attendee;
    meeting_create: typeof meeting_create;
    meeting_list: typeof meeting_list;
    meeting_get: typeof meeting_get;
    meeting_cancel: typeof meeting_cancel;
    meeting_update_attendees: typeof meeting_update_attendees;
    todo_create: typeof todo_create;
    todo_list: typeof todo_list;
    todo_get: typeof todo_get;
    todo_update_status: typeof todo_update_status;
    todo_update: typeof todo_update;
    todo_delete: typeof todo_delete;
    todo_accept: typeof todo_accept;
    todo_refuse: typeof todo_refuse;
    contact_get_userlist: typeof contact_get_userlist;
    contact_search: typeof contact_search;
    ping: typeof ping;
    preflight_check: typeof preflight_check;
};
/**
 * Default export (for CommonJS compatibility)
 */
export default exportedTools;
