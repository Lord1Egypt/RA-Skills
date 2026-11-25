// Bind public receipt requests to the explicitly configured WordPress site.
function siteUrl(value) {
  const url = new URL(value);
  if (!["https:", "http:"].includes(url.protocol) || url.username || url.password) {
    throw new Error("Expected an HTTP(S) site URL without embedded credentials");
  }
  return url;
}

function receiptUrl(value, site) {
  const url = siteUrl(value);
  if (url.origin !== siteUrl(site).origin) throw new Error("Receipt URL must match the configured site origin");
  url.hash = "";
  return url.href;
}

function requestOptions() {
  return { redirect: "error", signal: AbortSignal.timeout(30000) };
}

module.exports = { siteUrl, receiptUrl, requestOptions };
