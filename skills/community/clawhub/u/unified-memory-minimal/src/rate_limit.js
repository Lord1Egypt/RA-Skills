/**
 * Simple sliding window rate limiter for tool calls
 * P2-7: prevents burst of tool calls from overwhelming the system
 */

// Sliding window: max calls per key over time window
const callLog = new Map(); // key -> timestamp[]

export const RATE_LIMIT_WINDOW_MS = 10000; // 10 seconds
export const RATE_LIMIT_MAX_CALLS = 30;   // max calls per window per key

/**
 * Check if a call is allowed under rate limit
 * @param {string} key - identifier for the caller (session, agent, etc.)
 * @returns {{allowed: boolean, retryAfter: number|null}}
 */
export function checkRateLimit(key = 'default') {
  const now = Date.now();
  const windowStart = now - RATE_LIMIT_WINDOW_MS;
  
  // Clean old entries and count recent calls
  const timestamps = callLog.get(key) || [];
  const recent = timestamps.filter(t => t > windowStart);
  
  if (recent.length >= RATE_LIMIT_MAX_CALLS) {
    // Calculate when the oldest call in window will expire
    const oldest = Math.min(...recent);
    const retryAfter = Math.ceil((oldest + RATE_LIMIT_WINDOW_MS - now) / 1000);
    return { allowed: false, retryAfter: Math.max(1, retryAfter) };
  }
  
  recent.push(now);
  callLog.set(key, recent);
  return { allowed: true, retryAfter: null };
}

/**
 * Get current rate limit status for a key
 */
export function getRateLimitStatus(key = 'default') {
  const now = Date.now();
  const windowStart = now - RATE_LIMIT_WINDOW_MS;
  const timestamps = callLog.get(key) || [];
  const recent = timestamps.filter(t => t > windowStart);
  return {
    count: recent.length,
    limit: RATE_LIMIT_MAX_CALLS,
    remaining: Math.max(0, RATE_LIMIT_MAX_CALLS - recent.length),
    windowMs: RATE_LIMIT_WINDOW_MS,
  };
}

/**
 * Clean up expired entries (call periodically to prevent memory leak)
 */
export function cleanupRateLimit() {
  const now = Date.now();
  const windowStart = now - RATE_LIMIT_WINDOW_MS;
  for (const [key, timestamps] of callLog.entries()) {
    const recent = timestamps.filter(t => t > windowStart);
    if (recent.length === 0) {
      callLog.delete(key);
    } else {
      callLog.set(key, recent);
    }
  }
}
