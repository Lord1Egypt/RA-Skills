// SubsTracker API TypeScript Interfaces
// These serve as the canonical schema for all API operations.

// ─── Environment Config ───

export interface SubsTrackerEnv {
  SUBSTRACKER_URL: string;
  SUBSTRACKER_USER: string;
  SUBSTRACKER_PASS: string;
}

// ─── Subscription ───

export interface CreateSubscriptionInput {
  /** Subscription name (required) */
  name: string;
  /** Next renewal date, YYYY-MM-DD (required) */
  expiryDate: string;
  /** Cycle length, e.g. 1, 3, 6. Default: 1 */
  periodValue?: number;
  /** Cycle unit. Default: "month" */
  periodUnit?: "day" | "month" | "year";
  /** Price per cycle */
  amount?: number;
  /** Currency code. Default: "CNY" */
  currency?: string;
  /** Auto-renew on expiry. Default: true */
  autoRenew?: boolean;
  /** Reminder unit. Default: "day" */
  reminderUnit?: "day" | "hour";
  /** Days/hours before expiry to notify */
  reminderValue?: number;
  /** Legacy alias for reminderValue (day) */
  reminderDays?: number;
  /** Legacy alias for reminderValue (hour) */
  reminderHours?: number;
  /** Enable/disable. Default: true */
  isActive?: boolean;
  /** Free text notes */
  notes?: string;
  /** e.g. "娱乐", "工具", "云服务" */
  category?: string;
  /** e.g. "视频流媒体", "域名" */
  customType?: string;
  /** "cycle" = 累计续期, "reset" = 从当天起算. Default: "cycle" */
  subscriptionMode?: "cycle" | "reset";
  /** Subscription start date, ISO format */
  startDate?: string;
  /** Use lunar calendar for cycle calculation. Default: false */
  useLunar?: boolean;
}

export interface UpdateSubscriptionInput extends CreateSubscriptionInput {
  // same fields, name and expiryDate still required
}

export interface PaymentRecord {
  id: string;
  date: string;
  amount: number;
  /** "initial" = first payment, "manual" = manual renew, "auto" = auto renew */
  type: "initial" | "manual" | "auto";
  note: string;
  periodStart?: string;
  periodEnd?: string;
}

export interface Subscription {
  id: string;
  name: string;
  subscriptionMode: string;
  customType: string;
  category: string;
  startDate: string | null;
  expiryDate: string;
  periodValue: number;
  periodUnit: string;
  reminderUnit: string;
  reminderValue: number;
  reminderDays?: number;
  reminderHours?: number;
  notes: string;
  amount: number | null;
  currency: string;
  lastPaymentDate: string;
  paymentHistory: PaymentRecord[];
  isActive: boolean;
  autoRenew: boolean;
  useLunar: boolean;
  createdAt: string;
  updatedAt?: string;
}

// ─── Renew ───

export interface RenewOptions {
  /** Payment amount. Default: subscription's current amount */
  amount?: number;
  /** How many cycles to renew. Default: 1 */
  periodMultiplier?: number;
  /** ISO datetime, when payment was made. Default: now */
  paymentDate?: string;
  /** Payment note. Default: "手动续订" */
  note?: string;
}

// ─── Payment Edit ───

export interface EditPaymentInput {
  /** ISO datetime */
  date?: string;
  amount?: number;
  note?: string;
}

// ─── Dashboard ───

export interface DashboardStats {
  monthlyExpense: number;
  yearlyExpense: number;
  activeSubscriptions: {
    active: number;
    total: number;
    expiringSoon: number;
  };
  recentPayments: unknown[];
  upcomingRenewals: unknown[];
  expenseByType: unknown[];
  expenseByCategory: unknown[];
  schedulerStatus: unknown;
  schedulerStatusHistory: unknown[];
}

// ─── App Config ───
//
// Secret handling when updating config:
// - Sending "" does NOT clear a secret (prevents accidental wipes)
// - Sending "********" = no change (legacy compat)
// - To clear a secret: include its name in CLEAR_SECRET_FIELDS array
// - ADMIN_PASSWORD only changes when non-empty

export interface AppConfig {
  // ── Account ──
  /** Login username */
  ADMIN_USERNAME?: string;
  /** Set only to change password */
  ADMIN_PASSWORD?: string;

  // ── Telegram ──
  /** Bot token from @BotFather (secret) */
  TG_BOT_TOKEN?: string;
  /** Chat or user ID */
  TG_CHAT_ID?: string;

  // ── NotifyX ──
  /** NotifyX API key (secret) */
  NOTIFYX_API_KEY?: string;

  // ── Webhook ──
  /** Webhook endpoint URL (secret) */
  WEBHOOK_URL?: string;
  /** HTTP method. Default: "POST" */
  WEBHOOK_METHOD?: string;
  /** JSON string of custom headers (secret) */
  WEBHOOK_HEADERS?: string;
  /** Body template with {{title}}, {{content}}, {{tags}}, {{timestamp}} */
  WEBHOOK_TEMPLATE?: string;

  // ── WeChat Bot ──
  /** WeChat bot webhook URL (secret) */
  WECHATBOT_WEBHOOK?: string;
  /** Message type: "text" | "markdown". Default: "text" */
  WECHATBOT_MSG_TYPE?: string;
  /** Comma-separated mobile numbers to @mention */
  WECHATBOT_AT_MOBILES?: string;
  /** "true" to @all. Default: "false" */
  WECHATBOT_AT_ALL?: string;

  // ── Email (Resend) ──
  /** Resend API key (secret) */
  RESEND_API_KEY?: string;
  /** Sender email address */
  EMAIL_FROM?: string;
  /** Sender display name */
  EMAIL_FROM_NAME?: string;
  /** Recipient email address */
  EMAIL_TO?: string;

  // ── Bark ──
  /** iOS Bark device key (secret) */
  BARK_DEVICE_KEY?: string;
  /** Bark server URL. Default: "https://api.day.app" */
  BARK_SERVER?: string;
  /** Archive notifications: "true" | "false". Default: "false" */
  BARK_IS_ARCHIVE?: string;

  // ── Gotify ──
  /** Gotify server URL */
  GOTIFY_SERVER_URL?: string;
  /** Gotify app token (secret) */
  GOTIFY_APP_TOKEN?: string;

  // ── General ──
  /** Enabled notification channels. Default: ["notifyx"] */
  ENABLED_NOTIFIERS?: string[];
  /** Timezone, e.g. "Asia/Shanghai". Default: "UTC" */
  TIMEZONE?: string;
  /** Show lunar calendar dates. Default: false */
  SHOW_LUNAR?: boolean;
  /** UI theme: "light" | "dark" | "system". Default: "system" */
  THEME_MODE?: string;
  /** Allowed notification hours (UTC). Empty = always. Default: [] */
  NOTIFICATION_HOURS?: number[];
  /** Token for external /api/notify endpoint (secret) */
  THIRD_PARTY_API_TOKEN?: string;
  /** Enable debug logging. Default: false */
  DEBUG_LOGS?: boolean;
  /** Payment history limit per subscription. Range: 10–1000. Default: 100 */
  PAYMENT_HISTORY_LIMIT?: number;
  /** Field names to explicitly clear their secret values */
  CLEAR_SECRET_FIELDS?: string[];
}

// ─── Test Notification ───

export interface TestNotificationInput {
  /** Channel to test */
  type: "telegram" | "notifyx" | "webhook" | "wechatbot" | "email" | "bark" | "gotify";
  /** Optional config overrides for the channel being tested */
  [key: string]: unknown;
}

// ─── API Response ───

export interface ApiResponse<T = unknown> {
  success: boolean;
  message?: string;
  subscription?: T;
  data?: T;
  payments?: T;
}
