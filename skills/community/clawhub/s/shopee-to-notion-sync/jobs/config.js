console.log("=== USANDO SCRIPT NODE SHOPEE->NOTION ===");

require("dotenv").config({ path: "/data/.openclaw/workspace-sales/.env" });

const targets = {
  shopee_produtos: process.env.NOTION_DATABASE_ID
};

function getRequiredEnv(name) {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Variável de ambiente obrigatória não definida: ${name}`);
  }
  return value;
}

function getTargetDatabaseId(targetName) {
  const databaseId = targets[targetName];
  if (!databaseId) {
    throw new Error(`Target do Notion não encontrado: ${targetName}`);
  }
  return databaseId;
}

module.exports = {
  shopeeAppId: getRequiredEnv("SHOPEE_APP_ID"),
  shopeeSecret: getRequiredEnv("SHOPEE_SECRET"),
  notionToken: getRequiredEnv("NOTION_TOKEN"),
  notionVersion: "2022-06-28",
  getTargetDatabaseId,
  targets,
};