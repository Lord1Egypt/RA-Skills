// The Snitcher tracker settings a site loads, built from the installation
// snippet Cargo provisions (`visitingCompanies.config._trackingScript`).
//
// Only the snippet's public profile ID is used. The site carries its own
// loader (components/visitor-consent.tsx) and these settings, so a change in
// the provider's snippet is a reviewed change to this file, never code that
// arrives with a deploy. Anything but the documented shape fails the build.
//
// Snippet shape (https://docs.snitcher.com/product/tracker/installation):
//   <script>!function(e){…}({"apiEndpoint": "radar.snitcher.com",
//     "cdn": "cdn.snitcher.com", "namespace": "Snitcher", "profileId": "…"});</script>

export type SnitcherSettings = {
  apiEndpoint: "radar.snitcher.com";
  cdn: "cdn.snitcher.com";
  namespace: "Snitcher";
  profileId: string;
  // The gate already loads nothing before an explicit accept; this keeps the
  // tracker from persisting a visitor identity until it is told consent holds.
  waitForConsent: true;
  // Company and page signals only. A generated profile can switch these on
  // remotely, and the loader's settings win.
  features: {
    formTracking: false;
    clickTracking: false;
    downloadTracking: false;
    sessionRecording: false;
    errorCapture: false;
  };
};

export function snitcherSettings(snippet: string): SnitcherSettings {
  const call = /\}\((\{[\s\S]*\})\);?\s*(?:<\/script>)?\s*$/.exec(
    snippet.trim(),
  );
  if (call === null) {
    throw new Error(
      "Unrecognised Snitcher snippet: no settings call. Review it before changing lib/snitcher.ts.",
    );
  }
  const settings = JSON.parse(call[1]) as Record<string, unknown>;
  if (
    settings.namespace !== "Snitcher" ||
    settings.apiEndpoint !== "radar.snitcher.com" ||
    settings.cdn !== "cdn.snitcher.com" ||
    typeof settings.profileId !== "string" ||
    /^[A-Za-z0-9_-]+$/.test(settings.profileId) === false
  ) {
    throw new Error(
      "Unrecognised Snitcher snippet: unexpected namespace, endpoints or profile ID.",
    );
  }

  return {
    apiEndpoint: "radar.snitcher.com",
    cdn: "cdn.snitcher.com",
    namespace: "Snitcher",
    profileId: settings.profileId,
    waitForConsent: true,
    features: {
      formTracking: false,
      clickTracking: false,
      downloadTracking: false,
      sessionRecording: false,
      errorCapture: false,
    },
  };
}
