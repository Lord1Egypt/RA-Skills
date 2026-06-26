import * as fs from "fs";
import * as path from "path";

const CONFIG_DIR = path.join(process.env.HOME || process.env.USERPROFILE || ".", ".config", "ticktick-skill");
const CONFIG_PATH = path.join(CONFIG_DIR, "config.json");

interface Config {
  "default.project"?: string;
  "default.due"?: "none" | "today" | "tomorrow";
  "display.colors"?: boolean;
  "display.timezone"?: string;
  [key: string]: any;
}

const defaultConfig: Config = {
  "default.project": undefined,
  "default.due": "none",
  "display.colors": true,
  "display.timezone": "UTC",
};

function ensureConfigDir() {
  if (!fs.existsSync(CONFIG_DIR)) {
    fs.mkdirSync(CONFIG_DIR, { recursive: true });
  }
}

export function loadConfig(): Config {
  ensureConfigDir();
  if (!fs.existsSync(CONFIG_PATH)) {
    return { ...defaultConfig };
  }
  try {
    const raw = fs.readFileSync(CONFIG_PATH, "utf-8");
    return { ...defaultConfig, ...JSON.parse(raw) };
  } catch (e) {
    console.error(`❌ Failed to load config: ${e}`);
    return { ...defaultConfig };
  }
}

function saveConfig(config: Config): void {
  ensureConfigDir();
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2));
}

export async function configCommand(action: "get" | "set" | "list", key?: string, value?: string): Promise<void> {
  const config = loadConfig();

  try {
    if (action === "list") {
      console.log("\nCurrent configuration:");
      console.log(`  Config file: ${CONFIG_PATH}\n`);
      for (const [k, v] of Object.entries(config)) {
        console.log(`  ${k}: ${v}`);
      }
      console.log();
      return;
    }

    if (action === "get") {
      if (!key) {
        console.error("❌ Usage: config get <key>");
        process.exit(1);
      }
      if (config[key as keyof Config] === undefined) {
        console.log(`${key}: <not set> (default: ${defaultConfig[key as keyof Config] ?? "none"})`);
      } else {
        console.log(`${key}: ${config[key as keyof Config]}`);
      }
      return;
    }

    if (action === "set") {
      if (!key || value === undefined) {
        console.error("❌ Usage: config set <key> <value>");
        process.exit(1);
      }
      if (!(key in defaultConfig)) {
        console.warn(`⚠️  Unknown config key: ${key}. Setting anyway, but it may not be used.`);
      }

      // Type coercion based on key
      let typedValue: any = value;
      if (key === "display.colors") {
        typedValue = value === "true" || value === "1" || value === "yes";
      } else if (key === "default.due") {
        if (!["none", "today", "tomorrow"].includes(value)) {
          console.error(`❌ Invalid value for ${key}. Use none, today, or tomorrow.`);
          process.exit(1);
        }
      }

      config[key as keyof Config] = typedValue;
      saveConfig(config);
      console.log(`✓ Configuration saved: ${key} = ${typedValue}`);
      return;
    }
  } catch (error) {
    console.error(`❌ Error: ${error instanceof Error ? error.message : String(error)}`);
    process.exit(1);
  }
}
