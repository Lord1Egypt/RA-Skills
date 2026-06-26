import { CliError, ExitCode } from "./config.ts";

export type CommandName = "lookup" | "now" | "forecast" | "indices";

interface CommandFlagMap {
  lookup: {
    location: string;
    adm?: string;
    range?: string;
  };
  now: {
    location: string;
    lang: string;
    unit: string;
  };
  forecast: {
    location: string;
    days: string;
    lang: string;
    unit: string;
  };
  indices: {
    location: string;
    type: string;
  };
}

export type ValidatedFlags<K extends CommandName> = CommandFlagMap[K];

export interface CommandHelp {
  usage: string;
  description: string;
}

export const COMMAND_HELP_MAP: Record<CommandName, CommandHelp> = {
  lookup: {
    usage: "lookup --location <name|lon,lat> [--adm <text>] [--range <country>]",
    description: "Search for a city and get its LocationID.",
  },
  now: {
    usage: "now --location <LocationID|lon,lat> [--lang <zh|en>] [--unit <m|i>]",
    description: "Get real-time weather for a location.",
  },
  forecast: {
    usage: "forecast --location <LocationID|lon,lat> [--days <3|7>] [--lang <zh|en>] [--unit <m|i>]",
    description: "Get daily weather forecast (3 or 7 days).",
  },
  indices: {
    usage: "indices --location <LocationID|lon,lat> [--type <0|1,2,3...>]",
    description: "Get life index forecast (clothing, UV, car wash, etc.).",
  },
};

export const COMMAND_ORDER: CommandName[] = ["lookup", "now", "forecast", "indices"];

const COMMAND_NAME_SET = new Set<string>(COMMAND_ORDER);

const ALLOWED_FLAG_NAMES: Record<CommandName, readonly string[]> = {
  lookup: ["location", "adm", "range"],
  now: ["location", "lang", "unit"],
  forecast: ["location", "days", "lang", "unit"],
  indices: ["location", "type"],
};

function throwInvalidFlags(command: CommandName, message: string): never {
  throw new CliError(`Invalid flags for ${command}: ${message}`, ExitCode.PARAM_OR_CONFIG);
}

function ensureNoUnknownFlags(command: CommandName, rawFlags: Record<string, string>): void {
  const allowed = new Set(ALLOWED_FLAG_NAMES[command]);
  const unknownFlags: string[] = [];

  for (const key of Object.keys(rawFlags)) {
    if (!allowed.has(key)) {
      unknownFlags.push(`--${key}`);
    }
  }

  if (unknownFlags.length > 0) {
    throwInvalidFlags(command, `unknown flags: ${unknownFlags.join(", ")}`);
  }
}

function normalizeOptionalString(command: CommandName, rawFlags: Record<string, string>, key: string): string | undefined {
  const value = rawFlags[key];
  if (value === undefined) {
    return undefined;
  }

  const normalized = value.trim();
  if (normalized.length === 0) {
    throwInvalidFlags(command, `${key}: must be a non-empty string`);
  }

  return normalized;
}

function normalizeRequiredString(command: CommandName, rawFlags: Record<string, string>, key: string): string {
  const normalized = normalizeOptionalString(command, rawFlags, key);
  if (!normalized) {
    throwInvalidFlags(command, `${key}: is required`);
  }
  return normalized;
}

export function isCommandName(value: string): value is CommandName {
  return COMMAND_NAME_SET.has(value);
}

export function validateCommandFlags<K extends CommandName>(
  command: K,
  rawFlags: Record<string, string>,
): ValidatedFlags<K> {
  ensureNoUnknownFlags(command, rawFlags);

  switch (command) {
    case "lookup": {
      const location = normalizeRequiredString(command, rawFlags, "location");
      const adm = normalizeOptionalString(command, rawFlags, "adm");
      const range = normalizeOptionalString(command, rawFlags, "range");
      return { location, adm, range } as ValidatedFlags<K>;
    }
    case "now": {
      const location = normalizeRequiredString(command, rawFlags, "location");
      const lang = normalizeOptionalString(command, rawFlags, "lang") ?? "zh";
      const unit = normalizeOptionalString(command, rawFlags, "unit") ?? "m";
      if (unit !== "m" && unit !== "i") {
        throwInvalidFlags(command, `unit: must be "m" (metric) or "i" (imperial)`);
      }
      return { location, lang, unit } as ValidatedFlags<K>;
    }
    case "forecast": {
      const location = normalizeRequiredString(command, rawFlags, "location");
      const days = normalizeOptionalString(command, rawFlags, "days") ?? "3";
      if (days !== "3" && days !== "7") {
        throwInvalidFlags(command, `days: must be 3 or 7`);
      }
      const lang = normalizeOptionalString(command, rawFlags, "lang") ?? "zh";
      const unit = normalizeOptionalString(command, rawFlags, "unit") ?? "m";
      if (unit !== "m" && unit !== "i") {
        throwInvalidFlags(command, `unit: must be "m" (metric) or "i" (imperial)`);
      }
      return { location, days, lang, unit } as ValidatedFlags<K>;
    }
    case "indices": {
      const location = normalizeRequiredString(command, rawFlags, "location");
      const type = normalizeOptionalString(command, rawFlags, "type") ?? "0";
      return { location, type } as ValidatedFlags<K>;
    }
    default: {
      const unhandled: never = command;
      throwInvalidFlags(command, `unsupported command: ${String(unhandled)}`);
    }
  }
}
