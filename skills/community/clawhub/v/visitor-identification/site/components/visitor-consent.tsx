"use client";

import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import type { VisitorTracking } from "@/lib/visitors";

// The consent gate, and the only code that loads Snitcher. Rendered by the
// layout when lib/visitors.ts returns settings (a ready site with the snippet).
//
// Nothing from Snitcher loads before an explicit accept. Its own
// `waitForConsent` still tracks pageviews and sessions before consent, so the
// tracker script is not even requested until the visitor says yes. Global
// Privacy Control is a no; withdrawing reloads every open tab, which removes
// the tracker's listeners. It stops future collection; it does not erase what
// Snitcher already holds.

const STORAGE_KEY = "visitor-identification-consent-v1";

type Choice = "accepted" | "denied" | null;

// Snitcher's loader API, queued until its script initialises. The same stubs
// its installation snippet defines, so calls made before load are replayed.
const QUEUED_METHODS = [
  "track",
  "page",
  "identify",
  "company",
  "group",
  "alias",
  "ready",
  "debug",
  "on",
  "off",
  "once",
  "trackClick",
  "trackSubmit",
  "trackLink",
  "trackForm",
  "pageview",
  "screen",
  "reset",
  "register",
  "setAnonymousId",
  "addSourceMiddleware",
  "addIntegrationMiddleware",
  "addDestinationMiddleware",
  "giveCookieConsent",
  "denyCookieConsent",
];

type SnitcherQueue = unknown[] & {
  initialized?: boolean;
  _loaded?: boolean;
  [method: string]: unknown;
};

function snitcherGlobal(namespace: string): SnitcherQueue | undefined {
  return (window as unknown as Record<string, SnitcherQueue | undefined>)[
    namespace
  ];
}

// The provider's bootstrap, written out: queue the API, then load its script
// with our reviewed settings.
function loadSnitcher(settings: VisitorTracking["settings"]): void {
  const { namespace } = settings;
  const existing = snitcherGlobal(namespace);
  if (existing !== undefined && existing._loaded === true) return;
  // An array with the API's methods on it, the shape the provider expects.
  const queue = [] as unknown[] as SnitcherQueue;
  queue._loaded = true;
  for (const method of QUEUED_METHODS) {
    queue[method] = (...args: unknown[]) => {
      const current = snitcherGlobal(namespace);
      if (current === undefined) return undefined;
      if (current.initialized === true) {
        return (current[method] as (...a: unknown[]) => unknown)(...args);
      }
      current.push([method, ...args]);
      return current;
    };
  }
  (window as unknown as Record<string, SnitcherQueue>)[namespace] = queue;

  const script = document.createElement("script");
  script.async = true;
  script.id = "__radar__";
  script.setAttribute("data-settings", JSON.stringify(settings));
  script.src = `https://${settings.cdn}/releases/latest/radar.min.js`;
  document.head.append(script);
  (queue.giveCookieConsent as () => void)();
}

function readChoice(): Choice {
  try {
    const value = window.localStorage.getItem(STORAGE_KEY);
    return value === "accepted" || value === "denied" ? value : null;
  } catch {
    return null;
  }
}

function saveChoice(choice: "accepted" | "denied"): void {
  try {
    window.localStorage.setItem(STORAGE_KEY, choice);
  } catch {
    // The choice still applies to this page.
  }
}

function privacySignal(): boolean {
  return (
    (navigator as Navigator & { globalPrivacyControl?: boolean })
      .globalPrivacyControl === true
  );
}

export function VisitorConsent({ tracking }: { tracking: VisitorTracking }) {
  const [active, setActive] = useState(false);
  const [open, setOpen] = useState(false);
  const [loaded, setLoaded] = useState(false);
  const [gpc, setGpc] = useState(false);

  useEffect(() => {
    // Previews and the Cargo URL never track: only the canonical origin does.
    if (window.location.origin !== tracking.siteOrigin) return;
    setActive(true);
    const signal = privacySignal();
    setGpc(signal);
    const choice = readChoice();
    setOpen(choice === null);
    if (choice === "accepted" && signal === false) {
      loadSnitcher(tracking.settings);
      setLoaded(true);
    }

    // A choice withdrawn in another tab stops this tab's tracker too.
    const onStorage = (event: StorageEvent) => {
      if (
        (event.key === STORAGE_KEY || event.key === null) &&
        readChoice() !== "accepted" &&
        snitcherGlobal(tracking.settings.namespace) !== undefined
      ) {
        window.location.reload();
      }
    };
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, [tracking]);

  if (active === false) return null;

  const accept = () => {
    saveChoice("accepted");
    setOpen(false);
    if (gpc === false && loaded === false) {
      loadSnitcher(tracking.settings);
      setLoaded(true);
    }
  };

  const reject = () => {
    saveChoice("denied");
    setOpen(false);
    if (loaded) {
      const tracker = snitcherGlobal(tracking.settings.namespace);
      const deny =
        tracker === undefined ? undefined : tracker.denyCookieConsent;
      try {
        if (typeof deny === "function") deny();
      } catch {
        // The reload still stops collection.
      }
      window.location.reload();
    }
  };

  return (
    <>
      {open ? (
        <section
          aria-label="Website visitor tracking"
          className="fixed inset-x-4 bottom-16 z-50 max-w-lg rounded-lg border bg-background p-5 text-sm shadow-lg sm:left-4"
        >
          <p>
            {gpc
              ? "Visitor tracking is off because your browser sends a Global Privacy Control signal."
              : "Allow visitor tracking? We use Snitcher to identify the companies that visit this site and the pages they read. Nothing is tracked unless you accept."}
          </p>
          <a
            href={tracking.privacyPolicyUrl}
            className="mt-2 inline-block underline underline-offset-4"
          >
            Privacy details
          </a>
          <div className="mt-4 flex gap-2">
            <Button onClick={accept} disabled={gpc}>
              Accept tracking
            </Button>
            <Button variant="outline" onClick={reject}>
              Reject tracking
            </Button>
          </div>
        </section>
      ) : null}
      <Button
        variant="ghost"
        size="sm"
        className="fixed bottom-3 left-4 z-50"
        onClick={() => setOpen(true)}
      >
        Privacy choices
      </Button>
    </>
  );
}
