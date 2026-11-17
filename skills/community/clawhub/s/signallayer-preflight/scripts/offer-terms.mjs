/**
 * Pure x402 V2 offer validator.
 * No network, wallets, signatures, settlement or private-key handling.
 */
export const EXPECTED = Object.freeze({
  scheme: "exact",
  network: "eip155:8453",
  asset: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  payTo: "0x60B3C6c053E926460D1E1053c516c859C95365e6",
  amount: "10000"
});

const equalAddress = (a, b) =>
  typeof a === "string" && a.toLowerCase() === b.toLowerCase();

/**
 * @param {unknown} challenge A decoded PAYMENT-REQUIRED header.
 * @param {{resourceUrl?: string, expected?: typeof EXPECTED}} options
 * @returns {{valid: boolean, issues: string[], matchingOffers: number, offeredCount: number}}
 */
export function inspectOffer(challenge, options = {}) {
  const expected = options.expected || EXPECTED;
  const issues = [];
  if (!challenge || typeof challenge !== "object" || Array.isArray(challenge)) {
    return { valid: false, issues: ["challenge_not_object"], matchingOffers: 0, offeredCount: 0 };
  }
  if (challenge.x402Version !== 2) issues.push("unsupported_x402_version");
  const accepts = Array.isArray(challenge.accepts) ? challenge.accepts : [];
  if (accepts.length === 0) issues.push("no_payment_offers");

  const match = accepts.filter((offer) =>
    offer && typeof offer === "object" &&
    offer.scheme === expected.scheme &&
    offer.network === expected.network &&
    String(offer.amount) === expected.amount &&
    equalAddress(offer.asset, expected.asset) &&
    equalAddress(offer.payTo, expected.payTo)
  );

  if (accepts.length && !match.length) issues.push("no_offer_matches_allowed_terms");

  const resource = typeof challenge.resource === "string"
    ? challenge.resource
    : challenge.resource?.url;
  if (options.resourceUrl && typeof resource === "string") {
    try {
      const advertised = new URL(resource);
      const requested = new URL(options.resourceUrl);
      if (advertised.origin !== requested.origin || advertised.pathname !== requested.pathname) {
        issues.push("challenge_resource_mismatch");
      }
    } catch {
      issues.push("invalid_challenge_resource");
    }
  }

  return {
    valid: issues.length === 0,
    issues,
    matchingOffers: match.length,
    offeredCount: accepts.length
  };
}
