export interface MailAccountConfig {
  id: string;
  displayName?: string;
  protocol: {
    receive: "imap" | "pop3";
    send: "smtp";
  };
  imap?: {
    host: string;
    port: number;
    useTLS: boolean;
  };
  pop3?: {
    host: string;
    port: number;
    useTLS: boolean;
  };
  smtp: {
    host: string;
    port: number;
    useTLS: boolean;
  };
  auth: {
    username: string;
    password: string;
  };
  defaults: {
    inboxFolder: string;
    sentFolder: string;
    maxListLimit: number;
  };
}

export interface SkillConfig {
  mailAccounts: MailAccountConfig[];
}

export interface SendEmailRequest {
  accountId: string;
  to: string[];
  cc?: string[];
  bcc?: string[];
  subject: string;
  bodyText?: string;
  bodyHtml?: string;
  attachments?: {
    filename: string;
    contentBase64: string;
    mimeType?: string;
  }[];
}

export interface SendEmailResponse {
  status: "ok" | "error";
  accountId: string;
  messageId?: string;
  sentAt?: string;
  errorMessage?: string;
}

export interface ListMessagesRequest {
  accountId: string;
  folder?: string;
  limit?: number;
  unreadOnly?: boolean;
  since?: string;
  fromContains?: string;
  subjectContains?: string;
}

export interface MailSummary {
  id: string;
  subject: string;
  from: string;
  to: string[];
  date: string;
  isRead: boolean | null;
  hasAttachments: boolean;
  snippet: string;
}

export interface ListMessagesResponse {
  accountId: string;
  folder: string;
  total: number;
  messages: MailSummary[];
}

export interface GetMessageRequest {
  accountId: string;
  id: string;
  folder?: string;
}

export interface AttachmentMeta {
  id: string;
  filename: string;
  size: number;
  mimeType: string;
}

export interface GetMessageResponse {
  accountId: string;
  id: string;
  folder: string;
  subject: string;
  from: string;
  to: string[];
  cc: string[];
  date: string;
  isRead: boolean | null;
  bodyText?: string;
  bodyHtml?: string;
  attachments: AttachmentMeta[];
}

export interface GetAttachmentRequest {
  accountId: string;
  messageId: string;
  attachmentId: string;
  folder?: string;
}

export interface GetAttachmentResponse {
  accountId: string;
  filename: string;
  mimeType: string;
  contentBase64: string;
}

export interface UpdateMessageStatusRequest {
  accountId: string;
  id: string;
  folder?: string;
  markAsRead?: boolean;
  markAsUnread?: boolean;
  moveToFolder?: string;
}

export interface UpdateMessageStatusResponse {
  status: "ok" | "error";
  accountId: string;
  updated?: {
    isRead?: boolean | null;
    folder?: string;
  };
  errorMessage?: string;
}
