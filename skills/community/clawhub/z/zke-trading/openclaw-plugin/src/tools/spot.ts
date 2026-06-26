import { runMainJson } from "../python.js";
import type { PluginConfig, ToolSpec } from "../types.js";

export function createSpotTools(config?: PluginConfig): ToolSpec[] {
  return [
    {
      name: "zke_get_spot_ticker",
      description: "Get ZKE spot ticker for a symbol, e.g. BTCUSDT",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
        },
        required: ["symbol"],
        additionalProperties: false,
      },
      execute: async ({ symbol }) => {
        return await runMainJson(["ticker", String(symbol), "--json"], config);
      },
    },
    {
      name: "zke_get_spot_depth",
      description: "Get ZKE spot order book depth",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
          limit: { type: "integer", default: 20 },
        },
        required: ["symbol"],
        additionalProperties: false,
      },
      execute: async ({ symbol, limit = 20 }) => {
        return await runMainJson(["depth", String(symbol), String(limit), "--json"], config);
      },
    },
    {
      name: "zke_get_spot_klines",
      description: "Get ZKE spot kline data",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
          interval: { type: "string", default: "1day" },
        },
        required: ["symbol"],
        additionalProperties: false,
      },
      execute: async ({ symbol, interval = "1day" }) => {
        return await runMainJson(["klines", String(symbol), String(interval), "--json"], config);
      },
    },
    {
      name: "zke_get_spot_account",
      description: "Get raw ZKE spot account data",
      inputSchema: {
        type: "object",
        properties: {},
        additionalProperties: false,
      },
      execute: async () => {
        return await runMainJson(["account", "--json"], config);
      },
    },
    {
      name: "zke_get_spot_nonzero_balances",
      description: "Get non-zero ZKE spot balances",
      inputSchema: {
        type: "object",
        properties: {},
        additionalProperties: false,
      },
      execute: async () => {
        return await runMainJson(["account-nonzero", "--json"], config);
      },
    },
    {
      name: "zke_get_spot_balance",
      description: "Get ZKE spot balance summary for one asset, e.g. USDT",
      inputSchema: {
        type: "object",
        properties: {
          asset: { type: "string" },
        },
        required: ["asset"],
        additionalProperties: false,
      },
      execute: async ({ asset }) => {
        return await runMainJson(["balance", String(asset), "--json"], config);
      },
    },
    {
      name: "zke_get_spot_account_by_type",
      description: "Get ZKE spot account assets by account type",
      inputSchema: {
        type: "object",
        properties: {
          account_type: { type: "string", description: "1=spot, 2=isolated, 3=cross, 4=otc, 5=contract" },
        },
        required: ["account_type"],
        additionalProperties: false,
      },
      execute: async ({ account_type }) => {
        return await runMainJson(["account-by-type", String(account_type), "--json"], config);
      },
    },
    {
      name: "zke_get_spot_open_orders",
      description: "Get current ZKE spot open orders for a symbol",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
          limit: { type: "integer", default: 20 },
        },
        required: ["symbol"],
        additionalProperties: false,
      },
      execute: async ({ symbol, limit = 20 }) => {
        return await runMainJson(["open-orders", String(symbol), String(limit), "--json"], config);
      },
    },
    {
      name: "zke_get_spot_my_trades",
      description: "Get recent ZKE spot trades for a symbol",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
          limit: { type: "integer", default: 20 },
        },
        required: ["symbol"],
        additionalProperties: false,
      },
      execute: async ({ symbol, limit = 20 }) => {
        return await runMainJson(["my-trades", String(symbol), String(limit), "--json"], config);
      },
    },
    {
      name: "zke_get_spot_my_trades_v3",
      description: "Get ZKE spot trade history via v3 endpoint",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
          limit: { type: "integer", default: 50 },
        },
        required: ["symbol"],
        additionalProperties: false,
      },
      execute: async ({ symbol, limit = 50 }) => {
        return await runMainJson(["my-trades-v3", String(symbol), String(limit), "--json"], config);
      },
    },
    {
      name: "zke_get_spot_history_orders",
      description: "Get ZKE spot historical orders",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
          limit: { type: "integer", default: 50 },
        },
        required: ["symbol"],
        additionalProperties: false,
      },
      execute: async ({ symbol, limit = 50 }) => {
        return await runMainJson(["history-orders", String(symbol), String(limit), "--json"], config);
      },
    },
    {
      name: "zke_create_spot_order",
      description: "Create a ZKE spot order",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
          side: { type: "string", enum: ["BUY", "SELL"] },
          order_type: { type: "string", enum: ["LIMIT", "MARKET"] },
          volume: { type: "string" },
          price: { type: "string" },
        },
        required: ["symbol", "side", "order_type", "volume"],
        additionalProperties: false,
      },
      execute: async ({ symbol, side, order_type, volume, price = "" }) => {
        const args = [
          "create-order",
          String(symbol),
          String(side),
          String(order_type),
          String(volume),
        ];
        if (String(order_type).toUpperCase() === "LIMIT") {
          args.push(String(price));
        }
        args.push("--json");
        return await runMainJson(args, config);
      },
    },
    {
      name: "zke_cancel_spot_order",
      description: "Cancel a ZKE spot order by order id",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
          order_id: { type: "string" },
        },
        required: ["symbol", "order_id"],
        additionalProperties: false,
      },
      execute: async ({ symbol, order_id }) => {
        return await runMainJson(["cancel-order", String(symbol), String(order_id), "--json"], config);
      },
    },
  ];
}
