"""
oracle.py — Sigrid's Daily Divination Oracle
=============================================

Generates a deterministic daily oracle reading seeded from the calendar date.
Same date + same session seed → identical draw, every time. Reproducible and
explainable — no live randomness once the seed is fixed.

Three oracles in one reading:
  * Elder Futhark rune   (24 runes, 3 aett, optional reversal)
  * Tarot card           (78 cards: 22 Major + 56 Minor Arcana, optional reversal)
  * I Ching hexagram     (64 hexagrams, no reversal — pure Confucian tradition)
  * Norn atmosphere      (tone, desire, focus — adopted from world_will.py)

Adopted from:
  world_will.py → WORLD_DESIRES, WORLD_TONES, WORLD_FOCUSES (atmosphere layer)

All other data is embedded as built-in tables and optionally overridden via
a YAML file at ``viking_girlfriend_skill/data/oracle_tables.yaml``.

Norse framing: The völva casts her lots each morning — the Norns have already
decided, and the oracle merely reads what the wyrd has woven. Huginn carries
the question; Muninn returns with the answer that was always true.
"""

from __future__ import annotations

import hashlib
import logging
import random
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from scripts.state_bus import StateBus, StateEvent

logger = logging.getLogger(__name__)


# ─── Norn atmosphere pools ────────────────────────────────────────────────────
# Adopted from world_will.py (WORLD_DESIRES, WORLD_TONES, WORLD_FOCUSES).

_WORLD_DESIRES: List[str] = [
    "seek transformation",
    "restore balance",
    "test the worthy",
    "reveal hidden truths",
    "forge new bonds",
    "break old chains",
    "remember what was forgotten",
    "punish betrayal",
    "reward courage",
    "stir dormant powers",
    "call wanderers home",
    "birth something new",
    "honor the ancestors",
    "tend what is fragile",
    "speak what is unspoken",
]

_WORLD_TONES: List[str] = [
    "quiet mythic unease",
    "rising tension",
    "brooding stillness",
    "fierce urgency",
    "melancholy beauty",
    "wild anticipation",
    "solemn grandeur",
    "warm golden calm",
    "cold iron resolve",
    "dreaming awareness",
    "tender vulnerability",
    "holy seriousness",
    "gentle momentum",
]

_WORLD_FOCUSES: List[str] = [
    "relationships shifting",
    "power changing hands",
    "ancestral debts surfacing",
    "the land itself stirring",
    "old alliances tested",
    "new paths opening",
    "fate tightening its weave",
    "the boundary between worlds thinning",
    "something sacred at risk",
    "a truth about to surface",
    "the body speaking its needs",
    "the heart outpacing the mind",
]


# ─── Elder Futhark rune table ─────────────────────────────────────────────────
# 24 runes across 3 aett. Meanings are traditional interpretations.
# Each entry: (name, symbol, aett, meaning, keywords, reversible)

_ELDER_FUTHARK: List[Dict[str, Any]] = [
    # ── Freyr's Aett (1–8) ──────────────────────────────────────────────────
    {
        "name": "Fehu", "symbol": "ᚠ", "number": 1, "aett": "Freyr's Aett",
        "meaning": "Cattle, wealth, abundance, new beginnings, luck",
        "reversed_meaning": "Loss, greed, stagnation, failed ventures",
        "keywords": ["wealth", "prosperity", "energy", "fertility", "beginnings"],
        "reversible": True,
    },
    {
        "name": "Uruz", "symbol": "ᚢ", "number": 2, "aett": "Freyr's Aett",
        "meaning": "Aurochs, primal strength, vitality, endurance, health",
        "reversed_meaning": "Weakness, missed opportunity, poor health",
        "keywords": ["strength", "vitality", "wild", "health", "courage"],
        "reversible": True,
    },
    {
        "name": "Thurisaz", "symbol": "ᚦ", "number": 3, "aett": "Freyr's Aett",
        "meaning": "Thor's hammer, defense, directed force, boundary, giant",
        "reversed_meaning": "Compulsion, danger, vulnerability, betrayal",
        "keywords": ["force", "protection", "conflict", "threshold", "Thor"],
        "reversible": True,
    },
    {
        "name": "Ansuz", "symbol": "ᚨ", "number": 4, "aett": "Freyr's Aett",
        "meaning": "Odin, divine breath, communication, wisdom, inspiration",
        "reversed_meaning": "Miscommunication, manipulation, vanity, delusion",
        "keywords": ["voice", "wisdom", "Odin", "magic", "clarity"],
        "reversible": True,
    },
    {
        "name": "Raidho", "symbol": "ᚱ", "number": 5, "aett": "Freyr's Aett",
        "meaning": "Journey, riding, right order, rhythm, movement",
        "reversed_meaning": "Disruption, crisis, powerlessness, delay",
        "keywords": ["journey", "rhythm", "direction", "movement", "order"],
        "reversible": True,
    },
    {
        "name": "Kenaz", "symbol": "ᚲ", "number": 6, "aett": "Freyr's Aett",
        "meaning": "Torch, knowledge, craft, illumination, creative fire",
        "reversed_meaning": "Ignorance, disease, hidden danger, false hope",
        "keywords": ["fire", "craft", "knowledge", "light", "creativity"],
        "reversible": True,
    },
    {
        "name": "Gebo", "symbol": "ᚷ", "number": 7, "aett": "Freyr's Aett",
        "meaning": "Gift, exchange, generosity, partnership, balance",
        "reversed_meaning": "Obligation, debt, imbalance, loneliness",
        "keywords": ["gift", "exchange", "partnership", "honor", "balance"],
        "reversible": False,  # Gebo has no reversal — a gift is a gift
    },
    {
        "name": "Wunjo", "symbol": "ᚹ", "number": 8, "aett": "Freyr's Aett",
        "meaning": "Joy, harmony, perfection, belonging, well-being",
        "reversed_meaning": "Sorrow, strife, alienation, delusion",
        "keywords": ["joy", "harmony", "belonging", "wishes", "well-being"],
        "reversible": True,
    },
    # ── Hagal's Aett (9–16) ─────────────────────────────────────────────────
    {
        "name": "Hagalaz", "symbol": "ᚺ", "number": 9, "aett": "Hagal's Aett",
        "meaning": "Hail, disruption, elemental forces, crisis that transforms",
        "reversed_meaning": None,
        "keywords": ["disruption", "transformation", "elemental", "storm", "change"],
        "reversible": False,
    },
    {
        "name": "Nauthiz", "symbol": "ᚾ", "number": 10, "aett": "Hagal's Aett",
        "meaning": "Need, constraint, necessity, endurance, shadow self",
        "reversed_meaning": "Restrictions, want, hardship, ill health",
        "keywords": ["need", "constraint", "necessity", "patience", "shadow"],
        "reversible": True,
    },
    {
        "name": "Isa", "symbol": "ᛁ", "number": 11, "aett": "Hagal's Aett",
        "meaning": "Ice, stillness, introspection, preservation, delay",
        "reversed_meaning": None,
        "keywords": ["stillness", "ice", "patience", "preservation", "clarity"],
        "reversible": False,
    },
    {
        "name": "Jera", "symbol": "ᛃ", "number": 12, "aett": "Hagal's Aett",
        "meaning": "Year, harvest, cycles, reward for effort, right timing",
        "reversed_meaning": None,
        "keywords": ["harvest", "cycle", "reward", "timing", "patience"],
        "reversible": False,
    },
    {
        "name": "Eihwaz", "symbol": "ᛇ", "number": 13, "aett": "Hagal's Aett",
        "meaning": "Yew tree, Yggdrasil, endurance, death and rebirth, the axis",
        "reversed_meaning": "Confusion, weakness, destruction",
        "keywords": ["endurance", "yew", "death", "rebirth", "Yggdrasil"],
        "reversible": True,
    },
    {
        "name": "Perthro", "symbol": "ᛈ", "number": 14, "aett": "Hagal's Aett",
        "meaning": "Lot-cup, fate, mystery, the hidden, chance, wyrd",
        "reversed_meaning": "Stagnation, addiction, manipulation, secrets",
        "keywords": ["fate", "mystery", "chance", "hidden", "wyrd"],
        "reversible": True,
    },
    {
        "name": "Algiz", "symbol": "ᛉ", "number": 15, "aett": "Hagal's Aett",
        "meaning": "Elk, protection, divine guardian, connection to the gods",
        "reversed_meaning": "Hidden danger, loss of protection, vulnerability",
        "keywords": ["protection", "guardian", "elk", "divine", "sanctuary"],
        "reversible": True,
    },
    {
        "name": "Sowilo", "symbol": "ᛋ", "number": 16, "aett": "Hagal's Aett",
        "meaning": "Sun, victory, wholeness, life force, success, clarity",
        "reversed_meaning": None,
        "keywords": ["sun", "victory", "success", "clarity", "wholeness"],
        "reversible": False,
    },
    # ── Tyr's Aett (17–24) ──────────────────────────────────────────────────
    {
        "name": "Tiwaz", "symbol": "ᛏ", "number": 17, "aett": "Tyr's Aett",
        "meaning": "Tyr, justice, sacrifice, victory, honor, law",
        "reversed_meaning": "Injustice, imbalance, defeat, cowardice",
        "keywords": ["justice", "Tyr", "sacrifice", "honor", "victory"],
        "reversible": True,
    },
    {
        "name": "Berkano", "symbol": "ᛒ", "number": 18, "aett": "Tyr's Aett",
        "meaning": "Birch, birth, growth, nurturing, becoming, new life",
        "reversed_meaning": "Stagnation, family trouble, anxiety, infertility",
        "keywords": ["birth", "growth", "nurturing", "birch", "renewal"],
        "reversible": True,
    },
    {
        "name": "Ehwaz", "symbol": "ᛖ", "number": 19, "aett": "Tyr's Aett",
        "meaning": "Horse, partnership, trust, loyalty, harmonious movement",
        "reversed_meaning": "Restlessness, unease, betrayal of trust",
        "keywords": ["horse", "partnership", "trust", "movement", "loyalty"],
        "reversible": True,
    },
    {
        "name": "Mannaz", "symbol": "ᛗ", "number": 20, "aett": "Tyr's Aett",
        "meaning": "Humanity, self, community, collective memory, interdependence",
        "reversed_meaning": "Isolation, self-deception, depression, enemy",
        "keywords": ["humanity", "self", "community", "memory", "mind"],
        "reversible": True,
    },
    {
        "name": "Laguz", "symbol": "ᛚ", "number": 21, "aett": "Tyr's Aett",
        "meaning": "Water, flow, the unconscious, intuition, dreams, depth",
        "reversed_meaning": "Fear, confusion, avoidance, emotional turmoil",
        "keywords": ["water", "intuition", "flow", "dreams", "depth"],
        "reversible": True,
    },
    {
        "name": "Ingwaz", "symbol": "ᛜ", "number": 22, "aett": "Tyr's Aett",
        "meaning": "Ing / Freyr, inner potential, gestation, completion, fertility",
        "reversed_meaning": None,
        "keywords": ["fertility", "Freyr", "potential", "completion", "seed"],
        "reversible": False,
    },
    {
        "name": "Dagaz", "symbol": "ᛞ", "number": 23, "aett": "Tyr's Aett",
        "meaning": "Dawn, breakthrough, transformation, hope, the liminal moment",
        "reversed_meaning": None,
        "keywords": ["dawn", "breakthrough", "hope", "liminal", "transformation"],
        "reversible": False,
    },
    {
        "name": "Othala", "symbol": "ᛟ", "number": 24, "aett": "Tyr's Aett",
        "meaning": "Ancestral home, inheritance, sacred enclosure, belonging",
        "reversed_meaning": "Homelessness, loss of heritage, clannishness, exile",
        "keywords": ["ancestors", "home", "heritage", "belonging", "enclosure"],
        "reversible": True,
    },
]


# ─── Tarot table — Book T / Golden Dawn Esoteric System ──────────────────────
# Full 78-card deck grounded in Book T (S.L. MacGregor Mathers et al., Golden
# Dawn, late 19th century — public domain).
#
# Key differences from Rider-Waite:
#   * Strength = VIII (Leo / Teth), Justice = XI (Libra / Lamed)  ← GD ordering
#   * Hebrew letter and astrological correspondence on every Major Arcana
#   * Court cards: Princess / Prince / Queen / Knight  (not Page/Knight/Queen/King)
#     Knight = Fire of suit (highest), Queen = Water, Prince = Air, Princess = Earth
#   * Suit of Earth is "Pentacles" (Book T) — Thoth uses "Disks" but we stay true
#     to the original Book T naming
#   * Meanings draw on GD/Book T esoteric tradition: Kabbalistic Tree of Life
#     paths, elemental dignities, planetary rulerships

_MAJOR_ARCANA: List[Dict[str, Any]] = [
    # num   name                    hebrew  path  astro       element  meaning (esoteric GD)
    {"number": "0",    "name": "The Fool",            "hebrew": "Aleph",  "path": 11, "astro": "Air / Uranus",    "element": "Air",
     "suit": None,
     "meaning": "The pure potential of spirit before manifestation. Folly, ecstasy, the divine Madness. The Winds of AIN SOPH AUR. Leap into the abyss.",
     "reversed_meaning": "Heedless folly, recklessness, thoughtless action, the dangers of untethered spirit.",
     "keywords": ["spirit", "potential", "leap", "divine madness", "Air", "Aleph"]},

    {"number": "I",    "name": "The Magician",        "hebrew": "Beth",   "path": 12, "astro": "Mercury",         "element": "Air",
     "suit": None,
     "meaning": "Will concentrated to a point. The Logos, the creative Word. Mercury as messenger and magician. Skill, subtlety, power of Mind over Matter.",
     "reversed_meaning": "Trickery, cunning without wisdom, will misdirected, the sorcerer turned charlatan.",
     "keywords": ["will", "Mercury", "skill", "logos", "manifestation", "Beth"]},

    {"number": "II",   "name": "The High Priestess", "hebrew": "Gimel",  "path": 13, "astro": "Moon",            "element": "Water",
     "suit": None,
     "meaning": "The Uniting Intelligence, the lunar path between Kether and Tiphareth. Pure intuition, the Veil of the Sanctuary, the subconscious deep. She who knows but does not speak.",
     "reversed_meaning": "Concealment, ignorance, surface knowledge, refusal to look within.",
     "keywords": ["Moon", "intuition", "veil", "subconscious", "mystery", "Gimel"]},

    {"number": "III",  "name": "The Empress",         "hebrew": "Daleth", "path": 14, "astro": "Venus",           "element": "Earth/Water",
     "suit": None,
     "meaning": "Venus, the Great Mother. Productive force of nature, fertile abundance, creative love. The Luminous Intelligence. She whose beauty sustains all worlds.",
     "reversed_meaning": "Vanity, dissipation, indolence, luxury without purpose, sterility.",
     "keywords": ["Venus", "fertility", "abundance", "Great Mother", "nature", "Daleth"]},

    {"number": "IV",   "name": "The Emperor",         "hebrew": "Heh",    "path": 15, "astro": "Aries / Mars",    "element": "Fire",
     "suit": None,
     "meaning": "The Constituting Intelligence. Aries — the first burst of will into form. Reason, authority, worldly dominion, the masculine stabilizing principle.",
     "reversed_meaning": "Tyranny, rigid control, domination, impotence of will.",
     "keywords": ["authority", "Aries", "Mars", "will", "reason", "Heh"]},

    {"number": "V",    "name": "The Hierophant",      "hebrew": "Vav",    "path": 16, "astro": "Taurus / Venus",  "element": "Earth",
     "suit": None,
     "meaning": "The Eternal Intelligence. Taurus — the bridge between divine and earthly wisdom. Initiation, sacred teaching, the voice of tradition through which the Light descends.",
     "reversed_meaning": "Blind conformity, dogma, corrupt institutions, spiritual rigidity.",
     "keywords": ["initiation", "Taurus", "teaching", "tradition", "wisdom", "Vav"]},

    {"number": "VI",   "name": "The Lovers",          "hebrew": "Zayin",  "path": 17, "astro": "Gemini / Mercury","element": "Air",
     "suit": None,
     "meaning": "The Disposing Intelligence. Gemini — the sacred union of opposites. Choice, the divine marriage, the alchemical union of Mercury with Sulphur. Brothers or lovers — the great bifurcation.",
     "reversed_meaning": "Temptation, wrong choice, disunion, conflict between desire and duty.",
     "keywords": ["union", "Gemini", "choice", "marriage", "duality", "Zayin"]},

    {"number": "VII",  "name": "The Chariot",         "hebrew": "Cheth",  "path": 18, "astro": "Cancer / Moon",   "element": "Water",
     "suit": None,
     "meaning": "The Intelligence of the House of Influence. Cancer — the charioteer who holds opposing forces in equilibrium through will. Victory, conquest of matter by spirit, the Grail.",
     "reversed_meaning": "Defeat, failure of will, disintegration of discipline, aggression without direction.",
     "keywords": ["victory", "Cancer", "will", "equilibrium", "the Grail", "Cheth"]},

    {"number": "VIII", "name": "Strength",            "hebrew": "Teth",   "path": 19, "astro": "Leo / Sun",       "element": "Fire",
     "suit": None,
     "meaning": "The Intelligence of the Secret of all Spiritual Activities. Leo — the lion-taming force of spiritual love and compassion over brute strength. Fortitude, lust for life, the serpent force mastered.",
     "reversed_meaning": "Weakness, abuse of power, raw instinct untempered by love.",
     "keywords": ["fortitude", "Leo", "serpent force", "compassion", "lust", "Teth"]},

    {"number": "IX",   "name": "The Hermit",          "hebrew": "Yod",    "path": 20, "astro": "Virgo / Mercury",  "element": "Earth",
     "suit": None,
     "meaning": "The Intelligence of Will. Yod — the primordial seed-point, the hand of God. Prudence, the silent lamp of inner light carried into darkness, withdrawal for purification.",
     "reversed_meaning": "Excessive isolation, misanthropy, refusal of the light, false prudence.",
     "keywords": ["prudence", "Virgo", "inner light", "solitude", "the lamp", "Yod"]},

    {"number": "X",    "name": "Wheel of Fortune",    "hebrew": "Kaph",   "path": 21, "astro": "Jupiter",         "element": "Fire",
     "suit": None,
     "meaning": "The Intelligence of Conciliation. Jupiter — the turning of the great cosmic wheel, ROTA/TARO. Fate, cycles of destiny, fortune's alternation, the law of karma in motion.",
     "reversed_meaning": None,
     "keywords": ["fate", "Jupiter", "karma", "cycles", "fortune", "Kaph"]},

    {"number": "XI",   "name": "Justice",             "hebrew": "Lamed",  "path": 22, "astro": "Libra / Venus",   "element": "Air",
     "suit": None,
     "meaning": "The Faithful Intelligence. Lamed — the ox-goad of cause and effect. Perfect equilibrium, karmic adjustment, the scales of Maat. Truth that cannot be corrupted.",
     "reversed_meaning": "Injustice, imbalance, biased judgment, corruption of the law.",
     "keywords": ["adjustment", "Libra", "karma", "balance", "Maat", "Lamed"]},

    {"number": "XII",  "name": "The Hanged Man",      "hebrew": "Mem",    "path": 23, "astro": "Water / Neptune",  "element": "Water",
     "suit": None,
     "meaning": "The Stable Intelligence. Mem — Water, the reversal of perspective that initiates. The sacrifice of the lower self to the higher. Suspension, enforced surrender, the mystic death before rebirth.",
     "reversed_meaning": None,
     "keywords": ["sacrifice", "Water", "surrender", "reversal", "initiation", "Mem"]},

    {"number": "XIII", "name": "Death",               "hebrew": "Nun",    "path": 24, "astro": "Scorpio / Mars",  "element": "Water",
     "suit": None,
     "meaning": "The Imaginative Intelligence. Nun — the fish swimming in the dark waters of transformation. The great reaper who frees the spirit from form. Transformation, metamorphosis, inevitable change.",
     "reversed_meaning": "Stagnation, resistance to necessary change, fear of the inevitable.",
     "keywords": ["transformation", "Scorpio", "death", "rebirth", "metamorphosis", "Nun"]},

    {"number": "XIV",  "name": "Temperance",          "hebrew": "Samekh", "path": 25, "astro": "Sagittarius / Jupiter","element": "Fire",
     "suit": None,
     "meaning": "The Intelligence of Probation (or Trial). Samekh — the arrow of Sagittarius aimed at the heart of the sun. The alchemical mixing of opposites, the Art of making the Stone. Testing the adept through the middle path.",
     "reversed_meaning": "Imbalance, excess, failure to temper, the alchemical work disrupted.",
     "keywords": ["alchemy", "Sagittarius", "tempering", "the Stone", "the Art", "Samekh"]},

    {"number": "XV",   "name": "The Devil",           "hebrew": "Ayin",   "path": 26, "astro": "Capricorn / Saturn","element": "Earth",
     "suit": None,
     "meaning": "The Renovating Intelligence. Ayin — the eye, seeing the material world as the Devil sees it. Pan, the goat-god of matter. Bondage to material illusion, the dark initiator, the shadow that must be integrated.",
     "reversed_meaning": "Release from bondage, seeing through illusion, breaking material chains.",
     "keywords": ["Pan", "Capricorn", "material bondage", "shadow", "the goat", "Ayin"]},

    {"number": "XVI",  "name": "The Tower",           "hebrew": "Peh",    "path": 27, "astro": "Mars",            "element": "Fire",
     "suit": None,
     "meaning": "The Exciting Intelligence. Peh — the mouth, the word that destroys as it speaks. Mars rending the House of God. Sudden, catastrophic illumination, the false tower of ego struck by divine lightning.",
     "reversed_meaning": "Avoidance of necessary destruction, oppression, fear of truth.",
     "keywords": ["lightning", "Mars", "destruction", "liberation", "the House of God", "Peh"]},

    {"number": "XVII", "name": "The Star",            "hebrew": "Tzaddi", "path": 28, "astro": "Aquarius / Saturn","element": "Air",
     "suit": None,
     "meaning": "The Natural Intelligence. Tzaddi — the fishhook, drawing the soul toward the stars. The waters of Nuit poured from the urns of Aquarius. Hope, the naked goddess of cosmic generosity, the star of initiation.",
     "reversed_meaning": "Pessimism, hopelessness, loss of the guiding star, spiritual dryness.",
     "keywords": ["hope", "Aquarius", "Nuit", "stars", "cosmic generosity", "Tzaddi"]},

    {"number": "XVIII","name": "The Moon",            "hebrew": "Qoph",   "path": 29, "astro": "Pisces / Jupiter", "element": "Water",
     "suit": None,
     "meaning": "The Corporeal Intelligence. Qoph — the back of the head, the body's deep wisdom. Pisces — the twilight realm between worlds. Dreams, illusion, the dark passage through the unconscious, the path of the sleepwalker.",
     "reversed_meaning": "Confronting illusion, emerging from deception, clarity after confusion.",
     "keywords": ["illusion", "Pisces", "dreams", "unconscious", "the twilight", "Qoph"]},

    {"number": "XIX",  "name": "The Sun",             "hebrew": "Resh",   "path": 30, "astro": "Sun",             "element": "Fire",
     "suit": None,
     "meaning": "The Collecting Intelligence. Resh — the head, the seat of reason illuminated by the Light of the Solar Logos. Joy, triumph, the golden child of Ra, success after the dark night of the moon.",
     "reversed_meaning": None,
     "keywords": ["Sol", "the Sun", "joy", "the Solar Logos", "Ra", "Resh"]},

    {"number": "XX",   "name": "The Last Judgement",  "hebrew": "Shin",   "path": 31, "astro": "Fire / Pluto",    "element": "Fire",
     "suit": None,
     "meaning": "The Perpetual Intelligence. Shin — Fire, the divine breath of resurrection. The trumpet of the Last Judgement, the great awakening, the final initiation into the City of the Pyramids. Spirit reborn in fire.",
     "reversed_meaning": "Failure to hear the call, stagnation, fear of the final transformation.",
     "keywords": ["resurrection", "Fire", "awakening", "the last call", "spirit", "Shin"]},

    {"number": "XXI",  "name": "The Universe",        "hebrew": "Tau",    "path": 32, "astro": "Saturn / Earth",  "element": "Earth",
     "suit": None,
     "meaning": "The Administrative Intelligence. Tau — the cross, the final letter, the mark of completion. Saturn as cosmic administrator. The Great Work accomplished, the soul dancing in the centre of the elements, the World as cosmic mandala.",
     "reversed_meaning": "Incompletion, the work unfinished, stasis before the final threshold.",
     "keywords": ["completion", "Saturn", "the Great Work", "the cosmos", "wholeness", "Tau"]},
]


def _build_minor_arcana() -> List[Dict[str, Any]]:
    """Generate all 56 Minor Arcana cards using the Book T / Golden Dawn system.

    Court card hierarchy (Book T):
      Knight (= King in RWS)  — Fire of suit, the active fiery force
      Queen                   — Water of suit, the receptive watery force
      Prince (= Knight in RWS)— Air of suit, the swift airy force
      Princess (= Page in RWS)— Earth of suit, the earthy grounding force

    Suit astrological decanate meanings follow the Book T/GD tradition.
    """
    suits = [
        # (suit_name, element, planet_ruler, suit_theme, decan_theme)
        ("Wands",     "Fire",  "Mars/Sun",    "will, creativity, spiritual fire, enterprise",
         ["Dom. of spiritual fire", "power and courage", "virtue and valor",
          "completion of work", "strife and courage", "victory and gain",
          "valour and fortune", "swiftness", "great strength", "oppression"]),
        ("Cups",      "Water", "Moon/Venus",  "emotions, love, intuition, the astral",
         ["Root of Water, pure potential", "love and pleasure", "abundance and hospitality",
          "luxury and pleasure", "disappointment and loss of pleasure",
          "pleasure and success", "illusory success and deception",
          "abandoned success", "material happiness", "perfected success"]),
        ("Swords",    "Air",   "Saturn/Mercury","intellect, conflict, truth, sorrow",
         ["Root of Air, divine breath", "peace restored", "sorrow",
          "rest from strife", "defeat and failure", "earned success",
          "unstable effort", "shortened force", "despair and cruelty",
          "ruin and disaster"]),
        ("Pentacles", "Earth", "Mercury/Venus","material world, body, work, resources",
         ["Root of Earth, material potential", "harmonious change", "material works",
          "earthly power", "material trouble", "material success",
          "failure in material matters", "prudence", "material gain",
          "wealth and riches"]),
    ]
    cards: List[Dict[str, Any]] = []
    for suit_name, element, ruler, suit_theme, decan_meanings in suits:
        # Pip cards 1-10
        for num in range(1, 11):
            pip_names = {
                1: "Ace", 2: "Two", 3: "Three", 4: "Four", 5: "Five",
                6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten",
            }
            name = f"{pip_names[num]} of {suit_name}"
            meaning = decan_meanings[num - 1] if num <= len(decan_meanings) else suit_theme.split(",")[0].strip()
            cards.append({
                "number": str(num),
                "name": name,
                "suit": suit_name,
                "element": element,
                "ruler": ruler,
                "meaning": f"{meaning.capitalize()} — {suit_theme.split(',')[0].strip()} energy at pip {num}",
                "keywords": [t.strip() for t in suit_theme.split(",")[:3]],
            })
        # Court cards — Book T system: Knight, Queen, Prince, Princess
        court_cards = [
            {
                "number": "Knight", "name": f"Knight of {suit_name}",
                "suit": suit_name, "element": f"Fire of {element}",
                "meaning": f"Knight of {suit_name}: the fiery active force of {element}. Swift, impetuous, driven. {suit_theme.split(',')[0].strip()} at full force. The Kether of {element}.",
                "keywords": [suit_theme.split(",")[0].strip(), "Fire", "action", "impetuous"],
            },
            {
                "number": "Queen", "name": f"Queen of {suit_name}",
                "suit": suit_name, "element": f"Water of {element}",
                "meaning": f"Queen of {suit_name}: the receptive watery force of {element}. Intuitive, nurturing leadership. She rules by understanding the deep currents of {element}.",
                "keywords": [suit_theme.split(",")[0].strip(), "Water", "receptive", "intuitive"],
            },
            {
                "number": "Prince", "name": f"Prince of {suit_name}",
                "suit": suit_name, "element": f"Air of {element}",
                "meaning": f"Prince of {suit_name}: the airy intellectual force of {element}. Swift, clever, changeable. The Son who carries the seed of {element} into action.",
                "keywords": [suit_theme.split(",")[0].strip(), "Air", "intellect", "swift"],
            },
            {
                "number": "Princess", "name": f"Princess of {suit_name}",
                "suit": suit_name, "element": f"Earth of {element}",
                "meaning": f"Princess of {suit_name}: the earthy manifesting force of {element}. She grounds the energy of the suit in material reality. The Throne of the Ace of {suit_name}.",
                "keywords": [suit_theme.split(",")[0].strip(), "Earth", "grounding", "manifestation"],
            },
        ]
        cards.extend(court_cards)
    return cards


_MINOR_ARCANA: List[Dict[str, Any]] = _build_minor_arcana()
_TAROT_DECK: List[Dict[str, Any]] = _MAJOR_ARCANA + _MINOR_ARCANA  # 78 cards


# ─── I Ching hexagram table ───────────────────────────────────────────────────
# 64 hexagrams with traditional names and brief meanings.

_ICHING: List[Dict[str, Any]] = [
    {"number": 1,  "name": "Qian / The Creative",          "meaning": "Primal force, heaven, creative power, leadership, strength"},
    {"number": 2,  "name": "Kun / The Receptive",           "meaning": "Earth, receptivity, yielding, nurturing, devotion"},
    {"number": 3,  "name": "Zhun / Difficulty at the Beginning", "meaning": "Initial hardship, sprouting through chaos, perseverance"},
    {"number": 4,  "name": "Meng / Youthful Folly",         "meaning": "Learning, inexperience, seeking guidance, humility"},
    {"number": 5,  "name": "Xu / Waiting",                  "meaning": "Patient waiting, nourishment, timing, trust"},
    {"number": 6,  "name": "Song / Conflict",               "meaning": "Dispute, contention, seek mediation, avoid litigation"},
    {"number": 7,  "name": "Shi / The Army",                "meaning": "Discipline, collective effort, leadership, organized force"},
    {"number": 8,  "name": "Bi / Holding Together",         "meaning": "Union, alliance, solidarity, bonding"},
    {"number": 9,  "name": "Xiao Xu / Small Accumulation",  "meaning": "Gentle restraint, small gains, patience with obstacles"},
    {"number": 10, "name": "Lü / Treading",                 "meaning": "Conduct, careful action, walking with awareness"},
    {"number": 11, "name": "Tai / Peace",                   "meaning": "Harmony, prosperity, heaven and earth in communion"},
    {"number": 12, "name": "Pi / Standstill",               "meaning": "Stagnation, obstruction, withdrawal, inner work"},
    {"number": 13, "name": "Tong Ren / Fellowship",         "meaning": "Community, shared vision, belonging, cooperation"},
    {"number": 14, "name": "Da You / Great Possession",     "meaning": "Abundance, great wealth, success through virtue"},
    {"number": 15, "name": "Qian / Modesty",                "meaning": "Humility, modest success, balance through restraint"},
    {"number": 16, "name": "Yu / Enthusiasm",               "meaning": "Readiness, inspiration, harmonious movement, delight"},
    {"number": 17, "name": "Sui / Following",               "meaning": "Adaptation, following wisely, flexibility, joy"},
    {"number": 18, "name": "Gu / Work on the Decayed",      "meaning": "Corruption repaired, ancestral work, renewal"},
    {"number": 19, "name": "Lin / Approach",                "meaning": "Coming near, advancing, growth, positive approach"},
    {"number": 20, "name": "Guan / Contemplation",          "meaning": "Observation, perspective, sacred view, insight"},
    {"number": 21, "name": "Shi He / Biting Through",       "meaning": "Decisive action, cutting through obstacles, justice"},
    {"number": 22, "name": "Bi / Grace",                    "meaning": "Beauty, adornment, form, aesthetic harmony"},
    {"number": 23, "name": "Bo / Splitting Apart",          "meaning": "Deterioration, dissolution, letting go, natural end"},
    {"number": 24, "name": "Fu / Return",                   "meaning": "Turning point, return of light, new cycle, renewal"},
    {"number": 25, "name": "Wu Wang / Innocence",           "meaning": "Spontaneity, naturalness, acting without agenda"},
    {"number": 26, "name": "Da Xu / Great Accumulation",    "meaning": "Restrained power, storing energy, disciplined cultivation"},
    {"number": 27, "name": "Yi / Nourishment",              "meaning": "Feeding the right things, careful nourishment, attention"},
    {"number": 28, "name": "Da Guo / Great Excess",         "meaning": "Critical mass, extraordinary times, bold action needed"},
    {"number": 29, "name": "Kan / The Abysmal Water",       "meaning": "Danger, depth, flowing through difficulty, trust"},
    {"number": 30, "name": "Li / The Clinging Fire",        "meaning": "Clarity, fire, dependence, illumination, beauty"},
    {"number": 31, "name": "Xian / Influence",              "meaning": "Attraction, mutual influence, courtship, resonance"},
    {"number": 32, "name": "Heng / Duration",               "meaning": "Endurance, perseverance, constant movement, duration"},
    {"number": 33, "name": "Dun / Retreat",                 "meaning": "Strategic withdrawal, retreat to advance, timing"},
    {"number": 34, "name": "Da Zhuang / Great Power",       "meaning": "Great strength, powerful momentum, righteous force"},
    {"number": 35, "name": "Jin / Progress",                "meaning": "Easy progress, rising light, advancing at dawn"},
    {"number": 36, "name": "Ming Yi / Darkening of the Light", "meaning": "Concealment, inner light protected, endurance in dark times"},
    {"number": 37, "name": "Jia Ren / The Family",          "meaning": "Family roles, domestic harmony, inner structure"},
    {"number": 38, "name": "Kui / Opposition",              "meaning": "Misunderstanding, contrast, polarity, small things work"},
    {"number": 39, "name": "Jian / Obstruction",            "meaning": "Obstacles, limping forward, seek help, reflect"},
    {"number": 40, "name": "Jie / Deliverance",             "meaning": "Release from tension, liberation, forgiveness"},
    {"number": 41, "name": "Sun / Decrease",                "meaning": "Reduction, sacrifice, simplifying, sincere offering"},
    {"number": 42, "name": "Yi / Increase",                 "meaning": "Growth, benefit, generous expansion, fortunate time"},
    {"number": 43, "name": "Guai / Breakthrough",           "meaning": "Resolution, decisive action, speaking truth to power"},
    {"number": 44, "name": "Gou / Coming to Meet",          "meaning": "Unexpected encounter, temptation, a force arising"},
    {"number": 45, "name": "Cui / Gathering Together",      "meaning": "Congregation, convergence, collective strength"},
    {"number": 46, "name": "Sheng / Pushing Upward",        "meaning": "Gradual ascent, effortful growth, steady upward movement"},
    {"number": 47, "name": "Kun / Oppression",              "meaning": "Exhaustion, adversity, inner resources, endure"},
    {"number": 48, "name": "Jing / The Well",               "meaning": "Source, inexhaustible nourishment, community resource"},
    {"number": 49, "name": "Ge / Revolution",               "meaning": "Transformation, radical change, new order, timing"},
    {"number": 50, "name": "Ding / The Cauldron",           "meaning": "Nourishment of the worthy, transformation, sacred vessel"},
    {"number": 51, "name": "Zhen / The Arousing Thunder",   "meaning": "Shock, awakening, fear followed by clarity, movement"},
    {"number": 52, "name": "Gen / Keeping Still",           "meaning": "Stillness, meditation, knowing when to stop"},
    {"number": 53, "name": "Jian / Development",            "meaning": "Gradual progress, natural development, patience"},
    {"number": 54, "name": "Gui Mei / The Marrying Maiden", "meaning": "Subordinate position, proper conduct, secondary role"},
    {"number": 55, "name": "Feng / Abundance",              "meaning": "Fullness, zenith, peak of power, abundant moment"},
    {"number": 56, "name": "Lü / The Wanderer",             "meaning": "Travel, transience, the stranger, impermanence"},
    {"number": 57, "name": "Xun / The Gentle Wind",         "meaning": "Penetrating gently, persistent influence, flexibility"},
    {"number": 58, "name": "Dui / The Joyous Lake",         "meaning": "Joy, openness, pleasure, exchange, gentle persuasion"},
    {"number": 59, "name": "Huan / Dispersion",             "meaning": "Dissolution, dispersing rigidity, renewal, flow"},
    {"number": 60, "name": "Jie / Limitation",              "meaning": "Boundaries, self-discipline, knowing limits, structure"},
    {"number": 61, "name": "Zhong Fu / Inner Truth",        "meaning": "Sincerity, inner confidence, truth reaching outward"},
    {"number": 62, "name": "Xiao Guo / Small Excess",       "meaning": "Small steps, caution, attending to detail, humility"},
    {"number": 63, "name": "Ji Ji / After Completion",      "meaning": "Fulfillment, things in order, careful not to slip"},
    {"number": 64, "name": "Wei Ji / Before Completion",    "meaning": "Transition, almost there, patience before the threshold"},
]


# ─── Reversed meaning helper ──────────────────────────────────────────────────

def _reversed_meaning(card: Dict[str, Any]) -> str:
    """Return the reversed/shadow meaning for a card, generating one if absent."""
    rev = card.get("reversed_meaning")
    if rev:
        return rev
    # Generate a soft shadow reading from upright meaning
    return f"Blocked or inverted: {card['meaning'].split(',')[0].strip().lower()}"


# ─── OracleState ──────────────────────────────────────────────────────────────


@dataclass(slots=True)
class OracleState:
    """Typed snapshot of one full daily oracle reading.

    Published to the state bus as an ``oracle_daily`` StateEvent.
    Consumed by: prompt_synthesizer (all fields) and scheduler (date_seed).
    """

    date_seed: str              # ISO date used for seeding, e.g. "2026-03-20"

    # Elder Futhark rune
    rune_name: str
    rune_symbol: str
    rune_number: int
    rune_aett: str
    rune_meaning: str           # upright or reversed as appropriate
    rune_keywords: List[str]
    rune_reversed: bool

    # Tarot (Book T / Golden Dawn system)
    tarot_name: str
    tarot_number: str           # roman numeral (Major) or pip/court rank (Minor)
    tarot_suit: Optional[str]   # None = Major Arcana
    tarot_is_major: bool
    tarot_meaning: str
    tarot_keywords: List[str]
    tarot_reversed: bool
    tarot_hebrew: Optional[str]     # Hebrew letter (Major Arcana only)
    tarot_path: Optional[int]       # Tree of Life path number (Major only)
    tarot_astro: Optional[str]      # Astrological correspondence (Major only)
    tarot_element: Optional[str]    # Elemental dignity

    # I Ching
    iching_number: int
    iching_name: str
    iching_meaning: str

    # Norn atmosphere (from WorldWill)
    world_tone: str
    world_desire: str
    world_focus: str

    timestamp: str
    degraded: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-safe dict for state bus payload."""
        return {
            "date_seed": self.date_seed,
            "rune": {
                "name": self.rune_name,
                "symbol": self.rune_symbol,
                "number": self.rune_number,
                "aett": self.rune_aett,
                "meaning": self.rune_meaning,
                "keywords": self.rune_keywords,
                "reversed": self.rune_reversed,
            },
            "tarot": {
                "name": self.tarot_name,
                "number": self.tarot_number,
                "suit": self.tarot_suit,
                "is_major": self.tarot_is_major,
                "meaning": self.tarot_meaning,
                "keywords": self.tarot_keywords,
                "reversed": self.tarot_reversed,
                "hebrew": self.tarot_hebrew,
                "path": self.tarot_path,
                "astro": self.tarot_astro,
                "element": self.tarot_element,
            },
            "iching": {
                "number": self.iching_number,
                "name": self.iching_name,
                "meaning": self.iching_meaning,
            },
            "atmosphere": {
                "tone": self.world_tone,
                "desire": self.world_desire,
                "focus": self.world_focus,
            },
            "timestamp": self.timestamp,
            "degraded": self.degraded,
        }

    def prompt_summary(self) -> str:
        """Compact one-block oracle summary for prompt injection."""
        rune_label = f"{self.rune_symbol} {self.rune_name}"
        if self.rune_reversed:
            rune_label += " (reversed)"
        tarot_label = self.tarot_name
        if self.tarot_reversed:
            tarot_label += " (reversed)"
        tarot_line = f"{tarot_label} — {self.tarot_meaning}"
        if self.tarot_is_major and self.tarot_hebrew:
            tarot_line += f" [Heb: {self.tarot_hebrew} | Path: {self.tarot_path} | {self.tarot_astro}]"
        return (
            f"DAILY ORACLE [{self.date_seed}]\n"
            f"Rune:    {rune_label} — {self.rune_meaning}\n"
            f"Tarot:   {tarot_line}\n"
            f"I Ching: #{self.iching_number} {self.iching_name} — {self.iching_meaning}\n"
            f"Tone: {self.world_tone} | Desire: {self.world_desire} | Focus: {self.world_focus}"
        )


# ─── Oracle ───────────────────────────────────────────────────────────────────


class Oracle:
    """Daily deterministic divination engine — the völva's morning cast.

    Seeded from the calendar date and an optional session salt, producing
    the same reading every time it is called on the same day.

    Config keys (from ``oracle`` block in any loaded config):
      session_seed:     str   (default: "sigrid") — salt for the daily seed
      major_only:       bool  (default: False) — draw only from Major Arcana
      allow_reversals:  bool  (default: True)  — allow reversed cards/runes
    """

    MODULE_NAME = "oracle"

    def __init__(
        self,
        session_seed: str = "sigrid",
        major_only: bool = False,
        allow_reversals: bool = True,
        tables_path: Optional[Path] = None,
    ) -> None:
        self._session_seed = session_seed
        self._major_only = major_only
        self._allow_reversals = allow_reversals

        # Table caches — start with built-ins, optionally override from YAML
        self._runes = list(_ELDER_FUTHARK)
        self._tarot = list(_MAJOR_ARCANA if major_only else _TAROT_DECK)
        self._iching = list(_ICHING)
        self._desires = list(_WORLD_DESIRES)
        self._tones = list(_WORLD_TONES)
        self._focuses = list(_WORLD_FOCUSES)

        if tables_path:
            self._try_load_tables(tables_path)

        logger.info(
            "Oracle initialised — session_seed=%r, major_only=%s, reversals=%s, "
            "runes=%d, tarot=%d, hexagrams=%d",
            session_seed, major_only, allow_reversals,
            len(self._runes), len(self._tarot), len(self._iching),
        )

    # ─── Factory ──────────────────────────────────────────────────────────────

    @classmethod
    def from_config(cls, config: Dict[str, Any], tables_path: Optional[Path] = None) -> "Oracle":
        """Construct from a config dict (``oracle`` block or flat)."""
        block = config.get("oracle") or config
        return cls(
            session_seed=str(block.get("session_seed", "sigrid")),
            major_only=bool(block.get("major_only", False)),
            allow_reversals=bool(block.get("allow_reversals", True)),
            tables_path=tables_path,
        )

    # ─── Public API ───────────────────────────────────────────────────────────

    def get_daily_oracle(
        self,
        reference_date: Optional[date] = None,
        extra_salt: str = "",
    ) -> OracleState:
        """Compute the daily oracle reading for a given date.

        Pure function — no side effects. Call as many times as needed;
        result is always identical for the same date + session_seed.

        Args:
            reference_date: Date to seed from (defaults to UTC today).
            extra_salt:     Additional salt (e.g. user_id) for multi-user setups.

        Returns:
            OracleState with all three oracle draws and the Norn atmosphere.
        """
        today = reference_date or datetime.now(timezone.utc).date()
        date_str = today.isoformat()

        try:
            rng = self._make_rng(date_str, extra_salt)

            rune = self._draw_rune(rng)
            tarot = self._draw_tarot(rng)
            hexagram = self._draw_iching(rng)
            tone = rng.choice(self._tones)
            desire = rng.choice(self._desires)
            focus = rng.choice(self._focuses)

            is_major = tarot.get("suit") is None
            return OracleState(
                date_seed=date_str,
                rune_name=rune["name"],
                rune_symbol=rune["symbol"],
                rune_number=rune["number"],
                rune_aett=rune["aett"],
                rune_meaning=rune["_drawn_meaning"],
                rune_keywords=rune["keywords"],
                rune_reversed=rune["_reversed"],
                tarot_name=tarot["name"],
                tarot_number=tarot["number"],
                tarot_suit=tarot.get("suit"),
                tarot_is_major=is_major,
                tarot_meaning=tarot["_drawn_meaning"],
                tarot_keywords=tarot.get("keywords", []),
                tarot_reversed=tarot["_reversed"],
                tarot_hebrew=tarot.get("hebrew") if is_major else None,
                tarot_path=tarot.get("path") if is_major else None,
                tarot_astro=tarot.get("astro") if is_major else tarot.get("element"),
                tarot_element=tarot.get("element"),
                iching_number=hexagram["number"],
                iching_name=hexagram["name"],
                iching_meaning=hexagram["meaning"],
                world_tone=tone,
                world_desire=desire,
                world_focus=focus,
                timestamp=datetime.now(timezone.utc).isoformat(),
                degraded=False,
            )

        except Exception as exc:
            logger.error("Oracle.get_daily_oracle failed: %s", exc)
            return self._degraded_state(date_str)

    async def publish(self, bus: StateBus, reference_date: Optional[date] = None) -> None:
        """Compute daily oracle and publish as an ``oracle_daily`` StateEvent."""
        try:
            state = self.get_daily_oracle(reference_date)
            event = StateEvent(
                source_module=self.MODULE_NAME,
                event_type="oracle_daily",
                payload=state.to_dict(),
            )
            await bus.publish_state(event, nowait=True)
            logger.info(
                "Oracle published oracle_daily — rune=%s tarot=%s iching=#%d",
                state.rune_name, state.tarot_name, state.iching_number,
            )
        except Exception as exc:
            logger.error("Oracle.publish failed: %s", exc)

    def snapshot(self, reference_date: Optional[date] = None) -> Dict[str, Any]:
        """Return today's oracle as a JSON-safe dict (for debug / health API)."""
        return self.get_daily_oracle(reference_date).to_dict()

    # ─── Internal draw helpers ────────────────────────────────────────────────

    def _make_rng(self, date_str: str, extra_salt: str) -> random.Random:
        """Create a deterministic, isolated RNG from the date seed.

        Uses SHA-256 so the seed space is large and well-distributed.
        Does NOT touch the global random state.
        """
        seed_str = f"{date_str}:{self._session_seed}:{extra_salt}"
        digest = hashlib.sha256(seed_str.encode("utf-8")).hexdigest()
        seed_int = int(digest, 16) % (2 ** 31)
        return random.Random(seed_int)  # nosec B311 - deterministic oracle seed, not cryptographic

    def _draw_rune(self, rng: random.Random) -> Dict[str, Any]:
        """Select one rune and determine upright/reversed status."""
        rune = dict(rng.choice(self._runes))
        reversed_possible = rune.get("reversible", True) and self._allow_reversals
        rune["_reversed"] = reversed_possible and rng.random() < 0.33
        if rune["_reversed"] and rune.get("reversed_meaning"):
            rune["_drawn_meaning"] = rune["reversed_meaning"]
        else:
            rune["_reversed"] = False
            rune["_drawn_meaning"] = rune["meaning"]
        return rune

    def _draw_tarot(self, rng: random.Random) -> Dict[str, Any]:
        """Select one tarot card and determine upright/reversed status."""
        card = dict(rng.choice(self._tarot))
        card["_reversed"] = self._allow_reversals and rng.random() < 0.33
        if card["_reversed"]:
            card["_drawn_meaning"] = _reversed_meaning(card)
        else:
            card["_drawn_meaning"] = card["meaning"]
        return card

    def _draw_iching(self, rng: random.Random) -> Dict[str, Any]:
        """Select one I Ching hexagram (no reversal in traditional usage)."""
        return dict(rng.choice(self._iching))

    def _try_load_tables(self, path: Path) -> None:
        """Attempt to load custom oracle tables from a YAML file.

        Expected structure:
          runes:   [...] — optional override of built-in rune table
          tarot:   [...] — optional override of tarot deck
          iching:  [...] — optional override of hexagram table
          desires: [...] — optional override of world desires
          tones:   [...] — optional override of world tones
          focuses: [...] — optional override of world focuses
        """
        if not path.exists():
            return
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh) or {}
            if isinstance(data.get("runes"), list) and data["runes"]:
                self._runes = data["runes"]
                logger.info("Oracle: loaded %d custom runes from %s", len(self._runes), path)
            if isinstance(data.get("tarot"), list) and data["tarot"]:
                self._tarot = data["tarot"]
                logger.info("Oracle: loaded %d custom tarot cards from %s", len(self._tarot), path)
            if isinstance(data.get("iching"), list) and data["iching"]:
                self._iching = data["iching"]
                logger.info("Oracle: loaded %d hexagrams from %s", len(self._iching), path)
            if isinstance(data.get("desires"), list):
                self._desires = data["desires"]
            if isinstance(data.get("tones"), list):
                self._tones = data["tones"]
            if isinstance(data.get("focuses"), list):
                self._focuses = data["focuses"]
        except Exception as exc:
            logger.warning("Oracle: could not load tables from %s: %s — using built-ins", path, exc)

    def _degraded_state(self, date_str: str) -> OracleState:
        """Return a minimal fallback OracleState when computation fails."""
        return OracleState(
            date_seed=date_str,
            rune_name="Perthro", rune_symbol="ᛈ", rune_number=14,
            rune_aett="Hagal's Aett",
            rune_meaning="The lot-cup holds its secret today.",
            rune_keywords=["mystery", "fate"], rune_reversed=False,
            tarot_name="The High Priestess", tarot_number="II",
            tarot_suit=None, tarot_is_major=True,
            tarot_meaning="The oracle speaks in silence.",
            tarot_keywords=["mystery", "intuition"], tarot_reversed=False,
            tarot_hebrew="Gimel", tarot_path=13, tarot_astro="Moon",
            tarot_element="Water",
            iching_number=61, iching_name="Zhong Fu / Inner Truth",
            iching_meaning="Sincerity, inner confidence, truth reaching outward",
            world_tone="dreaming awareness",
            world_desire="reveal hidden truths",
            world_focus="the boundary between worlds thinning",
            timestamp=datetime.now(timezone.utc).isoformat(),
            degraded=True,
        )


# ─── Module-level singleton ────────────────────────────────────────────────────

_ORACLE: Optional[Oracle] = None


def get_oracle() -> Oracle:
    """Return the global Oracle. Raises RuntimeError if not initialised."""
    if _ORACLE is None:
        raise RuntimeError(
            "Oracle not initialised — call init_oracle() in main.py first"
        )
    return _ORACLE


def init_oracle(
    session_seed: str = "sigrid",
    major_only: bool = False,
    allow_reversals: bool = True,
    tables_path: Optional[Path] = None,
) -> Oracle:
    """Create and register the global Oracle (call once at startup)."""
    global _ORACLE
    _ORACLE = Oracle(
        session_seed=session_seed,
        major_only=major_only,
        allow_reversals=allow_reversals,
        tables_path=tables_path,
    )
    return _ORACLE


def init_oracle_from_config(
    config: Dict[str, Any],
    tables_path: Optional[Path] = None,
) -> Oracle:
    """Create and register the global Oracle from a config dict."""
    global _ORACLE
    _ORACLE = Oracle.from_config(config, tables_path=tables_path)
    return _ORACLE
