#!/usr/bin/env python3
r"""toon_json.py

A compact, *reversible* JSON <-> TOON encoder/decoder.

Design goals:
- Deterministic and lossless for JSON types (object, array, string, number, boolean, null)
- Smaller than JSON in tokens by:
  - optional key dictionary (schema) with short tokens
  - removal of quotes around keys (by mapping)
  - compact separators

Format (TOON v1):

A TOON document is either:
- without schema:  v1|J|<payload>
- with schema:     v1|S|<schema_b64>|<payload>

Where:
- <schema_b64> is base64url(JSON(schema)) without padding.
- <payload> is a compact token stream.

Token stream grammar (no whitespace):
- Object:  { <pairs>? }
  - pairs: <key><value>(;<key><value>)*
  - key is:
    - if schema present: ~<id> where <id> is base36
    - else: '...' (single-quoted string)
- Array:   [ <value>? (;<value>)* ]
- String:  '...'
- Number:  n<json-number> (e.g., n-1.2e3, n0, n3.14)
- True:    t
- False:   f
- Null:    z

String escaping inside single quotes:
- \\  -> \\ 
- \'  -> '
- \n, \r, \t supported
- \uXXXX supported

This script provides:
- encode: JSON -> TOON (optionally with schema)
- decode: TOON -> JSON
- schema: derive schema (key dictionary) from JSON

"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import sys
from typing import Any, Dict, List, Tuple


NUM_RE = re.compile(r"-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?$")


def b64url_no_pad(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def b64url_decode_no_pad(s: str) -> bytes:
    pad = "=" * ((4 - (len(s) % 4)) % 4)
    return base64.urlsafe_b64decode((s + pad).encode("ascii"))


def schema_digest(schema: Dict[str, Any]) -> str:
    raw = json.dumps(schema, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]


def escape_str(s: str) -> str:
    # Minimal JSON-like escapes plus single-quote.
    out = []
    for ch in s:
        o = ord(ch)
        if ch == "\\":
            out.append("\\\\")
        elif ch == "'":
            out.append("\\'")
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        elif o < 0x20:
            out.append(f"\\u{o:04x}")
        else:
            out.append(ch)
    return "".join(out)


def unescape_str(s: str) -> str:
    # s has no surrounding quotes
    i = 0
    out = []
    while i < len(s):
        ch = s[i]
        if ch != "\\":
            out.append(ch)
            i += 1
            continue
        if i + 1 >= len(s):
            raise ValueError("Invalid escape at end of string")
        nxt = s[i + 1]
        if nxt == "\\":
            out.append("\\")
            i += 2
        elif nxt == "'":
            out.append("'")
            i += 2
        elif nxt == "n":
            out.append("\n")
            i += 2
        elif nxt == "r":
            out.append("\r")
            i += 2
        elif nxt == "t":
            out.append("\t")
            i += 2
        elif nxt == "u":
            if i + 6 > len(s):
                raise ValueError("Invalid unicode escape")
            hexpart = s[i + 2 : i + 6]
            out.append(chr(int(hexpart, 16)))
            i += 6
        else:
            raise ValueError(f"Unsupported escape: \\{nxt}")
    return "".join(out)


def to_base36(n: int) -> str:
    chars = "0123456789abcdefghijklmnopqrstuvwxyz"
    if n == 0:
        return "0"
    neg = n < 0
    n = abs(n)
    digits = []
    while n:
        n, r = divmod(n, 36)
        digits.append(chars[r])
    s = "".join(reversed(digits))
    return "-" + s if neg else s


def from_base36(s: str) -> int:
    return int(s, 36)


def derive_schema(obj: Any, max_keys: int = 2048) -> Dict[str, Any]:
    # Collect keys by frequency (descending), then alphabetical.
    freq: Dict[str, int] = {}

    def walk(x: Any):
        if isinstance(x, dict):
            for k, v in x.items():
                if isinstance(k, str):
                    freq[k] = freq.get(k, 0) + 1
                walk(v)
        elif isinstance(x, list):
            for it in x:
                walk(it)

    walk(obj)
    items = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:max_keys]
    keys = [k for k, _ in items]
    key_to_id = {k: i for i, k in enumerate(keys)}
    return {"v": 1, "keys": keys, "key_to_id": key_to_id, "digest": None}


def _encode_value(x: Any, key_to_id: Dict[str, int] | None) -> str:
    if x is None:
        return "z"
    if x is True:
        return "t"
    if x is False:
        return "f"
    if isinstance(x, (int, float)) and not isinstance(x, bool):
        # JSON numbers (no NaN/Inf)
        s = json.dumps(x, separators=(",", ":"))
        if not NUM_RE.match(s):
            raise ValueError(f"Invalid JSON number: {s}")
        return "n" + s
    if isinstance(x, str):
        return "'" + escape_str(x) + "'"
    if isinstance(x, list):
        if not x:
            return "[]"
        return "[" + ";".join(_encode_value(it, key_to_id) for it in x) + "]"
    if isinstance(x, dict):
        if not x:
            return "{}"
        parts: List[str] = []
        for k, v in x.items():
            if not isinstance(k, str):
                raise ValueError("Only string keys are supported")
            if key_to_id is not None and k in key_to_id:
                kid = to_base36(key_to_id[k])
                parts.append("~" + kid + _encode_value(v, key_to_id))
            else:
                parts.append("'" + escape_str(k) + "'" + _encode_value(v, key_to_id))
        return "{" + ";".join(parts) + "}"
    raise ValueError(f"Unsupported type: {type(x)}")


def encode_json(obj: Any, use_schema: bool = False, max_keys: int = 2048) -> Tuple[str, Dict[str, Any] | None]:
    schema = None
    key_to_id = None
    if use_schema:
        schema = derive_schema(obj, max_keys=max_keys)
        # fill digest
        schema2 = {"v": schema["v"], "keys": schema["keys"]}
        schema["digest"] = schema_digest(schema2)
        key_to_id = schema["key_to_id"]
    payload = _encode_value(obj, key_to_id)
    if schema is None:
        return "v1|J|" + payload, None
    schema_min = {"v": 1, "keys": schema["keys"], "digest": schema["digest"]}
    schema_b64 = b64url_no_pad(json.dumps(schema_min, separators=(",", ":"), sort_keys=True).encode("utf-8"))
    return f"v1|S|{schema_b64}|{payload}", schema_min


class Parser:
    def __init__(self, s: str, schema_keys: List[str] | None):
        self.s = s
        self.i = 0
        self.schema_keys = schema_keys

    def peek(self) -> str:
        return self.s[self.i : self.i + 1]

    def take(self, ch: str):
        if self.peek() != ch:
            raise ValueError(f"Expected '{ch}' at {self.i}")
        self.i += 1

    def parse(self) -> Any:
        v = self.parse_value()
        if self.i != len(self.s):
            raise ValueError(f"Trailing data at {self.i}")
        return v

    def parse_value(self) -> Any:
        ch = self.peek()
        if ch == "{":
            return self.parse_obj()
        if ch == "[":
            return self.parse_arr()
        if ch == "'":
            return self.parse_str()
        if ch == "n":
            return self.parse_num()
        if ch == "-":
            # negative schema key id (only valid in key position, but tolerate here)
            raise ValueError(f"Unexpected '-' at {self.i}")
        if ch == "t":
            self.i += 1
            return True
        if ch == "f":
            self.i += 1
            return False
        if ch == "z":
            self.i += 1
            return None
        raise ValueError(f"Unexpected token '{ch}' at {self.i}")

    def parse_str(self) -> str:
        self.take("'")
        start = self.i
        out = []
        while True:
            if self.i >= len(self.s):
                raise ValueError("Unterminated string")
            ch = self.s[self.i]
            if ch == "'":
                raw = "".join(out) + self.s[start:self.i]
                self.i += 1
                return unescape_str(raw)
            if ch == "\\":
                # flush chunk before escape
                out.append(self.s[start:self.i])
                # include escape sequence marker, will be processed by unescape
                if self.i + 1 >= len(self.s):
                    raise ValueError("Bad escape")
                # keep escape as text
                if self.s[self.i + 1] == "u":
                    if self.i + 6 > len(self.s):
                        raise ValueError("Bad unicode escape")
                    out.append(self.s[self.i:self.i+6])
                    self.i += 6
                else:
                    out.append(self.s[self.i:self.i+2])
                    self.i += 2
                start = self.i
            else:
                self.i += 1

    def parse_num(self) -> Any:
        self.take("n")
        start = self.i
        while self.i < len(self.s) and self.s[self.i] not in ";]}":
            self.i += 1
        raw = self.s[start:self.i]
        if not raw or not NUM_RE.match(raw):
            raise ValueError(f"Invalid number at {start}")
        # Keep integers as int when possible
        if "." not in raw and "e" not in raw and "E" not in raw:
            return int(raw)
        return float(raw)

    def parse_arr(self) -> List[Any]:
        self.take("[")
        if self.peek() == "]":
            self.i += 1
            return []
        items = [self.parse_value()]
        while self.peek() == ";":
            self.i += 1
            items.append(self.parse_value())
        self.take("]")
        return items

    def parse_key(self) -> str:
        ch = self.peek()
        if ch == "~":
            if self.schema_keys is None:
                raise ValueError("Schema key used but no schema present")
            self.i += 1
            start = self.i
            if self.peek() == "-":
                self.i += 1
            while self.i < len(self.s) and self.s[self.i] in "0123456789abcdefghijklmnopqrstuvwxyz":
                # stop if next token begins a value
                if self.i > start and self.s[self.i] in "ntfz{['":
                    break
                self.i += 1
            kid = self.s[start:self.i]
            if kid in ("", "-"):
                raise ValueError("Empty schema key")
            idx = from_base36(kid)
            if idx < 0 or idx >= len(self.schema_keys):
                raise ValueError(f"Schema key index out of range: {idx}")
            return self.schema_keys[idx]
        if ch == "'":
            return self.parse_str()
        raise ValueError(f"Invalid key token '{ch}' at {self.i}")

    def parse_obj(self) -> Dict[str, Any]:
        self.take("{")
        if self.peek() == "}":
            self.i += 1
            return {}
        obj: Dict[str, Any] = {}
        k = self.parse_key()
        v = self.parse_value()
        obj[k] = v
        while self.peek() == ";":
            self.i += 1
            k = self.parse_key()
            v = self.parse_value()
            obj[k] = v
        self.take("}")
        return obj


def decode_toon(toon: str) -> Tuple[Any, Dict[str, Any] | None]:
    if not toon.startswith("v1|"):
        raise ValueError("Unsupported TOON header")
    parts = toon.split("|", 3)
    if len(parts) < 3:
        raise ValueError("Invalid TOON")
    _, kind, rest = parts[0], parts[1], "|".join(parts[2:])

    schema = None
    payload = None

    if kind == "J":
        payload = rest
        keys = None
    elif kind == "S":
        sub = rest.split("|", 1)
        if len(sub) != 2:
            raise ValueError("Invalid schema TOON")
        schema_b64, payload = sub
        schema = json.loads(b64url_decode_no_pad(schema_b64).decode("utf-8"))
        keys = schema.get("keys")
        if not isinstance(keys, list):
            raise ValueError("Schema keys missing")
    else:
        raise ValueError("Unknown TOON kind")

    parser = Parser(payload, keys)
    obj = parser.parse()
    return obj, schema


def cmd_encode(args: argparse.Namespace) -> int:
    src = sys.stdin.read() if args.input == "-" else open(args.input, "r", encoding="utf-8").read()
    obj = json.loads(src)
    toon, schema = encode_json(obj, use_schema=args.schema, max_keys=args.max_keys)
    if args.pretty:
        out = {"toon": toon}
        if schema:
            out["schema"] = schema
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(toon)
    return 0


def cmd_decode(args: argparse.Namespace) -> int:
    toon = sys.stdin.read().strip() if args.input == "-" else open(args.input, "r", encoding="utf-8").read().strip()
    obj, schema = decode_toon(toon)
    if args.pretty:
        out = {"json": obj}
        if schema:
            out["schema"] = schema
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(obj, ensure_ascii=False, separators=(",", ":")))
    return 0


def cmd_schema(args: argparse.Namespace) -> int:
    src = sys.stdin.read() if args.input == "-" else open(args.input, "r", encoding="utf-8").read()
    obj = json.loads(src)
    schema = derive_schema(obj, max_keys=args.max_keys)
    schema_min = {"v": 1, "keys": schema["keys"]}
    print(json.dumps({"schema": schema_min, "digest": schema_digest(schema_min)}, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(prog="toon-json", description="Lossless JSON <-> TOON encoder/decoder")
    sub = p.add_subparsers(dest="cmd", required=True)

    pe = sub.add_parser("encode", help="Encode JSON to TOON")
    pe.add_argument("-i", "--input", default="-", help="Input JSON file or - for stdin")
    pe.add_argument("--schema", action="store_true", help="Include key schema for compactness")
    pe.add_argument("--max-keys", type=int, default=2048)
    pe.add_argument("--pretty", action="store_true", help="Output JSON wrapper with schema")
    pe.set_defaults(func=cmd_encode)

    pd = sub.add_parser("decode", help="Decode TOON to JSON")
    pd.add_argument("-i", "--input", default="-", help="Input TOON file or - for stdin")
    pd.add_argument("--pretty", action="store_true")
    pd.set_defaults(func=cmd_decode)

    ps = sub.add_parser("schema", help="Derive schema from JSON")
    ps.add_argument("-i", "--input", default="-", help="Input JSON file or - for stdin")
    ps.add_argument("--max-keys", type=int, default=2048)
    ps.set_defaults(func=cmd_schema)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
