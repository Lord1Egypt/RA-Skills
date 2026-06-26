/**
 * XO Protocol — Dating App Integration Example
 *
 * Shows how a third-party dating app can use XO Protocol to:
 *   1. Filter out unverified / low-trust users
 *   2. Boost verified users in search results
 *   3. Show trust badges on profiles
 *
 * Prerequisites:
 *   - npm install @xo-protocol/sdk express express-session
 *   - An XO Protocol API key + OAuth client credentials
 */

const { XOClient } = require("../sdk");

const API_KEY = "your-api-key";
const CLIENT_ID = "your_client_id";
const CLIENT_SECRET = "your_client_secret";
const REDIRECT_URI = "https://yourapp.com/auth/xo/callback";

const xo = new XOClient({ apiKey: API_KEY });

// ─── Use Case 1: "Login with XO" button ────────────────────────────────────

function handleLoginWithXO(req, res) {
  const state = crypto.randomUUID();
  req.session.xoState = state;

  const url = xo.getAuthorizationUrl({
    clientId: CLIENT_ID,
    redirectUri: REDIRECT_URI,
    state,
    scopes: ["identity", "reputation", "social_signals"],
  });

  res.redirect(url);
}

async function handleOAuthCallback(req, res) {
  const { code, state } = req.query;
  if (state !== req.session.xoState) {
    return res.status(400).send("Invalid state");
  }

  // Exchange code for token
  const tokenData = await xo.exchangeCode({
    code,
    clientId: CLIENT_ID,
    clientSecret: CLIENT_SECRET,
    redirectUri: REDIRECT_URI,
  });

  // Get the user's full trust profile in one call
  const profile = await xo.getTrustProfile();

  // Store in your database
  req.session.xoProfile = profile;
  res.redirect("/profile");
}

// ─── Use Case 2: Filter unverified users from search ────────────────────────

function filterByTrust(users, minTrustScore = 0.5) {
  return users.filter((user) => {
    const xo = user.xoProfile;
    if (!xo) return false;

    // Require identity verification
    if (!xo.identity.verified) return false;

    // Require minimum trust score
    if (xo.identity.trust_score < minTrustScore) return false;

    return true;
  });
}

// ─── Use Case 3: Sort by trust quality ──────────────────────────────────────

const TIER_ORDER = {
  novice: 0, bronze: 1, silver: 2, gold: 3,
  platinum: 4, diamond: 5, s: 6,
};

function sortByTrust(users) {
  return [...users].sort((a, b) => {
    const aXO = a.xoProfile;
    const bXO = b.xoProfile;
    if (!aXO && !bXO) return 0;
    if (!aXO) return 1;
    if (!bXO) return -1;

    // Verified users first
    if (aXO.identity.verified !== bXO.identity.verified) {
      return aXO.identity.verified ? -1 : 1;
    }

    // Then by reputation tier
    const aTier = TIER_ORDER[aXO.reputation.tier] || 0;
    const bTier = TIER_ORDER[bXO.reputation.tier] || 0;
    if (aTier !== bTier) return bTier - aTier;

    // Then by engagement (only if confidence is high enough)
    const aEng = aXO.socialSignals.confidence > 0.5 ? aXO.socialSignals.engagement_score : 0;
    const bEng = bXO.socialSignals.confidence > 0.5 ? bXO.socialSignals.engagement_score : 0;
    return (bEng || 0) - (aEng || 0);
  });
}

// ─── Use Case 4: Trust summary for profile display ──────────────────────────

function getTrustSummary(xoProfile) {
  if (!xoProfile) {
    return { level: "unknown", label: "Not connected to XO", color: "#999" };
  }

  const { identity, reputation, socialSignals } = xoProfile;

  if (!identity.verified) {
    return { level: "unverified", label: "Unverified", color: "#ff3b30" };
  }

  if (identity.trust_score >= 0.8 && TIER_ORDER[reputation.tier] >= 3) {
    return { level: "high", label: "Highly Trusted", color: "#34c759" };
  }

  if (identity.trust_score >= 0.5) {
    return { level: "medium", label: "Verified", color: "#ff9500" };
  }

  return { level: "low", label: "New User", color: "#007aff" };
}

module.exports = {
  handleLoginWithXO,
  handleOAuthCallback,
  filterByTrust,
  sortByTrust,
  getTrustSummary,
};
