export function printSection(title: string) {
  console.log(`\n${title}`);
  console.log("-".repeat(title.length));
}

export function pretty(value: unknown) {
  return JSON.stringify(value, null, 2);
}

export function money(value: number | null) {
  if (value == null) {
    return "n/a";
  }

  return `$${value.toFixed(2)}`;
}
