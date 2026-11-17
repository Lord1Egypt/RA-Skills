import visitors from "../visitors.json";
import { site } from "./site";
import { type SnitcherSettings, snitcherSettings } from "./snitcher";

export type VisitorTracking = {
  settings: SnitcherSettings;
  siteOrigin: string;
  privacyPolicyUrl: string;
};

// Read at build time by app/layout.tsx. `null` renders no consent gate, so a
// draft site, a preview, or a build without the snippet loads nothing: there
// is no profile ID in the export to load it with.
//
// NEXT_PUBLIC_SNITCHER_SNIPPET is the app env token
// `visitingCompanies.config._trackingScript`. It is read here, on the server,
// and only its profile ID reaches the page.
export function visitorTracking(): VisitorTracking | null {
  const snippet = process.env.NEXT_PUBLIC_SNITCHER_SNIPPET;
  if (snippet === undefined || snippet === "" || site.status !== "ready") {
    return null;
  }
  if (site.canonicalUrl === "") {
    throw new Error(
      "Visitor tracking needs site.json canonicalUrl: it only runs on that origin.",
    );
  }
  if (visitors.privacyPolicyUrl === "") {
    throw new Error(
      "Visitor tracking needs visitors.json privacyPolicyUrl: the reviewed disclosure the consent banner links to.",
    );
  }

  return {
    settings: snitcherSettings(snippet),
    siteOrigin: new URL(site.canonicalUrl).origin,
    privacyPolicyUrl: visitors.privacyPolicyUrl,
  };
}
