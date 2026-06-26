/**
 * a16z Speedrun API client.
 *
 * No authentication required — all endpoints are plain JSON POSTs
 * to Next.js API routes at speedrun.a16z.com.
 */

const BASE_URL = "https://speedrun.a16z.com";

// --- Types ---

export interface SpeedrunCeo {
  first_name: string;
  last_name: string;
  email: string;
  phone_number: string;
  city: string;
  state?: string;
  country: string;
  citizenship: string;
  college: string;
  highest_education: string;
  years_of_experience: number;
  is_technical: boolean;
  linkedin_url: string;
  github_url?: string;
  x_url?: string;
  portfolio_url?: string;
}

export interface SpeedrunCofounder {
  first_name: string;
  last_name: string;
  email: string;
  phone_number?: string;
  linkedin_url: string;
}

export interface SpeedrunInvestor {
  name: string;
  email: string;
  amount_usd?: number;
}

export interface SpeedrunFunding {
  funding_total_usd: number;
  post_money_valuation_usd: number;
  burn_monthly_usd: number;
  runway_months: number;
  investors: SpeedrunInvestor[];
}

export interface SpeedrunFundraise {
  fundraising_target_amount_usd: number;
  fundraising_start_date: string;
  fundraising_target_description: string;
}

export interface SpeedrunUserMetrics {
  daily_active_users: number;
  weekly_active_users: number;
  monthly_active_users: number;
  user_growth_rate_monthly: number;
}

export interface SpeedrunRetentionMetrics {
  d1_retention: number;
  d7_retention: number;
  d30_retention: number;
  m1_retention: number;
}

export interface SpeedrunRevenueMetrics {
  annual_recurring_revenue_usd: number;
  avg_annual_contract_value_usd: number;
  net_dollar_retention: number;
  revenue_growth_rate_monthly: number;
}

export interface SpeedrunMetrics {
  launch_date: string;
  user_metrics?: SpeedrunUserMetrics;
  retention_metrics?: SpeedrunRetentionMetrics;
  revenue_metrics?: SpeedrunRevenueMetrics;
  metrics_description?: string;
}

export interface SpeedrunReferral {
  name: string;
  email: string;
  linkedin_url: string;
}

export interface SpeedrunApplication {
  company_name: string;
  one_liner: string;
  company_description: string;
  primary_category: string;
  secondary_category: string;
  company_city: string;
  company_state?: string;
  company_country: string;
  founding_date: string; // YYYY-MM
  website_url?: string;
  other_description?: string;
  is_full_time: boolean;
  num_full_time_founders: string;
  num_full_time_employees: number;
  team_description: string;
  ceo: SpeedrunCeo;
  other_founders: SpeedrunCofounder[];
  deck_gcs_url?: string;
  has_funding: boolean;
  funding?: SpeedrunFunding;
  is_fundraising: boolean;
  current_fundraise?: SpeedrunFundraise;
  has_metrics: boolean;
  metrics?: SpeedrunMetrics;
  has_referral: boolean;
  referral?: SpeedrunReferral;
  learned_about_speedrun?: string;
}

export const CATEGORIES = [
  "B2B / Enterprise Applications",
  "Consumer Applications",
  "Deep Tech",
  "Gaming / Entertainment Studio",
  "Infrastructure / Dev Tools",
  "Healthcare",
  "GovTech",
  "Web3",
  "Other",
] as const;

export const EDUCATION_LEVELS = [
  "High School Degree",
  "Bachelor's Degree (BA, BS)",
  "Master's / Professional Degree (MD, MBA, JD, etc.)",
  "Doctoral Degree (PhD)",
] as const;

// --- Error ---

export class SpeedrunApiError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public response?: string
  ) {
    super(message);
    this.name = "SpeedrunApiError";
  }
}

// --- Client ---

export class SpeedrunClient {
  async submitEmail(email: string): Promise<unknown> {
    const res = await fetch(`${BASE_URL}/api/apply/submit_email`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email }),
    });

    if (!res.ok) {
      const text = await res.text().catch(() => res.statusText);
      throw new SpeedrunApiError(
        `Email submission failed: ${res.status}`,
        res.status,
        text
      );
    }

    return res.json();
  }

  async submitApplication(application: SpeedrunApplication): Promise<unknown> {
    const res = await fetch(`${BASE_URL}/api/apply/submit-application`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(application),
    });

    if (!res.ok) {
      const body = await res.json().catch(() => ({ message: res.statusText }));
      throw new SpeedrunApiError(
        `Application submission failed: ${(body as { message?: string }).message || "Unknown error"}`,
        res.status,
        JSON.stringify(body)
      );
    }

    return res.json();
  }

  async getUploadUrl(
    fileType: string,
    expectedSizeBytes: number,
    applicationId?: string
  ): Promise<{ url: string; [key: string]: unknown }> {
    const body: Record<string, unknown> = {
      file_type: fileType,
      expected_size_bytes: expectedSizeBytes,
    };
    if (applicationId) body.application_id = applicationId;

    const res = await fetch(`${BASE_URL}/api/apply/get-upload-url`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      throw new SpeedrunApiError(
        `Failed to get upload URL: ${res.statusText}`,
        res.status
      );
    }

    return res.json() as Promise<{ url: string }>;
  }

  async uploadFile(url: string, file: Uint8Array, contentType: string): Promise<void> {
    const blob = new Blob([file as BlobPart], { type: contentType });
    const res = await fetch(url, {
      method: "PUT",
      headers: { "Content-Type": contentType },
      body: blob,
    });

    if (!res.ok) {
      const text = await res.text().catch(() => res.statusText);
      throw new SpeedrunApiError(
        `Upload failed: ${res.status}`,
        res.status,
        text
      );
    }
  }

  async submitVideo(data: Record<string, unknown>): Promise<unknown> {
    const res = await fetch(`${BASE_URL}/api/apply/submit_video`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!res.ok) {
      const body = await res.json().catch(() => ({ message: res.statusText }));
      throw new SpeedrunApiError(
        `Video submission failed: ${(body as { message?: string }).message || "Unknown error"}`,
        res.status
      );
    }

    return res.json();
  }
}
