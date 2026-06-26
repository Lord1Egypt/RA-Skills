export function fail(message, exitCode = 2) {
  console.error(message);
  process.exit(exitCode);
}

export function readOptionValue(args, index, optionName) {
  const value = args[index + 1];
  if (value === undefined || value === "") {
    fail(`Missing value for ${optionName}`);
  }
  return value;
}

export function parseCommaList(rawValue, optionName) {
  const values = rawValue
    .split(",")
    .map((value) => value.trim())
    .filter(Boolean);
  if (values.length === 0) {
    fail(`${optionName} expects at least one value`);
  }
  return values;
}

export function parseDomainList(rawValue, optionName) {
  return parseCommaList(rawValue, optionName);
}

export function validateDateStr(rawValue, optionName) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(rawValue)) {
    fail(`${optionName} must be in YYYY-MM-DD format`);
  }
}
