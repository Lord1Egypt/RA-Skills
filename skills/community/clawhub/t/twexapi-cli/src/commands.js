import {
  collectPositionals,
  exitWithError,
  findAllOptions,
  findOption,
  hasFlag,
  readCountOption,
  requireCommandValue,
} from "./utils.js";
import {
  handleAuthAppsCommand,
  handleAuthProfilesCommand,
  handleConfigCommand,
  resolveCookieArg,
  saveConfig,
} from "./config.js";
import { performRequest } from "./request.js";

function tweetActionBody(args, state, config) {
  const proxy = findOption(args, "--proxy");
  return {
    cookie: resolveCookieArg(args, state, config),
    ...(proxy ? { proxy } : {}),
  };
}

function buildTweetBody(args, state, config) {
  const text = requireCommandValue(findOption(args, "--text"), "Usage: twexapi tweet create --text <content> [--media-url <url>] [--reply-to <tweet_id>]");
  const mediaUrls = findAllOptions(args, "--media-url");
  const proxy = findOption(args, "--proxy");
  const delegatedAccount = findOption(args, "--delegated-account");
  const communityName = findOption(args, "--community");
  const schedule = findOption(args, "--schedule");
  const replyTweetId = findOption(args, "--reply-to");

  return {
    tweet_content: text,
    cookie: resolveCookieArg(args, state, config),
    ...(mediaUrls[0] ? { media_url: mediaUrls[0] } : {}),
    ...(delegatedAccount ? { delegated_account_username: delegatedAccount } : {}),
    ...(communityName ? { community_name: communityName } : {}),
    ...(schedule ? { schedule } : {}),
    ...(replyTweetId ? { reply_tweet_id: replyTweetId } : {}),
    ...(proxy ? { proxy } : {}),
  };
}

async function handleAuthCookieCommand(state, config, args) {
  const authToken = requireCommandValue(findOption(args, "--auth-token"), "Usage: twexapi auth cookie --auth-token <token> [--save-as <profile>] [--ct0 <value>]");
  const saveAs = findOption(args, "--save-as");
  const response = await performRequest(state, config, {
    method: "GET",
    path: `/twitter/${encodeURIComponent(authToken)}/cookie`,
    silent: Boolean(saveAs),
  });

  if (state.dryRun || !saveAs) {
    return;
  }

  const cookie = typeof response.data?.data === "string" ? response.data.data : "";
  if (!cookie) {
    exitWithError("Cookie response did not contain a usable cookie string.");
  }

  const ct0 = findOption(args, "--ct0");
  config.profiles[saveAs] = {
    cookie,
    authToken,
    ...(ct0 ? { ct0 } : {}),
  };
  if (!config.currentProfile || hasFlag(args, "--use")) {
    config.currentProfile = saveAs;
  }
  await saveConfig(state.configDir, config);

  console.log(JSON.stringify({
    saved: saveAs,
    currentProfile: config.currentProfile,
    profile: {
      cookie: cookie ? `${cookie.slice(0, 4)}...${cookie.slice(-4)}` : "",
      authToken: authToken ? `${authToken.slice(0, 4)}...${authToken.slice(-4)}` : "",
      ct0: ct0 ? `${ct0.slice(0, 4)}...${ct0.slice(-4)}` : "",
    },
  }, null, 2));
}

async function handleAuthCommand(state, config, args) {
  const area = args[1];
  if (area === "apps") {
    await handleAuthAppsCommand(state, config, args);
    return;
  }
  if (area === "profiles") {
    await handleAuthProfilesCommand(state, config, args);
    return;
  }
  if (area === "cookie") {
    await handleAuthCookieCommand(state, config, args);
    return;
  }

  exitWithError("Unknown auth command.", "Use: auth apps | auth profiles | auth cookie");
}

async function handleUsersCommand(state, config, args) {
  const usernames = collectPositionals(args, 1);
  if (usernames.length === 0) {
    exitWithError("Usage: twexapi users <username...>");
  }

  await performRequest(state, config, {
    method: "POST",
    path: "/twitter/users",
    body: usernames,
  });
}

async function handleAboutCommand(state, config, args) {
  const screenName = requireCommandValue(args[1], "Usage: twexapi about <screen_name>");
  await performRequest(state, config, {
    method: "GET",
    path: `/twitter/${encodeURIComponent(screenName)}/about`,
  });
}

async function handleSearchCommand(state, config, args) {
  const scope = args[1];

  if (scope === "tweets") {
    const terms = collectPositionals(args, 2, ["--count", "--sort"]);
    if (terms.length === 0) {
      exitWithError("Usage: twexapi search tweets <term...> [--count <n>] [--sort Latest|Top]");
    }

    await performRequest(state, config, {
      method: "POST",
      path: "/twitter/advanced_search",
      body: {
        searchTerms: terms,
        maxItems: readCountOption(args, 20),
        sortBy: findOption(args, "--sort") || "Latest",
      },
    });
    return;
  }

  if (scope === "users") {
    const keyword = requireCommandValue(args[2], "Usage: twexapi search users <keyword> [--count <n>]");
    await performRequest(state, config, {
      method: "GET",
      path: `/twitter/search-user/${encodeURIComponent(keyword)}/${readCountOption(args, 20)}`,
    });
    return;
  }

  exitWithError("Unknown search command.", "Use: search tweets | search users");
}

async function handleFollowersCommand(state, config, args) {
  const screenName = requireCommandValue(args[1], "Usage: twexapi followers <screen_name> [--count <n>]");
  await performRequest(state, config, {
    method: "GET",
    path: `/twitter/followers/${encodeURIComponent(screenName)}/${readCountOption(args, 200)}`,
  });
}

async function handleFollowingCommand(state, config, args) {
  const screenName = requireCommandValue(args[1], "Usage: twexapi following <screen_name> [--count <n>]");
  await performRequest(state, config, {
    method: "GET",
    path: `/twitter/following/${encodeURIComponent(screenName)}/${readCountOption(args, 200)}`,
  });
}

async function handleListCommand(state, config, args) {
  const action = args[1];

  if (action === "search") {
    const query = requireCommandValue(findOption(args, "--query"), "Usage: twexapi list search --query <text> [--count <n>]");
    await performRequest(state, config, {
      method: "POST",
      path: "/twitter/list/search",
      body: {
        query,
        target_count: readCountOption(args, 20),
      },
    });
    return;
  }

  if (action === "create") {
    const listName = requireCommandValue(findOption(args, "--name"), "Usage: twexapi list create --name <name> --description <text> [--private]");
    const listDescription = requireCommandValue(findOption(args, "--description"), "Usage: twexapi list create --name <name> --description <text> [--private]");
    await performRequest(state, config, {
      method: "POST",
      path: "/twitter/list/create",
      body: {
        cookie: resolveCookieArg(args, state, config),
        list_name: listName,
        list_description: listDescription,
        is_private: hasFlag(args, "--private"),
      },
    });
    return;
  }

  if (action === "members") {
    const listId = requireCommandValue(args[2], "Usage: twexapi list members <list_id> [--count <n>]");
    await performRequest(state, config, {
      method: "GET",
      path: `/twitter/list/${encodeURIComponent(listId)}/members/${readCountOption(args, 100)}`,
    });
    return;
  }

  if (action === "subscribers") {
    const listId = requireCommandValue(args[2], "Usage: twexapi list subscribers <list_id> [--count <n>]");
    await performRequest(state, config, {
      method: "GET",
      path: `/twitter/list/${encodeURIComponent(listId)}/subscribers/${readCountOption(args, 100)}`,
    });
    return;
  }

  exitWithError("Unknown list command.", "Use: list search | list create | list members | list subscribers");
}

async function handleTweetCommand(state, config, args) {
  const action = args[1];

  if (action === "create") {
    await performRequest(state, config, {
      method: "POST",
      path: "/twitter/tweets/create",
      body: buildTweetBody(args, state, config),
    });
    return;
  }

  if (action === "quote") {
    const quoteUrl = requireCommandValue(findOption(args, "--quote-url"), "Usage: twexapi tweet quote --text <content> --quote-url <url>");
    await performRequest(state, config, {
      method: "POST",
      path: "/twitter/tweets/quote",
      body: {
        ...buildTweetBody(args, state, config),
        quote_tweet_url: quoteUrl,
      },
    });
    return;
  }

  if (action === "lookup") {
    const tweetIds = collectPositionals(args, 2);
    if (tweetIds.length === 0) {
      exitWithError("Usage: twexapi tweet lookup <tweet_id...>");
    }
    await performRequest(state, config, {
      method: "POST",
      path: "/twitter/tweets/lookup",
      body: tweetIds,
    });
    return;
  }

  if (action === "replies") {
    const tweetId = requireCommandValue(args[2], "Usage: twexapi tweet replies <tweet_id> [--count <n>] [--sort Relevance|Recency|Likes]");
    const count = readCountOption(args, 50);
    const sort = findOption(args, "--sort");
    const querySuffix = sort ? `?sort_by=${encodeURIComponent(sort)}` : "";
    await performRequest(state, config, {
      method: "GET",
      path: `/twitter/tweets/${encodeURIComponent(tweetId)}/replies/${count}${querySuffix}`,
    });
    return;
  }

  if (action === "like" || action === "unlike" || action === "bookmark" || action === "unbookmark" || action === "retweet" || action === "unretweet") {
    const tweetId = requireCommandValue(args[2], `Usage: twexapi tweet ${action} <tweet_id>`);
    const mapping = {
      like: { method: "POST", path: `/twitter/tweets/${encodeURIComponent(tweetId)}/like` },
      unlike: { method: "DELETE", path: `/twitter/tweets/${encodeURIComponent(tweetId)}/like` },
      bookmark: { method: "POST", path: `/twitter/tweets/${encodeURIComponent(tweetId)}/bookmark` },
      unbookmark: { method: "DELETE", path: `/twitter/tweets/${encodeURIComponent(tweetId)}/bookmark` },
      retweet: { method: "POST", path: `/twitter/tweets/${encodeURIComponent(tweetId)}/retweet` },
      unretweet: { method: "DELETE", path: `/twitter/tweets/${encodeURIComponent(tweetId)}/retweet` },
    };
    await performRequest(state, config, {
      ...mapping[action],
      body: tweetActionBody(args, state, config),
    });
    return;
  }

  exitWithError(
    "Unknown tweet command.",
    "Use: tweet create | tweet quote | tweet lookup | tweet replies | tweet like | tweet unlike | tweet bookmark | tweet unbookmark | tweet retweet | tweet unretweet",
  );
}

async function handleUserCommand(state, config, args) {
  const action = args[1];
  const username = requireCommandValue(args[2], "Usage: twexapi user follow <username> | user unfollow <username>");
  const proxy = findOption(args, "--proxy");

  if (action === "follow") {
    await performRequest(state, config, {
      method: "POST",
      path: "/twitter/user/follow",
      body: {
        username,
        cookie: resolveCookieArg(args, state, config),
        ...(proxy ? { proxy } : {}),
      },
    });
    return;
  }

  if (action === "unfollow") {
    await performRequest(state, config, {
      method: "DELETE",
      path: "/twitter/user/follow",
      body: {
        username,
        cookie: resolveCookieArg(args, state, config),
        ...(proxy ? { proxy } : {}),
      },
    });
    return;
  }

  exitWithError("Unknown user command.", "Use: user follow | user unfollow");
}

async function handleGenericRequest(state, config, args) {
  const requestPath = requireCommandValue(args[0], "Usage: twexapi <path>");
  await performRequest(state, config, {
    method: state.method,
    path: requestPath,
    body: state.data,
  });
}

export async function runCommand(state, config) {
  const [command] = state.commandArgs;

  if (!command) {
    return false;
  }

  if (command.startsWith("/") || /^https?:\/\//i.test(command)) {
    await handleGenericRequest(state, config, state.commandArgs);
    return true;
  }

  if (command === "config") {
    await handleConfigCommand(state, config, state.commandArgs);
    return true;
  }

  if (command === "auth") {
    await handleAuthCommand(state, config, state.commandArgs);
    return true;
  }

  if (command === "users") {
    await handleUsersCommand(state, config, state.commandArgs);
    return true;
  }

  if (command === "about") {
    await handleAboutCommand(state, config, state.commandArgs);
    return true;
  }

  if (command === "search") {
    await handleSearchCommand(state, config, state.commandArgs);
    return true;
  }

  if (command === "followers") {
    await handleFollowersCommand(state, config, state.commandArgs);
    return true;
  }

  if (command === "following") {
    await handleFollowingCommand(state, config, state.commandArgs);
    return true;
  }

  if (command === "list") {
    await handleListCommand(state, config, state.commandArgs);
    return true;
  }

  if (command === "tweet") {
    await handleTweetCommand(state, config, state.commandArgs);
    return true;
  }

  if (command === "user") {
    await handleUserCommand(state, config, state.commandArgs);
    return true;
  }

  exitWithError(`Unknown command: ${command}`, "Run twexapi --help for usage.");
}
