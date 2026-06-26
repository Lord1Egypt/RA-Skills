import { afterEach, describe, expect, it, vi } from "vitest";

vi.mock("../src/api.js", () => ({
  buy: vi.fn(),
  details: vi.fn(),
  orders: vi.fn(),
  register: vi.fn(),
  search: vi.fn(),
  setAddress: vi.fn(),
  setEmail: vi.fn(),
  setName: vi.fn(),
  setPhone: vi.fn(),
  settingsPageLink: vi.fn(),
  settingsSummary: vi.fn(),
  stripePublishableKey: vi.fn()
}));

vi.mock("../src/stripe.js", () => ({
  tokenizeCard: vi.fn()
}));

import * as api from "../src/api.js";
import * as stripe from "../src/stripe.js";
import { runCli } from "../src/cli.js";

describe("buy command", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.clearAllMocks();
  });

  it("always tokenizes cards with stripe_publishable_key", async () => {
    (api.stripePublishableKey as any).mockResolvedValue({
      stripe_publishable_key: "pk_test_selva"
    });
    (stripe.tokenizeCard as any).mockResolvedValue({ token: "tok_test" });
    (api.buy as any).mockResolvedValue({ order_id: "ord_1", status: "shipping" });
    vi.spyOn(console, "log").mockImplementation(() => {});

    await runCli([
      "node",
      "selva",
      "buy",
      "amzn_B0TEST",
      "--method",
      "card",
      "--number",
      "4242424242424242",
      "--exp",
      "12/34",
      "--cvv",
      "123"
    ]);

    expect(stripe.tokenizeCard).toHaveBeenCalledWith(
      expect.objectContaining({
        publishableKey: "pk_test_selva"
      })
    );
    expect(api.buy).toHaveBeenCalledWith(
      expect.objectContaining({
        selva_id: "amzn_B0TEST",
        method: "card",
        payment_token: "tok_test"
      })
    );
  });

  it("fails fast when STRIPE_PUBLISHABLE_KEY is missing", async () => {
    (api.stripePublishableKey as any).mockResolvedValue({
      stripe_publishable_key: ""
    });
    vi.spyOn(console, "log").mockImplementation(() => {});

    await expect(
      runCli([
        "node",
        "selva",
        "buy",
        "amzn_B0TEST",
        "--method",
        "card",
        "--number",
        "4242424242424242",
        "--exp",
        "12/34",
        "--cvv",
        "123"
      ])
    ).rejects.toThrow("Card tokenization requires STRIPE_PUBLISHABLE_KEY on the API.");
  });
});
