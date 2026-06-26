/**
 * SolidPod-Data — Authentication Helper
 * Provides a cached, authenticated SOLID session using Client Credentials.
 * No browser required — uses machine-to-machine OIDC auth.
 */

import { Session } from "@inrupt/solid-client-authn-node";

let _session = null;

/**
 * Returns an authenticated SOLID session, creating one if needed.
 *
 * Required environment variables:
 *   SOLID_IDP        - Identity Provider URL (e.g. https://login.inrupt.com)
 *   SOLID_CLIENT_ID  - Client ID from your registered SOLID application
 *   SOLID_OIDC_KEY   - OIDC client key from your registered SOLID application
 *
 * Optional:
 *   SOLID_OIDC_ISSUER - Override OIDC issuer (defaults to SOLID_IDP)
 */
export async function getSession() {
  if (_session && _session.info.isLoggedIn) return _session;

  const idp      = process.env.SOLID_IDP;
  const clientId = process.env.SOLID_CLIENT_ID;
  const oidcKey  = process.env.SOLID_OIDC_KEY;
  const issuer   = process.env.SOLID_OIDC_ISSUER || idp;

  if (!idp || !clientId || !oidcKey) {
    throw new Error(
      "Missing required environment variables.\n" +
      "Please set: SOLID_IDP, SOLID_CLIENT_ID, SOLID_OIDC_KEY\n" +
      "See SKILL.md for setup instructions."
    );
  }

  _session = new Session();

  await _session.login({
    oidcIssuer:  issuer,
    clientName:  "SolidPod-Data",
    clientId,
    clientSecret: oidcKey,   // inrupt SDK parameter name — maps to our SOLID_OIDC_KEY
    tokenType:   "DPoP",
  });

  if (!_session.info.isLoggedIn) {
    throw new Error(
      "Authentication failed. Verify SOLID_CLIENT_ID and SOLID_OIDC_KEY are correct."
    );
  }

  return _session;
}

/** Returns the authenticated fetch function for use with @inrupt/solid-client. */
export async function getAuthFetch() {
  const session = await getSession();
  return session.fetch;
}

/** Returns the authenticated WebID. */
export async function getWebId() {
  const session = await getSession();
  return session.info.webId;
}
