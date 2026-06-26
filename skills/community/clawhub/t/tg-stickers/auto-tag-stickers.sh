#!/bin/bash
#
# Auto-tag stickers based on emoji meaning
# Usage: ./auto-tag-stickers.sh
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STICKERS_JSON="$SCRIPT_DIR/stickers.json"

echo "🏷️  Auto-tagging stickers based on emoji..."

# Python script to auto-tag
python3 - <<'PYTHON'
import json
from pathlib import Path

STICKERS_JSON = Path(__file__).parent / "stickers.json"

# Emoji to tags mapping
EMOJI_TAGS = {
    "😀": ["happy", "smile", "joy"],
    "😃": ["happy", "smile", "joy"],
    "😄": ["happy", "smile", "joy"],
    "😁": ["happy", "grin", "joy"],
    "😅": ["relief", "embarrassed", "nervous"],
    "😂": ["laugh", "joy", "funny"],
    "🤣": ["laugh", "joy", "funny"],
    "😊": ["happy", "warm", "gentle"],
    "😇": ["innocent", "angelic", "pure"],
    "🙂": ["neutral", "okay", "mild"],
    "🙃": ["playful", "silly", "upside-down"],
    "😉": ["wink", "playful", "flirt"],
    "😌": ["relief", "calm", "peaceful"],
    "😍": ["love", "heart-eyes", "adoration"],
    "🥰": ["love", "warm", "affection"],
    "😘": ["kiss", "love", "affection"],
    "😗": ["kiss", "affection"],
    "😙": ["kiss", "affection"],
    "😚": ["kiss", "affection"],
    "😋": ["yummy", "delicious", "tasty"],
    "😛": ["playful", "silly", "tongue"],
    "😝": ["playful", "silly", "tongue"],
    "😜": ["playful", "wink", "tongue"],
    "🤪": ["crazy", "silly", "wild"],
    "🤨": ["suspicious", "doubtful", "raised-eyebrow"],
    "🧐": ["thinking", "curious", "monocle"],
    "🤓": ["nerd", "geek", "smart"],
    "😎": ["cool", "confident", "sunglasses"],
    "🤩": ["star-struck", "excited", "amazed"],
    "🥳": ["party", "celebration", "excited"],
    "😏": ["smirk", "confident", "sly"],
    "😒": ["bored", "annoyed", "unimpressed"],
    "😞": ["sad", "disappointed", "down"],
    "😔": ["sad", "pensive", "thoughtful"],
    "😟": ["worried", "concerned", "anxious"],
    "😕": ["confused", "uncertain", "puzzled"],
    "🙁": ["sad", "frown", "disappointed"],
    "☹️": ["sad", "frown", "disappointed"],
    "😣": ["struggle", "persevere", "difficulty"],
    "😖": ["confused", "frustrated", "mixed"],
    "😫": ["tired", "exhausted", "weary"],
    "😩": ["weary", "tired", "fed-up"],
    "🥺": ["pleading", "puppy-eyes", "begging"],
    "😢": ["sad", "cry", "tears"],
    "😭": ["cry", "sob", "very-sad"],
    "😤": ["frustrated", "annoyed", "triumph"],
    "😠": ["angry", "mad", "furious"],
    "😡": ["angry", "rage", "furious"],
    "🤬": ["angry", "swear", "censored"],
    "🤯": ["mind-blown", "shocked", "exploding"],
    "😳": ["flushed", "embarrassed", "shocked"],
    "🥵": ["hot", "sweat", "feverish"],
    "🥶": ["cold", "freezing", "shiver"],
    "😱": ["scream", "shocked", "scared"],
    "😨": ["fearful", "scared", "anxious"],
    "😰": ["anxious", "cold-sweat", "worried"],
    "😥": ["sad", "relieved", "disappointed"],
    "😓": ["sweat", "tired", "hard-work"],
    "🤗": ["hug", "warm", "caring"],
    "🤔": ["thinking", "pondering", "hmm"],
    "🤭": ["giggle", "oops", "secret"],
    "🤫": ["shush", "quiet", "secret"],
    "🤥": ["lie", "pinocchio", "dishonest"],
    "😶": ["silent", "blank", "speechless"],
    "😐": ["neutral", "expressionless", "meh"],
    "😑": ["expressionless", "unimpressed", "deadpan"],
    "😬": ["grimace", "awkward", "oops"],
    "🙄": ["eye-roll", "annoyed", "whatever"],
    "😯": ["surprised", "wow", "shocked"],
    "😦": ["frown", "surprised", "concerned"],
    "😧": ["anguished", "worried", "shocked"],
    "😮": ["surprised", "wow", "gasp"],
    "😲": ["astonished", "shocked", "amazed"],
    "🥱": ["yawn", "tired", "bored"],
    "😴": ["sleep", "tired", "zzz"],
    "🤤": ["drool", "desire", "hungry"],
    "😪": ["sleepy", "tired", "drowsy"],
    "😵": ["dizzy", "confused", "knocked-out"],
    "🤐": ["zipper-mouth", "sealed", "secret"],
    "🥴": ["woozy", "dizzy", "drunk"],
    "🤢": ["nauseous", "sick", "disgust"],
    "🤮": ["vomit", "sick", "disgusted"],
    "🤧": ["sneeze", "sick", "tissue"],
    "😷": ["mask", "sick", "health"],
    "🤒": ["sick", "fever", "thermometer"],
    "🤕": ["injured", "bandage", "hurt"],
    "🤑": ["money", "greedy", "rich"],
    "🤠": ["cowboy", "western", "yee-haw"],
    "😈": ["devil", "evil", "mischief"],
    "👿": ["devil", "angry", "evil"],
    "👹": ["ogre", "monster", "scary"],
    "👺": ["goblin", "monster", "angry"],
    "🤡": ["clown", "silly", "joker"],
    "💩": ["poop", "silly", "crap"],
    "👻": ["ghost", "boo", "spooky"],
    "💀": ["skull", "dead", "danger"],
    "☠️": ["skull-crossbones", "danger", "pirate"],
    "👽": ["alien", "ufo", "extraterrestrial"],
    "👾": ["alien-monster", "game", "retro"],
    "🤖": ["robot", "ai", "mechanical"],
    "🎃": ["halloween", "pumpkin", "spooky"],
    "😺": ["cat", "happy", "smile"],
    "😸": ["cat", "grin", "happy"],
    "😹": ["cat", "laugh", "joy"],
    "😻": ["cat", "love", "heart-eyes"],
    "😼": ["cat", "smirk", "confident"],
    "😽": ["cat", "kiss", "affection"],
    "🙀": ["cat", "shocked", "surprised"],
    "😿": ["cat", "cry", "sad"],
    "😾": ["cat", "angry", "grumpy"],
    "👋": ["wave", "hello", "bye"],
    "🤚": ["raised-hand", "stop", "high-five"],
    "🖐️": ["hand", "stop", "five"],
    "✋": ["raised-hand", "stop", "halt"],
    "🖖": ["vulcan-salute", "star-trek", "live-long"],
    "👌": ["ok", "perfect", "good"],
    "🤌": ["pinched-fingers", "italian", "what"],
    "🤏": ["pinching-hand", "small", "tiny"],
    "✌️": ["victory", "peace", "two"],
    "🤞": ["crossed-fingers", "hope", "luck"],
    "🤟": ["love-you", "rock", "metal"],
    "🤘": ["rock-on", "metal", "horns"],
    "🤙": ["call-me", "hang-loose", "shaka"],
    "👈": ["point-left", "that", "direction"],
    "👉": ["point-right", "this", "direction"],
    "👆": ["point-up", "above", "look"],
    "🖕": ["middle-finger", "rude", "offensive"],
    "👇": ["point-down", "below", "look"],
    "☝️": ["point-up", "number-one", "attention"],
    "👍": ["thumbs-up", "good", "like"],
    "👎": ["thumbs-down", "bad", "dislike"],
    "✊": ["fist", "power", "solidarity"],
    "👊": ["fist-bump", "punch", "strong"],
    "🤛": ["left-fist-bump", "punch", "strong"],
    "🤜": ["right-fist-bump", "punch", "strong"],
    "👏": ["clap", "applause", "bravo"],
    "🙌": ["raising-hands", "celebration", "praise"],
    "👐": ["open-hands", "hug", "offering"],
    "🤲": ["palms-up", "prayer", "offering"],
    "🤝": ["handshake", "deal", "agreement"],
    "🙏": ["pray", "thanks", "namaste"],
    "✍️": ["writing", "note", "sign"],
    "💪": ["muscle", "strong", "flex"],
    "🦾": ["mechanical-arm", "strong", "robot"],
    "🦿": ["mechanical-leg", "prosthetic", "robot"],
    "🦵": ["leg", "kick", "limb"],
    "🦶": ["foot", "kick", "step"],
    "👂": ["ear", "listen", "hear"],
    "🦻": ["ear-hearing-aid", "listen", "assist"],
    "👃": ["nose", "smell", "sniff"],
    "🧠": ["brain", "smart", "think"],
    "🫀": ["heart-anatomy", "love", "life"],
    "🫁": ["lungs", "breath", "respiratory"],
    "🦷": ["tooth", "dental", "smile"],
    "🦴": ["bone", "skeleton", "structure"],
    "👀": ["eyes", "looking", "watching"],
    "👁️": ["eye", "see", "vision"],
    "👅": ["tongue", "taste", "lick"],
    "👄": ["mouth", "lips", "kiss"],
    "💋": ["kiss-mark", "lipstick", "love"],
    "🩸": ["blood", "donate", "injury"],
    "🔪": ["knife", "cut", "dangerous"],
    "❓": ["question", "confused", "unknown"],
    "❗": ["exclamation", "important", "alert"],
    "💯": ["hundred", "perfect", "full"],
    "💢": ["anger", "frustrated", "symbol"],
    "💥": ["collision", "boom", "explosion"],
    "💫": ["dizzy", "stars", "sparkle"],
    "💦": ["sweat", "water", "droplets"],
    "💨": ["dash", "wind", "fast"],
    "🕳️": ["hole", "empty", "void"],
    "💣": ["bomb", "explosive", "danger"],
    "💬": ["speech-balloon", "chat", "talk"],
    "👁️‍🗨️": ["eye-speech-bubble", "witness", "i-am-witness"],
    "🗨️": ["left-speech-bubble", "chat", "talk"],
    "🗯️": ["right-anger-bubble", "angry", "shout"],
    "💭": ["thought-balloon", "thinking", "dream"],
    "💤": ["zzz", "sleep", "tired"],
    "👨⚕️": ["doctor", "medical", "health"],
    "👩⚕️": ["doctor", "medical", "health"],
    "🙋♀️": ["woman-raising-hand", "question", "volunteer"],
    "🙋‍♂️": ["man-raising-hand", "question", "volunteer"],
    "🍚": ["rice", "food", "meal"],
    "🫠": ["melting", "hot", "dissolve"],
    "🫨": ["shaking", "vibrate", "earthquake"],
    "🌞": ["sun-face", "happy", "sunny", "positive"],
}

with open("stickers.json") as f:
    data = json.load(f)

tagged_count = 0
for sticker in data["collected"]:
    emoji = sticker["emoji"]
    # Skip if already has tags
    if sticker["tags"]:
        continue
    
    # Auto-tag based on emoji
    if emoji in EMOJI_TAGS:
        sticker["tags"] = EMOJI_TAGS[emoji]
        tagged_count += 1
        print(f"  ✅ Tagged {emoji}: {', '.join(EMOJI_TAGS[emoji])}")
    else:
        print(f"  ⏭️  Skipped {emoji}: no auto-tag rule")

with open("stickers.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Auto-tagged {tagged_count} stickers!")
PYTHON

echo ""
echo "📊 Run './check-collection.sh' to see your tagged collection"
