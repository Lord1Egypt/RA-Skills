// Plain helpers the domain scripts share. Not a script node themselves: they
// are bundled into each script that imports them.

// Hosts thousands of unrelated companies share. A company page that lists one
// of these as its website (a short or tracking link) has not told you its
// domain yet.
const SHARED_HOSTS = [
  "bit.ly",
  "buff.ly",
  "facebook.com",
  "github.com",
  "goo.gl",
  "google.com",
  "hubs.la",
  "hubs.ly",
  "instagram.com",
  "linkedin.com",
  "linktr.ee",
  "lnkd.in",
  "ow.ly",
  "t.co",
  "tinyurl.com",
];

/** "https://www.Acme.example/about?x=1" → "acme.example". */
export const bareDomain = (url: string | undefined): string => {
  if (!url) {
    return "";
  }
  const withoutScheme = url.trim().replace(/^https?:\/\//i, "");
  const host = withoutScheme.split(/[/?#]/)[0].toLowerCase();
  return host.replace(/^www\./, "");
};

export const isSharedHost = (domain: string): boolean => {
  return SHARED_HOSTS.some(
    (shared) => domain === shared || domain.endsWith(`.${shared}`),
  );
};
