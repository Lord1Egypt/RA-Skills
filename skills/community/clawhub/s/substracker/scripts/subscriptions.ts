// Subscription commands
import { api } from "./client";
import type { CreateSubscriptionInput, RenewOptions } from "./types";

export function flagsToSubscription(flags: Record<string, string | boolean>): CreateSubscriptionInput {
  const sub: CreateSubscriptionInput = {
    name: flags["name"] as string,
    expiryDate: (flags["expiry-date"] || flags["expiryDate"]) as string,
  };
  if (flags["period-value"]) sub.periodValue = Number(flags["period-value"]);
  if (flags["period-unit"]) sub.periodUnit = flags["period-unit"] as "day" | "month" | "year";
  if (flags["amount"]) sub.amount = Number(flags["amount"]);
  if (flags["currency"]) sub.currency = flags["currency"] as string;
  if (flags["auto-renew"] !== undefined) sub.autoRenew = flags["auto-renew"] !== "false";
  if (flags["reminder-unit"]) sub.reminderUnit = flags["reminder-unit"] as "day" | "hour";
  if (flags["reminder-value"]) sub.reminderValue = Number(flags["reminder-value"]);
  if (flags["reminder-days"]) sub.reminderDays = Number(flags["reminder-days"]);
  if (flags["active"] !== undefined) sub.isActive = flags["active"] !== "false";
  if (flags["notes"]) sub.notes = flags["notes"] as string;
  if (flags["category"]) sub.category = flags["category"] as string;
  if (flags["custom-type"]) sub.customType = flags["custom-type"] as string;
  if (flags["mode"]) sub.subscriptionMode = flags["mode"] as "cycle" | "reset";
  if (flags["start-date"]) sub.startDate = flags["start-date"] as string;
  if (flags["lunar"]) sub.useLunar = flags["lunar"] !== "false";
  return sub;
}

export async function list() {
  return api("GET", "/api/subscriptions");
}

export async function get(id: string) {
  return api("GET", `/api/subscriptions/${id}`);
}

export async function create(flags: Record<string, string | boolean>) {
  const input = flagsToSubscription(flags);
  if (!input.name || !input.expiryDate) throw new Error("Required: --name and --expiry-date");
  return api("POST", "/api/subscriptions", input);
}

export async function update(id: string, flags: Record<string, string | boolean>) {
  // GET current → merge flags → PUT (partial update support)
  const current = await api<{ subscription: Record<string, unknown> }>("GET", `/api/subscriptions/${id}`);
  const existing = current.subscription;
  const patch = flagsToSubscription(flags);

  const merged: Record<string, unknown> = { ...existing };
  for (const [k, v] of Object.entries(patch)) {
    if (v !== undefined) merged[k] = v;
  }
  return api("PUT", `/api/subscriptions/${id}`, merged);
}

export async function del(id: string) {
  return api("DELETE", `/api/subscriptions/${id}`);
}

export async function toggle(id: string, flags: Record<string, string | boolean>) {
  const isActive = flags["active"] !== "false";
  return api("POST", `/api/subscriptions/${id}/toggle-status`, { isActive });
}

export async function renew(id: string, flags: Record<string, string | boolean>) {
  const opts: RenewOptions = {};
  if (flags["amount"]) opts.amount = Number(flags["amount"]);
  if (flags["period-multiplier"]) opts.periodMultiplier = Number(flags["period-multiplier"]);
  if (flags["payment-date"]) opts.paymentDate = flags["payment-date"] as string;
  if (flags["note"]) opts.note = flags["note"] as string;
  return api("POST", `/api/subscriptions/${id}/renew`, opts);
}

export async function testNotify(id: string) {
  return api("POST", `/api/subscriptions/${id}/test-notify`);
}
