// Notification test command
import { api } from "./client";
import type { TestNotificationInput } from "./types";

export async function test(flags: Record<string, string | boolean>) {
  if (!flags["type"]) throw new Error("Required: --type (telegram|notifyx|webhook|wechatbot|email|bark|gotify)");

  const input: TestNotificationInput = {
    type: flags["type"] as TestNotificationInput["type"],
  };

  // pass through config overrides (e.g. --tg-bot-token → TG_BOT_TOKEN)
  for (const [k, v] of Object.entries(flags)) {
    if (k !== "type") {
      const configKey = k
        .split("-")
        .map((s) => s.toUpperCase())
        .join("_");
      (input as Record<string, unknown>)[configKey] = v;
    }
  }

  return api("POST", "/api/test-notification", input);
}
