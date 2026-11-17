const apiBaseUrl = "https://api.sociallisteningapi.com/api/v1";

const sourceConfig = {
  linkedin: {
    path: "/linkedin/search",
  },
  x: {
    path: "/x/search",
  },
  reddit: {
    path: "/reddit/search-posts",
  },
};

function printErrorAndExit(message) {
  process.stderr.write(`${message}\n`);
  process.exitCode = 1;
}

async function searchSource(query, platform, apiKey) {
  const config = sourceConfig[platform];
  const searchParams = new URLSearchParams({ query });
  const requestUrl = `${apiBaseUrl}${config.path}?${searchParams.toString()}`;

  try {
    const response = await fetch(requestUrl, {
      headers: {
        "x-api-key": apiKey,
      },
    });
    const body = await response.json();

    if (!response.ok || body.success !== true) {
      let message = `Request failed with status ${response.status}.`;

      // API error bodies can omit details, so keep a useful fallback for the review digest.
      if (body.error && body.error.message) {
        message = body.error.message;
      }

      return {
        error: {
          platform,
          message,
          status: response.status,
        },
      };
    }

    const items = body.data.items.map((item) => ({
      ...item,
      matched_query: query,
      source_platform: platform,
    }));

    return {
      creditsUsed: body.credits_used,
      items,
    };
  } catch (error) {
    return {
      error: {
        platform,
        message: `Could not search ${platform}: ${error.message}`,
        status: null,
      },
    };
  }
}

function sortNewestFirst(items) {
  return items.sort((firstItem, secondItem) => {
    const firstDate = Date.parse(firstItem.published_at || "1970-01-01");
    const secondDate = Date.parse(secondItem.published_at || "1970-01-01");

    return secondDate - firstDate;
  });
}

async function main() {
  const apiKey = process.env.SOCIALLISTENING_API_KEY;
  const query = process.env.SOCIALLISTENING_QUERY;
  const platformsValue = process.env.SOCIALLISTENING_PLATFORMS || "linkedin,x,reddit";

  // The key is required at this environment boundary to prevent unauthenticated requests.
  if (!apiKey) {
    printErrorAndExit("Missing SOCIALLISTENING_API_KEY. No request was made.");
    return;
  }

  // The query comes from the agent environment and must exist before a paid request is made.
  if (!query || !query.trim()) {
    printErrorAndExit("Missing SOCIALLISTENING_QUERY. No request was made.");
    return;
  }

  const platforms = platformsValue.split(",").map((platform) => platform.trim());

  for (const platform of platforms) {
    // Reject unknown CLI values so a typo cannot create a request to an unintended route.
    if (!sourceConfig[platform]) {
      printErrorAndExit(`Unsupported platform: ${platform}. No request was made.`);
      return;
    }
  }

  const items = [];
  const errors = [];
  let creditsUsed = 0;

  for (const platform of platforms) {
    const result = await searchSource(query.trim(), platform, apiKey);

    if (result.error) {
      errors.push(result.error);
      continue;
    }

    creditsUsed += result.creditsUsed;
    items.push(...result.items);
  }

  const sourceUrls = [];

  for (const item of items) {
    if (sourceUrls.indexOf(item.url) === -1) {
      sourceUrls.push(item.url);
    }
  }

  const output = {
    query: query.trim(),
    searchedPlatforms: platforms,
    items: sortNewestFirst(items),
    errors,
    creditsUsed,
    sourceUrls,
  };

  process.stdout.write(`${JSON.stringify(output, null, 2)}\n`);
}

main();
