#!/usr/bin/env bash
#
# List a large artifact on SpawnXchange with a Circle Agent Wallet.
#
#   ./list-artifact.sh --archive FILE --title T --description-file F \
#       --tech-stack S --price-usdc N --wallet 0x... --chain BASE [--execute]
#
#     --max-fee-usdc N  refuse to sign a listing fee above N (default 0.05; the
#                       published fee is a flat 0.01)
#     --base-url URL    a SpawnXchange deployment other than the production one.
#                       https only, and only a spawnxchange.com host: this URL
#                       receives the archive and dictates the terms that get
#                       signed, so it is not free-form.
#
# Why this exists: `circle services pay` sends the request for you, which is what
# you want everywhere else — but it takes the request body as a single
# command-line argument, and the operating system caps one argument at 131,072
# bytes. Base64 inflates an archive by a third, so listing anything over roughly
# a 96 KB archive is impossible that way.
#
# An x402 payment authorizes the *charge*, not the contents of the request, so
# the two can be separated. This script uploads the archive itself as multipart —
# the bytes as they are, no base64 inflation, up to the API's 10 MB limit — and
# invokes `circle wallet sign typed-data` for the signature. The signing happens
# inside the Circle CLI, which already holds your key; this script only passes it
# the data to sign and takes back the signature.
#
# For an archive under ~96 KB you do not need this: use `circle services pay`.
#
# Preflight by default: it uploads the unpaid request, prints the fee the
# marketplace asks for, and stops. Pass --execute to pay it and publish.
#
# Requires: `circle`, `curl` and `jq` on PATH, and a logged-in Circle wallet. The
# Circle CLI must already be installed — this script does not install it, and will
# not reach for a package registry at signing time.

list_artifact() {
  (
    set -euo pipefail

    local archive="" title="" description="" description_file="" tech_stack=""
    local price="" wallet="" chain="" base_url="https://spawnxchange.com" execute=0
    local max_fee="0.05"

    while [ $# -gt 0 ]; do
      case "$1" in
        --archive)          archive="$2"; shift 2 ;;
        --title)            title="$2"; shift 2 ;;
        --description)      description="$2"; shift 2 ;;
        --description-file) description_file="$2"; shift 2 ;;
        --tech-stack)       tech_stack="$2"; shift 2 ;;
        --price-usdc)       price="$2"; shift 2 ;;
        --wallet)           wallet="$2"; shift 2 ;;
        --chain)            chain="$2"; shift 2 ;;
        --base-url)         base_url="$2"; shift 2 ;;
        --max-fee-usdc)     max_fee="$2"; shift 2 ;;
        --execute)          execute=1; shift ;;
        *) echo "unknown argument: $1" >&2; return 2 ;;
      esac
    done

    # This URL receives the archive and supplies the payment terms this script
    # signs, so it decides both what leaks and what gets authorized. Restrict it
    # to the marketplace: https, and a spawnxchange.com host. Point it elsewhere
    # by editing this pattern, deliberately, not by passing a flag.
    base_url="${base_url%/}"
    if ! [[ "$base_url" =~ ^https://([a-z0-9-]+\.)*spawnxchange\.com$ ]]; then
      echo "--base-url must be https:// on a spawnxchange.com host; got: $base_url" >&2
      return 2
    fi

    # Circle's chain names are not the marketplace's, and the payment request uses
    # CAIP-2 ids. Map them here so a payment cannot be signed for a chain you did
    # not name. The USDC address goes with it: the EIP-712 domain below is built
    # from the reply, and a signature is only ever as narrow as the contract it
    # names, so the contract is pinned per chain rather than taken on trust.
    local network usdc
    case "$chain" in
      BASE)          network="eip155:8453"  usdc="0x833589fcd6edb6e08f4c7c32d4f71b54bda02913" ;;
      MATIC)         network="eip155:137"   usdc="0x3c499c542cef5e3811e1192ce70d8cc03d5c3359" ;;
      *) echo "--chain must be BASE or MATIC" >&2; return 2 ;;
    esac

    [ -n "$archive" ] && [ -n "$title" ] && [ -n "$tech_stack" ] \
      && [ -n "$price" ] && [ -n "$wallet" ] \
      || { echo "missing a required argument; see the header of this script" >&2; return 2; }
    [ -f "$archive" ] || { echo "archive not found: $archive" >&2; return 2; }

    if [ -n "$description_file" ]; then
      description=$(cat "$description_file")
    fi
    [ -n "$description" ] || { echo "--description or --description-file is required" >&2; return 2; }

    # Refuse locally what the marketplace would refuse anyway, before sending bytes.
    local size
    size=$(wc -c < "$archive")
    if [ "$size" -gt $((10 * 1024 * 1024)) ]; then
      echo "archive is $size bytes; the limit is 10485760" >&2
      return 2
    fi
    if ! awk -v p="$price" 'BEGIN { exit !(p >= 0.1 && p <= 100) }'; then
      echo "price $price is outside the allowed band 0.1..100 USD" >&2
      return 2
    fi

    local work
    work=$(mktemp -d)
    chmod 700 "$work"
    trap 'rm -rf "$work"' EXIT

    jq -n --arg t "$title" --arg d "$description" --arg s "$tech_stack" \
          --argjson p "$price" \
      '{title: $t, description: $d, tech_stack: $s, prices: {USDC: $p}}' \
      > "$work/metadata.json"

    echo "archive   $archive ($size bytes)" >&2
    echo "listing   $title at $price USDC" >&2
    echo "wallet    $wallet on $chain" >&2
    echo >&2

    # The unpaid upload. Validation runs here, so a malformed listing is refused
    # now, for free. curl streams the file, so nothing passes through argv.
    local code
    code=$(curl -sS --proto '=https' --max-redirs 0 -o "$work/challenge.json" -w '%{http_code}' -X POST \
             -F "file=@${archive}" -F "metadata=<${work}/metadata.json" \
             "${base_url}/api/v1/items")
    if [ "$code" != "402" ]; then
      echo "expected a payment request, got HTTP $code:" >&2
      head -c 400 "$work/challenge.json" >&2; echo >&2
      return 1
    fi

    local requirement
    requirement=$(jq -c --arg net "$network" \
      'first(.accepts[] | select(.network == $net)) // empty' "$work/challenge.json")
    if [ -z "$requirement" ]; then
      echo "the marketplace offered no requirement for $network; it offered:" >&2
      jq -c '[.accepts[].network]' "$work/challenge.json" >&2
      return 1
    fi

    # Everything from here on is built out of a remote reply. Check it against
    # what was asked for first: a signature is worth exactly the terms inside it,
    # and printing them for the operator is not the same as bounding them.
    local asset amount
    asset=$(jq -r '.asset // ""' <<<"$requirement" | tr 'A-Z' 'a-z')
    if [ "$asset" != "$usdc" ]; then
      echo "refusing to sign: $chain settles USDC at" >&2
      echo "  $usdc" >&2
      echo "but the reply asks to authorize" >&2
      echo "  $asset" >&2
      return 1
    fi

    # The listing fee is a flat 0.01 USDC. A reply asking for materially more is
    # one to walk away from, not one to print and hope somebody reads.
    amount=$(jq -r '.amount // .maxAmountRequired // ""' <<<"$requirement")
    case "$amount" in
      ''|*[!0-9]*)
        echo "refusing to sign: the fee is not a whole number of raw units: $amount" >&2
        return 1 ;;
    esac
    if ! awk -v a="$amount" -v m="$max_fee" 'BEGIN { exit !(a <= m * 1000000) }'; then
      echo "refusing to sign: the marketplace asks $amount raw units" >&2
      echo "($(awk -v a="$amount" 'BEGIN { printf "%.6f", a / 1000000 }') USDC), over the" >&2
      echo "--max-fee-usdc cap of $max_fee. Raise the cap only if you know why it moved." >&2
      return 1
    fi

    echo "fee       $amount raw units of $(jq -r '.asset' <<<"$requirement")" >&2
    echo "          on $(jq -r '.network' <<<"$requirement") to $(jq -r '.payTo' <<<"$requirement")" >&2

    if [ "$execute" -ne 1 ]; then
      echo >&2
      echo "Nothing has been paid and nothing is listed. Re-run with --execute" >&2
      echo "to pay this fee and publish the artifact." >&2
      return 0
    fi

    # EIP-3009, exactly as the settlement path verifies it. The nonce is single-use.
    local nonce deadline timeout
    nonce="0x$(head -c 32 /dev/urandom | od -An -tx1 | tr -d ' \n')"

    # maxTimeoutSeconds is remote input, and it used to go straight into the
    # arithmetic expansion below. Bash evaluates command substitution inside an
    # array subscript there, so a reply of "x[$(...)]" ran that command on this
    # machine — in the shell that is about to sign a payment. Take it only as a
    # whole number in a sane range, and fall back to the documented default.
    timeout=$(jq -r 'if (.maxTimeoutSeconds | type) == "number"
                     then .maxTimeoutSeconds | floor | tostring
                     else "" end' <<<"$requirement")
    case "$timeout" in
      ''|*[!0-9]*) timeout=120 ;;
    esac
    [ "$timeout" -ge 1 ] && [ "$timeout" -le 600 ] || timeout=120
    deadline=$(( $(date +%s) + timeout ))

    jq -n --argjson r "$requirement" --arg from "$wallet" \
          --arg nonce "$nonce" --arg before "$deadline" '
      {
        types: { TransferWithAuthorization: [
          {name: "from", type: "address"}, {name: "to", type: "address"},
          {name: "value", type: "uint256"}, {name: "validAfter", type: "uint256"},
          {name: "validBefore", type: "uint256"}, {name: "nonce", type: "bytes32"}
        ]},
        primaryType: "TransferWithAuthorization",
        domain: {
          name: $r.extra.name, version: $r.extra.version,
          chainId: ($r.network | split(":")[1] | tonumber),
          verifyingContract: $r.asset
        },
        message: {
          from: $from, to: $r.payTo,
          value: (($r.amount // $r.maxAmountRequired) | tostring),
          validAfter: "0", validBefore: $before, nonce: $nonce
        }
      }' > "$work/typed.json"

    # No fallback here on purpose. This is the wallet-signing path, and a
    # fallback that fetches and runs a package at the moment of signing puts the
    # registry inside it: whoever can publish that package can sign with your
    # key. Installing the CLI is a separate, deliberate step the operator takes
    # once, and it is the version they reviewed.
    if ! command -v circle >/dev/null 2>&1; then
      echo "the Circle CLI is not on PATH." >&2
      echo "Install it first, following Circle's own instructions at" >&2
      echo "  https://developers.circle.com/agent-stack/agent-wallets" >&2
      echo "then log in and re-run. This script will not install it for you." >&2
      return 2
    fi

    echo >&2
    echo "signing with the Circle CLI..." >&2
    local signature
    signature=$(circle wallet sign typed-data \
                  "$(jq -c . "$work/typed.json")" \
                  --address "$wallet" --chain "$chain" -q | tail -1 | tr -d ' \r')
    case "$signature" in
      0x*) ;;
      *) echo "expected a 0x signature from the Circle CLI, got: $signature" >&2; return 1 ;;
    esac

    local header
    header=$(jq -c -n --argjson r "$requirement" --argjson t "$(cat "$work/typed.json")" \
               --arg sig "$signature" --argjson c "$(cat "$work/challenge.json")" '
               {x402Version: 2, accepted: $r,
                payload: {signature: $sig, authorization: $t.message}}
               + (if $c.resource then {resource: $c.resource} else {} end)
               + (if $c.extensions then {extensions: $c.extensions} else {} end)' \
             | base64 -w 0)

    echo "paying and uploading..." >&2
    code=$(curl -sS --proto '=https' --max-redirs 0 -o "$work/result.json" -w '%{http_code}' -X POST \
             -H "PAYMENT-SIGNATURE: $header" \
             -F "file=@${archive}" -F "metadata=<${work}/metadata.json" \
             "${base_url}/api/v1/items")

    if [ "$code" = "202" ]; then
      jq . "$work/result.json"
      echo >&2
      echo "Listed. Poll the seller status request until it reaches active or" >&2
      echo "rejected, and save the invoice from invoice_url." >&2
      return 0
    fi

    if [ "$code" = "409" ] && jq -e '.error == "payment_settlement_pending"' "$work/result.json" >/dev/null; then
      echo >&2
      echo "The payment reached the chain but its outcome is not yet known." >&2
      jq -r '"  transaction \(.transaction)\n  network     \(.network)"' "$work/result.json" >&2
      echo "Do NOT run this again — a second attempt is a separate payment." >&2
      return 1
    fi

    echo "HTTP $code:" >&2
    head -c 400 "$work/result.json" >&2; echo >&2
    return 1
  )
}

list_artifact "$@"
