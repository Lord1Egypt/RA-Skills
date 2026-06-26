import { requireApiKey, resolveBaseUrl } from "./config.js";

export type Provider = "amazon" | "shopify";
export type AvailabilityStatus = "in_stock" | "out_of_stock" | "limited" | "unknown";

export interface Money {
  amount: number;
  currency: string;
  display?: string;
  compare_at_amount?: number | null;
}

export interface SelvaVariant {
  variant_id: string;
  title?: string | null;
  options?: Record<string, string>;
  price?: Money | null;
  image_url?: string | null;
  availability_status: AvailabilityStatus;
  checkout_url?: string | null;
}

export interface SelvaUserReview {
  title?: string | null;
  rating?: number | null;
  text: string;
  author?: string | null;
}

export interface SelvaProduct {
  selva_id: string;
  provider: Provider;
  provider_product_id: string;
  title: string;
  description?: string | null;
  url: string;
  image_url?: string | null;
  images?: string[];
  price?: Money | null;
  price_range?: { min?: Money; max?: Money } | null;
  rating?: number | null;
  review_count?: number | null;
  availability_status: AvailabilityStatus;
  stock_status_text?: string | null;
  delivery_estimate?: string | null;
  prime_eligible?: boolean | null;
  brand?: string | null;
  merchant?: { id?: string; name?: string; url?: string } | null;
  variants?: SelvaVariant[];
  attributes?: Record<string, string[]>;
  badges?: string[];
  features?: string[];
  user_reviews?: SelvaUserReview[];
  item_specifications?: string[];
}

async function parseResponse(response: Response) {
  const text = await response.text();
  let parsed: unknown = null;

  try {
    parsed = text.length ? JSON.parse(text) : null;
  } catch {
    parsed = { message: text };
  }

  if (!response.ok) {
    const message =
      typeof parsed === "object" && parsed && "message" in parsed
        ? String((parsed as { message: unknown }).message)
        : `Request failed with ${response.status}`;
    throw new Error(message);
  }

  return parsed;
}

export async function register() {
  const baseUrl = await resolveBaseUrl();
  const response = await fetch(`${baseUrl}/register`, {
    method: "POST"
  });
  return parseResponse(response) as Promise<{ api_key: string; message: string }>;
}

export async function settingsSummary() {
  const baseUrl = await resolveBaseUrl();
  const apiKey = await requireApiKey();

  const response = await fetch(`${baseUrl}/settings`, {
    headers: {
      "x-api-key": apiKey
    }
  });

  return parseResponse(response) as Promise<{
    settings: {
      name: string | null;
      phone: string | null;
      email: string | null;
      zip_code: string | null;
      address: {
        street: string;
        line2?: string | null;
        city: string;
        state: string;
        zip: string;
        country: string;
      } | null;
      approval_enabled: boolean;
      approval_threshold_amount: number | null;
      approval_threshold_currency: string;
      card: {
        issuer: string | null;
        last4: string | null;
      } | null;
    };
  }>;
}

export async function settingsPageLink() {
  const baseUrl = await resolveBaseUrl();
  const apiKey = await requireApiKey();

  const response = await fetch(`${baseUrl}/settings/link`, {
    method: "POST",
    headers: {
      "x-api-key": apiKey
    }
  });

  return parseResponse(response) as Promise<{ url: string; expires_in_hours: number }>;
}

export async function setAddress(input: {
  street: string;
  line2?: string | null;
  city: string;
  state: string;
  zip: string;
  country: string;
}) {
  const baseUrl = await resolveBaseUrl();
  const apiKey = await requireApiKey();

  const response = await fetch(`${baseUrl}/settings/address`, {
    method: "PUT",
    headers: {
      "content-type": "application/json",
      "x-api-key": apiKey
    },
    body: JSON.stringify(input)
  });

  return parseResponse(response);
}

export async function setName(name: string) {
  const baseUrl = await resolveBaseUrl();
  const apiKey = await requireApiKey();

  const response = await fetch(`${baseUrl}/settings/name`, {
    method: "PUT",
    headers: {
      "content-type": "application/json",
      "x-api-key": apiKey
    },
    body: JSON.stringify({ name })
  });

  return parseResponse(response);
}

export async function setPhone(phone: string) {
  const baseUrl = await resolveBaseUrl();
  const apiKey = await requireApiKey();

  const response = await fetch(`${baseUrl}/settings/phone`, {
    method: "PUT",
    headers: {
      "content-type": "application/json",
      "x-api-key": apiKey
    },
    body: JSON.stringify({ phone })
  });

  return parseResponse(response);
}

export async function setEmail(email: string) {
  const baseUrl = await resolveBaseUrl();
  const apiKey = await requireApiKey();

  const response = await fetch(`${baseUrl}/settings/email`, {
    method: "PUT",
    headers: {
      "content-type": "application/json",
      "x-api-key": apiKey
    },
    body: JSON.stringify({ email })
  });

  return parseResponse(response);
}

export async function search(query: string, options?: { includeRaw?: boolean }) {
  const baseUrl = await resolveBaseUrl();
  const apiKey = await requireApiKey();
  const includeRaw = options?.includeRaw === true;

  const response = await fetch(`${baseUrl}/search`, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-api-key": apiKey
    },
    body: JSON.stringify({ query, include_raw: includeRaw })
  });

  return parseResponse(response) as Promise<{
    notice?: string;
    pricing_note?: string;
    products: Array<{
      selva_id: string;
      provider: Provider;
      title: string;
      url: string;
      image_url?: string | null;
      price?: Money | null;
      rating?: number | null;
      review_count?: number | null;
      availability_status: AvailabilityStatus;
      delivery_estimate?: string | null;
      prime_eligible?: boolean | null;
    }>;
    raw_providers?: {
      amazon?: unknown;
      shopify?: unknown;
    };
    errors: Array<{ provider: Provider; message: string }>;
  }>;
}

export async function details(selvaId: string) {
  const baseUrl = await resolveBaseUrl();
  const apiKey = await requireApiKey();

  const response = await fetch(`${baseUrl}/details/${encodeURIComponent(selvaId)}`, {
    headers: {
      "x-api-key": apiKey
    }
  });

  return parseResponse(response) as Promise<{
    product: SelvaProduct;
    pricing_note?: string;
  }>;
}

export async function buy(input: {
  selva_id: string;
  method: "card" | "saved";
  payment_token?: string;
}) {
  const baseUrl = await resolveBaseUrl();
  const apiKey = await requireApiKey();

  const response = await fetch(`${baseUrl}/buy`, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-api-key": apiKey
    },
    body: JSON.stringify(input)
  });

  return parseResponse(response) as Promise<Record<string, unknown>>;
}

export async function orders() {
  const baseUrl = await resolveBaseUrl();
  const apiKey = await requireApiKey();

  const response = await fetch(`${baseUrl}/orders`, {
    headers: {
      "x-api-key": apiKey
    }
  });

  return parseResponse(response) as Promise<{
    orders: Array<{
      id: string;
      selva_id: string;
      status: string;
      payment_method: string;
      subtotal_amount: string | null;
      tax_amount: string | null;
      shipping_amount: string | null;
      total_amount: string | null;
      currency: string;
      failure_reason: string | null;
      created_at: string;
    }>;
  }>;
}

export async function stripePublishableKey() {
  const baseUrl = await resolveBaseUrl();
  const apiKey = await requireApiKey();

  const response = await fetch(`${baseUrl}/settings/stripe-publishable-key`, {
    headers: {
      "x-api-key": apiKey
    }
  });

  return parseResponse(response) as Promise<{
    stripe_publishable_key: string;
  }>;
}
