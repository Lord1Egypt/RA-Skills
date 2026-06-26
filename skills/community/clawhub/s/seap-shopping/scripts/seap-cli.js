"use strict";
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));

// src/seap-cli.ts
var import_commander = require("commander");
var fs = __toESM(require("fs"));
var mockGoodsData = [
  {
    skuId: "SKU001",
    name: "\u3010\u83AB\u585E\u5C14\u3011\u667A\u5229\u539F\u74F6\u8FDB\u53E3\u706B\u5C71\u8461\u8404\u9152",
    price: 208,
    description: "\u7EAF\u51C0\u98CE\u5473",
    imageUrl: "https://example.com/iphone13.jpg",
    rating: 4.8,
    storeName: "\u83AB\u585E\u5C14"
  },
  {
    skuId: "SKU002",
    name: "\u3010\u83AB\u585E\u5C14\u3011\u6CD5\u56FD\u5409\u54C8\u4F2F\u901A\u8461\u8404\u9152",
    price: 218,
    description: "\u5357\u6CD5\u9AD8\u539F\u4E0A\u7684\u73CD\u73E0",
    imageUrl: "https://example.com/s21.jpg",
    rating: 4.6,
    storeName: "\u83AB\u585E\u5C14"
  },
  {
    skuId: "SKU003",
    name: "\u3010\u83AB\u585E\u5C14\u3011\u6CD5\u56FD\u767D\u9A6C\u5E84\u56ED\u7EA2\u8461\u8404\u9152",
    price: 10062,
    description: "1955\u5206\u7EA7\u5236",
    imageUrl: "https://example.com/macbookair.jpg",
    rating: 4.9,
    storeName: "\u83AB\u585E\u5C14"
  }
];
var mockBuyResponse = {
  success: true,
  orderId: "ORDER" + Math.floor(Math.random() * 1e6),
  message: "Order placed successfully"
};
async function queryGoodsIntention(intent) {
  console.log(`Querying goods for intent: ${intent}`);
  const filteredGoods = mockGoodsData.filter(
    (good) => good.name.toLowerCase().includes(intent.toLowerCase()) || good.description.toLowerCase().includes(intent.toLowerCase())
  );
  return {
    success: true,
    data: filteredGoods.length > 0 ? filteredGoods : mockGoodsData.slice(0, 2),
    message: filteredGoods.length > 0 ? "Found matching goods" : "Using default goods for demo"
  };
}
async function scheduleBuyIntention(skuId) {
  console.log(`Scheduling purchase for SKU: ${skuId}`);
  const validSku = mockGoodsData.some((item) => item.skuId === skuId);
  if (!validSku) {
    return {
      success: false,
      orderId: "",
      message: `Invalid SKU: ${skuId}`
    };
  }
  return mockBuyResponse;
}
function goodsToMarkdown(goods) {
  let md = "# \u5546\u54C1\u641C\u7D22\u7ED3\u679C\n\n";
  for (const item of goods) {
    md += `## ${item.name}
`;
    md += `- **SKU**: ${item.skuId}
`;
    md += `- **\u4EF7\u683C**: \xA5${item.price}
`;
    md += `- **\u63CF\u8FF0**: ${item.description}
`;
    if (item.rating) {
      md += `- **\u8BC4\u5206**: ${item.rating}/5.0
`;
    }
    if (item.storeName) {
      md += `- **\u5E97\u94FA**: ${item.storeName}
`;
    }
    if (item.imageUrl) {
      md += `- **\u56FE\u7247**: ![${item.name}](${item.imageUrl})
`;
    }
    md += "\n";
  }
  return md;
}
var program = new import_commander.Command();
program.name("seap-cli").description("SEAP CLI for OpenClaw skills").version("1.0.0");
program.command("search").description("Search for goods").requiredOption("--sessionId <sessionId>", "Session ID").requiredOption("--intent <intent>", "Search intent").option("--format <format>", "Output format", "md").action(async (options) => {
  try {
    console.log(`Searching with sessionId: ${options.sessionId}, intent: ${options.intent}`);
    const response = await queryGoodsIntention(options.intent);
    if (options.format === "md") {
      const markdownOutput = goodsToMarkdown(response.data);
      console.log(markdownOutput);
    } else {
      console.log(JSON.stringify(response.data, null, 2));
    }
    const outputPath = `${options.sessionId}.json`;
    fs.writeFileSync(outputPath, JSON.stringify(response, null, 2));
    console.log(`Search results saved to ${outputPath}`);
  } catch (error) {
    console.error("Error during search:", error);
    process.exit(1);
  }
});
program.command("aipay").description("Complete purchase for a product").requiredOption("--sessionId <sessionId>", "Session ID").requiredOption("--skuId <skuId>", "SKU ID to purchase").action(async (options) => {
  try {
    console.log(`Processing purchase with sessionId: ${options.sessionId}, skuId: ${options.skuId}`);
    const response = await scheduleBuyIntention(options.skuId);
    console.log(JSON.stringify(response, null, 2));
    const outputPath = `${options.sessionId}.json`;
    fs.writeFileSync(outputPath, JSON.stringify(response, null, 2));
    console.log(`Purchase result saved to ${outputPath}`);
  } catch (error) {
    console.error("Error during purchase:", error);
    process.exit(1);
  }
});
program.parse();
