#!/usr/bin/env python3
"""
Zero-One-Two-Three 知识库密码锁 🔐 (工业增强版 v7.0)
对知识笔记进行智能加密：公开试读 + 核心加密 + 自动备份 + 助记词恢复
特性：
  1. 支持整数/小数百分比参数（如 30 或 0.3）
  2. 密码强度验证（≥8 位，含大小写字母和数字）
  3. 加密前自动备份原文件
  4. 区分"密码错误"与"文件损坏"错误
  5. 统一元信息格式标签
  6. 12 词助记词恢复机制（--recovery）

用法：
  加密：python3 knowledge_lock.py lock    <文件路径> <密码> [--preview 30] [--no-backup] [--recovery]
  解密：python3 knowledge_lock.py unlock  <文件路径> <密码>
  恢复：python3 knowledge_lock.py recover <文件路径> <12词助记词>
  查看：python3 knowledge_lock.py peek    <文件路径>
"""

import _encoding_compat

import os
import sys
import re
import json
import time
import shutil
import base64
import hashlib
import secrets
from datetime import datetime

try:
    from cryptography.fernet import Fernet
except ImportError:
    print("\n⚠️ 环境缺失：需要安装 cryptography 库")
    print("## ⚙️ 安装指南")
    print("pip install 'cryptography>=42.0.8,<43'")
    print("# 如需升级：pip install --upgrade cryptography")
    sys.exit(1)


class LockError(Exception):
    """知识库密码锁异常基类，用于库化调用时安全传递错误"""
    pass


RECOVERY_WORDLIST = [
    "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract",
    "absurd", "abuse", "access", "accident", "account", "accuse", "achieve", "acid",
    "acoustic", "acquire", "across", "act", "action", "actor", "actress", "actual",
    "adapt", "add", "addict", "address", "adjust", "admit", "adult", "advance",
    "advice", "aerobic", "affair", "afford", "afraid", "africa", "age", "agent",
    "agree", "ahead", "aim", "air", "airport", "aisle", "alarm", "album",
    "alcohol", "alert", "alien", "all", "alley", "allow", "almost", "alone",
    "alpha", "already", "also", "alter", "always", "amateur", "amazing", "among",
    "amount", "amused", "analyst", "anchor", "ancient", "anger", "angle", "angry",
    "animal", "ankle", "announce", "annual", "another", "answer", "antenna", "antique",
    "anxiety", "any", "apart", "apology", "appear", "apple", "approve", "april",
    "arch", "arctic", "area", "arena", "argue", "arm", "armed", "armor",
    "army", "around", "arrange", "arrest", "arrive", "arrow", "art", "artefact",
    "artist", "artwork", "ask", "aspect", "assault", "asset", "assist", "assume",
    "asthma", "athlete", "atom", "attack", "attend", "attitude", "attract", "auction",
    "audit", "august", "aunt", "author", "auto", "autumn", "average", "avocado",
    "avoid", "awake", "aware", "away", "awesome", "awful", "awkward", "axis",
    "baby", "bachelor", "bacon", "badge", "bag", "balance", "balcony", "ball",
    "bamboo", "banana", "banner", "bar", "barely", "bargain", "barrel", "base",
    "basic", "basket", "battle", "beach", "bean", "beauty", "because", "become",
    "beef", "before", "begin", "behave", "behind", "believe", "below", "belt",
    "bench", "benefit", "best", "betray", "better", "between", "beyond", "bicycle",
    "bid", "bike", "bind", "biology", "bird", "birth", "bitter", "black",
    "blade", "blame", "blanket", "blast", "bleak", "bless", "blind", "blood",
    "blossom", "blouse", "blue", "blur", "blush", "board", "boat", "body",
    "boil", "bomb", "bone", "bonus", "book", "boost", "border", "boring",
    "borrow", "boss", "bottom", "bounce", "box", "boy", "bracket", "brain",
    "brand", "brass", "brave", "bread", "breeze", "brick", "bridge", "brief",
    "bright", "bring", "brisk", "broccoli", "broken", "bronze", "broom", "brother",
    "brown", "brush", "bubble", "buddy", "budget", "buffalo", "build", "bulb",
    "bulk", "bullet", "bundle", "bunker", "burden", "burger", "burst", "bus",
    "business", "busy", "butter", "buyer", "buzz", "cabbage", "cabin", "cable",
    "cactus", "cage", "cake", "call", "calm", "camera", "camp", "can",
    "canal", "cancel", "candy", "cannon", "canoe", "canvas", "canyon", "capable",
    "capital", "captain", "car", "carbon", "card", "cargo", "carpet", "carry",
    "cart", "case", "cash", "casino", "castle", "casual", "cat", "catalog",
    "catch", "category", "cattle", "caught", "cause", "caution", "cave", "ceiling",
    "celery", "cement", "census", "century", "cereal", "certain", "chair", "chalk",
    "champion", "change", "chaos", "chapter", "charge", "chase", "chat", "cheap",
    "check", "cheese", "chef", "cherry", "chest", "chicken", "chief", "child",
    "chimney", "choice", "choose", "chronic", "chuckle", "chunk", "churn", "cigar",
    "cinnamon", "circle", "citizen", "city", "civil", "claim", "clap", "clarify",
    "claw", "clay", "clean", "clerk", "clever", "click", "client", "cliff",
    "climb", "clinic", "clip", "clock", "clog", "close", "cloth", "cloud",
    "clown", "club", "clump", "cluster", "clutch", "coach", "coast", "coconut",
    "code", "coffee", "coil", "coin", "collect", "color", "column", "combine",
    "come", "comfort", "comic", "common", "company", "concert", "conduct", "confirm",
    "congress", "connect", "consider", "control", "convince", "cook", "cool", "copper",
    "copy", "coral", "core", "corn", "correct", "cost", "cotton", "couch",
    "country", "couple", "course", "cousin", "cover", "coyote", "crack", "cradle",
    "craft", "cram", "crane", "crash", "crater", "crawl", "crazy", "cream",
    "credit", "creek", "crew", "cricket", "crime", "crisp", "critic", "crop",
    "cross", "crouch", "crowd", "crucial", "cruel", "cruise", "crumble", "crunch",
    "crush", "cry", "crystal", "cube", "culture", "cup", "cupboard", "curious",
    "current", "curtain", "curve", "cushion", "custom", "cute", "cycle", "dad",
    "damage", "damp", "dance", "danger", "daring", "dash", "daughter", "dawn",
    "day", "deal", "debate", "debris", "decade", "december", "decide", "decline",
    "decorate", "decrease", "deer", "defense", "define", "defy", "degree", "delay",
    "deliver", "demand", "demise", "denial", "dentist", "deny", "depart", "depend",
    "deposit", "depth", "deputy", "derive", "describe", "desert", "design", "desk",
    "despair", "destroy", "detail", "detect", "develop", "device", "devote", "diagram",
    "dial", "diamond", "diary", "dice", "diesel", "diet", "differ", "digital",
    "dignity", "dilemma", "dinner", "dinosaur", "direct", "dirt", "disagree", "discover",
    "disease", "dish", "dismiss", "disorder", "display", "distance", "divert", "divide",
    "divorce", "dizzy", "doctor", "document", "dog", "doll", "dolphin", "domain",
    "donate", "donkey", "donor", "door", "dose", "double", "dove", "draft",
    "dragon", "drama", "drastic", "draw", "dream", "dress", "drift", "drill",
    "drink", "drip", "drive", "drop", "drum", "dry", "duck", "dumb",
    "dune", "during", "dust", "dutch", "duty", "dwarf", "dynamic", "eager",
    "eagle", "early", "earn", "earth", "easily", "east", "easy", "echo",
    "ecology", "economy", "edge", "edit", "educate", "effort", "egg", "eight",
    "either", "elbow", "elder", "electric", "elegant", "element", "elephant", "elevator",
    "elite", "else", "embark", "embody", "embrace", "emerge", "emotion", "employ",
    "empower", "empty", "enable", "enact", "end", "endless", "endorse", "enemy",
    "energy", "enforce", "engage", "engine", "enhance", "enjoy", "enlist", "enough",
    "enrich", "enroll", "ensure", "enter", "entire", "entry", "envelope", "episode",
    "equal", "equip", "era", "erase", "erode", "erosion", "error", "erupt",
    "escape", "essay", "essence", "estate", "eternal", "ethics", "evidence", "evil",
    "evoke", "evolve", "exact", "example", "excess", "exchange", "excite", "exclude",
    "excuse", "execute", "exercise", "exhaust", "exhibit", "exile", "exist", "exit",
    "exotic", "expand", "expect", "expire", "explain", "expose", "express", "extend",
    "extra", "eye", "eyebrow", "fabric", "face", "faculty", "fade", "faint",
    "faith", "fall", "false", "fame", "family", "famous", "fan", "fancy",
    "fantasy", "farm", "fashion", "fat", "fatal", "father", "fatigue", "fault",
    "favorite", "feature", "february", "federal", "fee", "feed", "feel", "female",
    "fence", "festival", "fetch", "fever", "few", "fiber", "fiction", "field",
    "figure", "file", "film", "filter", "final", "find", "fine", "finger",
    "finish", "fire", "firm", "first", "fiscal", "fish", "fit", "fitness",
    "fix", "flag", "flame", "flash", "flat", "flavor", "flee", "flight",
    "flip", "float", "flock", "floor", "flower", "fluid", "flush", "fly",
    "foam", "focus", "fog", "foil", "fold", "follow", "food", "foot",
    "force", "forest", "forget", "fork", "fortune", "forum", "forward", "fossil",
    "foster", "found", "fox", "fragile", "frame", "frequent", "fresh", "friend",
    "fringe", "frog", "front", "frost", "frown", "frozen", "fruit", "fuel",
    "fun", "funny", "furnace", "fury", "future", "gadget", "gain", "galaxy",
    "gallery", "game", "gap", "garage", "garbage", "garden", "garlic", "garment",
    "gas", "gasp", "gate", "gather", "gauge", "gaze", "general", "genius",
    "genre", "gentle", "genuine", "gesture", "ghost", "giant", "gift", "giggle",
    "ginger", "giraffe", "girl", "give", "glad", "glance", "glare", "glass",
    "glide", "glimpse", "globe", "gloom", "glory", "glove", "glow", "glue",
    "goat", "goddess", "gold", "good", "goose", "gorilla", "gospel", "gossip",
    "govern", "gown", "grab", "grace", "grain", "grant", "grape", "grass",
    "gravity", "great", "green", "grid", "grief", "grit", "grocery", "group",
    "grow", "grunt", "guard", "guess", "guide", "guilt", "guitar", "gun",
    "gym", "habit", "hair", "half", "hammer", "hamster", "hand", "happy",
    "harbor", "hard", "harsh", "harvest", "hat", "have", "hawk", "hazard",
    "head", "health", "heart", "heavy", "hedgehog", "height", "hello", "helmet",
    "help", "hen", "hero", "hidden", "high", "hill", "hint", "hip",
    "hire", "history", "hobby", "hockey", "hold", "hole", "holiday", "hollow",
    "home", "honey", "hood", "hope", "horn", "horror", "horse", "hospital",
    "host", "hotel", "hour", "hover", "hub", "huge", "human", "humble",
    "humor", "hundred", "hungry", "hunt", "hurdle", "hurry", "hurt", "husband",
    "hybrid", "ice", "icon", "idea", "identify", "idle", "ignore", "ill",
    "illegal", "illness", "image", "imitate", "immense", "immune", "impact", "impose",
    "improve", "impulse", "inch", "include", "income", "increase", "index", "indicate",
    "indoor", "industry", "infant", "inflict", "inform", "inhale", "inherit", "initial",
    "inject", "injury", "inmate", "inner", "innocent", "input", "inquiry", "insane",
    "insect", "inside", "inspire", "install", "intact", "interest", "into", "invest",
    "invite", "involve", "island", "isolate", "issue", "item", "ivory", "jacket",
    "jaguar", "jar", "jazz", "jealous", "jeans", "jelly", "jewel", "job",
    "join", "joke", "journey", "joy", "judge", "juice", "jump", "jungle",
    "junior", "junk", "just", "kangaroo", "keen", "keep", "ketchup", "key",
    "kick", "kid", "kidney", "kind", "kingdom", "kiss", "kit", "kitchen",
    "kite", "kitten", "kiwi", "knee", "knife", "knock", "know", "lab",
    "label", "labor", "ladder", "lady", "lake", "lamp", "language", "laptop",
    "large", "later", "latin", "laugh", "laundry", "lava", "law", "lawn",
    "lawsuit", "layer", "lazy", "leader", "leaf", "learn", "leave", "lecture",
    "left", "leg", "legal", "legend", "leisure", "lemon", "lend", "length",
    "lens", "leopard", "lesson", "letter", "level", "liar", "liberty", "library",
    "license", "life", "lift", "light", "like", "limb", "limit", "link",
    "lion", "liquid", "list", "little", "live", "lizard", "load", "loan",
    "lobster", "local", "lock", "logic", "lonely", "long", "loop", "lottery",
    "loud", "lounge", "love", "loyal", "lucky", "luggage", "lumber", "lunar",
    "lunch", "luxury", "lyrics", "machine", "mad", "magic", "magnet", "maid",
    "mail", "main", "major", "make", "mammal", "man", "manage", "mandate",
    "mango", "mansion", "manual", "maple", "marble", "march", "margin", "marine",
    "market", "marriage", "mask", "mass", "master", "match", "material", "math",
    "matrix", "matter", "maximum", "maze", "meadow", "mean", "measure", "meat",
    "mechanic", "medal", "media", "melody", "melt", "member", "memory", "mention",
    "menu", "mercy", "merge", "merit", "merry", "mesh", "message", "metal",
    "method", "middle", "midnight", "milk", "million", "mimic", "mind", "minimum",
    "minor", "minute", "miracle", "mirror", "misery", "miss", "mistake", "mix",
    "mixed", "mixture", "mobile", "model", "modify", "mom", "moment", "monitor",
    "monkey", "monster", "month", "moon", "moral", "more", "morning", "mosquito",
    "mother", "motion", "motor", "mountain", "mouse", "move", "movie", "much",
    "muffin", "mule", "multiply", "muscle", "museum", "mushroom", "music", "must",
    "mutual", "myself", "mystery", "myth", "naive", "name", "napkin", "narrow",
    "nasty", "nation", "nature", "near", "neck", "need", "negative", "neglect",
    "neither", "nephew", "nerve", "nest", "net", "network", "neutral", "never",
    "news", "next", "nice", "night", "noble", "noise", "nominee", "noodle",
    "normal", "north", "nose", "notable", "note", "nothing", "notice", "novel",
    "now", "nuclear", "number", "nurse", "nut", "oak", "obey", "object",
    "oblige", "obscure", "observe", "obtain", "obvious", "occur", "ocean", "october",
    "odor", "off", "offer", "office", "often", "oil", "okay", "old",
    "olive", "olympic", "omit", "once", "one", "onion", "online", "only",
    "open", "opera", "opinion", "oppose", "option", "orange", "orbit", "orchard",
    "order", "ordinary", "organ", "orient", "original", "orphan", "ostrich", "other",
    "outdoor", "outer", "output", "outside", "oval", "oven", "over", "own",
    "owner", "oxygen", "oyster", "ozone", "pact", "paddle", "page", "pair",
    "palace", "palm", "panda", "panel", "panic", "panther", "paper", "parade",
    "parent", "park", "parrot", "party", "pass", "patch", "path", "patient",
    "patrol", "pattern", "pause", "pave", "payment", "peace", "peanut", "pear",
    "peasant", "pelican", "pen", "penalty", "pencil", "people", "pepper", "perfect",
    "permit", "person", "pet", "phone", "photo", "phrase", "physical", "piano",
    "picnic", "picture", "piece", "pig", "pigeon", "pill", "pilot", "pink",
    "pioneer", "pipe", "pistol", "pitch", "pizza", "place", "planet", "plastic",
    "plate", "play", "please", "pledge", "pluck", "plug", "plunge", "poem",
    "poet", "point", "polar", "pole", "police", "pond", "pony", "pool",
    "popular", "portion", "position", "possible", "post", "potato", "pottery", "poverty",
    "powder", "power", "practice", "praise", "predict", "prefer", "prepare", "present",
    "pretty", "prevent", "price", "pride", "primary", "print", "priority", "prison",
    "private", "prize", "problem", "process", "produce", "profit", "program", "project",
    "promote", "proof", "property", "prosper", "protect", "proud", "provide", "public",
    "pudding", "pull", "pulp", "pulse", "pumpkin", "punch", "pupil", "puppy",
    "purchase", "purity", "purpose", "purse", "push", "put", "puzzle", "pyramid",
    "quality", "quantum", "quarter", "question", "quick", "quit", "quiz", "quote",
    "rabbit", "raccoon", "race", "rack", "radar", "radio", "rail", "rain",
    "raise", "rally", "ramp", "ranch", "random", "range", "rapid", "rare",
    "rate", "rather", "raven", "raw", "razor", "ready", "real", "reason",
    "rebel", "rebuild", "recall", "receive", "recipe", "record", "recycle", "reduce",
    "reflect", "reform", "refuse", "region", "regret", "regular", "reject", "relax",
    "release", "relief", "rely", "remain", "remember", "remind", "remove", "render",
    "renew", "rent", "reopen", "repair", "repeat", "replace", "report", "require",
    "rescue", "resemble", "resist", "resource", "response", "result", "retire", "retreat",
    "return", "reunion", "reveal", "review", "reward", "rhythm", "rib", "ribbon",
    "rice", "rich", "ride", "ridge", "rifle", "right", "rigid", "ring",
    "riot", "ripple", "risk", "ritual", "rival", "river", "road", "roast",
    "robot", "robust", "rocket", "romance", "roof", "rookie", "room", "rose",
    "rotate", "rough", "round", "route", "royal", "rubber", "rude", "rug",
    "rule", "run", "runway", "rural", "sad", "saddle", "sadness", "safe",
    "sail", "salad", "salmon", "salon", "salt", "salute", "same", "sample",
    "sand", "satisfy", "satoshi", "sauce", "sausage", "save", "say", "scale",
    "scan", "scare", "scatter", "scene", "scheme", "school", "science", "scissors",
    "scorpion", "scout", "scrap", "screen", "script", "scrub", "sea", "search",
    "season", "seat", "second", "secret", "section", "security", "seed", "seek",
    "segment", "select", "sell", "seminar", "senior", "sense", "sentence", "series",
    "service", "session", "settle", "setup", "seven", "shadow", "shaft", "shallow",
    "share", "shed", "shell", "sheriff", "shield", "shift", "shine", "ship",
    "shiver", "shock", "shoe", "shoot", "shop", "short", "shoulder", "shove",
    "shrimp", "shrug", "shuffle", "shy", "sibling", "sick", "side", "siege",
    "sight", "sign", "silent", "silk", "silly", "silver", "similar", "simple",
    "since", "sing", "siren", "sister", "situate", "six", "size", "skate",
    "sketch", "ski", "skill", "skin", "skirt", "skull", "slab", "slam",
    "sleep", "slender", "slice", "slide", "slight", "slim", "slogan", "slot",
    "slow", "slush", "small", "smart", "smile", "smoke", "smooth", "snack",
    "snake", "snap", "sniff", "snow", "soap", "soccer", "social", "sock",
    "soda", "soft", "solar", "soldier", "solid", "solution", "solve", "someone",
    "song", "soon", "sorry", "sort", "soul", "sound", "soup", "source",
    "south", "space", "spare", "spatial", "spawn", "speak", "special", "speed",
    "spell", "spend", "sphere", "spice", "spider", "spike", "spin", "spirit",
    "split", "spoil", "sponsor", "spoon", "sport", "spot", "spray", "spread",
    "spring", "spy", "square", "squeeze", "squirrel", "stable", "stadium", "staff",
    "stage", "stairs", "stamp", "stand", "start", "state", "stay", "steak",
    "steel", "stem", "step", "stereo", "stick", "still", "sting", "stock",
    "stomach", "stone", "stool", "story", "stove", "strategy", "street", "strike",
    "strong", "struggle", "student", "stuff", "stumble", "style", "subject", "submit",
    "subway", "success", "such", "sudden", "suffer", "sugar", "suggest", "suit",
    "summer", "sun", "sunny", "sunset", "super", "supply", "supreme", "sure",
    "surface", "surge", "surprise", "surround", "survey", "suspect", "sustain", "swallow",
    "swamp", "swap", "swarm", "swear", "sweet", "swift", "swim", "swing",
    "switch", "sword", "symbol", "symptom", "syrup", "system", "table", "tackle",
    "tag", "tail", "talent", "talk", "tank", "tape", "target", "task",
    "taste", "tattoo", "taxi", "teach", "team", "tell", "ten", "tenant",
    "tennis", "tent", "term", "test", "text", "thank", "that", "theme",
    "then", "theory", "there", "they", "thing", "this", "thought", "three",
    "thrive", "throw", "thumb", "thunder", "ticket", "tide", "tiger", "tilt",
    "timber", "time", "tiny", "tip", "tired", "tissue", "title", "toast",
    "tobacco", "today", "toddler", "toe", "together", "toilet", "token", "tomato",
    "tomorrow", "tone", "tongue", "tonight", "tool", "tooth", "top", "topic",
    "topple", "torch", "tornado", "tortoise", "toss", "total", "tourist", "toward",
    "tower", "town", "toy", "track", "trade", "traffic", "tragic", "train",
    "transfer", "trap", "trash", "travel", "tray", "treat", "tree", "trend",
    "trial", "tribe", "trick", "trigger", "trim", "trip", "trophy", "trouble",
    "truck", "true", "truly", "trumpet", "trust", "truth", "try", "tube",
    "tuition", "tumble", "tuna", "tunnel", "turkey", "turn", "turtle", "twelve",
    "twenty", "twice", "twin", "twist", "two", "type", "typical", "ugly",
    "umbrella", "unable", "unaware", "uncle", "uncover", "under", "undo", "unfair",
    "unfold", "unhappy", "uniform", "unique", "unit", "universe", "unknown", "unlock",
    "until", "unusual", "unveil", "update", "upgrade", "uphold", "upon", "upper",
    "upset", "urban", "urge", "usage", "use", "used", "useful", "useless",
    "usual", "utility", "vacant", "vacuum", "vague", "valid", "valley", "valve",
    "van", "vanish", "vapor", "various", "vast", "vault", "vehicle", "velvet",
    "vendor", "venture", "venue", "verb", "verify", "version", "very", "vessel",
    "veteran", "viable", "vibrant", "vicious", "victory", "video", "view", "village",
    "vintage", "violin", "virtual", "virus", "visa", "visit", "visual", "vital",
    "vivid", "vocal", "voice", "void", "volcano", "volume", "vote", "voyage",
    "wage", "wagon", "wait", "walk", "wall", "walnut", "want", "warfare",
    "warm", "warrior", "wash", "wasp", "waste", "water", "wave", "way",
    "wealth", "weapon", "wear", "weasel", "weather", "web", "wedding", "weekend",
    "weird", "welcome", "west", "wet", "whale", "what", "wheat", "wheel",
    "when", "where", "whip", "whisper", "wide", "width", "wife", "wild",
    "will", "win", "window", "wine", "wing", "wink", "winner", "winter",
    "wire", "wisdom", "wise", "wish", "witness", "wolf", "woman", "wonder",
    "wood", "wool", "word", "work", "world", "worry", "worth", "wrap",
    "wreck", "wrestle", "wrist", "write", "wrong", "yard", "year", "yellow",
    "you", "young", "youth", "zebra", "zero", "zone", "zoo",
]


def _get_wordlist_size():
    return len(RECOVERY_WORDLIST)


def generate_mnemonic(num_words: int = 12) -> str:
    """生成 BIP39 风格的助记词"""
    if num_words not in (12, 15, 18, 21, 24):
        num_words = 12
    indices = [secrets.randbelow(len(RECOVERY_WORDLIST)) for _ in range(num_words)]
    words = [RECOVERY_WORDLIST[i] for i in indices]
    return " ".join(words)


def derive_key(password: str) -> bytes:
    """从用户密码派生 Fernet 兼容的 32 字节密钥"""
    digest = hashlib.sha256(password.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(digest)


def _mnemonic_to_recovery_key(mnemonic: str) -> bytes:
    """从助记词派生恢复密钥"""
    normalized = " ".join(mnemonic.strip().lower().split())
    digest = hashlib.sha256(f"RECOVERY:{normalized}".encode('utf-8')).digest()
    return base64.urlsafe_b64encode(digest)


def _encrypt_password_with_mnemonic(password: str, mnemonic: str) -> str:
    """用助记词加密密码，返回 base64 密文"""
    recovery_key = _mnemonic_to_recovery_key(mnemonic)
    fernet = Fernet(recovery_key)
    encrypted = fernet.encrypt(password.encode('utf-8'))
    return encrypted.decode('utf-8')


def _decrypt_password_with_mnemonic(encrypted_password: str, mnemonic: str) -> str:
    """用助记词解密密码"""
    recovery_key = _mnemonic_to_recovery_key(mnemonic)
    fernet = Fernet(recovery_key)
    decrypted = fernet.decrypt(encrypted_password.encode('utf-8'))
    return decrypted.decode('utf-8')


def check_password_strength(password: str) -> tuple:
    """
    检查密码强度
    返回 (bool, str): (是否通过，提示信息)
    """
    if len(password) < 8:
        return False, "❌ 密码长度至少 8 位（当前 {} 位）".format(len(password))
    if not re.search(r'[A-Z]', password):
        return False, "❌ 密码需包含至少一个大写字母"
    if not re.search(r'[a-z]', password):
        return False, "❌ 密码需包含至少一个小写字母"
    if not re.search(r'\d', password):
        return False, "❌ 密码需包含至少一个数字"
    return True, "✅ 密码强度验证通过"


def parse_preview_ratio(value: str) -> float:
    """
    解析 preview 参数，支持整数（如 30）和小数（如 0.3）
    返回 0.05~0.95 之间的浮点数
    """
    try:
        val = float(value)
        if val > 1:
            ratio = val / 100.0
        else:
            ratio = val
        return max(0.05, min(0.95, ratio))
    except ValueError:
        return 0.3


def split_content_for_preview(content: str, preview_ratio: float = 0.3) -> tuple:
    """智能分割内容：公开试读区 + 核心加密区"""
    h2_pattern = r'\n## '
    matches = list(re.finditer(h2_pattern, content))

    if len(matches) >= 2:
        split_pos = matches[1].start()
        preview = content[:split_pos].strip()
        core = content[split_pos:].strip()

        if len(preview) < 200:
            split_pos = int(len(content) * preview_ratio)
            preview = content[:split_pos].strip()
            core = content[split_pos:].strip()

        return preview, core

    split_pos = int(len(content) * preview_ratio)
    return content[:split_pos].strip(), content[split_pos:].strip()


def backup_file(filepath: str) -> str:
    """创建带时间戳的备份文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base, ext = os.path.splitext(filepath)
    backup_path = f"{base}.backup_{timestamp}{ext}"
    shutil.copy2(filepath, backup_path)
    return backup_path


def lock_file(filepath: str, password: str, preview_ratio: float = 0.3,
              do_backup: bool = True, enable_recovery: bool = False):
    """智能加密文件

    参数:
        filepath: 源文件路径
        password: 加密密码
        preview_ratio: 公开试读比例 (0.05~0.95)
        do_backup: 是否自动备份
        enable_recovery: 是否生成助记词恢复短语

    返回:
        dict: {"locked_path": str, "mnemonic": str|None}
        如果 enable_recovery=True，mnemonic 为 12 词恢复短语

    异常:
        LockError: 文件不存在、密码强度不足、写入失败
    """
    if not os.path.exists(filepath):
        raise LockError(f"❌ 文件不存在：{filepath}")

    passed, msg = check_password_strength(password)
    print(msg)
    if not passed:
        print("\n💡 建议：使用密码管理器生成强密码（如 Bitwarden/1Password）")
        raise LockError("密码强度不足")

    if do_backup:
        backup_path = backup_file(filepath)
        print(f"💾 已备份原文件：{backup_path}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    preview_content, core_content = split_content_for_preview(content, preview_ratio)

    key = derive_key(password)
    fernet = Fernet(key)
    encrypted_core = fernet.encrypt(core_content.encode('utf-8'))

    mnemonic = None
    recovery_line = ""
    if enable_recovery:
        mnemonic = generate_mnemonic(12)
        encrypted_password = _encrypt_password_with_mnemonic(password, mnemonic)
        recovery_line = f"<!-- 恢复: {encrypted_password} -->\n"

    meta = {
        "tool": "Zero-One-Two-Three Knowledge Lock",
        "version": "7.0 (P0-Fixed)",
        "locked_at": datetime.now().isoformat(),
        "source_file": os.path.basename(filepath),
        "preview_ratio": preview_ratio,
        "content_hash": hashlib.sha256(content.encode('utf-8')).hexdigest()[:16],
        "preview_hash": hashlib.sha256(preview_content.encode('utf-8')).hexdigest()[:16],
        "core_hash": hashlib.sha256(core_content.encode('utf-8')).hexdigest()[:16],
        "has_recovery": enable_recovery,
    }

    locked_path = filepath + '.locked'
    try:
        with open(locked_path, 'w', encoding='utf-8') as f:
            f.write(preview_content)
            f.write("\n\n---\n\n")
            f.write("<!-- 🔐 ZERO-ONE-TWO-THREE LOCK: 以下为加密核心内容 -->\n")
            f.write(f"<!-- 元信息: {json.dumps(meta, ensure_ascii=False)} -->\n")
            if recovery_line:
                f.write(recovery_line)
            f.write("<!-- 密文: -->\n")
            f.write(encrypted_core.decode('utf-8'))
            f.write("\n")
    except IOError as e:
        raise LockError(f"❌ 写入加密文件失败：{e}")

    print(f"🔐 智能加密成功！")
    print(f"   加密文件：{locked_path}")
    print(f"   👀 公开试读：{len(preview_content)} 字符")
    print(f"   🔒 核心加密：{len(core_content)} 字符")

    if enable_recovery and mnemonic:
        print(f"\n🔑 ========== 助记词恢复短语（请离线安全保存！）==========")
        print(f"   {mnemonic}")
        print(f"==================================================================")
        print(f"⚠️  重要提醒：")
        print(f"   1. 请将这 12 个单词抄写在纸上，离线保存")
        print(f"   2. 切勿截图或存储在云端")
        print(f"   3. 忘记密码时，使用以下命令恢复：")
        print(f"      python knowledge_lock.py recover {locked_path} \"{mnemonic}\"")
        print(f"")

    return {"locked_path": locked_path, "mnemonic": mnemonic}


def unlock_file(filepath: str, password: str):
    """解密文件，区分密码错误与文件损坏

    参数:
        filepath: 加密文件路径 (.locked)
        password: 解密密码

    返回:
        str: 还原后的文件路径

    异常:
        LockError: 文件不存在、格式无效、密码错误、元信息损坏
    """
    if not os.path.exists(filepath):
        raise LockError(f"❌ 文件不存在：{filepath}")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except IOError as e:
        raise LockError(f"❌ 读取文件失败：{e}")

    if "<!-- 🔐 ZERO-ONE-TWO-THREE LOCK:" not in content:
        raise LockError("❌ 不是有效的 Zero-One-Two-Three 加密文件")

    lock_section_marker = "\n\n---\n\n<!-- 🔐 ZERO-ONE-TWO-THREE LOCK:"
    lock_pos = content.find(lock_section_marker)

    if lock_pos == -1:
        raise LockError("❌ 无法定位加密区标记")

    preview_content = content[:lock_pos].strip()
    encrypted_part = content[lock_pos + len("\n\n---\n"):].strip()

    meta_line = None
    encrypted_content = None

    for line in encrypted_part.split('\n'):
        if line.startswith("<!-- 恢复:"):
            continue
        if line.startswith("<!-- 元信息:"):
            try:
                meta_json = line.replace("<!-- 元信息:", "").replace("-->", "").strip()
                meta_line = json.loads(meta_json)
            except json.JSONDecodeError:
                raise LockError("❌ 元信息格式损坏！文件可能已被篡改或传输过程中损坏。")
        elif line.startswith("<!-- 密文: -->"):
            encrypted_content = encrypted_part.split("<!-- 密文: -->\n")[1].strip()
            break

    if not encrypted_content:
        raise LockError("❌ 无法解析加密文件格式！文件可能已损坏。")

    key = derive_key(password)
    fernet = Fernet(key)

    try:
        decrypted_core = fernet.decrypt(encrypted_content.encode('utf-8'))
        core_content = decrypted_core.decode('utf-8')
    except Exception:
        raise LockError(
            "❌ 解密失败！密码错误。\n"
            "💡 提示：请确认密码大小写及特殊字符是否正确。\n"
            "💡 如已设置助记词恢复，请使用 recover 命令。"
        )

    full_content = preview_content + "\n\n" + core_content

    preview_hash = hashlib.sha256(preview_content.encode('utf-8')).hexdigest()[:16]
    core_hash = hashlib.sha256(core_content.encode('utf-8')).hexdigest()[:16]

    if meta_line and preview_hash == meta_line.get("preview_hash") and core_hash == meta_line.get("core_hash"):
        print(f"✅ 指纹验证通过：{meta_line.get('content_hash')}")
    else:
        print("⚠️ 指纹不匹配！文件可能在加密后被篡改或损坏。")

    if filepath.endswith('.locked'):
        unlocked_path = filepath[:-7]
    else:
        unlocked_path = filepath + '.unlocked'

    with open(unlocked_path, 'w', encoding='utf-8') as f:
        f.write(full_content)

    print(f"🔓 解密成功！完整内容已还原")
    print(f"   还原文件：{unlocked_path}")
    return unlocked_path


def recover_file(filepath: str, mnemonic: str):
    """使用助记词恢复密码并解密文件

    参数:
        filepath: 加密文件路径 (.locked)
        mnemonic: 12 词助记词恢复短语

    返回:
        str: 还原后的文件路径

    异常:
        LockError: 文件无恢复信息、助记词无效
    """
    if not os.path.exists(filepath):
        raise LockError(f"❌ 文件不存在：{filepath}")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except IOError as e:
        raise LockError(f"❌ 读取文件失败：{e}")

    encrypted_password = None
    for line in content.split('\n'):
        if line.startswith("<!-- 恢复:"):
            encrypted_password = line.replace("<!-- 恢复:", "").replace("-->", "").strip()
            break

    if not encrypted_password:
        raise LockError(
            "❌ 该文件未设置助记词恢复。\n"
            "💡 加密时请使用 --recovery 参数启用恢复功能。"
        )

    try:
        password = _decrypt_password_with_mnemonic(encrypted_password, mnemonic)
    except Exception:
        raise LockError(
            "❌ 助记词无效！请检查 12 个单词的顺序和拼写是否正确。\n"
            "💡 助记词区分大小写和空格，请确保完全一致。"
        )

    print(f"🔑 助记词验证通过！已恢复原始密码。")
    return unlock_file(filepath, password)


def peek_file(filepath: str):
    """查看加密文件的元信息

    参数:
        filepath: 加密文件路径

    返回:
        dict: 元信息字典

    异常:
        LockError: 文件不存在、格式无效、元信息损坏
    """
    if not os.path.exists(filepath):
        raise LockError(f"❌ 文件不存在：{filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    for line in content.split('\n'):
        if line.startswith("<!-- 元信息:"):
            try:
                meta_json = line.replace("<!-- 元信息:", "").replace("-->", "").strip()
                meta = json.loads(meta_json)
                print(f"📋 加密文件元信息：")
                print(f"   工具：{meta.get('tool', '?')}")
                print(f"   版本：{meta.get('version', '?')}")
                print(f"   原始文件：{meta.get('source_file', '?')}")
                print(f"   加密时间：{meta.get('locked_at', '?')}")
                print(f"   内容指纹：{meta.get('content_hash', '?')}")
                has_recovery = meta.get("has_recovery", False)
                print(f"   助记词恢复：{'✅ 已启用' if has_recovery else '❌ 未启用'}")
                return meta
            except json.JSONDecodeError:
                raise LockError("❌ 元信息格式损坏！")

    raise LockError("❌ 无法解析元信息")


def main():
    if len(sys.argv) < 2:
        print("🔐 Zero-One-Two-Three 知识库密码锁 v7.0 (P0-Fixed)")
        print("")
        print("用法：")
        print("  加密：  python3 knowledge_lock.py lock    <文件路径> <密码> [--preview 30] [--no-backup] [--recovery]")
        print("  解密：  python3 knowledge_lock.py unlock  <文件路径> <密码>")
        print("  恢复：  python3 knowledge_lock.py recover <文件路径> <12词助记词>")
        print("  查看：  python3 knowledge_lock.py peek    <文件路径>")
        print("")
        print("## ⚙️ 安装依赖")
        print("pip install 'cryptography>=42.0.8,<43'")
        sys.exit(0)

    action = sys.argv[1]

    try:
        if action == "lock":
            if len(sys.argv) < 4:
                print("❌ 加密需要提供密码")
                sys.exit(1)
            filepath = sys.argv[2]
            password = sys.argv[3]

            preview_ratio = 0.3
            do_backup = True
            enable_recovery = False

            if "--preview" in sys.argv:
                idx = sys.argv.index("--preview")
                if idx + 1 < len(sys.argv):
                    preview_ratio = parse_preview_ratio(sys.argv[idx + 1])

            if "--no-backup" in sys.argv:
                do_backup = False

            if "--recovery" in sys.argv:
                enable_recovery = True

            lock_file(filepath, password, preview_ratio, do_backup, enable_recovery)

        elif action == "unlock":
            if len(sys.argv) < 4:
                print("❌ 解密需要提供密码")
                sys.exit(1)
            filepath = sys.argv[2]
            password = sys.argv[3]
            unlock_file(filepath, password)

        elif action == "recover":
            if len(sys.argv) < 4:
                print("❌ 恢复需要提供 12 词助记词")
                sys.exit(1)
            filepath = sys.argv[2]
            mnemonic = " ".join(sys.argv[3:])
            word_count = len(mnemonic.strip().split())
            if word_count < 12:
                print(f"❌ 助记词不足 12 个单词（当前 {word_count} 个）")
                print("💡 请用引号包裹完整的 12 词短语，例如：")
                print('   python knowledge_lock.py recover file.md.locked "word1 word2 ... word12"')
                sys.exit(1)
            recover_file(filepath, mnemonic)

        elif action == "peek":
            if len(sys.argv) < 3:
                print("❌ 请提供文件路径")
                sys.exit(1)
            peek_file(sys.argv[2])

        else:
            print(f"❌ 未知操作：{action}")
            sys.exit(1)

    except LockError as e:
        print(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()