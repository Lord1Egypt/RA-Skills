// Config commands
import { api } from "./client";
import type { AppConfig } from "./types";

export async function get() {
  return api("GET", "/api/config");
}

export async function update(flags: Record<string, string | boolean>) {
  const cfg: AppConfig = {};
  if (flags["username"]) cfg.ADMIN_USERNAME = flags["username"] as string;
  if (flags["password"]) cfg.ADMIN_PASSWORD = flags["password"] as string;
  if (flags["tg-bot-token"]) cfg.TG_BOT_TOKEN = flags["tg-bot-token"] as string;
  if (flags["tg-chat-id"]) cfg.TG_CHAT_ID = flags["tg-chat-id"] as string;
  if (flags["timezone"]) cfg.TIMEZONE = flags["timezone"] as string;
  if (flags["show-lunar"] !== undefined) cfg.SHOW_LUNAR = flags["show-lunar"] !== "false";
  if (flags["theme"]) cfg.THEME_MODE = flags["theme"] as string;
  if (flags["notifiers"]) cfg.ENABLED_NOTIFIERS = (flags["notifiers"] as string).split(",");
  if (flags["webhook-url"]) cfg.WEBHOOK_URL = flags["webhook-url"] as string;
  if (flags["webhook-method"]) cfg.WEBHOOK_METHOD = flags["webhook-method"] as string;
  if (flags["webhook-template"]) cfg.WEBHOOK_TEMPLATE = flags["webhook-template"] as string;
  if (flags["wechat-webhook"]) cfg.WECHATBOT_WEBHOOK = flags["wechat-webhook"] as string;
  if (flags["bark-key"]) cfg.BARK_DEVICE_KEY = flags["bark-key"] as string;
  if (flags["bark-server"]) cfg.BARK_SERVER = flags["bark-server"] as string;
  if (flags["gotify-url"]) cfg.GOTIFY_SERVER_URL = flags["gotify-url"] as string;
  if (flags["gotify-token"]) cfg.GOTIFY_APP_TOKEN = flags["gotify-token"] as string;
  if (flags["email-from"]) cfg.EMAIL_FROM = flags["email-from"] as string;
  if (flags["email-to"]) cfg.EMAIL_TO = flags["email-to"] as string;
  if (flags["resend-key"]) cfg.RESEND_API_KEY = flags["resend-key"] as string;
  if (flags["clear-secrets"]) cfg.CLEAR_SECRET_FIELDS = (flags["clear-secrets"] as string).split(",");
  if (flags["debug"] !== undefined) cfg.DEBUG_LOGS = flags["debug"] !== "false";
  if (flags["payment-history-limit"]) cfg.PAYMENT_HISTORY_LIMIT = Number(flags["payment-history-limit"]);
  return api("POST", "/api/config", cfg);
}
