import { runMainJson } from "../python.js";
import type { PluginConfig, ToolSpec } from "../types.js";

export function createFuturesTools(config?: PluginConfig): ToolSpec[] {
  return [
    {
      name: "zke_get_futures_ticker",
      description: "Get ZKE futures ticker, e.g. E-BTC-USDT",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
        },
        required: ["symbol"],
        additionalProperties: false,
      },
      execute: async ({ symbol }) => {
        return await runMainJson(["futures-ticker", String(symbol), "--json"], config);
      },
    },
    {
      name: "zke_get_futures_index",
      description: "Get ZKE futures mark/index price",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
        },
        required: ["symbol"],
        additionalProperties: false,
      },
      execute: async ({ symbol }) => {
        return await runMainJson(["futures-index", String(symbol), "--json"], config);
      },
    },
    {
      name: "zke_get_futures_balance",
      description: "Get ZKE futures account balance for a margin coin",
      inputSchema: {
        type: "object",
        properties: {
          margin_coin: { type: "string", default: "USDT" },
        },
        additionalProperties: false,
      },
      execute: async ({ margin_coin = "USDT" }) => {
        return await runMainJson(["futures-balance", String(margin_coin), "--json"], config);
      },
    },
    {
      name: "zke_get_futures_positions",
      description: "Get current ZKE futures positions",
      inputSchema: {
        type: "object",
        properties: {},
        additionalProperties: false,
      },
      execute: async () => {
        return await runMainJson(["futures-positions", "--json"], config);
      },
    },
    {
      name: "zke_get_futures_order",
      description: "Query a ZKE futures order by order id",
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
        return await runMainJson(["futures-order", String(symbol), String(order_id), "--json"], config);
      },
    },
    {
      name: "zke_get_futures_open_orders",
      description: "Get current ZKE futures open orders",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
        },
        required: ["symbol"],
        additionalProperties: false,
      },
      execute: async ({ symbol }) => {
        return await runMainJson(["futures-open-orders", String(symbol), "--json"], config);
      },
    },
    {
      name: "zke_get_futures_my_trades",
      description: "Get recent ZKE futures trades",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
          limit: { type: "integer", default: 10 },
        },
        required: ["symbol"],
        additionalProperties: false,
      },
      execute: async ({ symbol, limit = 10 }) => {
        return await runMainJson(["futures-my-trades", String(symbol), String(limit), "--json"], config);
      },
    },
    {
      name: "zke_get_futures_order_history",
      description: "Get ZKE futures historical orders",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
          limit: { type: "integer", default: 10 },
        },
        required: ["symbol"],
        additionalProperties: false,
      },
      execute: async ({ symbol, limit = 10 }) => {
        return await runMainJson(["futures-order-historical", String(symbol), String(limit), "--json"], config);
      },
    },
    {
      name: "zke_get_futures_profit_history",
      description: "Get ZKE futures profit history",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
          limit: { type: "integer", default: 10 },
        },
        required: ["symbol"],
        additionalProperties: false,
      },
      execute: async ({ symbol, limit = 10 }) => {
        return await runMainJson(["futures-profit-historical", String(symbol), String(limit), "--json"], config);
      },
    },
    {
      name: "zke_create_futures_order",
      description: "Create a ZKE futures order",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
          side: { type: "string", enum: ["BUY", "SELL"] },
          open_action: { type: "string", enum: ["OPEN", "CLOSE"] },
          position_type: {
            type: "integer",
            enum: [1, 2],
            description: "1 = cross, 2 = isolated",
          },
          order_type: { type: "string", enum: ["LIMIT", "MARKET"] },
          volume: { type: "string" },
          price: { type: "string" },
        },
        required: [
          "symbol",
          "side",
          "open_action",
          "position_type",
          "order_type",
          "volume",
        ],
        additionalProperties: false,
      },
      execute: async ({
        symbol,
        side,
        open_action,
        position_type,
        order_type,
        volume,
        price = "",
      }) => {
        const args = [
          "futures-create-order",
          String(symbol),
          String(side),
          String(open_action),
          String(position_type),
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
      name: "zke_create_futures_condition_order",
      description: "Create a ZKE futures conditional order",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
          side: { type: "string", enum: ["BUY", "SELL"] },
          open_action: { type: "string", enum: ["OPEN", "CLOSE"] },
          position_type: { type: "integer", enum: [1, 2] },
          order_type: { type: "string", enum: ["LIMIT", "MARKET"] },
          volume: { type: "string" },
          trigger_type: { type: "string" },
          trigger_price: { type: "string" },
          price: { type: "string" },
        },
        required: [
          "symbol",
          "side",
          "open_action",
          "position_type",
          "order_type",
          "volume",
          "trigger_type",
          "trigger_price",
        ],
        additionalProperties: false,
      },
      execute: async ({
        symbol,
        side,
        open_action,
        position_type,
        order_type,
        volume,
        trigger_type,
        trigger_price,
        price = "",
      }) => {
        const args = [
          "futures-condition-order",
          String(symbol),
          String(side),
          String(open_action),
          String(position_type),
          String(order_type),
          String(volume),
          String(trigger_type),
          String(trigger_price),
        ];
        if (String(price).trim()) {
          args.push(String(price));
        }
        args.push("--json");
        return await runMainJson(args, config);
      },
    },
    {
      name: "zke_cancel_futures_order",
      description: "Cancel a ZKE futures order by order id",
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
        return await runMainJson(["futures-cancel-order", String(symbol), String(order_id), "--json"], config);
      },
    },
    {
      name: "zke_cancel_all_futures_orders",
      description: "Cancel all ZKE futures open orders, optionally for one symbol",
      inputSchema: {
        type: "object",
        properties: {
          symbol: { type: "string" },
        },
        additionalProperties: false,
      },
      execute: async ({ symbol = "" }) => {
        if (String(symbol).trim()) {
          return await runMainJson(["futures-cancel-all-orders", String(symbol), "--json"], config);
        }
        return await runMainJson(["futures-cancel-all-orders", "--json"], config);
      },
    },
  ];
}
