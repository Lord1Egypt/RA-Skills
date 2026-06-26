#!/usr/bin/env bash
# RateLint -- Rate Limiting Anti-Pattern Definitions
# 90 patterns across 6 categories, 15 patterns each.
#
# Format per line:
#   REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
#
# Severity levels:
#   critical -- Security vulnerability or guaranteed failure
#   high     -- Significant problem that causes incorrect behavior
#   medium   -- Moderate concern that should be addressed
#   low      -- Best practice suggestion
#
# IMPORTANT: All regexes use POSIX ERE syntax (grep -E compatible).
# - Use [[:space:]] instead of \s
# - Use [[:alnum:]] instead of \w
# - NEVER use pipe (|) for alternation inside regex -- it conflicts with
#   the field delimiter. Use separate patterns or character classes instead.

set -euo pipefail

# ===========================================================================
# RL -- Rate Limit Configuration (15 patterns: RL-001 to RL-015)
# Free tier
# ===========================================================================

declare -a RATELINT_RL_PATTERNS=(
  'app\.(get|post|put|patch|delete)\([[:space:]]*["\x27]/api/|medium|RL-001|API route without visible rate limiting middleware|Add rate limiting middleware (e.g., express-rate-limit) to all API routes'
  'router\.(get|post|put|patch|delete)\([[:space:]]*["\x27]/|medium|RL-002|Router endpoint without visible rate limiting middleware|Apply rate limiter middleware before route handlers'
  '@(Get|Post|Put|Patch|Delete)Mapping|medium|RL-003|Spring endpoint without visible rate limit annotation|Add @RateLimiter or use a rate limiting filter for this endpoint'
  'max[[:space:]]*:[[:space:]]*0[[:space:]]*[,}]|critical|RL-004|Rate limiter max set to 0 effectively disables rate limiting|Set a positive max value for meaningful rate limit enforcement'
  'windowMs[[:space:]]*:[[:space:]]*0|critical|RL-005|Rate limiter window set to 0ms disables time-based limiting|Set windowMs to a meaningful duration (e.g., 15 * 60 * 1000 for 15 minutes)'
  'rateLimit\([[:space:]]*\{[[:space:]]*\}|high|RL-006|Rate limiter initialized with empty configuration|Provide max, windowMs, and handler options to rate limiter'
  'X-RateLimit|low|RL-007|Reference to X-RateLimit headers -- ensure they are set on responses|Set X-RateLimit-Limit, X-RateLimit-Remaining, and X-RateLimit-Reset headers'
  'app\.use\([[:space:]]*cors|low|RL-008|CORS middleware without adjacent rate limiting|Apply rate limiting before or alongside CORS middleware'
  'unlimited[[:space:]]*[:=][[:space:]]*true|critical|RL-009|Rate limiting explicitly set to unlimited|Remove unlimited flag and set appropriate rate limits'
  'skipRateLimit|high|RL-010|Rate limiting is being skipped or bypassed|Remove rate limit bypass unless absolutely necessary for internal health checks'
  'RATE_LIMIT[[:space:]]*=[[:space:]]*-1|critical|RL-011|Rate limit set to -1 typically means unlimited|Set a positive rate limit value instead of -1'
  'disable[[:space:]]*rate[[:space:]]*limit|high|RL-012|Rate limiting is being explicitly disabled|Keep rate limiting enabled in production environments'
  'rateLimit[[:space:]]*=[[:space:]]*None|high|RL-013|Rate limit set to None disables throttling|Set a numeric rate limit value for API protection'
  'throttle_rate[[:space:]]*=[[:space:]]*["\x27]0/|critical|RL-014|Django throttle rate set to zero requests|Set a meaningful throttle rate (e.g., 100/hour)'
  'limiter\.skip|medium|RL-015|Rate limiter skip function may bypass protection for some requests|Ensure skip logic only excludes truly safe requests like health checks'
)

# ===========================================================================
# BF -- Brute Force Protection (15 patterns: BF-001 to BF-015)
# Free tier
# ===========================================================================

declare -a RATELINT_BF_PATTERNS=(
  '(post|put)\([[:space:]]*["\x27][^"]*login["\x27]|high|BF-001|Login endpoint without visible brute force protection|Add rate limiting and account lockout to login endpoints'
  '(post|put)\([[:space:]]*["\x27][^"]*signin["\x27]|high|BF-002|Sign-in endpoint without visible brute force protection|Add rate limiting and progressive delays to sign-in endpoints'
  '(post|put)\([[:space:]]*["\x27][^"]*password[^"]*reset["\x27]|high|BF-003|Password reset endpoint without visible rate limiting|Rate limit password reset to prevent email flooding (e.g., 3/hour)'
  '(post|put)\([[:space:]]*["\x27][^"]*forgot["\x27]|high|BF-004|Forgot password endpoint without visible rate limiting|Rate limit forgot password to prevent abuse (e.g., 5/hour per IP)'
  '(post|put)\([[:space:]]*["\x27][^"]*otp["\x27]|high|BF-005|OTP endpoint without visible rate limiting|Rate limit OTP requests to prevent brute force (e.g., 5/minute)'
  '(post|put)\([[:space:]]*["\x27][^"]*verify["\x27]|medium|BF-006|Verification endpoint without visible rate limiting|Rate limit verification attempts to prevent enumeration'
  '(post|put)\([[:space:]]*["\x27][^"]*register["\x27]|medium|BF-007|Registration endpoint without visible rate limiting|Rate limit registration to prevent mass account creation'
  '(post|put)\([[:space:]]*["\x27][^"]*signup["\x27]|medium|BF-008|Signup endpoint without visible rate limiting|Rate limit signup to prevent spam registrations'
  'maxLoginAttempts[[:space:]]*=[[:space:]]*[0-9]{3,}|high|BF-009|Login attempt limit set too high (100+ attempts allowed)|Set maxLoginAttempts to 5-10 to prevent brute force'
  'lockout[[:space:]]*=[[:space:]]*false|critical|BF-010|Account lockout explicitly disabled|Enable account lockout after repeated failed login attempts'
  'LOCKOUT_TIME[[:space:]]*=[[:space:]]*0|critical|BF-011|Account lockout duration set to 0 (no lockout)|Set lockout duration to at least 15 minutes after failed attempts'
  '(post|put)\([[:space:]]*["\x27][^"]*token[^"]*refresh["\x27]|medium|BF-012|Token refresh endpoint without visible rate limiting|Rate limit token refresh to prevent token abuse'
  '(post|put)\([[:space:]]*["\x27][^"]*2fa["\x27]|high|BF-013|2FA endpoint without visible rate limiting|Rate limit 2FA attempts to prevent code brute force (e.g., 5/minute)'
  'failedAttempts[[:space:]]*>[[:space:]]*[0-9]{3,}|high|BF-014|Failed attempt threshold too high (100+ before action)|Set failed attempt threshold to 5-10 before lockout or CAPTCHA'
  'authenticate\([[:space:]]*[[:alnum:]]+[[:space:]]*,[[:space:]]*[[:alnum:]]+[[:space:]]*\)|medium|BF-015|Authentication function without visible attempt tracking|Add login attempt tracking and progressive delays to auth functions'
)

# ===========================================================================
# TH -- Throttling & Backpressure (15 patterns: TH-001 to TH-015)
# Pro tier
# ===========================================================================

declare -a RATELINT_TH_PATTERNS=(
  'addEventListener\([[:space:]]*["\x27]scroll["\x27]|medium|TH-001|Scroll event listener without visible debounce or throttle|Wrap scroll handler in throttle (e.g., lodash.throttle, 100ms)'
  'addEventListener\([[:space:]]*["\x27]resize["\x27]|medium|TH-002|Resize event listener without visible debounce or throttle|Wrap resize handler in debounce (e.g., lodash.debounce, 250ms)'
  'addEventListener\([[:space:]]*["\x27]mousemove["\x27]|medium|TH-003|Mousemove event listener without visible throttle|Throttle mousemove handlers to prevent excessive calls (e.g., 16ms)'
  'addEventListener\([[:space:]]*["\x27]input["\x27]|low|TH-004|Input event listener -- consider debouncing for search or API calls|Debounce input handlers that trigger API calls (e.g., 300ms)'
  'addEventListener\([[:space:]]*["\x27]keyup["\x27]|low|TH-005|Keyup event listener -- consider debouncing for typeahead or search|Debounce keyup handlers that trigger network requests'
  'onChange[[:space:]]*=[[:space:]]*\{|low|TH-006|React onChange handler -- consider debouncing for expensive operations|Use useDebouncedCallback or lodash.debounce for onChange with API calls'
  'onScroll[[:space:]]*=[[:space:]]*\{|medium|TH-007|React onScroll handler without visible throttle|Use throttle on onScroll to prevent jank and excessive re-renders'
  'webhook[[:space:]]*endpoint|medium|TH-008|Webhook endpoint without visible throttle or deduplication|Add request deduplication and rate limiting to webhook handlers'
  'socket\.on\([[:space:]]*["\x27]|medium|TH-009|WebSocket event handler without visible throttle|Throttle incoming WebSocket messages to prevent flooding'
  'EventEmitter|low|TH-010|EventEmitter usage -- ensure high-frequency events are throttled|Add throttling for events that may fire rapidly (e.g., data streams)'
  'setInterval\([[:space:]]*[[:alnum:]]+[[:space:]]*,[[:space:]]*[0-9]{1,2}\)|high|TH-011|setInterval with very short delay (under 100ms) may overwhelm resources|Use requestAnimationFrame or increase interval to 100ms+'
  'setTimeout\([[:space:]]*[[:alnum:]]+[[:space:]]*,[[:space:]]*0\)|low|TH-012|setTimeout with 0ms delay -- ensure this is intentional and not in a loop|Verify zero-delay timeout is not called recursively or in tight loops'
  'process\.nextTick|low|TH-013|process.nextTick in a loop can starve I/O|Use setImmediate instead of nextTick for recursive async patterns'
  'requestAnimationFrame|low|TH-014|requestAnimationFrame -- ensure callback does not trigger additional frames unbounded|Guard rAF callbacks to prevent runaway frame requests'
  'while[[:space:]]*\([[:space:]]*true[[:space:]]*\)|high|TH-015|Infinite loop without visible yield or throttle mechanism|Add sleep, yield, or throttle to prevent CPU starvation in tight loops'
)

# ===========================================================================
# BP -- Backoff & Retry (15 patterns: BP-001 to BP-015)
# Pro tier
# ===========================================================================

declare -a RATELINT_BP_PATTERNS=(
  'retry[[:space:]]*:[[:space:]]*[0-9]{3,}|high|BP-001|Retry count over 100 may cause retry storms on failing services|Set retry count to 3-5 with exponential backoff and jitter'
  'maxRetries[[:space:]]*=[[:space:]]*-1|critical|BP-002|maxRetries set to -1 (infinite) will retry forever on persistent failures|Set finite maxRetries (3-5) with exponential backoff'
  'MAX_RETRIES[[:space:]]*=[[:space:]]*[0-9]{3,}|high|BP-003|MAX_RETRIES over 100 creates retry storm risk on cascading failures|Set MAX_RETRIES to 3-5 and use circuit breaker pattern'
  'retryForever|critical|BP-004|Retry forever will never stop on persistent failures -- causes resource waste|Use finite retries with dead letter queue for persistent failures'
  'retryDelay[[:space:]]*:[[:space:]]*[0-9]{1,3}[[:space:]]*[,}]|medium|BP-005|Fixed retry delay without backoff -- can cause thundering herd|Use exponential backoff with jitter instead of fixed retry delay'
  'sleep\([[:space:]]*[0-9]+[[:space:]]*\)[[:space:]]*.*retry|medium|BP-006|Fixed sleep before retry -- lacks exponential backoff|Implement exponential backoff: delay = baseDelay * 2^attempt + jitter'
  'retryWhen|low|BP-007|retryWhen operator -- ensure it includes backoff and max attempts|Add exponential backoff and max retry count to retryWhen logic'
  'catch[[:space:]]*\{[^}]*retry|medium|BP-008|Catch block with retry -- ensure backoff and max attempts are used|Add exponential backoff and retry counter to catch-and-retry logic'
  'except[[:space:]]*.*retry|medium|BP-009|Exception handler with retry -- ensure backoff and max attempts|Add exponential backoff and max retry limit to exception retry logic'
  'retry[[:space:]]*=[[:space:]]*True|medium|BP-010|Boolean retry flag without visible max attempts or backoff|Replace boolean retry with configurable maxRetries and backoff strategy'
  'Retry-After|low|BP-011|Retry-After header reference -- ensure it is respected by clients|Parse and honor Retry-After header value before retrying requests'
  'idempotency[Kk]ey|low|BP-012|Idempotency key reference -- verify retries include idempotency keys|Include idempotency key in all retried requests to prevent duplicates'
  'jitter|low|BP-013|Jitter reference -- verify jitter is applied to retry backoff|Add random jitter to backoff delay to prevent thundering herd'
  'circuitBreaker|low|BP-014|Circuit breaker reference -- verify it is properly integrated with retries|Configure circuit breaker thresholds (failure rate, timeout, half-open count)'
  'while[[:space:]]*\([[:space:]]*[!]*[[:space:]]*success|high|BP-015|Retry loop without visible max attempts -- may loop forever|Add max attempt counter and exponential backoff to retry loops'
)

# ===========================================================================
# QO -- Queue & Buffer Overflow (15 patterns: QO-001 to QO-015)
# Team tier
# ===========================================================================

declare -a RATELINT_QO_PATTERNS=(
  'queue[[:space:]]*=[[:space:]]*\[\]|medium|QO-001|Array used as queue without visible max size limit|Use a bounded queue with maxSize to prevent unbounded memory growth'
  'queue\.push\(|medium|QO-002|Pushing to queue without visible size check|Check queue length before push and reject or drop when at capacity'
  'buffer[[:space:]]*=[[:space:]]*\[\]|medium|QO-003|Array used as buffer without visible max size limit|Add max buffer size and handle overflow (drop oldest or reject new)'
  'buffer\.push\(|medium|QO-004|Pushing to buffer without visible size check|Check buffer length before push to prevent unbounded memory growth'
  'pending[[:space:]]*=[[:space:]]*\[\]|medium|QO-005|Pending array without visible max size -- may grow unbounded|Add max pending limit and handle overflow condition'
  'messages[[:space:]]*=[[:space:]]*\[\]|medium|QO-006|Message array without visible max size -- may grow unbounded|Bound message buffer and implement overflow strategy (drop or persist)'
  'maxQueue[[:space:]]*=[[:space:]]*0|critical|QO-007|Queue max size set to 0 -- may mean unlimited depending on library|Set maxQueue to a positive value for bounded queue behavior'
  'MAX_QUEUE[[:space:]]*=[[:space:]]*-1|critical|QO-008|Queue max set to -1 (unlimited) allows unbounded memory growth|Set a finite MAX_QUEUE value based on available memory and throughput'
  'deadLetter|low|QO-009|Dead letter reference -- ensure DLQ is properly configured for failed messages|Configure dead letter queue with proper retry and monitoring'
  'prefetch[[:space:]]*=[[:space:]]*0|high|QO-010|AMQP prefetch set to 0 (unlimited) can overwhelm consumers|Set prefetch to a reasonable value (10-100) for flow control'
  'prefetchCount[[:space:]]*:[[:space:]]*0|high|QO-011|Prefetch count of 0 means unlimited messages sent to consumer|Set prefetchCount to limit unacknowledged messages (e.g., 10-50)'
  'cache\.[[:alnum:]]*\([[:space:]]*[[:alnum:]]|low|QO-012|Cache operation without visible TTL or max entries|Set TTL and maxEntries on caches to prevent unbounded memory growth'
  'new[[:space:]]+Map\(\)|low|QO-013|Map without visible max size -- can grow without bound|Use LRU cache or add periodic cleanup to prevent unbounded Map growth'
  'new[[:space:]]+Set\(\)|low|QO-014|Set without visible max size -- can grow without bound|Add max size tracking or use bounded collection to prevent memory leaks'
  'accumulator\.[[:alnum:]]*\(|medium|QO-015|Accumulator operation without visible flush or size limit|Add periodic flush and max size to accumulators to prevent overflow'
)

# ===========================================================================
# DD -- DDoS & Abuse Prevention (15 patterns: DD-001 to DD-015)
# Team tier
# ===========================================================================

declare -a RATELINT_DD_PATTERNS=(
  'Access-Control-Allow-Origin[[:space:]]*:[[:space:]]*["\x27]\*["\x27]|critical|DD-001|CORS wildcard origin allows any site to make cross-origin requests|Restrict Access-Control-Allow-Origin to specific trusted domains'
  'cors\([[:space:]]*\)|high|DD-002|CORS middleware with no options allows all origins by default|Configure CORS with explicit origin whitelist and allowed methods'
  'origin[[:space:]]*:[[:space:]]*["\x27]\*["\x27]|critical|DD-003|Wildcard origin in CORS config allows unrestricted cross-origin access|Replace wildcard with explicit list of allowed origins'
  'X-Forwarded-For|medium|DD-004|X-Forwarded-For header usage without visible proxy trust validation|Validate X-Forwarded-For only behind trusted proxies to prevent IP spoofing'
  'trust[[:space:]]*proxy|medium|DD-005|Trust proxy setting -- ensure only known proxies are trusted|Set trust proxy to specific proxy IPs rather than true or a high number'
  'bodyParser\.json\(\)|medium|DD-006|JSON body parser without visible size limit allows large payload abuse|Set limit option: bodyParser.json({ limit: 100kb }) to prevent large payloads'
  'bodyParser\.urlencoded\(\)|medium|DD-007|URL-encoded body parser without visible size limit|Set limit and parameterLimit options to prevent oversized form submissions'
  'express\.json\(\)|medium|DD-008|Express JSON parser without visible size limit allows payload abuse|Set limit option: express.json({ limit: 100kb }) to restrict payload size'
  'express\.urlencoded\(\)|medium|DD-009|Express URL-encoded parser without visible size limit|Add limit and parameterLimit options to prevent abuse via oversized forms'
  'multer\(\)|high|DD-010|File upload middleware without visible size or count limits|Configure limits: multer({ limits: { fileSize: 5MB, files: 5 } })'
  'upload\.single\(|medium|DD-011|File upload endpoint -- ensure file size limit is configured|Set maxFileSize limit on upload middleware to prevent storage abuse'
  'upload\.array\(|high|DD-012|Multi-file upload without visible count or size limits|Set file count limit and per-file size limit on array upload endpoints'
  'helmet|low|DD-013|Helmet reference -- verify all security headers are enabled|Enable all helmet middleware options including HSTS, CSP, and X-Frame-Options'
  'allowedHosts[[:space:]]*:[[:space:]]*\[|low|DD-014|Allowed hosts configuration -- verify it restricts to known domains|Set allowedHosts to only your production and staging domains'
  'ipBan|low|DD-015|IP banning reference -- verify ban logic includes expiry and logging|Implement IP ban with TTL expiry, logging, and admin review process'
)

# ===========================================================================
# Utility Functions
# ===========================================================================

# Count total patterns
ratelint_pattern_count() {
  local count=0
  count=$((count + ${#RATELINT_RL_PATTERNS[@]}))
  count=$((count + ${#RATELINT_BF_PATTERNS[@]}))
  count=$((count + ${#RATELINT_TH_PATTERNS[@]}))
  count=$((count + ${#RATELINT_BP_PATTERNS[@]}))
  count=$((count + ${#RATELINT_QO_PATTERNS[@]}))
  count=$((count + ${#RATELINT_DD_PATTERNS[@]}))
  echo "$count"
}

# Count patterns in a specific category
ratelint_category_count() {
  local cat="$1"
  case "$cat" in
    RL) echo "${#RATELINT_RL_PATTERNS[@]}" ;;
    BF) echo "${#RATELINT_BF_PATTERNS[@]}" ;;
    TH) echo "${#RATELINT_TH_PATTERNS[@]}" ;;
    BP) echo "${#RATELINT_BP_PATTERNS[@]}" ;;
    QO) echo "${#RATELINT_QO_PATTERNS[@]}" ;;
    DD) echo "${#RATELINT_DD_PATTERNS[@]}" ;;
    *)  echo "0" ;;
  esac
}

# Get the bash array name for a category code
get_ratelint_patterns_for_category() {
  local cat="$1"
  case "$cat" in
    RL) echo "RATELINT_RL_PATTERNS" ;;
    BF) echo "RATELINT_BF_PATTERNS" ;;
    TH) echo "RATELINT_TH_PATTERNS" ;;
    BP) echo "RATELINT_BP_PATTERNS" ;;
    QO) echo "RATELINT_QO_PATTERNS" ;;
    DD) echo "RATELINT_DD_PATTERNS" ;;
    *)  echo "" ;;
  esac
}

# Get human-readable label for a category code
get_ratelint_category_label() {
  local cat="$1"
  case "$cat" in
    RL) echo "Rate Limit Configuration" ;;
    BF) echo "Brute Force Protection" ;;
    TH) echo "Throttling & Backpressure" ;;
    BP) echo "Backoff & Retry" ;;
    QO) echo "Queue & Buffer Overflow" ;;
    DD) echo "DDoS & Abuse Prevention" ;;
    *)  echo "Unknown" ;;
  esac
}

# Get space-separated list of category codes available at a given tier level.
# Tier levels: 0=free (RL, BF), 1=pro (RL, BF, TH, BP), 2/3=team/enterprise (all)
get_ratelint_categories_for_tier() {
  local tier_level="$1"
  case "$tier_level" in
    0) echo "RL BF" ;;
    1) echo "RL BF TH BP" ;;
    2|3) echo "RL BF TH BP QO DD" ;;
    *) echo "RL BF" ;;
  esac
}

# Severity to point deduction mapping
severity_to_points() {
  local severity="$1"
  case "$severity" in
    critical) echo 25 ;;
    high)     echo 15 ;;
    medium)   echo  8 ;;
    low)      echo  3 ;;
    *)        echo  0 ;;
  esac
}

# Validate that a string is a known category code
is_valid_ratelint_category() {
  local cat="$1"
  case "$cat" in
    RL|BF|TH|BP|QO|DD) return 0 ;;
    *) return 1 ;;
  esac
}

# List patterns in a given category or "all"
ratelint_list_patterns() {
  local filter="${1:-all}"

  local categories="RL BF TH BP QO DD"
  if [[ "$filter" != "all" ]]; then
    filter=$(echo "$filter" | tr '[:lower:]' '[:upper:]')
    categories="$filter"
  fi

  for cat in $categories; do
    local label
    label=$(get_ratelint_category_label "$cat")
    echo -e "${BOLD:-}--- ${cat}: ${label} ---${NC:-}"

    local arr_name
    arr_name=$(get_ratelint_patterns_for_category "$cat")
    [[ -z "$arr_name" ]] && continue

    local -n _arr="$arr_name"
    for entry in "${_arr[@]}"; do
      IFS='|' read -r regex severity check_id description recommendation <<< "$entry"
      local sev_upper
      sev_upper=$(echo "$severity" | tr '[:lower:]' '[:upper:]')
      echo "  [$sev_upper] $check_id: $description"
    done
    echo ""
  done
}
