export function parseExpiry(exp: string) {
  const match = exp.match(/^(\d{1,2})\/(\d{2}|\d{4})$/);
  if (!match) {
    throw new Error("Invalid expiry format. Use MM/YY or MM/YYYY.");
  }

  const monthPart = match[1];
  const yearPart = match[2];
  if (!monthPart || !yearPart) {
    throw new Error("Invalid expiry format. Use MM/YY or MM/YYYY.");
  }

  const month = Number.parseInt(monthPart, 10);
  if (month < 1 || month > 12) {
    throw new Error("Invalid expiry month.");
  }

  let year = Number.parseInt(yearPart, 10);
  if (year < 100) {
    year += 2000;
  }

  return { month, year };
}

export async function tokenizeCard(input: {
  publishableKey: string;
  number: string;
  exp: string;
  cvv: string;
}) {
  if (!input.publishableKey) {
    throw new Error("Stripe publishable key is missing from API response.");
  }

  const expiry = parseExpiry(input.exp);
  const body = new URLSearchParams({
    "card[number]": input.number,
    "card[exp_month]": String(expiry.month),
    "card[exp_year]": String(expiry.year),
    "card[cvc]": input.cvv
  });

  const auth = Buffer.from(`${input.publishableKey}:`).toString("base64");

  const response = await fetch("https://api.stripe.com/v1/tokens", {
    method: "POST",
    headers: {
      authorization: `Basic ${auth}`,
      "content-type": "application/x-www-form-urlencoded"
    },
    body
  });

  const json = (await response.json()) as Record<string, unknown>;

  if (!response.ok || !json.id) {
    const message =
      typeof json.error === "object" && json.error !== null && "message" in json.error
        ? String((json.error as { message?: unknown }).message)
        : `Stripe tokenization failed (${response.status})`;
    throw new Error(message);
  }

  return { token: String(json.id), raw: json };
}
