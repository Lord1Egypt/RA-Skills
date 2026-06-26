import { chargeUser } from "../../shared/billing";
import type { SkillResponse } from "../../shared/types";

interface Env {
  SKILLPAY_API_KEY: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    if (request.method !== "POST") {
      return Response.json({ error: "POST required" }, { status: 405 });
    }

    const body = await request.json() as { user_id: string };

    if (!body.user_id) {
      return Response.json({ error: "user_id required" }, { status: 400 });
    }

    const billing = await chargeUser({
      userId: body.user_id,
      apiKey: env.SKILLPAY_API_KEY,
      priceUsdt: 0.005,
      skillName: "sea-doc-summarizer",
    });

    if (!billing.success) {
      return Response.json({
        success: false,
        payment_url: billing.payment_url,
        error: billing.error,
      } satisfies SkillResponse);
    }

    return Response.json({
      success: true,
      data: { charged: true },
    } satisfies SkillResponse);
  },
};
