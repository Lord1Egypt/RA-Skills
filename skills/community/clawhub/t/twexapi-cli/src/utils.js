export function exitWithError(message, details) {
  console.error(message);
  if (details) {
    console.error(details);
  }
  process.exit(1);
}

export function parseJson(label, value) {
  try {
    return JSON.parse(value);
  } catch (error) {
    exitWithError(`Invalid JSON for ${label}.`, error.message);
  }
}

export function parseHeader(value) {
  const separator = value.indexOf(":");
  if (separator === -1) {
    exitWithError(`Invalid header format: ${value}`, 'Expected "Name: Value".');
  }

  const name = value.slice(0, separator).trim();
  const headerValue = value.slice(separator + 1).trim();
  if (!name) {
    exitWithError(`Invalid header format: ${value}`, "Header name cannot be empty.");
  }

  return [name, headerValue];
}

export function findOption(args, name) {
  const index = args.indexOf(name);
  if (index === -1) {
    return "";
  }

  const value = args[index + 1];
  if (!value) {
    exitWithError(`Missing value for ${name}.`);
  }
  return value;
}

export function findAllOptions(args, name) {
  const values = [];
  for (let index = 0; index < args.length; index += 1) {
    if (args[index] !== name) {
      continue;
    }

    const value = args[index + 1];
    if (!value) {
      exitWithError(`Missing value for ${name}.`);
    }
    values.push(value);
    index += 1;
  }
  return values;
}

export function hasFlag(args, ...flags) {
  return flags.some((flag) => args.includes(flag));
}

export function collectPositionals(args, startIndex, optionsWithValues = [], booleanFlags = []) {
  const values = [];

  for (let index = startIndex; index < args.length; index += 1) {
    const current = args[index];
    if (optionsWithValues.includes(current)) {
      index += 1;
      continue;
    }
    if (booleanFlags.includes(current)) {
      continue;
    }
    if (current.startsWith("--")) {
      continue;
    }
    values.push(current);
  }

  return values;
}

export function readCountOption(args, fallback) {
  const value = findOption(args, "--count");
  if (!value) {
    return fallback;
  }

  const count = Number.parseInt(value, 10);
  if (!Number.isFinite(count) || count <= 0) {
    exitWithError(`Invalid --count value: ${value}`);
  }
  return count;
}

export function requireCommandValue(value, usage) {
  if (!value) {
    exitWithError(usage);
  }
  return value;
}

export function maskSecret(value) {
  if (!value) {
    return "";
  }
  if (value.length <= 8) {
    return "*".repeat(value.length);
  }
  return `${value.slice(0, 4)}...${value.slice(-4)}`;
}

export function sanitizeForOutput(value, key = "") {
  if (Array.isArray(value)) {
    return value.map((item) => sanitizeForOutput(item, key));
  }

  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value).map(([entryKey, entryValue]) => [entryKey, sanitizeForOutput(entryValue, entryKey)]),
    );
  }

  if (typeof value === "string") {
    const lowered = key.toLowerCase();
    if (
      lowered.includes("authorization") ||
      (lowered.includes("api") && lowered.includes("key")) ||
      lowered.includes("cookie") ||
      lowered.includes("token")
    ) {
      return maskSecret(value);
    }
  }

  return value;
}

export function printJson(value) {
  console.log(JSON.stringify(value, null, 2));
}

export function normalizePath(requestPath) {
  if (/^https?:\/\//i.test(requestPath)) {
    return requestPath;
  }

  return requestPath.startsWith("/") ? requestPath : `/${requestPath}`;
}
