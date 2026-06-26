import { CliError, ExitCode } from "./config.ts";

export type CommandName = "convert" | "latest" | "history" | "series" | "currencies";

interface CommandFlagMap {
  convert: {
    from: string;
    to: string;
    amount?: string;
    date?: string;
  };
  latest: {
    from: string;
    to?: string;
  };
  history: {
    from: string;
    date: string;
    to?: string;
  };
  series: {
    from: string;
    start: string;
    end: string;
    to?: string;
  };
  currencies: Record<string, never>;
}

export type ValidatedFlags<K extends CommandName> = CommandFlagMap[K];

export interface CommandHelp {
  usage: string;
  description: string;
}

export const COMMAND_HELP_MAP: Record<CommandName, CommandHelp> = {
  convert: {
    usage: "convert --from <CODE> --to <CODE> [--amount <number>] [--date <YYYY-MM-DD>]",
    description: "Convert an amount between two currencies.",
  },
  latest: {
    usage: "latest --from <CODE> [--to <CODE,CODE,...>]",
    description: "Show latest exchange rates for a base currency.",
  },
  history: {
    usage: "history --from <CODE> --date <YYYY-MM-DD> [--to <CODE,CODE,...>]",
    description: "Show exchange rate on a specific date.",
  },
  series: {
    usage: "series --from <CODE> --start <YYYY-MM-DD> --end <YYYY-MM-DD> [--to <CODE,CODE,...>]",
    description: "Show exchange rate trend over a date range.",
  },
  currencies: {
    usage: "currencies",
    description: "List all supported currency codes.",
  },
};

export const COMMAND_ORDER: CommandName[] = ["convert", "latest", "history", "series", "currencies"];

const COMMAND_NAME_SET = new Set<string>(COMMAND_ORDER);

const VALID_CURRENCIES = new Set([
  "AUD", "BRL", "CAD", "CHF", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD",
  "HUF", "IDR", "ILS", "INR", "ISK", "JPY", "KRW", "MXN", "MYR", "NOK",
  "NZD", "PHP", "PLN", "RON", "SEK", "SGD", "THB", "TRY", "USD", "ZAR",
]);

const ALLOWED_FLAG_NAMES: Record<CommandName, readonly string[]> = {
  convert: ["from", "to", "amount", "date"],
  latest: ["from", "to"],
  history: ["from", "date", "to"],
  series: ["from", "start", "end", "to"],
  currencies: [],
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

function validateCurrencyCode(command: CommandName, key: string, value: string): string {
  const upper = value.toUpperCase();
  if (!VALID_CURRENCIES.has(upper)) {
    throwInvalidFlags(command, `${key}: unknown currency code "${value}". Run 'currencies' to see all supported codes.`);
  }
  return upper;
}

function validateCurrencyCodes(command: CommandName, key: string, value: string): string {
  const codes = value.split(",").map((c) => c.trim());
  for (const code of codes) {
    validateCurrencyCode(command, key, code);
  }
  return codes.map((c) => c.toUpperCase()).join(",");
}

function validateDate(command: CommandName, key: string, value: string): string {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) {
    throwInvalidFlags(command, `${key}: must be in YYYY-MM-DD format`);
  }

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    throwInvalidFlags(command, `${key}: invalid date "${value}"`);
  }

  return value;
}

function validateAmount(command: CommandName, key: string, value: string): string {
  const num = Number(value);
  if (!Number.isFinite(num) || num <= 0) {
    throwInvalidFlags(command, `${key}: must be a positive number`);
  }
  return value;
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
    case "convert": {
      const from = validateCurrencyCode(command, "from", normalizeRequiredString(command, rawFlags, "from"));
      const to = validateCurrencyCode(command, "to", normalizeRequiredString(command, rawFlags, "to"));
      const amountRaw = normalizeOptionalString(command, rawFlags, "amount");
      const amount = amountRaw ? validateAmount(command, "amount", amountRaw) : undefined;
      const dateRaw = normalizeOptionalString(command, rawFlags, "date");
      const date = dateRaw ? validateDate(command, "date", dateRaw) : undefined;

      return { from, to, amount, date } as ValidatedFlags<K>;
    }
    case "latest": {
      const from = validateCurrencyCode(command, "from", normalizeRequiredString(command, rawFlags, "from"));
      const toRaw = normalizeOptionalString(command, rawFlags, "to");
      const to = toRaw ? validateCurrencyCodes(command, "to", toRaw) : undefined;

      return { from, to } as ValidatedFlags<K>;
    }
    case "history": {
      const from = validateCurrencyCode(command, "from", normalizeRequiredString(command, rawFlags, "from"));
      const date = validateDate(command, "date", normalizeRequiredString(command, rawFlags, "date"));
      const toRaw = normalizeOptionalString(command, rawFlags, "to");
      const to = toRaw ? validateCurrencyCodes(command, "to", toRaw) : undefined;

      return { from, date, to } as ValidatedFlags<K>;
    }
    case "series": {
      const from = validateCurrencyCode(command, "from", normalizeRequiredString(command, rawFlags, "from"));
      const start = validateDate(command, "start", normalizeRequiredString(command, rawFlags, "start"));
      const end = validateDate(command, "end", normalizeRequiredString(command, rawFlags, "end"));
      const toRaw = normalizeOptionalString(command, rawFlags, "to");
      const to = toRaw ? validateCurrencyCodes(command, "to", toRaw) : undefined;

      if (start > end) {
        throwInvalidFlags(command, `start date (${start}) must be before end date (${end})`);
      }

      return { from, start, end, to } as ValidatedFlags<K>;
    }
    case "currencies": {
      return {} as ValidatedFlags<K>;
    }
    default: {
      const unhandled: never = command;
      throwInvalidFlags(command, `unsupported command: ${String(unhandled)}`);
    }
  }
}
