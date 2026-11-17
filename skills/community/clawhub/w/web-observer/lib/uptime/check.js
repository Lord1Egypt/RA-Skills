/**
 * Performing one uptime check.
 *
 * This is the only module in Web Observer that makes an outbound request of its
 * own, and every request it makes is checked against the allowlist first, on the
 * initial URL and again on every redirect hop. The allowlist is derived from the
 * user's configured watch URLs and nothing else, so a redirect cannot take a
 * request, or a configured header, to a host the user never named.
 *
 * Nothing a server sends is copied into a failure detail. A body is measured,
 * never quoted, and a header is never echoed: a check runs against a site that
 * may be compromised or simply misconfigured, its output is delivered straight
 * into a chat, and a detail line has no business carrying whatever a stranger
 * put in a response.
 */
import { allowedUrl, statusMatches, describeStatusExpectations } from "../config.js";
/**
 * How much of a body is read when a body expectation exists.
 *
 * A health endpoint's answer is small; a home page is not, and an unbounded read
 * of a page being served by a broken origin is a way to run out of memory. A
 * match beyond this point is reported as a mismatch, and the detail says the
 * body was truncated so the number is never mistaken for a verdict on the whole
 * document.
 */
export const MAX_BODY_BYTES = 1_048_576;
/** Node system error codes that mean the name never resolved. */
const DNS_CODES = new Set(["ENOTFOUND", "EAI_AGAIN", "EAI_NODATA", "EAI_NONAME"]);
/** Codes that mean the connection was actively refused or reset. */
const REFUSED_CODES = new Set(["ECONNREFUSED", "ECONNRESET", "EHOSTUNREACH", "ENETUNREACH"]);
/** Codes that mean the transport gave up on time. */
const TIMEOUT_CODES = new Set([
    "ETIMEDOUT",
    "UND_ERR_CONNECT_TIMEOUT",
    "UND_ERR_HEADERS_TIMEOUT",
    "UND_ERR_BODY_TIMEOUT",
]);
/**
 * Turn a thrown request error into one of the fixed reasons.
 *
 * Node's fetch wraps the real cause, so the chain is walked rather than the
 * outer message read: the outer message is the useless `fetch failed`.
 *
 * @returns The reason, and one line naming what happened. The line is built from
 *   the error's own code and message, both of which describe the transport, not
 *   the response body.
 */
export function classifyError(error) {
    const seen = new Set();
    let current = error;
    let name = "";
    let code = "";
    let message = "";
    while (current !== null && current !== undefined && !seen.has(current)) {
        seen.add(current);
        if (current instanceof Error) {
            if (name === "")
                name = current.name;
            if (message === "")
                message = current.message;
            const candidate = current.code;
            if (code === "" && typeof candidate === "string")
                code = candidate;
            current = current.cause;
            continue;
        }
        if (typeof current === "object") {
            const candidate = current.code;
            if (code === "" && typeof candidate === "string")
                code = candidate;
        }
        break;
    }
    if (name === "AbortError" || name === "TimeoutError") {
        return { reason: "timeout", detail: "no response before the timeout" };
    }
    if (TIMEOUT_CODES.has(code)) {
        return { reason: "timeout", detail: `the connection timed out (${code})` };
    }
    if (DNS_CODES.has(code)) {
        return { reason: "dns", detail: `the host name did not resolve (${code})` };
    }
    if (REFUSED_CODES.has(code)) {
        return { reason: "connection-refused", detail: `the connection failed (${code})` };
    }
    if (/^(ERR_TLS|ERR_SSL|CERT_|DEPTH_ZERO|SELF_SIGNED|UNABLE_TO_VERIFY|HOSTNAME_MISMATCH)/.test(code)) {
        return { reason: "tls", detail: `the TLS handshake failed (${code})` };
    }
    const suffix = code !== "" ? ` (${code})` : "";
    return {
        reason: "network",
        // The message rather than the code, because an unclassified failure is
        // exactly the case where the code alone says nothing useful.
        detail: `the request failed${suffix}${message !== "" ? `: ${message}` : ""}`,
    };
}
/**
 * Read at most {@link MAX_BODY_BYTES} of a response body as text.
 *
 * Reads through the stream rather than calling `response.text()` so a very
 * large or endless body cannot exhaust memory.
 */
async function readBoundedText(response) {
    const body = response.body;
    if (!body)
        return { text: "", truncated: false };
    const reader = body.getReader();
    const chunks = [];
    let total = 0;
    let truncated = false;
    try {
        for (;;) {
            const { done, value } = await reader.read();
            if (done)
                break;
            if (!value)
                continue;
            total += value.byteLength;
            if (total > MAX_BODY_BYTES) {
                chunks.push(value.subarray(0, value.byteLength - (total - MAX_BODY_BYTES)));
                truncated = true;
                break;
            }
            chunks.push(value);
        }
    }
    finally {
        // Releasing matters even on the truncated path: an unreleased reader holds
        // the socket open, and a monitor that leaks one socket per check is a
        // monitor that stops working after a while.
        await reader.cancel().catch(() => undefined);
    }
    const merged = new Uint8Array(chunks.reduce((sum, chunk) => sum + chunk.byteLength, 0));
    let offset = 0;
    for (const chunk of chunks) {
        merged.set(chunk, offset);
        offset += chunk.byteLength;
    }
    return { text: new TextDecoder().decode(merged), truncated };
}
/** Discard a body that will not be read, so the connection can be reused. */
async function discardBody(response) {
    await response.body?.cancel().catch(() => undefined);
}
/**
 * Whether a status is one the redirect logic should act on.
 *
 * 304 is excluded: it is a cache answer, not a relocation, and it carries no
 * Location to follow.
 */
function isRedirect(status) {
    return status === 301 || status === 302 || status === 303 || status === 307 || status === 308;
}
/** One request, plus however many redirect hops the watch permits. */
async function attemptOnce(watch, allowlist, deps, signal) {
    let url = watch.url;
    for (let hop = 0;; hop += 1) {
        // Re-checked on every hop, including the first. The first is already
        // guaranteed by config validation; checking it here as well is what makes
        // the guarantee a property of the request path rather than of the caller.
        const target = allowedUrl(url, allowlist);
        if (!target) {
            return {
                ok: false,
                reason: "redirect-off-allowlist",
                detail: hop === 0
                    ? `${url} is not on the allowlist built from the configured watch URLs`
                    : `a redirect pointed at ${safeHost(url)}, which is not a host any watch configures. ` +
                        "Add it as its own watch if that redirect is expected",
                status: null,
                url,
            };
        }
        // Configured headers go only to the watch's own host. The allowlist is
        // shared by every watch, so without this a redirect could carry one watch's
        // credential to another watch's host.
        const sameHost = target.host.toLowerCase() === new URL(watch.url).host.toLowerCase();
        let response;
        try {
            response = await deps.fetch(target.toString(), {
                method: watch.method,
                headers: sameHost ? watch.headers : {},
                redirect: "manual",
                signal,
            });
        }
        catch (error) {
            return { ok: false, ...classifyError(error), status: null, url: target.toString() };
        }
        const status = response.status;
        if (isRedirect(status) && hop < watch.followRedirects) {
            const location = response.headers.get("location");
            await discardBody(response);
            if (location === null || location.trim() === "") {
                return {
                    ok: false,
                    reason: "network",
                    detail: `a ${status} carried no Location header to follow`,
                    status,
                    url: target.toString(),
                };
            }
            let next;
            try {
                next = new URL(location, target).toString();
            }
            catch {
                return {
                    ok: false,
                    reason: "network",
                    detail: `a ${status} carried a Location that is not a URL`,
                    status,
                    url: target.toString(),
                };
            }
            // The allowlist compares hosts, and https and http share one. A downgrade
            // would send any configured header in the clear, so it is refused here.
            if (target.protocol === "https:" && new URL(next).protocol === "http:") {
                return {
                    ok: false,
                    reason: "redirect-off-allowlist",
                    detail: `a redirect downgraded ${safeHost(next)} from https to http, which is never ` +
                        "followed. Point the watch at the http URL if that is expected",
                    status,
                    url: target.toString(),
                };
            }
            url = next;
            continue;
        }
        return await evaluate(watch, response, target.toString());
    }
}
/**
 * The host of a URL, or a placeholder.
 *
 * Only the host is ever quoted from a redirect. A full Location can carry a
 * query string a stranger chose, and this string ends up in a chat message.
 */
function safeHost(url) {
    try {
        return new URL(url).host;
    }
    catch {
        return "an unparseable address";
    }
}
/** Test one response against a watch's expectations. */
async function evaluate(watch, response, url) {
    const status = response.status;
    if (!statusMatches(status, watch.expectStatus)) {
        await discardBody(response);
        return {
            ok: false,
            reason: "status-mismatch",
            detail: `returned ${status}, expected ${describeStatusExpectations(watch.expectStatus)}`,
            status,
            url,
        };
    }
    const wantsBody = watch.expectBody !== null || watch.expectBodyRegex !== null;
    if (!wantsBody) {
        await discardBody(response);
        return { ok: true, status, url };
    }
    const { text, truncated } = await readBoundedText(response);
    const truncationNote = truncated ? ` (only the first ${MAX_BODY_BYTES} bytes were read)` : "";
    if (watch.expectBody !== null && !text.includes(watch.expectBody)) {
        return {
            ok: false,
            reason: "body-mismatch",
            detail: `returned ${status} but the body does not contain ${JSON.stringify(watch.expectBody)}` +
                ` (${text.length} characters read)${truncationNote}`,
            status,
            url,
        };
    }
    if (watch.expectBodyRegex !== null && !new RegExp(watch.expectBodyRegex).test(text)) {
        return {
            ok: false,
            reason: "body-mismatch",
            detail: `returned ${status} but the body does not match /${watch.expectBodyRegex}/` +
                ` (${text.length} characters read)${truncationNote}`,
            status,
            url,
        };
    }
    return { ok: true, status, url };
}
/**
 * Check one watch, retrying within the check as configured.
 *
 * A check succeeds as soon as any attempt succeeds, so `attempts` is the guard
 * against a single dropped packet. The reason reported on failure is the last
 * attempt's: an intermittent failure that changes character between attempts is
 * best described by the most recent one, and the count of attempts spent is
 * reported alongside so a reader knows it was not a one-off.
 *
 * @param watch The watch to check, with defaults already applied.
 * @param allowlist From `allowlistOf`, enforced on every request.
 * @param deps Injected clock, sleep and fetch.
 */
export async function performCheck(watch, allowlist, deps) {
    const startedAt = deps.now();
    let last = null;
    for (let attempt = 1; attempt <= watch.attempts; attempt += 1) {
        if (attempt > 1 && watch.retryDelayMs > 0) {
            await deps.sleep(watch.retryDelayMs);
        }
        // One signal per attempt, so the timeout is the per-request budget rather
        // than a budget for all of them together. `AbortSignal.timeout` does not
        // hold the event loop open, so a finished run still exits promptly.
        const signal = AbortSignal.timeout(watch.timeoutMs);
        last = await attemptOnce(watch, allowlist, deps, signal);
        if (last.ok) {
            return {
                ok: true,
                status: last.status,
                durationMs: deps.now() - startedAt,
                attemptsUsed: attempt,
                url: last.url,
            };
        }
        // A misconfigured or hostile redirect will not fix itself in ten seconds,
        // and retrying it would only make more requests to a host the user did not
        // configure. Fail immediately.
        if (last.reason === "redirect-off-allowlist") {
            return {
                ok: false,
                reason: last.reason,
                detail: last.detail,
                status: last.status,
                durationMs: deps.now() - startedAt,
                attemptsUsed: attempt,
                url: last.url,
            };
        }
    }
    if (last === null) {
        // Unreachable: config guarantees attempts >= 1. Handled rather than
        // asserted, because a thrown TypeError here would be reported as the site
        // being down.
        return {
            ok: false,
            reason: "network",
            detail: "no attempt was made",
            status: null,
            durationMs: deps.now() - startedAt,
            attemptsUsed: 0,
            url: watch.url,
        };
    }
    return {
        ok: false,
        reason: last.ok ? "network" : last.reason,
        detail: last.ok ? "" : last.detail,
        status: last.ok ? null : last.status,
        durationMs: deps.now() - startedAt,
        attemptsUsed: watch.attempts,
        url: last.url,
    };
}
/** The real dependencies, used by the CLI. */
export const liveDeps = {
    fetch: (url, init) => fetch(url, init),
    now: () => Date.now(),
    sleep: (ms) => new Promise((resolve) => {
        // Deliberately **not** unref'd. An unref'd timer does not keep the event
        // loop alive, so with nothing else pending Node would exit while this
        // promise was still awaited: the retry would never run, the process would
        // report success, and the delay would exist only in the documentation.
        // A retry pause is work to be waited for, not background upkeep.
        setTimeout(resolve, ms);
    }),
};
