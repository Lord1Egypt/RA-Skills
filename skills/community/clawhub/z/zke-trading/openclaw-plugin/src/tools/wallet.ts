import { runMainJson } from "../python.js";
import type { PluginConfig, ToolSpec } from "../types.js";

export function createWalletTools(config?: PluginConfig): ToolSpec[] {
  return [
    {
      name: "zke_transfer_spot_to_futures",
      description: "Transfer assets from ZKE spot account to futures account",
      inputSchema: {
        type: "object",
        properties: {
          coin: { type: "string" },
          amount: { type: "string" },
        },
        required: ["coin", "amount"],
        additionalProperties: false,
      },
      execute: async ({ coin, amount }) => {
        return await runMainJson(
          ["transfer-spot-to-futures", String(coin), String(amount), "--json"],
          config
        );
      },
    },
    {
      name: "zke_transfer_futures_to_spot",
      description: "Transfer assets from ZKE futures account to spot account",
      inputSchema: {
        type: "object",
        properties: {
          coin: { type: "string" },
          amount: { type: "string" },
        },
        required: ["coin", "amount"],
        additionalProperties: false,
      },
      execute: async ({ coin, amount }) => {
        return await runMainJson(
          ["transfer-futures-to-spot", String(coin), String(amount), "--json"],
          config
        );
      },
    },
    {
      name: "zke_get_transfer_history",
      description: "Get ZKE transfer history between spot and futures",
      inputSchema: {
        type: "object",
        properties: {
          coin: { type: "string", default: "" },
          from_account: { type: "string", default: "" },
          to_account: { type: "string", default: "" },
          limit: { type: "integer", default: 20 },
        },
        additionalProperties: false,
      },
      execute: async ({ coin = "", from_account = "", to_account = "", limit = 20 }) => {
        const args = ["transfer-history"];
        if (String(coin).trim()) args.push(String(coin));
        if (String(from_account).trim()) args.push(String(from_account));
        if (String(to_account).trim()) args.push(String(to_account));
        args.push(String(limit));
        args.push("--json");
        return await runMainJson(args, config);
      },
    },
    {
      name: "zke_get_withdraw_history",
      description: "Get ZKE withdraw history",
      inputSchema: {
        type: "object",
        properties: {
          coin: { type: "string", default: "" },
          limit: { type: "integer", default: 20 },
        },
        additionalProperties: false,
      },
      execute: async ({ coin = "", limit = 20 }) => {
        if (coin) {
          return await runMainJson(["withdraw-history", String(coin), String(limit), "--json"], config);
        }
        return await runMainJson(["withdraw-history", "--json"], config);
      },
    },
    {
      name: "zke_create_withdraw",
      description: "Create a ZKE withdrawal request",
      inputSchema: {
        type: "object",
        properties: {
          coin: { type: "string", description: "e.g. USDTBSC or asset symbol used by your local CLI" },
          address: { type: "string" },
          amount: { type: "string" },
          memo: { type: "string" },
        },
        required: ["coin", "address", "amount"],
        additionalProperties: false,
      },
      execute: async ({ coin, address, amount, memo = "" }) => {
        const args = ["withdraw", String(coin), String(address), String(amount)];
        if (String(memo).trim()) {
          args.push(String(memo));
        }
        args.push("--json");
        return await runMainJson(args, config);
      },
    },
  ];
}
