#!/usr/bin/env python3
"""PassGen · 纯本地密码与密钥生成器

基于 Python 标准库 secrets（密码学安全随机数）。零第三方依赖、跨平台、
无网络、无 API Key。所有输出仅打印到终端，不落盘、不上传。

子命令：password / passphrase / token / uuid / pin / strength
"""
import argparse
import base64
import math
import secrets
import string
import sys
import uuid

# 内置常用英文单词表（用于密码短语；约 280 词，随包分发，无需外部字典）
WORDLIST = (
    "apple", "banana", "bread", "brick", "cake", "candy", "clock", "cloud",
    "crane", "creek", "crime", "crown", "dance", "deck", "dog", "dream",
    "dress", "drill", "duck", "eagle", "earth", "ember", "enemy", "engine",
    "essay", "face", "fact", "fairy", "fame", "farm", "fear", "feather",
    "field", "fire", "fish", "flame", "floor", "flower", "fog", "forest",
    "fork", "fox", "frame", "free", "frog", "frost", "fruit", "game",
    "garden", "gate", "ghost", "gift", "glass", "glide", "gold", "goose",
    "grape", "grass", "grave", "green", "ground", "gulf", "hair", "half",
    "hall", "hand", "happy", "harbor", "hawk", "hazel", "heart", "heel",
    "hill", "hive", "honey", "horn", "horse", "host", "hour", "house",
    "ice", "icon", "idea", "iron", "island", "ivy", "item", "jacket",
    "jade", "jail", "jazz", "jelly", "jewel", "joke", "joy", "jump",
    "jungle", "keel", "kite", "knee", "knife", "knot", "lake", "lamp",
    "land", "leaf", "lemon", "light", "lime", "lion", "list", "lock",
    "log", "luck", "maple", "marble", "marsh", "meadow", "metal", "milk",
    "mint", "mirror", "mist", "money", "moon", "moss", "moth", "mouse",
    "mountain", "mud", "music", "nail", "navy", "needle", "nest", "net",
    "news", "night", "noble", "north", "note", "oak", "ocean", "olive",
    "onion", "orange", "oval", "owl", "oxen", "page", "paint", "palm",
    "panel", "paper", "park", "pearl", "pen", "pet", "phone", "piano",
    "pine", "pink", "pipe", "planet", "plant", "plate", "plum", "pond",
    "pool", "port", "prize", "queen", "quilt", "rabbit", "rail", "rain",
    "rat", "raven", "reed", "river", "road", "robin", "rock", "rose",
    "royal", "ruby", "rug", "sail", "salt", "sand", "scale", "seal",
    "seed", "shadow", "sheep", "shelf", "shell", "ship", "shirt", "shoe",
    "shore", "sign", "silk", "silver", "skate", "sky", "slate", "sloth",
    "snail", "snow", "soap", "soil", "song", "soul", "sparrow", "specter",
    "spider", "spike", "spine", "spring", "squirrel", "star", "steam",
    "stone", "storm", "straw", "stream", "sugar", "summer", "sun", "swamp",
    "swan", "table", "tail", "tiger", "token", "tool", "tower", "town",
    "train", "tree", "trout", "tulip", "tunnel", "turtle", "twig", "urban",
    "vale", "vault", "vine", "voice", "volcano", "wagon", "wall", "water",
    "wave", "wax", "web", "weed", "wheel", "willow", "wind", "window",
    "wing", "winter", "wish", "witch", "wolf", "wood", "wool", "word",
    "worm", "wrist", "yarn", "yard", "year", "yew", "zebra", "zest",
    "zinc", "zone",
)

SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?"


def _charset(lower, upper, digits, symbols, no_ambiguous):
    amb = set("il1Lo0O|`'\";:.,")
    low = string.ascii_lowercase
    up = string.ascii_uppercase
    dig = string.digits
    sym = SYMBOLS
    if no_ambiguous:
        low = "".join(c for c in low if c not in amb)
        up = "".join(c for c in up if c not in amb)
        dig = "".join(c for c in dig if c not in amb)
        sym = "".join(c for c in sym if c not in amb)
    groups = []
    if lower:
        groups.append(low)
    if upper:
        groups.append(up)
    if digits:
        groups.append(dig)
    if symbols:
        groups.append(sym)
    return groups


def gen_password(length=16, lower=True, upper=True, digits=True, symbols=True,
                 no_ambiguous=False, count=1):
    groups = _charset(lower, upper, digits, symbols, no_ambiguous)
    if not groups:
        raise ValueError("至少需要启用一种字符集（--lower/--upper/--digits/--symbols）")
    pool = "".join(groups)
    length = max(length, len(groups))
    rng = secrets.SystemRandom()
    for _ in range(count):
        chars = [secrets.choice(g) for g in groups]          # 每类至少 1 个
        chars += [secrets.choice(pool) for _ in range(length - len(groups))]
        rng.shuffle(chars)
        yield "".join(chars)


def gen_passphrase(words=5, sep="-", add_number=False, count=1):
    for _ in range(count):
        picked = [secrets.choice(WORDLIST) for _ in range(words)]
        phrase = sep.join(picked)
        if add_number:
            phrase += sep + str(secrets.randbelow(9000) + 1000)
        yield phrase


def gen_token(nbytes=32, fmt="urlsafe", count=1):
    for _ in range(count):
        raw = secrets.token_bytes(nbytes)
        if fmt == "hex":
            yield raw.hex()
        elif fmt == "urlsafe":
            yield base64.urlsafe_b64encode(raw).rstrip(b"=").decode()
        elif fmt == "base64":
            yield base64.b64encode(raw).decode()
        else:
            raise ValueError("fmt 必须为 hex | urlsafe | base64")


def gen_uuid(count=1):
    for _ in range(count):
        yield str(uuid.uuid4())


def gen_pin(length=6, count=1):
    for _ in range(count):
        yield "".join(secrets.choice(string.digits) for _ in range(length))


def estimate_strength(pw):
    space = 0
    if any(c.islower() for c in pw):
        space += 26
    if any(c.isupper() for c in pw):
        space += 26
    if any(c.isdigit() for c in pw):
        space += 10
    if any(not c.isalnum() for c in pw):
        space += len(SYMBOLS)
    if space == 0:
        space = 1
    entropy = len(pw) * math.log2(space)
    if entropy < 28:
        rating = "极弱"
    elif entropy < 40:
        rating = "弱"
    elif entropy < 60:
        rating = "中"
    elif entropy < 80:
        rating = "强"
    else:
        rating = "极强"
    tips = []
    if len(pw) < 12:
        tips.append("长度建议 ≥ 12")
    if not any(c.islower() for c in pw):
        tips.append("加入小写字母")
    if not any(c.isupper() for c in pw):
        tips.append("加入大写字母")
    if not any(c.isdigit() for c in pw):
        tips.append("加入数字")
    if not any(not c.isalnum() for c in pw):
        tips.append("加入符号")
    return len(pw), space, round(entropy, 1), rating, tips


# --------------------------------------------------------------------------- #
# 子命令
# --------------------------------------------------------------------------- #
def _emit(generator):
    for item in generator:
        print(item)


def cmd_password(args):
    _emit(gen_password(
        length=args.length, lower=not args.no_lower, upper=not args.no_upper,
        digits=not args.no_digits, symbols=not args.no_symbols,
        no_ambiguous=args.no_ambiguous, count=args.count))


def cmd_passphrase(args):
    _emit(gen_passphrase(
        words=args.words, sep=args.sep, add_number=args.add_number, count=args.count))


def cmd_token(args):
    _emit(gen_token(nbytes=args.bytes, fmt=args.format, count=args.count))


def cmd_uuid(args):
    _emit(gen_uuid(count=args.count))


def cmd_pin(args):
    _emit(gen_pin(length=args.length, count=args.count))


def cmd_strength(args):
    pw = args.password
    if pw is None:
        pw = sys.stdin.read().strip()
    if not pw:
        sys.exit("[错误] 未提供待检测的口令（参数或 stdin）")
    length, space, entropy, rating, tips = estimate_strength(pw)
    print(f"长度      : {length}")
    print(f"字符空间  : {space} 种")
    print(f"估算熵    : {entropy} bits")
    print(f"强度评级  : {rating}")
    print(f"字符类    : "
          f"{'小写 ' if any(c.islower() for c in pw) else ''}"
          f"{'大写 ' if any(c.isupper() for c in pw) else ''}"
          f"{'数字 ' if any(c.isdigit() for c in pw) else ''}"
          f"{'符号' if any(not c.isalnum() for c in pw) else ''}".strip() or "（无）")
    if tips:
        print(f"建议      : {'；'.join(tips)}")
    else:
        print("建议      : 已满足常见强度要求")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser():
    parser = argparse.ArgumentParser(
        prog="passgen.py",
        description="纯本地密码与密钥生成器（零依赖 / 跨平台 / 无网络 / 基于 secrets）")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("password", help="生成强密码")
    p.add_argument("--length", type=int, default=16)
    p.add_argument("--no-lower", action="store_true")
    p.add_argument("--no-upper", action="store_true")
    p.add_argument("--no-digits", action="store_true")
    p.add_argument("--no-symbols", action="store_true")
    p.add_argument("--no-ambiguous", action="store_true",
                   help="排除易混字符 i l 1 L o 0 O 等")
    p.add_argument("--count", type=int, default=1)
    p.set_defaults(func=cmd_password)

    p = sub.add_parser("passphrase", help="生成密码短语（易记且强）")
    p.add_argument("--words", type=int, default=5)
    p.add_argument("--sep", default="-")
    p.add_argument("--add-number", action="store_true")
    p.add_argument("--count", type=int, default=1)
    p.set_defaults(func=cmd_passphrase)

    p = sub.add_parser("token", help="生成随机令牌 / API key")
    p.add_argument("--bytes", type=int, default=32)
    p.add_argument("--format", choices=["hex", "urlsafe", "base64"], default="urlsafe")
    p.add_argument("--count", type=int, default=1)
    p.set_defaults(func=cmd_token)

    p = sub.add_parser("uuid", help="生成 UUID v4")
    p.add_argument("--count", type=int, default=1)
    p.set_defaults(func=cmd_uuid)

    p = sub.add_parser("pin", help="生成数字 PIN")
    p.add_argument("--length", type=int, default=6)
    p.add_argument("--count", type=int, default=1)
    p.set_defaults(func=cmd_pin)

    p = sub.add_parser("strength", help="检测口令强度（只读）")
    p.add_argument("password", nargs="?", default=None,
                   help="待检测口令；省略则从 stdin 读取")
    p.set_defaults(func=cmd_strength)

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
