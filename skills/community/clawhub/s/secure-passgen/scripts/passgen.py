#!/usr/bin/env python3
"""
Secure Password Generator — Uses secrets module (CSPRNG)
No personal data, no external dependencies
"""

import argparse
import secrets
import string
import sys
import math

WORDLIST = [
    "abacus", "abrupt", "absurd", "abyss", "acorn", "acre", "agent", "agile", "album", "alley",
    "alpine", "amber", "anchor", "angel", "antenna", "anvil", "apple", "archive", "arctic", "arena",
    "armor", "arrow", "atlas", "attic", "aurora", "avalanche", "avenue", "badge", "bamboo", "barrel",
    "basil", "basket", "beacon", "bedrock", "bicycle", "bison", "blanket", "blizzard", "blossom", "boulder",
    "breeze", "brick", "bronze", "bubble", "buffet", "bullet", "bunker", "cabin", "cactus", "camel",
    "canvas", "canyon", "carbon", "cargo", "carpet", "castle", "cavern", "cedar", "chamber", "champion",
    "chapel", "charter", "chimney", "cinnamon", "cipher", "citadel", "cliff", "clover", "cobalt", "cobweb",
    "coconut", "comet", "compass", "condor", "copper", "coral", "cosmos", "couch", "cradle", "crane",
    "crater", "crimson", "crystal", "cuckoo", "curtain", "cushion", "cycle", "dagger", "dawn", "delta",
    "desert", "diamond", "dinosaur", "dolphin", "dungeon", "eagle", "eclipse", "ember", "emerald", "enigma",
    "equinox", "everest", "falcon", "fathom", "feather", "fellow", "fence", "ferret", "festival", "fjord",
    "flame", "flannel", "flask", "flint", "flute", "foliage", "forest", "forge", "fortune", "fossil",
    "fox", "fragment", "fresco", "fridge", "frigate", "frontier", "frost", "galaxy", "galleon", "garden",
    "garlic", "garnet", "gauge", "gazelle", "geyser", "glacier", "glade", "goblet", "gorilla", "granite",
    "grape", "gravel", "grenade", "grotto", "guardian", "guitar", "gully", "hammer", "harbor", "hatchet",
    "haven", "hazard", "hearth", "helix", "hermit", "highland", "horizon", "husk", "hydra", "iceberg",
    "igloo", "impulse", "insect", "iron", "ivory", "jade", "jasmine", "jester", "jigsaw", "jungle",
    "karate", "kayak", "kettle", "kingdom", "kiosk", "knight", "knot", "lagoon", "lantern", "lapis",
    "lava", "leather", "legend", "lemon", "leopard", "lilac", "lily", "limbo", "linen", "llama",
    "lotus", "lunar", "lyric", "magenta", "mammoth", "manor", "marble", "marmalade", "maze", "meadow",
    "mercury", "mesa", "midnight", "mimic", "mirage", "moat", "mocha", "monarch", "monsoon", "mosaic",
    "muffin", "mustard", "myth", "nacho", "nectar", "nebula", "neon", "night", "nimbus", "noble",
    "noodle", "nova", "nugget", "nylon", "oasis", "obsidian", "ocean", "olive", "onyx", "opal",
    "orbit", "orchid", "origami", "ostrich", "otter", "oxygen", "oyster", "paddle", "pajama", "palace",
    "panda", "panther", "papaya", "paper", "paradise", "parcel", "parsley", "pasta", "pastel", "patriot",
    "peacock", "peanut", "pearl", "penguin", "pepper", "peridot", "phoenix", "piano", "pillar", "pinnacle",
    "pixel", "pizza", "plaid", "planet", "plaster", "platinum", "plaza", "plume", "polar", "poncho",
    "poppy", "prairie", "prism", "protein", "pudding", "pumpkin", "puzzle", "python", "quartz", "quest",
    "quilt", "rabbit", "raccoon", "radar", "rainbow", "rampart", "raven", "realm", "rebel", "reef",
    "relic", "remedy", "riddle", "ridge", "rift", "rocket", "rodeo", "rooster", "ruby", "rumble",
    "saffron", "sage", "sapphire", "sash", "satellite", "savanna", "scarlet", "scorpion", "sculpture", "shadow",
    "shamrock", "sherpa", "shrapnel", "sierra", "silicon", "silver", "siren", "skeleton", "skull", "sleet",
    "smuggler", "solar", "soldier", "solstice", "sonata", "sorbet", "spark", "specter", "spider", "spiral",
    "spirit", "sponge", "spruce", "squadron", "squid", "squirrel", "statue", "steam", "stiletto", "storm",
    "subway", "sultan", "summit", "sundae", "sunflower", "supernova", "surf", "sushi", "swamp", "swan",
    "sylvan", "symbol", "symphony", "talisman", "tapestry", "tarn", "telescope", "temple", "thistle",
    "thorn", "thunder", "tiara", "tiger", "tiramisu", "titanium", "topaz", "tornado", "torpedo", "tortoise",
    "totem", "trampoline", "treasure", "tribune", "trident", "truffle", "tulip", "tumbler", "turbo", "turtle",
    "umbrella", "unicorn", "uranium", "utopia", "valley", "vampire", "vanilla", "velvet", "venom", "vertex",
    "vessel", "violin", "vista", "vivace", "vodka", "volcano", "vortex", "voyage", "walrus", "warden",
    "warlock", "warrior", "wasp", "watchtower", "waterfall", "weasel", "whale", "willow", "window", "winter",
    "wizard", "wolverine", "wonder", "woodland", "wool", "wraith", "xenon", "yacht", "yarrow", "yearling",
    "yeti", "yogurt", "yonder", "zebra", "zenith", "zephyr", "zinc", "zodiac", "zombie", "zucchini"
]


def gen_password(length=20, symbols=True, numbers=True):
    chars = string.ascii_letters
    if numbers:
        chars += string.digits
    if symbols:
        chars += "!@#$%^&*()-_=+[]{}|;:,.<>?"
    return ''.join(secrets.choice(chars) for _ in range(length))


def gen_passphrase(words=5, separator="-"):
    return separator.join(secrets.choice(WORDLIST) for _ in range(words))


def gen_apikey(prefix="sk"):
    random_part = secrets.token_hex(32)
    return f"{prefix}_{random_part}"


def gen_pin(length=6):
    return ''.join(secrets.choice(string.digits) for _ in range(length))


def gen_hex(length=32):
    return secrets.token_hex(length)


def gen_base64(length=32):
    import base64
    return base64.urlsafe_b64encode(secrets.token_bytes(length)).decode().rstrip('=')


def calc_entropy(result, charset_size):
    return len(result) * math.log2(charset_size) if charset_size > 0 else 0


def main():
    parser = argparse.ArgumentParser(description="Secure Password Generator")
    parser.add_argument("--type", choices=["password", "passphrase", "apikey", "pin", "hex", "base64"],
                        default="password")
    parser.add_argument("--length", type=int, default=20)
    parser.add_argument("--words", type=int, default=5)
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--no-symbols", action="store_true")
    parser.add_argument("--no-numbers", action="store_true")
    parser.add_argument("--separator", default="-")
    parser.add_argument("--entropy", action="store_true")
    parser.add_argument("--prefix", default="sk", help="API key prefix")
    args = parser.parse_args()

    for _ in range(args.count):
        if args.type == "password":
            result = gen_password(args.length, not args.no_symbols, not args.no_numbers)
            charset = len(string.ascii_letters) + (len(string.digits) if not args.no_numbers else 0) + \
                      (26 if not args.no_symbols else 0)
        elif args.type == "passphrase":
            result = gen_passphrase(args.words, args.separator)
            charset = len(WORDLIST)
        elif args.type == "apikey":
            result = gen_apikey(args.prefix)
            charset = 16  # hex
        elif args.type == "pin":
            result = gen_pin(args.length)
            charset = 10
        elif args.type == "hex":
            result = gen_hex(args.length)
            charset = 16
        elif args.type == "base64":
            result = gen_base64(args.length)
            charset = 64

        if args.entropy:
            ent = calc_entropy(result, charset)
            print(f"{result}  (entropy: {ent:.1f} bits)")
        else:
            print(result)


if __name__ == "__main__":
    main()
