// The company's real domain, cheapest evidence first:
//
//   1. what LinkedIn says, when it is a real domain;
//   2. what the source that found the company returned (AI Ark, Apollo and Exa
//      all return one; LinkedIn and they disagree mostly when LinkedIn lists a
//      short link);
//   3. where LinkedIn's short link actually goes: "bit.ly/4lE…" redirects to
//      the company's own site. Followed hop by hop through the Location
//      header, never the page.
//
// Empty only when all three come up empty. Every step is free.

import { defineScript } from "@cargo-ai/cdk";

import { bareDomain, isSharedHost } from "./domains";

// The script sandbox exposes `axios` to `require`; nothing is installed here.
declare const require: (id: string) => {
  get: (
    url: string,
    options: Record<string, unknown>,
  ) => Promise<{ status: number; headers: Record<string, string> }>;
};

const MAX_HOPS = 5;

// The sandbox has no global `URL`, so a relative Location ("/home") is joined
// to the current origin by hand.
const nextUrl = (current: string, location: string): string => {
  if (/^https?:\/\//i.test(location)) {
    return location;
  }
  const origin = current.match(/^https?:\/\/[^/?#]+/i);
  if (!origin) {
    return location;
  }
  if (location.startsWith("/")) {
    return `${origin[0]}${location}`;
  }
  return `${origin[0]}/${location}`;
};

const followLink = async (url: string): Promise<string> => {
  const axios = require("axios");
  let current = url;
  for (let hop = 0; hop < MAX_HOPS; hop += 1) {
    const response = await axios.get(current, {
      maxRedirects: 0,
      timeout: 8000,
      validateStatus: () => true,
    });
    const location = response.headers.location;
    if (response.status < 300 || response.status >= 400 || !location) {
      return current;
    }
    current = nextUrl(current, location);
  }
  return current;
};

export const companyDomain = defineScript(
  async ({
    linkedinDomain,
    linkedinWebsite,
    sourceDomain,
  }: {
    linkedinDomain: string;
    linkedinWebsite: string;
    sourceDomain: string;
  }): Promise<string> => {
    const fromLinkedin = bareDomain(linkedinDomain || linkedinWebsite);
    if (fromLinkedin && !isSharedHost(fromLinkedin)) {
      return fromLinkedin;
    }

    const fromSource = bareDomain(sourceDomain);
    if (fromSource && !isSharedHost(fromSource)) {
      return fromSource;
    }

    if (!linkedinWebsite) {
      return "";
    }
    try {
      const landed = bareDomain(await followLink(linkedinWebsite));
      if (landed && !isSharedHost(landed)) {
        return landed;
      }
    } catch {
      return "";
    }
    return "";
  },
);
