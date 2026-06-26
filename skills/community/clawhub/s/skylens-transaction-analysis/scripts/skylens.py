#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "zstandard",
# ]
# ///
import json
import base64
import io
import argparse
import sys
from pathlib import Path
from typing import Any
from urllib import request, error

SKYLENS_API_BASE = "https://skylens.certik.com/server/api/v2/crossguard"
SUPPORTED_CHAINS = (
    "eth",
    "bsc",
    "polygon",
    "optimism",
    "arb",
    "base",
    "blast",
    "avalanche",
    "scroll",
    "linea",
    "sonic",
    "kaia",
    "world",
    "unichain",
    "hyperliquid",
    "plasma",
)

def _zstd_decompress(data: bytes) -> bytes:
    # Python 3.14+ standard library backend.
    try:
        import compression.zstd as pyzstd  # type: ignore[attr-defined]

        return pyzstd.decompress(data)
    except Exception:
        pass

    # Third-party backend for older Python versions.
    try:
        import zstandard as zstd

        dctx = zstd.ZstdDecompressor()
        with dctx.stream_reader(io.BytesIO(data)) as reader:
            return reader.read()
    except Exception as exc:
        raise RuntimeError(
            "No zstd backend available. Use Python 3.14+ or install `zstandard`."
        ) from exc


def _decode_zstd_base64_json(compressed_result: str) -> Any:
    compressed_bytes = base64.b64decode(compressed_result)
    decoded = _zstd_decompress(compressed_bytes)
    return json.loads(decoded)


def _http_get_json(url: str, timeout: int = 30) -> Any:
    req = request.Request(url, method="GET")
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            status_code = getattr(resp, "status", 200)
            if status_code < 200 or status_code >= 300:
                raise RuntimeError(f"HTTP request failed: {url} status={status_code}")
            body = resp.read()
    except error.HTTPError as exc:
        detail = ""
        try:
            detail = exc.read().decode("utf-8", errors="replace")
        except Exception:
            detail = str(exc)
        raise RuntimeError(f"HTTP request failed: {url} status={exc.code} body={detail[:300]}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Network error for {url}: {exc.reason}") from exc

    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        preview = body[:300].decode("utf-8", errors="replace")
        raise RuntimeError(f"Invalid JSON response from {url}: {preview}") from exc


def _validate_chain_or_exit(chain: str, parser: argparse.ArgumentParser) -> str:
    normalized = chain.strip().lower()
    if normalized not in SUPPORTED_CHAINS:
        parser.error(
            "--CHAIN must be one of: " + ", ".join(SUPPORTED_CHAINS)
        )
    return normalized


def _get_skylens_trace(network: str, tx: str) -> list[dict]:
    url = f"{SKYLENS_API_BASE}/tx/{network}/{tx}/events"
    payload = _http_get_json(url)

    # Compatible with both old raw-array API and new compressed payload API.
    if isinstance(payload, list):
        return payload

    compressed_result = payload.get("compressedResult")
    if not compressed_result:
        raise ValueError(f"Invalid Skylens response: missing compressedResult, got keys: {list(payload.keys())}")

    trace = _decode_zstd_base64_json(compressed_result)
    if not isinstance(trace, list):
        raise ValueError(f"Decoded Skylens trace must be a list, got {type(trace)}")
    return trace


def _get_skylens_balance_changes(network: str, tx: str) -> dict:
    url = f"{SKYLENS_API_BASE}/tx/{network}/{tx}/balancechanges"
    payload = _http_get_json(url)
    if not isinstance(payload, dict):
        raise ValueError(f"Invalid balancechanges response type: {type(payload)}")
    return payload


def _get_skylens_state_change(network: str, tx: str) -> dict:
    url = f"{SKYLENS_API_BASE}/tx/{network}/{tx}/statechange"
    payload = _http_get_json(url)
    if not isinstance(payload, dict):
        raise ValueError(f"Invalid statechange response type: {type(payload)}")
    compressed_result = payload.get("compressedResult")
    if not compressed_result:
        raise ValueError(
            f"Invalid statechange response: missing compressedResult, got keys: {list(payload.keys())}"
        )
    decoded = _decode_zstd_base64_json(compressed_result)
    if not isinstance(decoded, dict):
        raise ValueError(f"Decoded statechange must be a dict, got {type(decoded)}")
    return decoded


def _get_skylens_source_code_all(network: str, tx: str) -> dict:
    url = f"{SKYLENS_API_BASE}/source?network={network}&txHash={tx}"
    payload = _http_get_json(url)
    if not isinstance(payload, dict):
        raise ValueError(f"Invalid source/code response type: {type(payload)}")

    compressed_result = payload.get("compressedResult")
    if compressed_result:
        decoded = _decode_zstd_base64_json(compressed_result)
    else:
        decoded = payload.get("result")

    if not isinstance(decoded, dict):
        raise ValueError(f"Decoded source/code payload must be a dict, got {type(decoded)}")
    return decoded


def _to_hex_bytes(value: Any) -> str:
    if isinstance(value, list):
        return "0x" + "".join(f"{int(x) & 0xFF:02x}" for x in value)
    if isinstance(value, str):
        return value if value.startswith("0x") else "0x" + value
    return str(value)


def _bytes_from_trace_field(value: Any) -> bytes:
    if value is None:
        return b""
    if isinstance(value, list):
        return bytes((int(v) & 0xFF) for v in value)
    if isinstance(value, str):
        if value.startswith("0x"):
            value = value[2:]
        if value == "":
            return b""
        if len(value) % 2 == 1:
            value = "0" + value
        try:
            return bytes.fromhex(value)
        except ValueError:
            return value.encode("utf-8")
    return str(value).encode("utf-8")


def _format_long_bytes(value: Any) -> str:
    b = _bytes_from_trace_field(value)
    head = b[:10]
    s = head.hex()
    if len(b) > 10:
        s += "..."
    return s


def _value_format(value: Any) -> str:
    try:
        v = int(str(value))
    except Exception:
        return f"{value} wei"
    if v > 10**18:
        return f"{v // 10**18} ETH"
    if v > 10**9:
        return f"{v // 10**9} gwei"
    return f"{v} wei"


def _parse_int(value: Any) -> int | None:
    try:
        return int(str(value))
    except Exception:
        return None


def _format_proto_value(value: dict) -> str:
    if "primitive" in value:
        return str(value["primitive"])
    arr = None
    if "fixedArray" in value:
        arr = value["fixedArray"]
    elif "array" in value:
        arr = value["array"]
    elif "tuple" in value:
        arr = value["tuple"]
    if isinstance(arr, dict):
        vals = arr.get("values") or []
        open_ch, close_ch = ("(", ")") if "tuple" in value else ("[", "]")
        return f"{open_ch}{', '.join(_format_decoded_param(v) for v in vals)}{close_ch}"
    return str(value)


def _format_decoded_param(param: dict) -> str:
    value = param.get("value")
    if value is None:
        return ""
    if not isinstance(value, dict):
        rendered = str(value)
    else:
        rendered = _format_proto_value(value)
    name = param.get("name", "")
    return rendered if name == "" else f"{name}={rendered}"


def _format_decoded_call(call: dict) -> str:
    fn = call.get("functionName", "")
    params = call.get("parameters") or []
    ret_vals = call.get("returnValues") or []
    s = f"{fn}({', '.join(_format_decoded_param(p) for p in params)})"
    if ret_vals:
        s += f" -> ({', '.join(_format_decoded_param(v) for v in ret_vals)})"
    return s


def _format_decoded_log(log: dict) -> str:
    name = log.get("eventName", "")
    topics = log.get("topics") or []
    data = log.get("data") or []
    # Keep same behavior as Rust: topics/data are concatenated directly.
    return (
        f"{name}("
        f"{', '.join(_format_decoded_param(p) for p in topics)}"
        f"{', '.join(_format_decoded_param(p) for p in data)}"
        f")"
    )


def _format_call_event(event: dict) -> str:
    caller = event.get("caller", "")
    target = event.get("targetAddress") or ""
    value = event.get("value", "0")
    data_bytes = _bytes_from_trace_field(event.get("data"))
    decoded_calls = event.get("decodedCalls") or []
    ret = f"{caller}->{target}"
    parsed_value = _parse_int(value)
    if parsed_value is not None and parsed_value != 0:
        ret += f"[value={_value_format(value)}]"
    ret += "."
    if len(data_bytes) >= 4 and decoded_calls and isinstance(decoded_calls[0], dict):
        ret += _format_decoded_call(decoded_calls[0])
    else:
        if len(data_bytes) == 0:
            ret += "fallback()"
        else:
            ret += f"call({_format_long_bytes(data_bytes)})"
        return_value = _bytes_from_trace_field(event.get("returnValue"))
        if len(return_value) > 0:
            ret += f" -> ({_format_long_bytes(return_value)})"
    return ret


def _format_create_event(event: dict) -> str:
    initiator = event.get("initiator", "")
    at = event.get("at", "")
    value = event.get("value", "0")
    init_code = event.get("initCode")
    ret = ""
    if str(value) != "0":
        ret += f" value={_value_format(value)}"
    ret += f"{initiator}->0x0({_format_long_bytes(init_code)})"
    if at:
        ret += f" -> {at}"
    return ret


def _format_storage_access_event(event: dict) -> str:
    initiator = event.get("initiator", "")
    slot = event.get("slot", "")
    original_value = event.get("originalValue")
    new_value = event.get("newValue")
    orig_raw = ""
    new_raw = None
    if isinstance(original_value, dict):
        orig_raw = str(original_value.get("raw", "0x0"))
    else:
        orig_raw = str(original_value)
    if isinstance(new_value, dict):
        new_raw = str(new_value.get("raw", "0x0"))
    elif new_value is not None:
        new_raw = str(new_value)

    ret = f"{initiator}[0x{slot}] = {orig_raw}"
    if new_raw is not None:
        ret += f"-> {new_raw}"
    return ret


def _format_keccak256_event(event: dict) -> str:
    initiator = event.get("initiator", "?")
    offset = event.get("offset", "?")
    size = event.get("size", "?")
    hash_hex = _to_hex_bytes(event.get("hash"))
    return f"KECCAK256 {initiator} | offset={offset} size={size} | hash={hash_hex}"


def _format_log_event(event: dict) -> str:
    initiator = event.get("initiator", "?")
    decoded_logs = event.get("decodedLogs") or []
    if decoded_logs:
        first = decoded_logs[0]
        if isinstance(first, dict):
            return _format_decoded_log(first)
    topics = event.get("topics") or []
    data = event.get("data") or ""
    parts = [f"{initiator}("]
    for i, topic in enumerate(topics):
        if isinstance(topic, dict):
            topic_v = topic.get("topic", "")
        else:
            topic_v = str(topic)
        parts.append(f"topic{i}={topic_v},")
    if data:
        parts.append(f"data={_format_long_bytes(data)},")
    parts.append(")")
    return "".join(parts)

def format_trace_item(item: dict) -> str:
    event = item.get("event", {})
    if not isinstance(event, dict) or not event:
        return "depth=-1 | unknown | malformed event"

    event_type, event_data = next(iter(event.items()))
    if not isinstance(event_data, dict):
        return f"depth=-1 | {event_type} | malformed payload"

    depth = event_data.get("depth", -1)
    index = event_data.get("index", item.get("instIdx", -1))
    op = (
        event_data.get("op")
        or (
            "LOG"
            if event_type == "logEvent"
            else "KECCAK256" if event_type == "keccak256Event" else "UNKNOWN"
        )
    )

    if event_type == "callEvent":
        detail = _format_call_event(event_data)
    elif event_type == "createEvent":
        detail = _format_create_event(event_data)
    elif event_type == "storageAccessEvent":
        detail = _format_storage_access_event(event_data)
    elif event_type == "keccak256Event":
        detail = _format_keccak256_event(event_data)
    elif event_type == "logEvent":
        detail = _format_log_event(event_data)
    else:
        detail = json.dumps(event_data, ensure_ascii=False, separators=(",", ":"))

    line = f"{index}({depth}) {op} {detail}"
    position = item.get("position")
    if isinstance(position, dict):
        contract_address = position.get("contractAddress", "")
        file_idx = position.get("fileIdx", "")
        start = position.get("start", "")
        length = position.get("length", "")
        line += f" source: [c: {contract_address}, f:{file_idx}, s:{start}, o:{length}]"
    return line

def tx_trace(network: str, tx: str) -> list[str]:
    trace = _get_skylens_trace(network, tx)
    return [format_trace_item(item) for item in trace]


def _normalize_addr(addr: str) -> str:
    s = addr.strip().lower()
    if s.startswith("0x"):
        s = s[2:]
    return s


def _fmt_delta(delta: str) -> str:
    return f"+{delta}" if not delta.startswith("-") else delta


def _extract_balance_lines(
    root: dict, holder: str, section_name: str, subject_label: str = "holder"
) -> list[str]:
    holder_norm = _normalize_addr(holder)
    lines: list[str] = []

    # Native balance changes keyed by holder address.
    native_changes = root.get("nativeBalanceChange", {})
    if isinstance(native_changes, dict):
        for addr, change in native_changes.items():
            if _normalize_addr(addr) != holder_norm or not isinstance(change, dict):
                continue
            before = str(change.get("before", ""))
            after = str(change.get("after", ""))
            delta = str(change.get("delta", "0"))
            lines.append(
                f"{section_name} Native ETH: {subject_label}={addr} before={before} after={after} delta={_fmt_delta(delta)}"
            )

    # Token changes: top-level key is token address, nested key is holder address.
    token_changes = root.get("tokenBalanceChange", {})
    if isinstance(token_changes, dict):
        for token_addr, token_entry in token_changes.items():
            if not isinstance(token_entry, dict):
                continue
            token = str(token_entry.get("token", token_addr))
            holder_map = token_entry.get("tokenBalanceChange", {})
            if not isinstance(holder_map, dict):
                continue
            for addr, change in holder_map.items():
                if _normalize_addr(addr) != holder_norm or not isinstance(change, dict):
                    continue
                before = str(change.get("before", ""))
                after = str(change.get("after", ""))
                delta = str(change.get("delta", "0"))
                lines.append(
                    f"{section_name} Token: token={token} {subject_label}={addr} before={before} after={after} delta={_fmt_delta(delta)}"
                )

    # NFT changes can vary by schema; keep robust and human-readable.
    nft_changes = root.get("nftBalanceChange", {})
    if isinstance(nft_changes, dict):
        for collection, collection_entry in nft_changes.items():
            if not isinstance(collection_entry, dict):
                continue
            holder_map = collection_entry.get("nftBalanceChange", collection_entry)
            if not isinstance(holder_map, dict):
                continue
            for addr, change in holder_map.items():
                if _normalize_addr(addr) != holder_norm:
                    continue
                if isinstance(change, dict):
                    before = str(change.get("before", ""))
                    after = str(change.get("after", ""))
                    delta = str(change.get("delta", "0"))
                    lines.append(
                        f"{section_name} NFT: collection={collection} {subject_label}={addr} before={before} after={after} delta={_fmt_delta(delta)}"
                    )
                else:
                    lines.append(
                        f"{section_name} NFT: collection={collection} {subject_label}={addr} change={change}"
                    )
    return lines


def balance_change(network: str, tx: str, holder: str) -> list[str]:
    payload = _get_skylens_balance_changes(network, tx)
    root = payload.get("balanceChangeFromBalanceOf", {})
    if not isinstance(root, dict):
        return [f"No balance change payload found for tx={tx}"]
    lines = _extract_balance_lines(root, holder, "BalanceOf")
    if not lines:
        lines.append(f"No balance change found for holder={holder} in tx={tx} on chain={network}")
    return lines


def _extract_primitive(value: Any) -> str:
    if isinstance(value, dict):
        inner = value.get("value")
        if isinstance(inner, dict) and "primitive" in inner:
            return str(inner["primitive"])
        if "raw" in value:
            return str(value["raw"])
    return str(value)


def state_change(network: str, tx: str, holder: str) -> list[str]:
    data = _get_skylens_state_change(network, tx)
    holder_norm = _normalize_addr(holder)
    lines: list[str] = []

    storage_change = data.get("storageChange", {})
    if isinstance(storage_change, dict):
        for addr, change in storage_change.items():
            if _normalize_addr(addr) != holder_norm or not isinstance(change, dict):
                continue
            slot_change = change.get("slotChange", {})
            if not isinstance(slot_change, dict):
                continue
            for slot, slot_delta in slot_change.items():
                if not isinstance(slot_delta, dict):
                    continue
                before = slot_delta.get("before", {})
                after = slot_delta.get("after", {})
                before_raw = before.get("raw") if isinstance(before, dict) else before
                after_raw = after.get("raw") if isinstance(after, dict) else after
                lines.append(
                    f"Storage: address={addr} slot=0x{slot} before={before_raw} after={after_raw}"
                )

    if not lines:
        lines.append(f"No storage change found for address={holder} in tx={tx} on chain={network}")
    return lines


def nonce_change(network: str, tx: str, address: str) -> list[str]:
    data = _get_skylens_state_change(network, tx)
    target = _normalize_addr(address)
    nonce_change_map = data.get("nonceChange", {})
    if not isinstance(nonce_change_map, dict):
        return [f"No nonce change found for address={address} in tx={tx} on chain={network}"]

    lines: list[str] = []
    for addr, change in nonce_change_map.items():
        if _normalize_addr(addr) != target or not isinstance(change, dict):
            continue
        before = _extract_primitive(change.get("before"))
        after = _extract_primitive(change.get("after"))
        lines.append(f"Nonce: address={addr} before={before} after={after}")

    if not lines:
        lines.append(f"No nonce change found for address={address} in tx={tx} on chain={network}")
    return lines


def _parse_contract_artifact(raw: Any) -> dict:
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            return {}
    return {}


def _build_source_code_files_index(source_payload: dict, contract_address: str) -> tuple[str | None, list[dict]]:
    target = _normalize_addr(contract_address)
    matched_key = None
    for key in source_payload.keys():
        if _normalize_addr(str(key)) == target:
            matched_key = str(key)
            break
    if matched_key is None:
        return None, []

    entry = source_payload.get(matched_key)
    if not isinstance(entry, dict):
        return matched_key, []

    source_code_entries = entry.get("sourceCode")
    if not isinstance(source_code_entries, list):
        return matched_key, []

    files: list[dict] = []
    for artifact_idx, raw_artifact in enumerate(source_code_entries):
        artifact = _parse_contract_artifact(raw_artifact)
        artifact_name = str(artifact.get("name") or f"artifact_{artifact_idx}")
        sources = artifact.get("sources")
        if not isinstance(sources, list):
            continue

        for src in sources:
            name: str | None = None
            content: str | None = None

            # Common shape observed: ["Contract.sol", {"content": "..."}]
            if isinstance(src, list):
                if src and isinstance(src[0], str):
                    name = src[0]
                if len(src) > 1 and isinstance(src[1], dict):
                    c = src[1].get("content")
                    if isinstance(c, str):
                        content = c
            elif isinstance(src, dict):
                name = str(src.get("path") or src.get("name") or "")
                c = src.get("content")
                if isinstance(c, str):
                    content = c
            elif isinstance(src, str):
                name = f"{artifact_name}-source-{len(files)}"
                content = src

            if not name:
                name = f"{artifact_name}-source-{len(files)}"

            files.append(
                {
                    "index": len(files),
                    "artifact_name": artifact_name,
                    "name": name,
                    "content": content,
                }
            )
    return matched_key, files


def list_source_files(network: str, tx: str, address: str) -> list[str]:
    source_payload = _get_skylens_source_code_all(network, tx)
    matched_key, files = _build_source_code_files_index(source_payload, address)
    if matched_key is None:
        return [f"Contract not found in source/code payload: address={address}"]
    if not files:
        return [f"No source files found for address={matched_key} in tx={tx} on chain={network}"]

    lines = [f"Contract: {matched_key}", f"Files: {len(files)}"]
    for item in files:
        availability = "source" if isinstance(item.get("content"), str) and item["content"].strip() else "none"
        lines.append(
            f"[{item['index']}] {item['name']} (artifact={item['artifact_name']}, available={availability})"
        )
    return lines


def get_source_file(
    network: str, tx: str, address: str, file_index: int, output: str | None = None
) -> list[str]:
    source_payload = _get_skylens_source_code_all(network, tx)
    matched_key, files = _build_source_code_files_index(source_payload, address)
    if matched_key is None:
        return [f"Contract not found in source/code payload: address={address}"]
    if not files:
        return [f"No source files found for address={matched_key} in tx={tx} on chain={network}"]
    if file_index < 0 or file_index >= len(files):
        return [
            f"Invalid file index: {file_index}. Available range: 0..{len(files)-1}",
        ]

    target = files[file_index]
    header = (
        f"File[{target['index']}]: {target['name']} "
        f"(contract={matched_key}, artifact={target['artifact_name']})"
    )

    if isinstance(target.get("content"), str):
        content = target["content"]
        if output:
            out_path = Path(output).expanduser()
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(content, encoding="utf-8")
            return [header, f"Saved source file to: {out_path}"]
        return [header, content]
    return [header, "# Source content is unavailable for this file"]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Skylens trace helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    get_trace = subparsers.add_parser(
        "get-trace",
        help="Get readable trace lines from a transaction",
    )
    get_trace.add_argument("--TX", dest="tx", required=True, help="Transaction hash")
    get_trace.add_argument("--CHAIN", dest="chain", required=True, help="Chain key")
    get_trace.add_argument(
        "--OFFSET",
        dest="offset",
        type=int,
        default=0,
        help="Start index (default: 0)",
    )
    get_trace.add_argument(
        "--SIZE",
        dest="size",
        type=int,
        default=100,
        help="Page size (default: 100)",
    )

    balance_change_parser = subparsers.add_parser(
        "balance-change",
        help="Get holder balance changes from a transaction",
    )
    balance_change_parser.add_argument("--TX", dest="tx", required=True, help="Transaction hash")
    balance_change_parser.add_argument("--CHAIN", dest="chain", required=True, help="Chain key")
    balance_change_parser.add_argument("--HOLDER", dest="holder", required=True, help="Holder address")

    state_change_parser = subparsers.add_parser(
        "state-change",
        help="Get address state changes from a transaction",
    )
    state_change_parser.add_argument("--TX", dest="tx", required=True, help="Transaction hash")
    state_change_parser.add_argument("--CHAIN", dest="chain", required=True, help="Chain key")
    state_change_parser.add_argument("--ADDRESS", dest="address", required=True, help="Address")

    nonce_change_parser = subparsers.add_parser(
        "nonce-change",
        help="Get address nonce change from a transaction",
    )
    nonce_change_parser.add_argument("--TX", dest="tx", required=True, help="Transaction hash")
    nonce_change_parser.add_argument("--CHAIN", dest="chain", required=True, help="Chain key")
    nonce_change_parser.add_argument("--ADDRESS", dest="address", required=True, help="Address")

    list_source_files_parser = subparsers.add_parser(
        "list-source-files",
        help="List source files for a contract in one transaction",
    )
    list_source_files_parser.add_argument("--TX", dest="tx", required=True, help="Transaction hash")
    list_source_files_parser.add_argument("--CHAIN", dest="chain", required=True, help="Chain key")
    list_source_files_parser.add_argument("--ADDRESS", dest="address", required=True, help="Contract address")

    get_source_file_parser = subparsers.add_parser(
        "get-source-file",
        help="Get one source file by index for a contract in one transaction",
    )
    get_source_file_parser.add_argument("--TX", dest="tx", required=True, help="Transaction hash")
    get_source_file_parser.add_argument("--CHAIN", dest="chain", required=True, help="Chain key")
    get_source_file_parser.add_argument("--ADDRESS", dest="address", required=True, help="Contract address")
    get_source_file_parser.add_argument(
        "--FILE_INDEX",
        dest="file_index",
        required=True,
        type=int,
        help="File index from list-source-files output",
    )
    get_source_file_parser.add_argument(
        "--OUTPUT",
        dest="output",
        required=False,
        help="Optional output file path to save source content",
    )

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "get-trace":
        chain = _validate_chain_or_exit(args.chain, parser)
        if args.offset < 0:
            parser.error("--OFFSET must be >= 0")
        if args.size <= 0:
            parser.error("--SIZE must be > 0")

        lines = tx_trace(chain, args.tx)
        paged = lines[args.offset : args.offset + args.size]
        if not paged:
            print(
                f"No trace lines in page: offset={args.offset}, size={args.size}, total={len(lines)}",
                file=sys.stderr,
            )
            return 2
        for line in paged:
            print(line)
        return 0

    if args.command == "balance-change":
        chain = _validate_chain_or_exit(args.chain, parser)
        lines = balance_change(chain, args.tx, args.holder)
        for line in lines:
            print(line)
        return 0

    if args.command == "state-change":
        chain = _validate_chain_or_exit(args.chain, parser)
        lines = state_change(chain, args.tx, args.address)
        for line in lines:
            print(line)
        return 0

    if args.command == "nonce-change":
        chain = _validate_chain_or_exit(args.chain, parser)
        lines = nonce_change(chain, args.tx, args.address)
        for line in lines:
            print(line)
        return 0

    if args.command == "list-source-files":
        chain = _validate_chain_or_exit(args.chain, parser)
        lines = list_source_files(chain, args.tx, args.address)
        for line in lines:
            print(line)
        return 0

    if args.command == "get-source-file":
        chain = _validate_chain_or_exit(args.chain, parser)
        lines = get_source_file(chain, args.tx, args.address, args.file_index, args.output)
        for line in lines:
            print(line)
        return 0

    parser.error(f"unsupported command: {args.command}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())