#!/usr/bin/env node

const path = require("path");
require("dotenv").config({ path: path.join(__dirname, ".env") });

const crypto = require("crypto");
const http = require("http");
const https = require("https");
const { HttpsProxyAgent } = require("https-proxy-agent");
const { SocksProxyAgent } = require("socks-proxy-agent");
const { program } = require("commander");

function requiredEnv(name) {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing required env var: ${name}`);
  }
  return value;
}

function getCredentials() {
  return {
    consumerKey: requiredEnv("X_API_KEY"),
    consumerSecret: requiredEnv("X_API_SECRET"),
    accessToken: requiredEnv("X_ACCESS_TOKEN"),
    accessTokenSecret: requiredEnv("X_ACCESS_TOKEN_SECRET"),
  };
}

function getBaseUrls() {
  const preferred = process.env.X_API_BASE_URL || "https://api.twitter.com";
  const urls = [preferred, "https://api.x.com", "https://api.twitter.com"];
  return [...new Set(urls)];
}

function percentEncode(value) {
  return encodeURIComponent(String(value))
    .replace(/[!'()*]/g, (char) => `%${char.charCodeAt(0).toString(16).toUpperCase()}`);
}

function buildOAuthParams(credentials) {
  return {
    oauth_consumer_key: credentials.consumerKey,
    oauth_nonce: crypto.randomBytes(16).toString("hex"),
    oauth_signature_method: "HMAC-SHA1",
    oauth_timestamp: Math.floor(Date.now() / 1000).toString(),
    oauth_token: credentials.accessToken,
    oauth_version: "1.0",
  };
}

function normalizeParams(params) {
  return Object.keys(params)
    .sort()
    .map((key) => `${percentEncode(key)}=${percentEncode(params[key])}`)
    .join("&");
}

function buildSignature(method, baseUrl, params, credentials) {
  const parameterString = normalizeParams(params);
  const signatureBase = [
    method.toUpperCase(),
    percentEncode(baseUrl),
    percentEncode(parameterString),
  ].join("&");
  const signingKey = `${percentEncode(credentials.consumerSecret)}&${percentEncode(credentials.accessTokenSecret)}`;
  return crypto.createHmac("sha1", signingKey).update(signatureBase).digest("base64");
}

function buildAuthHeader(oauthParams) {
  const header = Object.keys(oauthParams)
    .sort()
    .map((key) => `${percentEncode(key)}="${percentEncode(oauthParams[key])}"`)
    .join(", ");
  return `OAuth ${header}`;
}

function resolveProxyAgent() {
  const proxyUrl = process.env.HTTPS_PROXY || process.env.HTTP_PROXY || process.env.ALL_PROXY || "";
  if (!proxyUrl) {
    return undefined;
  }
  if (proxyUrl.toLowerCase().startsWith("socks")) {
    return new SocksProxyAgent(proxyUrl);
  }
  return new HttpsProxyAgent(proxyUrl);
}

function requestJson(url, { method, headers, body, agent }) {
  const transport = url.protocol === "http:" ? http : https;
  return new Promise((resolve, reject) => {
    const req = transport.request(
      url,
      {
        method,
        headers,
        agent,
      },
      (res) => {
        const chunks = [];
        res.on("data", (chunk) => chunks.push(chunk));
        res.on("end", () => {
          const raw = Buffer.concat(chunks).toString("utf-8");
          let data = null;
          try {
            data = raw ? JSON.parse(raw) : null;
          } catch (_) {
            data = raw;
          }
          resolve({
            status: res.statusCode || 0,
            data,
          });
        });
      }
    );
    req.on("error", reject);
    if (body) {
      req.write(JSON.stringify(body));
    }
    req.end();
  });
}

async function signedRequest(method, path, { query = {}, body = null } = {}) {
  const credentials = getCredentials();
  const baseUrls = getBaseUrls();
  let lastError = null;
  const agent = resolveProxyAgent();

  for (const baseUrl of baseUrls) {
    const url = new URL(path, `${baseUrl}/`);
    for (const [key, value] of Object.entries(query)) {
      if (value !== undefined && value !== null && value !== "") {
        url.searchParams.set(key, value);
      }
    }

    const oauthParams = buildOAuthParams(credentials);
    const signatureParams = { ...oauthParams };
    for (const [key, value] of url.searchParams.entries()) {
      signatureParams[key] = value;
    }
    oauthParams.oauth_signature = buildSignature(method, url.origin + url.pathname, signatureParams, credentials);

    try {
      const { status, data } = await requestJson(url, {
        method,
        headers: {
          Authorization: buildAuthHeader(oauthParams),
          "Content-Type": "application/json",
          "User-Agent": "x-growth-operator/1.0",
        },
        body,
        agent,
      });

      if (status < 200 || status >= 300) {
        return {
          ok: false,
          baseUrl,
          status,
          data,
        };
      }

      return {
        ok: true,
        baseUrl,
        data,
      };
    } catch (error) {
      lastError = {
        ok: false,
        baseUrl,
        error: error && error.message ? error.message : String(error),
        code: error && error.code ? error.code : undefined,
        stack: error && error.stack ? error.stack : undefined,
      };
    }
  }

  return lastError || { ok: false, error: "Unknown request failure" };
}

async function postTweet(text, options) {
  const body = { text };
  if (options.replyTo) {
    body.reply = { in_reply_to_tweet_id: options.replyTo };
  }
  if (options.quote) {
    body.quote_tweet_id = options.quote;
  }

  const result = await signedRequest("POST", "/2/tweets", { body });
  if (!result.ok) {
    throw new Error(JSON.stringify(result));
  }

  console.log(JSON.stringify({
    ok: true,
    action: "post",
    baseUrl: result.baseUrl,
    id: result.data.data.id,
    url: `https://x.com/i/status/${result.data.data.id}`,
  }, null, 2));
}

async function postThread(parts) {
  const posted = [];
  let previousId = null;

  for (const part of parts) {
    const body = { text: part };
    if (previousId) {
      body.reply = { in_reply_to_tweet_id: previousId };
    }
    const result = await signedRequest("POST", "/2/tweets", { body });
    if (!result.ok) {
      throw new Error(JSON.stringify(result));
    }
    previousId = result.data.data.id;
    posted.push({
      id: previousId,
      url: `https://x.com/i/status/${previousId}`,
      text: part,
      baseUrl: result.baseUrl,
    });
  }

  console.log(JSON.stringify({
    ok: true,
    action: "thread",
    tweets: posted,
  }, null, 2));
}

async function getCurrentUser() {
  const result = await signedRequest("GET", "/2/users/me", {
    query: { "user.fields": "id,name,username,public_metrics,created_at" },
  });
  if (!result.ok) {
    throw new Error(JSON.stringify(result));
  }

  console.log(JSON.stringify({
    ok: true,
    action: "me",
    baseUrl: result.baseUrl,
    user: result.data.data,
  }, null, 2));
}

async function getTweet(tweetId) {
  const result = await signedRequest("GET", `/2/tweets/${tweetId}`, {
    query: {
      "tweet.fields": "author_id,conversation_id,created_at,entities,referenced_tweets,reply_settings,text",
    },
  });
  if (!result.ok) {
    throw new Error(JSON.stringify(result));
  }

  console.log(JSON.stringify({
    ok: true,
    action: "tweet",
    baseUrl: result.baseUrl,
    tweet: result.data.data,
  }, null, 2));
}

function safeError(error) {
  const message = error && error.message ? error.message : String(error);
  try {
    return JSON.parse(message);
  } catch (_) {
    return { ok: false, error: message };
  }
}

program
  .command("post")
  .requiredOption("--text <text>", "Tweet text")
  .option("--reply-to <id>", "Reply to tweet id")
  .option("--quote <id>", "Quote tweet id")
  .action(async (options) => {
    try {
      await postTweet(options.text, options);
    } catch (error) {
      console.error(JSON.stringify(safeError(error), null, 2));
      process.exit(1);
    }
  });

program
  .command("thread")
  .requiredOption("--parts <parts...>", "Thread parts")
  .action(async (options) => {
    try {
      await postThread(options.parts);
    } catch (error) {
      console.error(JSON.stringify(safeError(error), null, 2));
      process.exit(1);
    }
  });

program
  .command("me")
  .action(async () => {
    try {
      await getCurrentUser();
    } catch (error) {
      console.error(JSON.stringify(safeError(error), null, 2));
      process.exit(1);
    }
  });

program
  .command("tweet")
  .requiredOption("--id <id>", "Tweet id")
  .action(async (options) => {
    try {
      await getTweet(options.id);
    } catch (error) {
      console.error(JSON.stringify(safeError(error), null, 2));
      process.exit(1);
    }
  });

program.parse(process.argv);
