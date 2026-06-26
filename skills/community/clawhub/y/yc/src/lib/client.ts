/**
 * YC Startup School API client.
 *
 * Hybrid architecture:
 *  - Reading: GraphQL at POST /graphql (Apollo Client on frontend)
 *  - Writing: Traditional Rails REST (form POST with CSRF token)
 */

import { type YcCookies, cookiesToString } from "./cookies.js";

const BASE_URL = "https://www.startupschool.org";

const USER_AGENT =
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36";

// --- Error types ---

export class YcApiError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public response?: string
  ) {
    super(message);
    this.name = "YcApiError";
  }
}

export class NotAuthenticatedError extends YcApiError {
  constructor() {
    super(
      "Session expired or invalid. Log in at https://www.startupschool.org/ in Chrome, then try again."
    );
    this.name = "NotAuthenticatedError";
  }
}

// --- Types ---

export interface Update {
  id: string;
  formattedDate: string;
  createdAt: string;
  canEdit: boolean;
  metricDisplayName: string;
  metricValue: number;
  morale: number;
  talkedTo: number;
  learnedFromUsers: string | null;
  biggestChange: string | null;
  biggestBlocker: string | null;
  goals: string | null;
  path: string;
  completableGoals: Array<{
    key: string;
    goal: string;
    completed: boolean | null;
  }>;
}

export interface Dashboard {
  currentStreak: number;
  curriculum: {
    completed: number;
    required: number;
    nextItem: {
      id: string;
      title: string;
      url: string;
    } | null;
  };
  updatesByWeek: Array<{
    url: string | null;
    weekLabel: string;
  }>;
}

export interface CurrentUser {
  slug: string;
  firstName: string;
  track: string;
  returningUser: boolean;
}

export interface UpdateInput {
  metric_value: number;
  talked_to: number;
  morale: number;
  learned_from_users?: string;
  biggest_change?: string;
  biggest_blocker?: string;
  goals?: string[];
}

// --- Client ---

export class YcClient {
  private cookies: YcCookies;
  private csrfToken: string | null = null;

  constructor(cookies: YcCookies) {
    this.cookies = cookies;
  }

  private baseHeaders(): Record<string, string> {
    return {
      "User-Agent": USER_AGENT,
      Cookie: cookiesToString(this.cookies),
    };
  }

  // --- GraphQL ---

  async graphqlQuery<T>(
    operationName: string,
    query: string,
    variables?: Record<string, unknown>
  ): Promise<T> {
    // Rails requires CSRF token for all POST requests, including GraphQL
    const csrf = await this.getCsrfToken();

    const res = await fetch(`${BASE_URL}/graphql`, {
      method: "POST",
      headers: {
        ...this.baseHeaders(),
        "Content-Type": "application/json",
        Accept: "application/json",
        "X-CSRF-Token": csrf,
      },
      body: JSON.stringify({ operationName, query, variables }),
    });

    if (res.status === 401 || res.status === 302) {
      throw new NotAuthenticatedError();
    }

    if (!res.ok) {
      const text = await res.text().catch(() => "");
      throw new YcApiError(
        `GraphQL request failed: ${res.status} ${res.statusText}`,
        res.status,
        text.slice(0, 500)
      );
    }

    const json = (await res.json()) as { data?: T; errors?: Array<{ message: string }> };

    if (json.errors && json.errors.length > 0) {
      throw new YcApiError(
        `GraphQL error: ${json.errors.map((e) => e.message).join(", ")}`
      );
    }

    if (!json.data) {
      throw new YcApiError("GraphQL response missing data field");
    }

    return json.data;
  }

  // --- CSRF Token ---

  async getCsrfToken(): Promise<string> {
    if (this.csrfToken) return this.csrfToken;

    const res = await fetch(`${BASE_URL}/dashboard`, {
      headers: this.baseHeaders(),
      redirect: "follow",
    });

    if (res.status === 401 || res.url.includes("account.ycombinator.com")) {
      throw new NotAuthenticatedError();
    }

    const html = await res.text();
    const match = html.match(/<meta\s+name="csrf-token"\s+content="([^"]+)"/);
    if (!match) {
      throw new YcApiError("Could not extract CSRF token from page");
    }

    this.csrfToken = match[1];
    return this.csrfToken;
  }

  // --- Rails REST ---

  async railsPost(path: string, data: Record<string, string>): Promise<string> {
    const csrf = await this.getCsrfToken();

    const formData = new URLSearchParams({
      ...data,
      authenticity_token: csrf,
    });

    const res = await fetch(`${BASE_URL}${path}`, {
      method: "POST",
      headers: {
        ...this.baseHeaders(),
        "Content-Type": "application/x-www-form-urlencoded",
        Accept: "text/html, application/json",
      },
      body: formData.toString(),
      redirect: "follow",
    });

    if (res.status === 401 || res.status === 422) {
      throw new YcApiError(
        `Rails POST failed: ${res.status} ${res.statusText}`,
        res.status
      );
    }

    return res.url; // Returns redirect URL on success
  }

  async railsPut(path: string, data: Record<string, string>): Promise<string> {
    // Rails uses _method=put for PUT via POST
    return this.railsPost(path, { ...data, _method: "put" });
  }

  // --- High-level API ---

  async getCurrentUser(): Promise<CurrentUser> {
    const { CURRENT_USER } = await import("./queries.js");
    const data = await this.graphqlQuery<{ currentUser: CurrentUser }>(
      "CURRENT_USER",
      CURRENT_USER
    );
    return data.currentUser;
  }

  async getDashboard(): Promise<{ user: CurrentUser; dashboard: Dashboard; completedActions: string[] }> {
    const { DASHBOARD_DATA } = await import("./queries.js");
    const data = await this.graphqlQuery<{
      currentUser: CurrentUser;
      dashboard: Dashboard;
      completedActions: string[];
    }>("DASHBOARD_DATA", DASHBOARD_DATA);
    return {
      user: data.currentUser,
      dashboard: data.dashboard,
      completedActions: data.completedActions,
    };
  }

  async getUpdates(companyId?: number): Promise<{ companyName: string; updates: Update[]; thisWeekSubmitted: boolean }> {
    const { UPDATES_INDEX } = await import("./queries.js");
    const data = await this.graphqlQuery<{
      updates: {
        companyName: string;
        updates: Update[];
        thisWeekSubmitted: boolean;
      };
    }>("UPDATES_INDEX", UPDATES_INDEX, companyId ? { companyId } : undefined);
    return data.updates;
  }

  async createUpdate(input: UpdateInput): Promise<string> {
    const data: Record<string, string> = {
      "update[metric_value]": String(input.metric_value),
      "update[talked_to]": String(input.talked_to),
      "update[morale]": String(input.morale),
    };

    if (input.learned_from_users) {
      data["update[learned_from_users]"] = input.learned_from_users;
    }
    if (input.biggest_change) {
      data["update[biggest_change]"] = input.biggest_change;
    }
    if (input.biggest_blocker) {
      data["update[biggest_blocker]"] = input.biggest_blocker;
    }
    if (input.goals) {
      input.goals.forEach((goal, i) => {
        data[`update[goals][${i}]`] = goal;
      });
    }

    return this.railsPost("/updates", data);
  }

  async editUpdate(id: string, input: Partial<UpdateInput>): Promise<string> {
    const data: Record<string, string> = {};

    if (input.metric_value !== undefined) {
      data["update[metric_value]"] = String(input.metric_value);
    }
    if (input.talked_to !== undefined) {
      data["update[talked_to]"] = String(input.talked_to);
    }
    if (input.morale !== undefined) {
      data["update[morale]"] = String(input.morale);
    }
    if (input.learned_from_users !== undefined) {
      data["update[learned_from_users]"] = input.learned_from_users;
    }
    if (input.biggest_change !== undefined) {
      data["update[biggest_change]"] = input.biggest_change;
    }
    if (input.biggest_blocker !== undefined) {
      data["update[biggest_blocker]"] = input.biggest_blocker;
    }
    if (input.goals) {
      input.goals.forEach((goal, i) => {
        data[`update[goals][${i}]`] = goal;
      });
    }

    return this.railsPut(`/updates/${id}`, data);
  }
}
