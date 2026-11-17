#!/usr/bin/env bash
# setup_domain.sh — Domain availability check, purchase, and DNS configuration
# Usage:
#   MODE=check   DOMAIN=example.com bash setup_domain.sh
#   MODE=price   DOMAIN=example.com [YEARS=1] bash setup_domain.sh   # real registration price; exits 40 if not confirmable
#   MODE=suggest PROJECT=myapp [SUFFIXES="com net org online site top tech me co"] bash setup_domain.sh  # pick default my-<project>.<tld>
#   MODE=buy     DOMAIN=example.com REGISTRANT_PROFILE_ID=12345 bash setup_domain.sh
#   MODE=dns     DOMAIN=example.com IP=1.2.3.4 bash setup_domain.sh
#   MODE=verify  DOMAIN=example.com IP=1.2.3.4 bash setup_domain.sh
#   MODE=wait-delegation DOMAIN=example.com bash setup_domain.sh   # poll until the TLD delegates NS to AliDNS (new domains)
#   MODE=profiles bash setup_domain.sh
#   MODE=create-profile EMAIL=x REGISTRANT_NAME=x COUNTRY=x PROVINCE=x CITY=x \
#        ADDRESS=x POSTAL_CODE=x TEL_AREA=x TELEPHONE=x bash setup_domain.sh
#   MODE=send-email-verification EMAIL=x bash setup_domain.sh
#   MODE=check-email-verification EMAIL=x bash setup_domain.sh
#
# Environment:
#   DOMAIN_ENDPOINT — override domain API endpoint (default: domain.aliyuncs.com)
#   DNS_ENDPOINT    — override alidns API endpoint (default: auto)
set -uo pipefail

DOMAIN_ENDPOINT="${DOMAIN_ENDPOINT:-domain.aliyuncs.com}"
DOMAIN_API_VERSION="${DOMAIN_API_VERSION:-2018-01-29}"

err() { echo "ERROR: $*" >&2; exit 1; }
info() { echo "[domain] $*" >&2; }

# Default record TTL. AliDNS free/basic plans reject TTL < 600 (InvalidTTL.Malformed);
# 600 is the safe minimum. Override with RECORD_TTL if you have a paid plan.
RECORD_TTL="${RECORD_TTL:-600}"

# Run an alidns record command; on a TTL-range error, retry once WITHOUT --TTL so
# the account default applies (never let a TTL constraint block record creation).
alidns_with_ttl_fallback() {
  local out rc
  out=$(aliyun alidns "$@" --TTL "$RECORD_TTL" 2>&1); rc=$?
  if [ $rc -ne 0 ] && echo "$out" | grep -qiE "TTL"; then
    info "TTL=$RECORD_TTL rejected; retrying with the account default TTL"
    out=$(aliyun alidns "$@" 2>&1); rc=$?
  fi
  printf '%s' "$out"
  return $rc
}

MODE="${MODE:?missing MODE (check|price|suggest|buy|dns|verify|wait-delegation|profiles|create-profile|send-email-verification|check-email-verification)}"

case "$MODE" in
  # ─── Suggest a default registrable domain ────────────────────────────────
  # Builds "my-<project>.<tld>" and probes candidate TLDs in priority
  # order, returning the FIRST registrable one.
  # Output (stdout, JSON): {"suggested":"my-myapp.com","available":true,
  #   "tld":"com","candidates_tried":["com"],"format":"my-<project>.<tld>"}
  # Exits 41 if none of the candidates is registrable.
  # Default suffix order rationale — INTERNATIONAL-SITE access key (measured
  # against domain.aliyuncs.com; .com verified registrable, Avail:1 with a real
  # activate price):
  #   com             → most trusted / recognizable, preferred default
  #   net/org         → classic gTLDs, professional look
  #   online/site/top → generic gTLDs, cheapest first year, fast propagation
  #   tech/me/co      → registrable fallback
  # NOTE: .cn / .com.cn are intentionally EXCLUDED here: although CheckDomain
  # returns Avail:1, registering them with an international-site account requires
  # China real-name verification / a China-based entity and will typically fail.
  # NOTE: All domains are hosted on AliDNS after purchase, so *resolution* speed
  # does not depend on the TLD; only initial TLD-root propagation differs.
  suggest)
    : "${PROJECT:?missing PROJECT}"
    # sanitize: lowercase, keep [a-z0-9-], collapse repeats, trim dashes
    SLUG=$(printf '%s' "$PROJECT" | tr '[:upper:]' '[:lower:]' \
      | sed -E 's/[^a-z0-9]+/-/g; s/-+/-/g; s/^-//; s/-$//')
    [ -n "$SLUG" ] || err "PROJECT produced an empty domain label"
    BASE="my-${SLUG}"
    SUFFIXES="${SUFFIXES:-com net org online site top tech me co}"
    info "Suggesting default domain for base: $BASE (suffixes: $SUFFIXES)"
    TRIED=""
    for TLD in $SUFFIXES; do
      CAND="${BASE}.${TLD}"
      TRIED="${TRIED:+$TRIED,}$TLD"
      RAW=$(ALIBABA_CLOUD_DOMAIN_API_VERSION="$DOMAIN_API_VERSION" \
        aliyun domain check-domain --domain-name "$CAND" --endpoint "$DOMAIN_ENDPOINT" 2>&1)
      # Skip unsupported suffixes / errors; only accept explicit Avail:1.
      if printf '%s' "$RAW" | grep -Eq '"Avail"[[:space:]]*:[[:space:]]*"?1"?[[:space:]]*[,}]'; then
        # Official live-price page for THIS exact name (real, accurate price;
        # Alibaba Cloud exposes no scriptable domain price API — see price mode).
        PRICE_URL="https://www.alibabacloud.com/zh/domain/search?keyword=${BASE}&suffix=.${TLD}"
        printf '{"suggested":"%s","available":true,"tld":"%s","candidates_tried":"%s","format":"my-<project>.<tld>","price_url":"%s"}\n' \
          "$CAND" "$TLD" "$TRIED" "$PRICE_URL"
        exit 0
      fi
      info "  $CAND not registrable here, trying next suffix"
    done
    echo "SUGGEST_NONE: no candidate suffix ($SUFFIXES) is registrable for base $BASE" >&2
    exit 41
    ;;

  # ─── Query REAL registration price (must be accurate or fail) ────────────
  # Prints a single JSON object on stdout with confirmed price, e.g.
  #   {"domain":"x.com","available":true,"currency":"USD","price":"11.00","years":1,"source":"CheckDomain"}
  # Exits 40 (PRICE_UNCONFIRMED) when an accurate price CANNOT be established.
  # NEVER emits an estimated/guessed price. Callers MUST block auto-purchase on
  # any non-zero exit and direct the user to the console for the live price.
  # ─── Price: NEVER report an API/estimated price ──────────────────────────
  # HARD RULE: We must NOT show any price obtained from the CheckDomain API (or
  # any other scriptable source) — those figures are not authoritative and have
  # been wrong. The ONLY approved way to show a price is the official live-price
  # web page for this exact domain. This mode therefore ALWAYS emits that URL
  # and exits 40 (blocking auto-purchase); it never calls a price API and never
  # prints a number.
  price)
    : "${DOMAIN:?missing DOMAIN}"
    YEARS="${YEARS:-1}"
    info "Domain price is only available on the official page (no scriptable price API): $DOMAIN"
    DOMAIN="$DOMAIN" python3 -c '
import os, json
domain = os.environ["DOMAIN"]
parts = domain.split(".")
if len(parts) >= 3 and parts[-2] in ("com", "net", "org", "gov", "edu"):
    base = ".".join(parts[:-2]); tld = ".".join(parts[-2:])
else:
    base = ".".join(parts[:-1]); tld = parts[-1]
url = f"https://www.alibabacloud.com/zh/domain/search?keyword={base}&suffix=.{tld}"
print(json.dumps({
    "domain": domain,
    "price": None,
    "price_confirmed": False,
    "price_url": url,
    "reason": "no_scriptable_price_api",
    "note": "Alibaba Cloud has no scriptable/authoritative domain price API. Show ONLY "
            "this official live-price URL; never report a number from any API.",
}, ensure_ascii=False))
'
    echo "PRICE_UNCONFIRMED: use price_url for the accurate price; never report an API price." >&2
    exit 40
    ;;

  # ─── Check domain availability ───────────────────────────────────────────
  check)
    : "${DOMAIN:?missing DOMAIN}"
    info "Checking availability: $DOMAIN"
    RESULT=$(ALIBABA_CLOUD_DOMAIN_API_VERSION="$DOMAIN_API_VERSION" \
      aliyun domain check-domain --domain-name "$DOMAIN" --endpoint "$DOMAIN_ENDPOINT" 2>&1) || {
      echo "$RESULT" >&2
      err "Domain check API failed"
    }
    echo "$RESULT"
    ;;

  # ─── Query existing registrant profiles ──────────────────────────────────
  profiles)
    info "Querying registrant profiles"
    RESULT=$(ALIBABA_CLOUD_DOMAIN_API_VERSION="$DOMAIN_API_VERSION" \
      aliyun domain query-registrant-profiles --endpoint "$DOMAIN_ENDPOINT" 2>&1) || {
      echo "$RESULT" >&2
      err "Query registrant profiles failed"
    }
    echo "$RESULT"
    ;;

  # ─── Create registrant profile ──────────────────────────────────────────
  create-profile)
    : "${EMAIL:?missing EMAIL}"
    : "${REGISTRANT_NAME:?missing REGISTRANT_NAME}"
    : "${COUNTRY:?missing COUNTRY}"
    : "${PROVINCE:?missing PROVINCE}"
    : "${CITY:?missing CITY}"
    : "${ADDRESS:?missing ADDRESS}"
    : "${POSTAL_CODE:?missing POSTAL_CODE}"
    : "${TEL_AREA:?missing TEL_AREA}"
    : "${TELEPHONE:?missing TELEPHONE}"
    REGISTRANT_ORG="${REGISTRANT_ORG:-$REGISTRANT_NAME}"
    REGISTRANT_TYPE="${REGISTRANT_TYPE:-1}"

    info "Creating registrant profile for: $REGISTRANT_NAME <$EMAIL>"
    RESULT=$(ALIBABA_CLOUD_DOMAIN_API_VERSION="$DOMAIN_API_VERSION" \
      aliyun domain save-registrant-profile \
        --endpoint "$DOMAIN_ENDPOINT" \
        --registrant-name "$REGISTRANT_NAME" \
        --registrant-organization "$REGISTRANT_ORG" \
        --email "$EMAIL" \
        --country "$COUNTRY" \
        --province "$PROVINCE" \
        --city "$CITY" \
        --address "$ADDRESS" \
        --postal-code "$POSTAL_CODE" \
        --tel-area "$TEL_AREA" \
        --telephone "$TELEPHONE" \
        --registrant-type "$REGISTRANT_TYPE" \
        --default-registrant-profile true \
        2>&1) || {
      echo "$RESULT" >&2
      err "Create registrant profile failed"
    }
    echo "$RESULT"
    ;;

  # ─── Purchase/register domain ────────────────────────────────────────────
  buy)
    : "${DOMAIN:?missing DOMAIN}"
    : "${REGISTRANT_PROFILE_ID:?missing REGISTRANT_PROFILE_ID}"
    SUBSCRIPTION_DURATION="${SUBSCRIPTION_DURATION:-1}"

    info "Registering domain: $DOMAIN (profile=$REGISTRANT_PROFILE_ID, years=$SUBSCRIPTION_DURATION)"
    RESULT=$(ALIBABA_CLOUD_DOMAIN_API_VERSION="$DOMAIN_API_VERSION" \
      aliyun domain save-single-taREDACTED-SECRET \
        --endpoint "$DOMAIN_ENDPOINT" \
        --domain-name "$DOMAIN" \
        --registrant-profile-id "$REGISTRANT_PROFILE_ID" \
        --subscription-duration "$SUBSCRIPTION_DURATION" \
        --aliyun-dns true \
        --enable-domain-proxy true \
        2>&1) || {
      echo "$RESULT" >&2
      err "Domain registration failed"
    }
    echo "$RESULT"
    ;;

  # ─── Add DNS A record ───────────────────────────────────────────────────
  dns)
    : "${DOMAIN:?missing DOMAIN}"
    : "${IP:?missing IP}"
    # Split domain: "sub.example.com" → RR="sub", DomainName="example.com"
    # "example.com" → RR="@", DomainName="example.com"
    PARTS=(${DOMAIN//./ })
    NUM_PARTS=${#PARTS[@]}
    if [ "$NUM_PARTS" -le 2 ]; then
      RR="@"
      DNS_DOMAIN="$DOMAIN"
    else
      # e.g. app.example.com → RR=app, DNS_DOMAIN=example.com
      RR="${PARTS[0]}"
      DNS_DOMAIN="${DOMAIN#*.}"
    fi

    info "Adding A record: $RR.$DNS_DOMAIN → $IP"

    # First, add the domain to alidns if not already there
    aliyun alidns AddDomain --DomainName "$DNS_DOMAIN" 2>/dev/null || true

    # Add/update A record
    # Check if record already exists
    EXISTING=$(aliyun alidns DescribeDomainRecords \
      --DomainName "$DNS_DOMAIN" --RRKeyWord "$RR" --TypeKeyWord A 2>&1) || true

    RECORD_ID=$(echo "$EXISTING" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    records = d.get('DomainRecords', {}).get('Record', [])
    for r in records:
        if r.get('RR') == '$RR' and r.get('Type') == 'A':
            print(r['RecordId'])
            break
except:
    pass
" 2>/dev/null)

    if [ -n "$RECORD_ID" ]; then
      info "Updating existing A record (ID=$RECORD_ID)"
      RESULT=$(alidns_with_ttl_fallback UpdateDomainRecord \
        --RecordId "$RECORD_ID" --RR "$RR" --Type A --Value "$IP") || {
        echo "$RESULT" >&2
        err "Update DNS record failed"
      }
    else
      info "Creating new A record"
      RESULT=$(alidns_with_ttl_fallback AddDomainRecord \
        --DomainName "$DNS_DOMAIN" --RR "$RR" --Type A --Value "$IP") || {
        echo "$RESULT" >&2
        err "Add DNS record failed"
      }
    fi
    echo "$RESULT"
    ;;

  # ─── Verify DNS resolution ──────────────────────────────────────────────
  verify)
    : "${DOMAIN:?missing DOMAIN}"
    : "${IP:?missing IP}"
    info "Verifying DNS resolution: $DOMAIN → $IP"

    # Poll with a short first interval that backs off (2→10s): a fast record is
    # confirmed in ~2s instead of waiting a fixed 10s.
    DEADLINE=$(( $(date +%s) + ${MAX_WAIT_SEC:-120} ))
    WAIT=2; i=0
    while [ "$(date +%s)" -lt "$DEADLINE" ]; do
      i=$((i + 1))
      RESOLVED=$(dig +short "$DOMAIN" A 2>/dev/null | head -1)
      if [ "$RESOLVED" = "$IP" ]; then
        info "✅ DNS verified: $DOMAIN → $IP (attempt $i)"
        echo '{"status":"resolved","domain":"'"$DOMAIN"'","ip":"'"$IP"'"}'
        exit 0
      fi
      info "Waiting for DNS propagation (attempt $i): got '$RESOLVED', expecting '$IP'"
      sleep "$WAIT"; [ "$WAIT" -lt 10 ] && WAIT=$((WAIT + 2))
    done
    err "DNS verification timed out after ${MAX_WAIT_SEC:-120}s. $DOMAIN does not resolve to $IP yet."
    ;;

  # ─── Send email verification ──────────────────────────────────────────
  send-email-verification)
    : "${EMAIL:?missing EMAIL}"
    info "Sending email verification to: $EMAIL"
    RESULT=$(ALIBABA_CLOUD_DOMAIN_API_VERSION="$DOMAIN_API_VERSION" \
      aliyun domain submit-email-verification \
        --endpoint "$DOMAIN_ENDPOINT" \
        --email "$EMAIL" \
        --send-if-exist true \
        2>&1) || {
      echo "$RESULT" >&2
      err "Send email verification failed"
    }
    echo "$RESULT"
    ;;

  # ─── Check email verification status ────────────────────────────────────
  check-email-verification)
    : "${EMAIL:?missing EMAIL}"
    info "Checking email verification status: $EMAIL"
    RESULT=$(ALIBABA_CLOUD_DOMAIN_API_VERSION="$DOMAIN_API_VERSION" \
      aliyun domain query-email-verification \
        --endpoint "$DOMAIN_ENDPOINT" \
        --email "$EMAIL" \
        2>&1) || {
      echo "$RESULT" >&2
      err "Query email verification failed"
    }
    echo "$RESULT"
    ;;


  # ─── Add DNS TXT record (for Let's Encrypt DNS-01 challenge) ─────────────
  dns-txt)
    : "${DOMAIN:?missing DOMAIN}"
    : "${TXT_NAME:?missing TXT_NAME (e.g. _acme-challenge)}"
    : "${TXT_VALUE:?missing TXT_VALUE}"
    # Split domain: for "example.com" → DNS_DOMAIN="example.com"
    # For "sub.example.com" → DNS_DOMAIN="example.com"
    PARTS=(${DOMAIN//./ })
    NUM_PARTS=${#PARTS[@]}
    if [ "$NUM_PARTS" -le 2 ]; then
      DNS_DOMAIN="$DOMAIN"
    else
      # e.g. app.example.com → DNS_DOMAIN=example.com (root domain for DNS API)
      DNS_DOMAIN="${PARTS[-2]}.${PARTS[-1]}"
    fi

    # Build the full RR: _acme-challenge or _acme-challenge.sub
    if [ "$NUM_PARTS" -le 2 ]; then
      RR="$TXT_NAME"
    else
      # sub.example.com → RR="_acme-challenge.sub"
      SUB="${DOMAIN%.$DNS_DOMAIN}"
      RR="${TXT_NAME}.${SUB}"
    fi

    info "Adding TXT record: $RR.$DNS_DOMAIN → $TXT_VALUE"

    # Ensure domain exists in alidns
    aliyun alidns AddDomain --DomainName "$DNS_DOMAIN" 2>/dev/null || true

    # Check if TXT record already exists (to update rather than duplicate)
    EXISTING=$(aliyun alidns DescribeDomainRecords \
      --DomainName "$DNS_DOMAIN" --RRKeyWord "$RR" --TypeKeyWord TXT 2>&1) || true

    RECORD_ID=$(echo "$EXISTING" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    records = d.get('DomainRecords', {}).get('Record', [])
    for r in records:
        if r.get('RR') == '$RR' and r.get('Type') == 'TXT':
            print(r['RecordId'])
            break
except:
    pass
" 2>/dev/null)

    if [ -n "$RECORD_ID" ]; then
      info "Updating existing TXT record (ID=$RECORD_ID)"
      RESULT=$(alidns_with_ttl_fallback UpdateDomainRecord \
        --RecordId "$RECORD_ID" --RR "$RR" --Type TXT --Value "$TXT_VALUE") || {
        echo "$RESULT" >&2
        err "Update TXT record failed"
      }
    else
      info "Creating new TXT record"
      RESULT=$(alidns_with_ttl_fallback AddDomainRecord \
        --DomainName "$DNS_DOMAIN" --RR "$RR" --Type TXT --Value "$TXT_VALUE") || {
        echo "$RESULT" >&2
        err "Add TXT record failed"
      }
    fi
    echo "$RESULT"
    ;;

  # ─── Verify DNS TXT record propagation ──────────────────────────────────
  # Queries the AUTHORITATIVE nameservers directly (not the local recursive
  # resolver). This is what Let's Encrypt actually does for DNS-01: it resolves
  # the domain's NS and queries them for the _acme-challenge TXT. Because of this
  # we do NOT need to wait for global NS delegation / TLD propagation — as soon
  # as the TXT record is live on the authoritative DNS (e.g. Alibaba Cloud DNS),
  # validation can succeed. This eliminates the "waiting 30-60min for .xyz NS
  # delegation" trap that blocked deploys.
  #
  # SOFT-FAIL: If we can't confirm within the window we return a non-fatal
  # "unconfirmed" status (exit 0) instead of hard-erroring, because the final
  # arbiter is Let's Encrypt itself. The caller may proceed to complete the
  # challenge; if the TXT truly isn't propagated certbot will report it.
  verify-txt)
    : "${DOMAIN:?missing DOMAIN}"
    : "${TXT_NAME:?missing TXT_NAME (e.g. _acme-challenge)}"
    : "${TXT_VALUE:?missing TXT_VALUE}"
    FQDN="${TXT_NAME}.${DOMAIN}"

    # Root/registered domain (for NS lookup): last two labels.
    PARTS=(${DOMAIN//./ })
    NUM_PARTS=${#PARTS[@]}
    if [ "$NUM_PARTS" -le 2 ]; then
      ROOT_DOMAIN="$DOMAIN"
    else
      ROOT_DOMAIN="${PARTS[-2]}.${PARTS[-1]}"
    fi

    # Discover the authoritative nameservers for the domain. Prefer the alidns
    # API (works even before NS delegation is globally visible); fall back to dig.
    NS_LIST=$(aliyun alidns DescribeDomainNs --DomainName "$ROOT_DOMAIN" 2>/dev/null \
      | python3 -c "
import json,sys
try:
    d=json.load(sys.stdin)
    for n in d.get('DnsServers',{}).get('DnsServer',[]):
        print(n)
except: pass
" 2>/dev/null)
    if [ -z "$NS_LIST" ]; then
      NS_LIST=$(dig +short "$ROOT_DOMAIN" NS 2>/dev/null | sed 's/\.$//')
    fi

    if [ -n "$NS_LIST" ]; then
      info "Verifying TXT against authoritative NS for $ROOT_DOMAIN: $(echo $NS_LIST | tr '\n' ' ')"
    else
      info "Could not determine authoritative NS; falling back to local resolver"
    fi

    # Poll authoritative NS with a short first interval that backs off (2→10s):
    # once the record is live the confirm returns in ~2s.
    DEADLINE=$(( $(date +%s) + ${MAX_WAIT_SEC:-180} ))
    WAIT=2; i=0
    while [ "$(date +%s)" -lt "$DEADLINE" ]; do
      i=$((i + 1))
      RESOLVED=""
      if [ -n "$NS_LIST" ]; then
        # Query each authoritative NS directly.
        for ns in $NS_LIST; do
          ANS=$(dig @"$ns" +short "$FQDN" TXT 2>/dev/null | tr -d \'\")
          RESOLVED="$RESOLVED $ANS"
        done
      else
        RESOLVED=$(dig +short "$FQDN" TXT 2>/dev/null | tr -d \'\")
      fi
      if echo "$RESOLVED" | grep -qF "$TXT_VALUE"; then
        info "✅ TXT verified on authoritative NS: $FQDN (attempt $i)"
        echo "{\"status\":\"resolved\",\"fqdn\":\"$FQDN\",\"value\":\"$TXT_VALUE\"}"
        exit 0
      fi
      info "Waiting for TXT on authoritative NS (attempt $i): got '$(echo $RESOLVED | tr -s ' ')', expecting '$TXT_VALUE'"
      sleep "$WAIT"; [ "$WAIT" -lt 10 ] && WAIT=$((WAIT + 2))
    done

    # Soft-fail: don't block the pipeline; let certbot / Let's Encrypt decide.
    info "⚠️  Could not confirm TXT on authoritative NS after ${MAX_WAIT_SEC:-180}s."
    info "    Proceeding anyway — Let's Encrypt queries authoritative NS directly and may still succeed."
    echo "{\"status\":\"unconfirmed\",\"fqdn\":\"$FQDN\",\"value\":\"$TXT_VALUE\",\"note\":\"soft_fail_proceed\"}"
    exit 0
    ;;

  # ─── Remove DNS TXT record (cleanup after DNS-01 challenge) ─────────────
  dns-txt-clean)
    : "${DOMAIN:?missing DOMAIN}"
    : "${TXT_NAME:?missing TXT_NAME (e.g. _acme-challenge)}"
    PARTS=(${DOMAIN//./ })
    NUM_PARTS=${#PARTS[@]}
    if [ "$NUM_PARTS" -le 2 ]; then
      DNS_DOMAIN="$DOMAIN"
      RR="$TXT_NAME"
    else
      DNS_DOMAIN="${PARTS[-2]}.${PARTS[-1]}"
      SUB="${DOMAIN%.$DNS_DOMAIN}"
      RR="${TXT_NAME}.${SUB}"
    fi

    info "Removing TXT record: $RR.$DNS_DOMAIN"

    EXISTING=$(aliyun alidns DescribeDomainRecords \
      --DomainName "$DNS_DOMAIN" --RRKeyWord "$RR" --TypeKeyWord TXT 2>&1) || true

    RECORD_ID=$(echo "$EXISTING" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    records = d.get('DomainRecords', {}).get('Record', [])
    for r in records:
        if r.get('RR') == '$RR' and r.get('Type') == 'TXT':
            print(r['RecordId'])
            break
except:
    pass
" 2>/dev/null)

    if [ -n "$RECORD_ID" ]; then
      RESULT=$(aliyun alidns DeleteDomainRecord --RecordId "$RECORD_ID" 2>&1) || {
        echo "$RESULT" >&2
        err "Delete TXT record failed"
      }
      info "✅ TXT record removed"
      echo "$RESULT"
    else
      info "No TXT record found to remove (already clean)"
      echo "{\"status\":\"not_found\"}"
    fi
    ;;

  # ─── Wait for NS delegation of a freshly-registered domain ──────────────
  # A newly registered domain is only usable once the TLD root delegates its NS
  # to AliDNS. Until then public recursive resolvers return NXDOMAIN for ANY
  # record (A/TXT), which is the classic "new domain first HTTPS/ACME fails"
  # trap. Instead of a fixed sleep, poll public resolvers until they can see the
  # domain's NS, then return immediately — as fast as delegation allows.
  #
  # Ready condition: at least one public resolver returns an NS record for the
  # registered (root) domain. We query several resolvers to avoid single-resolver
  # caching skew.
  #
  # SOFT-FAIL: returns exit 0 with status "unconfirmed" if not ready within the
  # window, so the caller can still proceed (the final arbiter is the ACME/DNS
  # query itself); it never hard-blocks the pipeline.
  wait-delegation)
    : "${DOMAIN:?missing DOMAIN}"
    PARTS=(${DOMAIN//./ })
    NUM_PARTS=${#PARTS[@]}
    if [ "$NUM_PARTS" -le 2 ]; then
      ROOT_DOMAIN="$DOMAIN"
    else
      ROOT_DOMAIN="${PARTS[-2]}.${PARTS[-1]}"
    fi

    RESOLVERS="${RESOLVERS:-223.5.5.5 8.8.8.8 1.1.1.1}"
    info "Waiting for NS delegation of $ROOT_DOMAIN (resolvers: $RESOLVERS)"

    # Poll public resolvers; return the instant any resolver sees the NS. Short
    # first interval that backs off (2→15s) so a quick delegation is caught fast.
    DEADLINE=$(( $(date +%s) + ${MAX_WAIT_SEC:-300} ))
    WAIT=2; i=0
    while [ "$(date +%s)" -lt "$DEADLINE" ]; do
      i=$((i + 1))
      for r in $RESOLVERS; do
        NS=$(dig @"$r" +short "$ROOT_DOMAIN" NS 2>/dev/null | head -1)
        if [ -n "$NS" ]; then
          info "✅ NS delegation live for $ROOT_DOMAIN via $r: $NS (attempt $i)"
          echo "{\"status\":\"delegated\",\"domain\":\"$ROOT_DOMAIN\",\"ns\":\"$NS\",\"resolver\":\"$r\"}"
          exit 0
        fi
      done
      info "NS not yet delegated for $ROOT_DOMAIN (attempt $i); waiting ${WAIT}s"
      sleep "$WAIT"; [ "$WAIT" -lt 15 ] && WAIT=$((WAIT + 3))
    done

    info "⚠️  NS delegation not confirmed for $ROOT_DOMAIN after ${MAX_WAIT_SEC:-300}s — proceeding anyway."
    echo "{\"status\":\"unconfirmed\",\"domain\":\"$ROOT_DOMAIN\",\"note\":\"soft_fail_proceed\"}"
    exit 0
    ;;

  *)
    err "Unknown MODE: $MODE (expected: check|buy|dns|dns-txt|verify|verify-txt|wait-delegation|dns-txt-clean|profiles|create-profile|send-email-verification|check-email-verification)"
    ;;
esac
