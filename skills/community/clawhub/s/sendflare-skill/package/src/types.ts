/**
 * Sendflare Skill Types
 */

/**
 * Sendflare API 配置
 */
export interface SendflareConfig {
  apiToken: string;
}

/**
 * 发送邮件请求
 */
export interface SendEmailRequest {
  /** 发件人邮箱 */
  from: string;
  /** 收件人邮箱 */
  to: string;
  /** 邮件主题 */
  subject: string;
  /** 邮件内容 */
  body: string;
  /** 抄送邮箱列表 */
  cc?: string[];
  /** 密送邮箱列表 */
  bcc?: string[];
}

/**
 * 发送邮件响应
 */
export interface SendEmailResponse {
  /** 是否成功 */
  success: boolean;
  /** 邮件 ID */
  messageId?: string;
  /** 响应消息 */
  message: string;
}

/**
 * 联系人数据
 */
export interface ContactData {
  firstName?: string;
  lastName?: string;
  company?: string;
  phone?: string;
  [key: string]: string | undefined;
}

/**
 * 保存联系人请求
 */
export interface SaveContactRequest {
  /** 应用 ID */
  appId: string;
  /** 联系人邮箱 */
  emailAddress: string;
  /** 联系人数据 */
  data?: ContactData;
}

/**
 * 删除联系人请求
 */
export interface DeleteContactRequest {
  /** 应用 ID */
  appId: string;
  /** 联系人邮箱 */
  emailAddress: string;
}

/**
 * 获取联系人列表请求
 */
export interface GetContactListRequest {
  /** 应用 ID */
  appId: string;
  /** 页码 */
  page?: number;
  /** 每页数量 */
  pageSize?: number;
}

/**
 * 联系人信息
 */
export interface Contact {
  /** 邮箱地址 */
  emailAddress: string;
  /** 联系人数据 */
  data?: ContactData;
  /** 创建时间 */
  createdAt?: string;
  /** 更新时间 */
  updatedAt?: string;
}

/**
 * 联系人列表响应
 */
export interface GetContactListResponse {
  /** 联系人列表 */
  contacts: Contact[];
  /** 总数 */
  total: number;
  /** 当前页 */
  page: number;
  /** 每页数量 */
  pageSize: number;
}

/**
 * Skill 执行上下文
 */
export interface SkillContext {
  userMessage: {
    content: string;
  };
  config?: SendflareConfig;
}

/**
 * Skill 执行结果
 */
export interface SkillResult {
  success: boolean;
  message: string;
  data?: any;
  suggestActions?: string[];
  error?: string;
}
