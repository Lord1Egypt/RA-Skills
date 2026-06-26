// Payment commands
import { api } from "./client";
import type { EditPaymentInput } from "./types";

export async function list(subId: string) {
  return api("GET", `/api/subscriptions/${subId}/payments`);
}

export async function edit(subId: string, paymentId: string, flags: Record<string, string | boolean>) {
  const input: EditPaymentInput = {};
  if (flags["date"]) input.date = flags["date"] as string;
  if (flags["amount"]) input.amount = Number(flags["amount"]);
  if (flags["note"]) input.note = flags["note"] as string;
  return api("PUT", `/api/subscriptions/${subId}/payments/${paymentId}`, input);
}

export async function del(subId: string, paymentId: string) {
  return api("DELETE", `/api/subscriptions/${subId}/payments/${paymentId}`);
}
