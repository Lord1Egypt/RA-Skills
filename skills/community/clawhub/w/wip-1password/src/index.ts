import { readFileSync, existsSync } from "node:fs";
import {
  createClient,
  type Client,
  ItemCategory,
  ItemFieldType,
} from "@1password/sdk";

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

const PKG_VERSION = "0.1.0";
const DEFAULT_VAULT = "Agent Secrets";
const DEFAULT_TOKEN_PATH = `${process.env.HOME}/.openclaw/secrets/op-sa-token`;

// ── SDK client (lazy singleton) ─────────────────────────────────────

let _client: Client | null = null;
let _tokenPath: string = DEFAULT_TOKEN_PATH;

async function getClient(): Promise<Client> {
  if (_client) return _client;

  const path = process.env.OP_SA_TOKEN_PATH || _tokenPath;
  if (!existsSync(path)) {
    throw new Error(
      `1Password service account token not found at ${path}. ` +
        `See README for setup instructions.`,
    );
  }

  const token = readFileSync(path, "utf-8").trim();
  if (!token.startsWith("ops_")) {
    throw new Error(
      `Token at ${path} doesn't look like a 1Password service account token (expected "ops_" prefix).`,
    );
  }

  _client = await createClient({
    auth: token,
    integrationName: "OpenClaw",
    integrationVersion: PKG_VERSION,
  });
  return _client;
}

// ── high-level helpers ──────────────────────────────────────────────

async function resolveSecret(
  vault: string,
  item: string,
  field: string,
): Promise<string> {
  const client = await getClient();
  return await client.secrets.resolve(`op://${vault}/${item}/${field}`);
}

async function listVaults(): Promise<
  Array<{ id: string; title: string }>
> {
  const client = await getClient();
  return await client.vaults.list();
}

async function listItems(
  vaultId: string,
): Promise<Array<{ id: string; title: string; category: string }>> {
  const client = await getClient();
  return await client.items.list(vaultId);
}

function redact(value: string): string {
  if (value.length > 12) {
    return `${value.slice(0, 6)}...[${value.length - 10} chars]...${value.slice(-4)}`;
  }
  return "[short value]";
}

/** MCP-style tool result helper */
function toolResult(text: string, isError = false) {
  return {
    content: [{ type: "text" as const, text }],
    details: undefined as unknown,
    ...(isError ? { isError: true } : {}),
  };
}

// ── resolveSecretRefs ───────────────────────────────────────────────

const OP_REF_PATTERN = /^op:\/\/(.+)\/(.+)\/(.+)$/;

/**
 * Walk a config object and resolve any string values matching `op://vault/item/field`.
 * Returns a new object with secrets resolved. Non-matching values pass through unchanged.
 */
export async function resolveSecretRefs<T>(obj: T): Promise<T> {
  if (typeof obj === "string") {
    const match = obj.match(OP_REF_PATTERN);
    if (match) {
      return (await resolveSecret(match[1], match[2], match[3])) as unknown as T;
    }
    return obj;
  }
  if (Array.isArray(obj)) {
    return (await Promise.all(obj.map((v) => resolveSecretRefs(v)))) as unknown as T;
  }
  if (obj !== null && typeof obj === "object") {
    const result: Record<string, unknown> = {};
    for (const [key, value] of Object.entries(obj)) {
      result[key] = await resolveSecretRefs(value);
    }
    return result as T;
  }
  return obj;
}

// ── plugin ──────────────────────────────────────────────────────────

const opSecretsPlugin = {
  id: "op-secrets",
  name: "1Password Secrets",
  description:
    "Read secrets from 1Password via JS SDK (headless, no desktop app needed)",
  configSchema: {
    type: "object" as const,
    additionalProperties: false,
    properties: {
      defaultVault: { type: "string" as const },
      tokenPath: { type: "string" as const },
    },
  },

  register(api: OpenClawPluginApi) {
    const pluginConfig = (api.config as any)?.plugins?.entries?.[
      "1password"
    ]?.config;
    const defaultVault = pluginConfig?.defaultVault || DEFAULT_VAULT;
    _tokenPath = pluginConfig?.tokenPath || DEFAULT_TOKEN_PATH;

    // ── Agent tool: read a secret ───────────────────────────────────

    api.registerTool(
      {
        name: "op_read_secret",
        label: "Read 1Password Secret",
        description:
          "Read a secret from 1Password. Returns the secret value for the " +
          "specified vault/item/field. Fully headless via service account. " +
          "NEVER log or echo the returned value.",
        parameters: {
          type: "object",
          properties: {
            vault: {
              type: "string",
              description: `Vault name (default: "${defaultVault}")`,
            },
            item: {
              type: "string",
              description:
                "Item title in the vault (e.g. 'OpenAI API', 'Anthropic Auth Token')",
            },
            field: {
              type: "string",
              description: 'Field name to read (default: "api key")',
            },
          },
          required: ["item"],
        },
        async execute(
          _id: string,
          params: { vault?: string; item: string; field?: string },
        ) {
          const vault = params.vault || defaultVault;
          const field = params.field || "api key";
          try {
            const secret = await resolveSecret(vault, params.item, field);
            if (!secret) {
              return toolResult(
                `No value found for ${vault}/${params.item}/${field}`,
              );
            }
            return toolResult(secret);
          } catch (err: any) {
            return toolResult(`1Password error: ${err.message}`, true);
          }
        },
      } as any,
      { optional: true },
    );

    // ── Agent tool: list items ──────────────────────────────────────

    api.registerTool(
      {
        name: "op_list_items",
        label: "List 1Password Items",
        description:
          "List all items in a 1Password vault. Returns item titles and categories.",
        parameters: {
          type: "object",
          properties: {
            vault: {
              type: "string",
              description: `Vault name (default: "${defaultVault}")`,
            },
          },
        },
        async execute(_id: string, params: { vault?: string }) {
          const vaultName = params.vault || defaultVault;
          try {
            const vaults = await listVaults();
            const vault = vaults.find((v) => v.title === vaultName);
            if (!vault) {
              return toolResult(
                `Vault "${vaultName}" not found. Available: ${vaults.map((v) => v.title).join(", ")}`,
                true,
              );
            }
            const items = await listItems(vault.id);
            const summary = items
              .map((i) => `${i.title} (${i.category})`)
              .join("\n");
            return toolResult(summary || "No items found.");
          } catch (err: any) {
            return toolResult(`1Password error: ${err.message}`, true);
          }
        },
      } as any,
      { optional: true },
    );

    // ── Agent tool: create/update a secret ──────────────────────────

    api.registerTool(
      {
        name: "op_write_secret",
        label: "Write 1Password Secret",
        description:
          "Create or update a secret in 1Password. Use this to store new API keys " +
          "or credentials. The service account must have write access to the vault.",
        parameters: {
          type: "object",
          properties: {
            vault: {
              type: "string",
              description: `Vault name (default: "${defaultVault}")`,
            },
            item: {
              type: "string",
              description: "Item title (e.g. 'New API Key')",
            },
            field: {
              type: "string",
              description: 'Field name (default: "api key")',
            },
            value: {
              type: "string",
              description: "The secret value to store",
            },
            category: {
              type: "string",
              description:
                'Item category (default: "API Credential"). Only used when creating new items.',
            },
          },
          required: ["item", "value"],
        },
        async execute(
          _id: string,
          params: {
            vault?: string;
            item: string;
            field?: string;
            value: string;
            category?: string;
          },
        ) {
          const vaultName = params.vault || defaultVault;
          const field = params.field || "api key";
          try {
            const client = await getClient();
            const vaults = await listVaults();
            const vault = vaults.find((v) => v.title === vaultName);
            if (!vault) {
              return toolResult(`Vault "${vaultName}" not found.`, true);
            }

            // Check if item already exists
            const items = await listItems(vault.id);
            const existing = items.find(
              (i) => i.title.toLowerCase() === params.item.toLowerCase(),
            );

            if (existing) {
              // Update existing item — get it, update field, put it back
              const full = await client.items.get(vault.id, existing.id);
              let fieldFound = false;
              for (const f of full.fields) {
                if (f.title?.toLowerCase() === field.toLowerCase()) {
                  f.value = params.value;
                  fieldFound = true;
                  break;
                }
              }
              if (!fieldFound) {
                full.fields.push({
                  id: "",
                  title: field,
                  value: params.value,
                  fieldType: ItemFieldType.Concealed,
                });
              }
              await client.items.put(full);
              return toolResult(
                `Updated "${params.item}" in ${vaultName} (field: ${field})`,
              );
            } else {
              // Create new item
              await client.items.create({
                vaultId: vault.id,
                title: params.item,
                category: ItemCategory.ApiCredentials,
                fields: [
                  {
                    id: "",
                    title: field,
                    value: params.value,
                    fieldType: ItemFieldType.Concealed,
                  },
                ],
              });
              return toolResult(
                `Created "${params.item}" in ${vaultName} (field: ${field})`,
              );
            }
          } catch (err: any) {
            return toolResult(`1Password error: ${err.message}`, true);
          }
        },
      } as any,
      { optional: true },
    );

    // ── CLI commands ────────────────────────────────────────────────

    api.registerCli(
      ({ program }) => {
        const cmd = program
          .command("op-secrets")
          .description("1Password secrets plugin (SDK)");

        cmd
          .command("test")
          .description("Test 1Password connectivity")
          .action(async () => {
            try {
              console.log("Connecting via service account...");
              const vaults = await listVaults();
              console.log(
                `1Password connection OK — ${vaults.length} vault(s):`,
              );
              for (const v of vaults) {
                const items = await listItems(v.id);
                console.log(
                  `  - ${v.title} (${v.id}) — ${items.length} item(s)`,
                );
                for (const i of items) {
                  console.log(`      ${i.title} (${i.category})`);
                }
              }
            } catch (err: any) {
              console.error("1Password connection FAILED:", err.message);
              process.exit(1);
            }
          });

        cmd
          .command("read")
          .description("Read a secret (redacted preview)")
          .argument("<item>", "Item title")
          .option("-v, --vault <vault>", "Vault name", defaultVault)
          .option("-f, --field <field>", "Field name", "api key")
          .action(
            async (item: string, opts: { vault: string; field: string }) => {
              try {
                const value = await resolveSecret(
                  opts.vault,
                  item,
                  opts.field,
                );
                console.log(
                  `${opts.vault}/${item}/${opts.field}: ${redact(value)}`,
                );
              } catch (err: any) {
                console.error("Read failed:", err.message);
                process.exit(1);
              }
            },
          );

        cmd
          .command("resolve")
          .description("Resolve op:// references in a JSON file (dry run)")
          .argument("<file>", "Path to JSON file")
          .action(async (file: string) => {
            try {
              const raw = readFileSync(file, "utf-8");
              const obj = JSON.parse(raw);
              const resolved = await resolveSecretRefs(obj);
              // Show which keys were resolved (redacted values)
              const diff = findResolvedKeys(obj, resolved);
              if (diff.length === 0) {
                console.log("No op:// references found.");
              } else {
                console.log(`Resolved ${diff.length} secret reference(s):`);
                for (const d of diff) {
                  console.log(`  ${d.path}: ${redact(d.value)}`);
                }
              }
            } catch (err: any) {
              console.error("Resolve failed:", err.message);
              process.exit(1);
            }
          });
      },
      { commands: ["op-secrets"] },
    );

    // ── Service: resolve op:// references at startup ──────────────
    // Config mutation via Object.assign doesn't reliably propagate to all
    // subsystems (memory search reads a separate config snapshot). Instead,
    // resolve known secrets and set them as environment variables, which are
    // globally visible.

    api.registerService?.({
      id: "op-secret-resolver",
      async start(ctx: any) {
        try {
          // Resolve op:// refs in config and mutate in-place (best effort)
          const resolved = await resolveSecretRefs(ctx.config);
          Object.assign(ctx.config, resolved);

          // Resolve OpenAI key directly from 1Password and set as env var.
          // Memory search uses resolveApiKeyForProvider() which checks
          // process.env.OPENAI_API_KEY as a fallback — so we set it here.
          // The config should NOT have remote.apiKey set, because if it does,
          // memory search uses it directly (skipping the env var fallback).
          if (!process.env.OPENAI_API_KEY) {
            try {
              const key = await resolveSecret(defaultVault, "OpenAI API", "api key");
              if (key) {
                process.env.OPENAI_API_KEY = key;
                ctx.logger.info("1password: set OPENAI_API_KEY from 1Password");
              }
            } catch (err: any) {
              ctx.logger.warn(`1password: failed to resolve OpenAI key: ${err.message}`);
            }
          }

          ctx.logger.info("1password: op:// secret references resolved");
        } catch (err: any) {
          ctx.logger.warn(
            `1password: failed to resolve secret references: ${err.message}`
          );
        }
      },
    });

    api.logger.info(
      `1password plugin registered (vault: ${defaultVault}, SDK mode)`,
    );
  },
};

/** Compare original vs resolved config to find which keys changed */
function findResolvedKeys(
  original: any,
  resolved: any,
  path = "",
): Array<{ path: string; value: string }> {
  const results: Array<{ path: string; value: string }> = [];
  if (typeof original === "string" && OP_REF_PATTERN.test(original)) {
    results.push({ path: path || "(root)", value: resolved });
  } else if (original !== null && typeof original === "object") {
    for (const key of Object.keys(original)) {
      results.push(
        ...findResolvedKeys(
          original[key],
          resolved[key],
          path ? `${path}.${key}` : key,
        ),
      );
    }
  }
  return results;
}

export default opSecretsPlugin;
