#!/usr/bin/env bash
#
# Run one SpawnXchange x402 call with a CDP-managed wallet.
#
#   WALLET_ADDRESS=0x... ./x402-call.sh [FLAGS] <METHOD> <URL> [BODY]
#
#     BODY   inline JSON, or @/path/to/file to stream a large body from disk
#
#   FLAGS, before the method:
#
#     --execute            required before anything that actually costs money
#     --max-amount-raw N   the most this call may spend, in raw units. Required
#                          with --execute: a price read from the reply and shown
#                          to you is not a limit, it is a report, and the reply
#                          is written by whoever answers the URL.
#     --network <caip2>    which chain to pay on, e.g. eip155:8453
#     --upload <file>      send this file as the `file` part of a multipart
#     --metadata <file>    with this JSON file as the `metadata` part
#     --confirm-delete <item_id>
#                          required for DELETE: names the listing being removed.
#                          Removal is irreversible, so a DELETE is refused before
#                          anything is sent unless the URL is exactly
#                          /api/v1/items/<item_id> and this flag names that id.
#
# --upload is how a listing larger than the shell's argument limit is sent: the
# bytes go as they are, where base64-in-JSON would add a third to every one of
# them. The two parts are the only multipart form this API has, so the script
# builds them itself rather than taking form arguments — anything it passed
# through to curl could name a second destination, and the PAYMENT-SIGNATURE
# header goes to every destination curl is given.
#
# Works for paid routes and for free 0 USDC identity routes alike — the amount
# comes from the challenge, not from here. A free call runs as-is; a call that
# would spend money prints the price and stops unless --execute is given, so the
# cost is always seen before it is paid. Prints the final response body on stdout
# and the price on stderr.
#
# The URL must be https on a spawnxchange.com host. This script hands a remote
# reply straight to a signing key, so the set of hosts allowed to produce that
# reply is part of what keeps it safe; point it at another deployment by editing
# the pattern below, deliberately, not by passing a different argument.
#
# Requires: cdp CLI (`cdp env live`), curl, jq.

x402_call() {
  (
    set -euo pipefail

    local execute=0 network="" upload="" metadata="" max_amount="" confirm_delete=""
    while [ $# -gt 0 ]; do
      case "$1" in
        --execute)        execute=1; shift ;;
        --max-amount-raw) max_amount="$2"; shift 2 ;;
        --network)  network="$2"; shift 2 ;;
        --upload)   upload="$2"; shift 2 ;;
        --metadata) metadata="$2"; shift 2 ;;
        --confirm-delete) confirm_delete="$2"; shift 2 ;;
        *) break ;;
      esac
    done

    local method="${1:?method required, e.g. GET or POST}"
    local url="${2:?url required}"
    local wallet="${WALLET_ADDRESS:?WALLET_ADDRESS must be set to your CDP wallet address}"
    shift 2

    # Flags are read before the method, so anything still dash-shaped here was
    # written after the URL and would otherwise be sent as the request body
    # without a word. Say so instead.
    local body="${1:-}"
    case "$body" in
      --*) echo "flags go before the method, not after the URL: $body" >&2; return 2 ;;
    esac
    [ $# -le 1 ] || { echo "unexpected extra arguments: ${*:2}" >&2; return 2; }
    if [ -n "$upload" ] && [ -n "$body" ]; then
      echo "--upload sends the request body; do not also pass one" >&2
      return 2
    fi
    if [ -z "$upload" ] && [ -n "$metadata" ]; then
      echo "--metadata is part of an upload; pass --upload too" >&2
      return 2
    fi

    # Whatever answers this URL decides what gets signed. Keep it to the
    # marketplace, over TLS.
    if ! [[ "$url" =~ ^https://([a-z0-9-]+\.)*spawnxchange\.com(/|$) ]]; then
      echo "refusing: the URL must be https:// on a spawnxchange.com host" >&2
      echo "got: $url" >&2
      return 2
    fi

    # Removing a listing cannot be undone, so the operator's confirmation is
    # checked here, by the script, not only asked for in prose: the flag must
    # name the exact item the URL deletes. Refused before any request is sent.
    local method_uc
    method_uc=$(printf '%s' "$method" | tr '[:lower:]' '[:upper:]')
    if [ "$method_uc" = "DELETE" ]; then
      local delete_re='^https://([a-z0-9-]+\.)*spawnxchange\.com/api/v1/items/([0-9a-fA-F-]{36})$'
      if ! [[ "$url" =~ $delete_re ]]; then
        echo "refusing: DELETE is only for a listing, https://spawnxchange.com/api/v1/items/<item_id>" >&2
        return 2
      fi
      local target="${BASH_REMATCH[2]}"
      if [ -z "$confirm_delete" ] || [ "$confirm_delete" != "$target" ]; then
        echo "refusing: removing listing $target is irreversible; confirm it with" >&2
        echo "  --confirm-delete $target" >&2
        return 2
      fi
    elif [ -n "$confirm_delete" ]; then
      echo "--confirm-delete only applies to DELETE" >&2
      return 2
    fi

    local work
    work=$(mktemp -d)
    chmod 700 "$work"
    trap 'rm -rf "$work"' EXIT

    # curl arguments for the request body, shared by the probe and the retry.
    # Both requests must carry the same body: the challenge is issued against a
    # validated request, and the retry has to be that same request plus a header.
    local -a body_args=()
    if [ -n "$upload" ]; then
      [ -r "$upload" ] || { echo "--upload cannot read: $upload" >&2; return 2; }
      body_args=(-F "file=@${upload}")
      if [ -n "$metadata" ]; then
        [ -r "$metadata" ] || { echo "--metadata cannot read: $metadata" >&2; return 2; }
        body_args+=(-F "metadata=<${metadata}")
      fi
      # No Content-Type here — curl sets it, with the boundary, and overriding it
      # breaks the upload.
    elif [ -n "$body" ]; then
      case "$body" in
        @*) body_args=(-H "Content-Type: application/json" --data-binary "$body") ;;
        *)  body_args=(-H "Content-Type: application/json" --data "$body") ;;
      esac
    fi

    # 1. Unsigned probe. The reply is the 402 carrying the requirements to sign.
    curl -sS --proto '=https' --max-redirs 0 -X "$method" "${body_args[@]}" "$url" > "$work/challenge.json"

    if ! jq -e '.accepts' "$work/challenge.json" >/dev/null 2>&1; then
      # Not a challenge: either the route is public, or it refused us outright
      # (403 region_unavailable, 400 validation, ...). Either way, show it.
      cat "$work/challenge.json"
      return 0
    fi

    # Narrow to one chain when asked, so a payment cannot be signed for a network
    # you did not choose. Without --network the challenge is passed through as it
    # came, and CDP picks.
    if [ -n "$network" ]; then
      jq -c --arg net "$network" '[.accepts[] | select(.network == $net)]' \
        "$work/challenge.json" > "$work/accepts.json"
      if [ "$(cat "$work/accepts.json")" = "[]" ]; then
        echo "the challenge offers no requirement for $network; it offered:" >&2
        jq -c '[.accepts[].network]' "$work/challenge.json" >&2
        return 1
      fi
    else
      jq -c '.accepts' "$work/challenge.json" > "$work/accepts.json"
    fi

    jq -r '.[] | "  price: \(.amount) raw on \(.network) -> \(.payTo)"' \
      "$work/accepts.json" >&2

    # Prices come from the reply, so they are checked before anything acts on
    # them: each must be a plain non-negative integer of raw units. A float, a
    # sign, or a null is a challenge this script cannot reason about.
    local amounts='[.[] | .amount // .maxAmountRequired // "0" | tostring]'
    if ! jq -e "$amounts | all(test(\"^[0-9]+$\"))" "$work/accepts.json" >/dev/null; then
      echo "refusing: a requirement states a price this script cannot read:" >&2
      jq -c "$amounts" "$work/accepts.json" >&2
      return 1
    fi

    # Free means every requirement is free. Reading only the first one let a
    # challenge that offered a free entry ahead of a paid one skip the
    # confirmation below, and then handed CDP the whole array to choose from.
    local paid=1
    jq -e "$amounts | all(. == \"0\")" "$work/accepts.json" >/dev/null && paid=0

    # A paid requirement must settle in USDC on its chain. The cap below is in raw
    # units, which only means dollars for USDC; a challenge naming another asset
    # would turn the same number into a different amount of a different token.
    if [ "$paid" -eq 1 ] && ! jq -e '
        {"eip155:8453": "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
         "eip155:137": "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359"} as $usdc
        | all(.[]; (.asset // "" | ascii_downcase) == $usdc[.network])' \
        "$work/accepts.json" >/dev/null; then
      echo "refusing: a requirement does not settle in USDC on Base or Polygon:" >&2
      jq -c '[.[] | {network, asset}]' "$work/accepts.json" >&2
      return 1
    fi

    # A zero-amount challenge is the identity handshake: it proves who you are
    # and moves no money. Anything else spends USDC.
    if [ "$paid" -eq 1 ] && [ "$execute" -ne 1 ]; then
      echo >&2
      echo "This request costs money. Nothing has been paid." >&2
      echo "Re-run with --execute and --max-amount-raw to pay it." >&2
      return 3
    fi

    # A price that came from the reply and was printed for you is a report, not
    # a limit. The limit is the number you decided on before you looked, so a
    # paying call has to carry one.
    if [ "$paid" -eq 1 ]; then
      case "$max_amount" in
        ''|*[!0-9]*)
          echo "refusing: --max-amount-raw is required to spend, as a whole number" >&2
          echo "of raw units. The endpoint is asking for:" >&2
          jq -c "$amounts" "$work/accepts.json" >&2
          return 2 ;;
      esac
      local asking
      asking=$(jq -r "$amounts | .[0]" "$work/accepts.json")
      if [ "$asking" -gt "$max_amount" ]; then
        echo "refusing: the endpoint asks $asking raw units, over your" >&2
        echo "--max-amount-raw of $max_amount. Nothing has been signed." >&2
        return 1
      fi
    fi

    # Nothing is signed against a set of requirements. One is chosen, or the
    # script stops and asks which.
    if [ "$paid" -eq 1 ] && [ "$(jq 'length' "$work/accepts.json")" -ne 1 ]; then
      echo "the challenge offers several chains; pass --network to choose one" >&2
      jq -c '[.[].network]' "$work/accepts.json" >&2
      return 1
    fi

    # 2. Typed data from those exact requirements.
    cdp util x402 build --from "$wallet" \
      --payment-requirements "$(cat "$work/accepts.json")" \
      > "$work/typed_data.json"

    # 3. Sign. The key never leaves CDP.
    cdp evm accounts sign typed-data "$wallet" \
      primaryType="$(jq -r '.primaryType' "$work/typed_data.json")" \
      domain:="$(jq -c '.domain' "$work/typed_data.json")" \
      message:="$(jq -c '.message' "$work/typed_data.json")" \
      types:="$(jq -c '.types' "$work/typed_data.json")" \
      | jq -r '.signature' > "$work/signature.txt"

    # 4. Encode and retry. Requirements, signature and authorization must all come
    #    from this one challenge — nonces are single-use and windows are short.
    cdp util x402 encode --x402-version 2 \
      --payment-requirements "$(cat "$work/accepts.json")" \
      --signature "$(cat "$work/signature.txt")" \
      --authorization "$(jq -c '.message' "$work/typed_data.json")" > "$work/header.txt"

    curl -sS --proto '=https' --max-redirs 0 -X "$method" \
      -H "PAYMENT-SIGNATURE: $(cat "$work/header.txt")" \
      "${body_args[@]}" "$url"
  )
}

x402_call "$@"
