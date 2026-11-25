"""Shared helpers for the UGC creator scripts: files, video probing, each platform's limits, text
rules, the brief phrases that are refused or never followed, claim words, time and money, and the
one ledger. Standard library only."""
import datetime, functools, hashlib, json, os, re, subprocess, sys, unicodedata

try:  # Windows consoles default to cp1252; captions are often not Latin
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Sizes are decimal megabytes (1 MB = 1,000,000 bytes): the stricter reading of every platform's
# limit, so a file that passes here passes whichever way a platform counts.
MB = 1000 ** 2
GB = 1000 * MB
# Documented limits for one video post through each platform's own posting API (seconds, bytes,
# characters). "text" is the caption or description; YouTube counts its description in bytes.
LIMITS = {
    "TIKTOK": {"label": "TikTok", "min_s": 3, "max_s": 600, "bytes": 4 * GB, "text": 2200,
               "fps": (23, 60), "max_side": 4096, "min_side": 360},
    "INSTAGRAM": {"label": "Instagram Reels", "min_s": 3, "max_s": 900, "bytes": 300 * MB, "text": 2200,
                  "fps": (23, 60), "max_width": 1920, "tags_max": 5, "strict": True},
    "YOUTUBE": {"label": "YouTube Shorts", "min_s": 1, "max_s": 180, "bytes": 256 * GB,
                "text_bytes": 5000, "title": 100},
}
PLATFORMS = tuple(LIMITS)
TIKTOK_PRIVACY = ("PUBLIC_TO_EVERYONE", "MUTUAL_FOLLOW_FRIENDS", "FOLLOWER_OF_CREATOR", "SELF_ONLY")
HDR_TRANSFER = ("smpte2084", "arib-std-b67")
WINDOWS_RESERVED = {"con", "prn", "aux", "nul"} | {f"com{n}" for n in range(1, 10)} | {f"lpt{n}" for n in range(1, 10)}
SUBMIT_MINUTES = 30      # most campaigns take a post only when it is submitted within 30 minutes of going live
DEFAULT_WINDOW_DAYS = 30
DEFAULT_FEE_PCT = 10.0

# Brief or caption text that asks to hide that a video is paid. Never followed; campaign.py flags each one.
_NEG = r"(?:do not|don'?t|dont|never|avoid|no need to|please don'?t)"
_ADTAG = r"#\s?(?:ad|ads|sponsored|spon|paid|advert|advertisement)\b"
_ADWORD = r"(?:ad|ads|paid|sponsor(?:ed|ship)?|partnership|brand(?:ed)?|promo(?:tion(?:al)?)?)"
# A disclosure named in words: "disclosure", "the ad label", "paid partnership label", "branded content toggle".
_DISCWORD = (r"(?:(?:ad\s+|paid\s+|sponsor(?:ship|ed)?\s+)?(?:disclosures?|disclaimers?)|(?:ad|sponsor(?:ed)?)\s+(?:label|tag|hashtag)s?"
             r"|paid[- ]partnership(?:\s+(?:label|toggle|tag))?|branded[- ]content(?:\s+(?:label|toggle|setting))?)")
_TOGGLE = (r"paid[- ]partnership|branded[- ]content|promotion(?:al)?(?:\s+content)?|sponsor(?:ed|ship)?|content disclosure"
           r"|disclosure|ad\s+(?:label|toggle|setting)")
_REJECT = (r"\b(?:rejected|refused|declined|disqualif\w*|not (?:be )?(?:approved|accepted|paid|counted)|"
           r"won'?t (?:be )?(?:approved|accepted|paid|counted)|unpaid|removed)\b")
_WITH_AD_REJECTED = (r"\bwith\s+(?:an?\s+|the\s+|any\s+)?(?:" + _ADTAG + r"|" + _DISCWORD + r")[^.\n]{0,60}?" + _REJECT)
# Brief text about how the video should FEEL ("keep it natural", "shouldn't feel like an ad", "make it look
# native"). That is style direction, not a ban on the disclosure: the campaign stays GO, the sentence is
# shown as a tone note, and the disclosure stays. Only text that forbids, drops, hides or moves the
# disclosure itself (HIDE_AD) stops a campaign.
TONE_AD = [
    _NEG + r"\s+(?:make|let)\s+(?:it|this|them|the (?:clip|video|post)s?)\s+(?:look|feel|seem|sound|appear)\s+like\s+(?:an?\s+)?(?:ad|advert|advertisement|sponsored|promo|paid|commercial)",
    _NEG + r"\s+(?:make|let)\s+(?:it|this|them|the (?:clip|video|post)s?)\s+(?:look|feel|seem|appear)\s+(?:sponsored|paid|promotional|branded|like a promotion|salesy|scripted|staged)",
    r"\b(?:make|keep)\s+(?:it|them|this|the (?:clip|video|post)s?)\s+(?:look|feel|seem|looking|feeling|seeming)\s+(?:organic|native|natural|authentic|real|like (?:a |an )?(?:fan|organic|regular|normal|random))",
    r"\b(?:look|feel|seem|appear|read)s?\s+like\s+[^.\n]{0,40}?,?\s*not\s+(?:like\s+)?(?:an?\s+)?(?:ad|advert|advertisement|sponsored|paid|promo|commercial)\b",
    r"\b(?:look|feel|seem)s?\s+(?:natural|organic|authentic)\b[^.\n]{0,40}\bnot\s+(?:an?\s+)?(?:ad|paid|sponsored|commercial)",
    r"\bnot\s+(?:obviously|clearly|too)\s+(?:an?\s+)?(?:ad|sponsored|paid|salesy|commercial)",
    r"\b(?:shouldn'?t|should not|mustn'?t|must not|can'?t|cannot|won'?t)\s+(?:feel|look|seem|sound|come across|read)\s+(?:like\s+|as\s+)?(?:an?\s+)?"
    r"(?:ad|ads|advert|advertisement|commercial|promo|sponsored|paid|salesy)\b",
    r"\bno\s+(?:ad|ads|advert|sponsored|promo|commercial|salesy)[- ]?(?:vibes?|feel(?:ing)?|look|energy|style|tone)\b",
    r"\b(?:look|looks|feel|feels|seem|seems|sound|sounds|come across|comes across)\s+(?:like\s+|as\s+)?(?:an?\s+)?"
    r"(?:ad|ads|advert|advertisement|promo|commercial)\b[^.\n]{0,40}?" + _REJECT,
    r"\bnot\s+(?:too\s+)?salesy\b",
    # "a regular post, not an ad", "native content, not an ad", "a recommendation from a friend, not an advert"
    r"\b(?:post|tiktok|video|content|reel|short|recommendation|vlog|story|review|clip|ugc)s?\b[^.\n]{0,40}?,\s*not\s+"
    r"(?:an?\s+)?(?:ad|advert|advertisement|commercial|ad read)\b",
    r"\bnot\s+an?\s+(?:ad|advert)\s+read\b",
    r"\b(?:blend|fit)s?\s+in\b[^.\n]{0,60}\b(?:feed|for you|fyp|content)\b",
    r"\b(?:avoid|no)\s+(?:anything\s+that\s+)?(?:screams?|looks?\s+like)\s+(?:an?\s+)?(?:ad|advert|commercial)\b",
]
# Moving or swapping the disclosure is hiding it too: "#ad at the end with the other hashtags", "keep #ad
# out of the first line", "use #partner instead of #ad".
_MOVE_AD = [
    r"(?:" + _ADTAG + r")[^.\n]{0,40}\b(?:at|to)\s+the\s+(?:end|bottom)\b",
    r"(?:" + _ADTAG + r")[^.\n]{0,40}\b(?:last|with the other (?:hash)?tags|after the other (?:hash)?tags|below the fold)\b",
    r"\b(?:keep|leave|move)\s+(?:the\s+)?(?:" + _ADTAG + r")(?:\s+hashtag)?\s+(?:out of|off|away from|below)\s+the\s+(?:first|top)\b",
    r"\b(?:use|put|write)\s+(?:#\w+)\s+instead\s+of\s+(?:" + _ADTAG + r")",
    r"(?:" + _ADTAG + r")[^.\n]{0,20}\binstead\s+(?:use|put|write)\s+#\w+",
    r"\b(?:" + _TOGGLE + r")\s*(?:label|toggle|tag|setting|box|switch)?\s+(?:should|must|can)\s+(?:stay|be|remain)\s+(?:off|disabled|unticked)\b",
]
HIDE_AD_CORE = [
    r"(?:\bno|without|skip|remove|drop|leave out|lose|ditch)\s+(?:the\s+|any\s+|a\s+)?" + _ADTAG,
    _NEG + r"\s+(?:use|put|add|include|using|adding|putting|including|write|type|tag)\s+(?:the\s+|a\s+|an\s+|any\s+)?(?:" + _ADTAG
    + r"|" + _ADWORD + r"\s+(?:disclosure|label|tag|toggle|hashtag|setting)s?)",
    _NEG + r"\s+(?:disclose|mention|say|tag|label|tell|flag|mark)\b[^.\n]{0,40}\b(?:ad|paid|sponsor|sponsored|partnership|brand deal|promotion)",
    _NEG + r"\s+(?:use|turn on|tick|enable|add|switch on|toggle)\s+(?:the\s+)?(?:paid[- ]partnership|branded[- ]content|promotion(?:al)?|sponsor(?:ed)?|content disclosure)\s*(?:label|toggle|tag|tool|setting|disclosure|box)?",
    r"\b(?:leave out|skip|drop|remove|forget|no|without|ditch)\s+(?:the\s+|any\s+|a\s+)?(?:ad\s+|paid\s+|sponsor(?:ship|ed)?\s+)?(?:disclosures?|paid[- ]partnership(?:\s+(?:label|toggle|tag|setting))?|branded[- ]content(?:\s+(?:label|toggle|setting))?)\b",
    r"\b(?:hide|hiding|conceal)\s+(?:that|the fact)\b[^.\n]{0,40}\b(?:paid|ad|sponsor)",
    r"\b(?:no|without)\s+(?:ad|sponsor(?:ship|ed)?|paid)\s+(?:disclosure|label|tag|hashtag)s?\b",
    r"\bpretend\b[^.\n]{0,40}\b(?:fan|found|organic|not paid|your own)",
    r"\b(?:#sp|#collab)\s+(?:is\s+)?(?:enough|instead)\b",
    r"\b(?:nobody|no one|no-one|people (?:won't|don't|shouldn't))\s+(?:knows?|can tell|realis|realiz|notices?|finds? out)[^.\n]{0,30}\b(?:ad|paid|sponsor)",
    r"\bmake\s+(?:viewers|people|them|your (?:audience|followers))\s+(?:think|believe)\b",
    _WITH_AD_REJECTED,
] + _MOVE_AD + [
    # toggles switched off: "Turn off the branded content toggle", "Leave the Paid Partnership label off"
    r"\b(?:turn|switch|toggle|keep|leave)\s+off\s+(?:the\s+|any\s+)?(?:" + _TOGGLE + r")",
    r"\b(?:turn|switch|toggle|keep|leave)\s+(?:the\s+|any\s+)?(?:" + _TOGGLE + r")\s*(?:label|toggle|tag|setting|box|switch)?\s+off\b",
    r"\b(?:no|without|avoid|skip)\s+(?:hash)?tags?\s+(?:like|such as)\s+(?:the\s+)?" + _ADTAG,
    # "Don't make it obvious it's an ad", "nobody should know it's sponsored"
    _NEG + r"\s+mak\w*\s+(?:it|this|them|the (?:clip|video|post)s?)\s+(?:too\s+|so\s+)?(?:obvious|clear|evident|apparent)\b"
    r"[^.\n]{0,30}\b(?:ad|ads|advert|sponsored|paid|promo\w*|brand deal|commercial)\b",
    r"\b(?:nobody|no one|no-one|(?:viewers?|people|followers?|they)\s+(?:shouldn'?t|should not|mustn'?t|must not|"
    r"don'?t need to|can'?t|cannot))\b[^.\n]{0,30}\b(?:know|tell|notice|realise|realize|guess|see)\b[^.\n]{0,40}\b"
    r"(?:ad|ads|advert|sponsored|paid|promo\w*|brand deal|partnership|commercial)\b",
]
# A paid video that says it isn't one, or walks the disclosure back: "not an ad, just my opinion", "I'm not
# being paid to say this", "nobody is paying me", "I'd post this anyway". In a script, a caption, a title
# or a take these are errors no tag or confirmation clears. In a brief they count only when the brief tells
# the creator to say them ("Say it's not an ad"): "a regular post, not an ad" is a tone note.
DENY_AD = [
    r"(?<![\w'])(?:is\s+|isn'?t\s+|'s\s+)?not\s+(?:even\s+)?(?:an?\s+)?(?:ad|advert|advertisement|sponsored|paid)\b"
    r"(?!\s+(?:campaign|agency|agencies|blocker|budget|spend|account|manager|platform|network|read))",
    r"\b(?:this|it|that)\s+(?:isn'?t|is not|wasn'?t|was not)\s+(?:even\s+)?(?:an?\s+)?(?:ad|advert|advertisement|sponsored|paid)\b",
    r"\b(?:nobody|no one|no-one|no brands?|zero brands?|none of (?:them|the brands))\s+(?:is\s+|has\s+|'s\s+|ever\s+)?"
    r"(?:paying|paid|pays|sponsor\w*|asked)\b",
    r"\b(?:i'?m|i am|we'?re|we are|i was|we were|i'?ve|i have)\s+(?:not|never)\s+(?:been\s+)?(?:being\s+)?(?:paid|sponsored)\b",
    r"\bnot\s+(?:being\s+)?(?:paid|sponsored)\s+(?:to|for|by)\s+(?:say|post|make|talk|share|do|this|it)\b",
    r"\beven\s+if\s+(?:they|you|nobody|no one|the brand|it|\w+)\s+(?:didn'?t|did not|wasn'?t|weren'?t|was not|don'?t|do not|"
    r"hadn'?t)\s+(?:pay|paid|sponsor)",
    r"\bwould(?:'ve| have)?\s+(?:post|say|make|share|film)\w*\s+(?:about\s+)?(?:this|it)\s+(?:anyway|regardless|for free)\b",
    r"\bno\s+(?:brand\s+deal|sponsorship|paid\s+(?:deal|partnership))\b",
    r"\bunsponsored\b", r"#\s?not\s?an?\s?ad\b", r"\bjust\s+my\s+(?:honest\s+)?opinion,?\s+not\s+(?:an?\s+)?(?:ad|sponsored)",
]
_INSTRUCT = r"\b(?:say|said|saying|mention|tell|write|claim|state|caption|add|put|include|type|tag)\b"
HIDE_AD = HIDE_AD_CORE + DENY_AD
# When to disclose, not whether: "Never say it's an ad in the hook", "don't say ad in the first 2 seconds".
# A GO with a note; campaign.json's disclosure.not_in_hook and not_before_s carry the rule into the checks.
DISCLOSURE_TIMING = [
    r"\b(?:never|don'?t|do not|avoid)\s+(?:say|saying|mention|start with|open with|lead with)\b[^.\n]{0,40}?\b(?:ad|sponsored|paid|"
    r"disclos\w*)\b[^.\n]{0,25}?\b(?:in|during|for)\s+(?:the\s+|your\s+)?(?:hook|opening|intro|first line|first (?:\d+|two|three|"
    r"few) (?:s|secs?|seconds?))\b",
    r"\b(?:hook|open|start)\s+first,?\s+then\s+(?:disclose|say)",
    r"\b(?:not|never)\s+in\s+the\s+hook\b",
]
# The brief calls the disclosure optional or says no small print: the skill discloses anyway, as the law
# requires. A GO with a warning, never a NO-GO.
DISCLOSURE_OPTIONAL = [
    r"(?:" + _ADTAG + r"|" + _DISCWORD + r"|(?:spoken|verbal|on[- ]screen)\s+(?:disclosure|ad)|(?:the\s+)?(?:paid[- ]partnership|"
    r"branded[- ]content)\s+(?:toggle|label|setting))\s+(?:is|are)\s*(?:not|n'?t)\s+(?:required|needed|necessary|mandatory)",
    r"(?:" + _ADTAG + r"|" + _DISCWORD + r"|(?:spoken|verbal|on[- ]screen)\s+(?:disclosure|ad)|(?:paid[- ]partnership|"
    r"branded[- ]content)\s+(?:toggle|label|setting))\s+(?:is|are)\s+(?:optional|not a must)\b",
    r"\b(?:don'?t|do not|doesn'?t|does not|won'?t)\s+need\s+(?:to\s+)?(?:disclose|label|tag|mark|flag|add\s+(?:the\s+)?#)",
    r"\b(?:disclosure|disclosing|#ad|the ad label|labell?ing)\s+(?:is\s+)?(?:optional|up to you)\b",
    r"\bneed\s*(?:n'?t|not)\s+(?:disclose|label|tag|mark)\b",
    r"\bno\s+need\s+(?:for|to)\s+(?:a|an|the|any)?\s*(?:ad\s+|paid\s+)?(?:disclos\w*|disclaimer|#?ad\b|label)",
    r"\b(?:no|without|skip(?:\s+the)?)\s+(?:legal\s+)?disclaimers?\b",
]
# Where the brief wants the disclosure, against the rule: "#ad in the first comment", "caption only, nothing
# in the video". A comment doesn't count as a disclosure, and Content Rewards wants #ad first in the caption;
# the skill keeps #ad first in the caption and says it out loud. A GO with a warning.
DISCLOSURE_PLACEMENT = [
    r"(?:" + _ADTAG + r"|" + _DISCWORD + r"|disclose)\b[^.\n]{0,40}?\b(?:in|as|into)\s+(?:a|the|the first|your first|your)\s+comments?\b",
    r"\b(?:in|as)\s+(?:a|the|the first|your first)\s+comments?\b[^.\n]{0,30}?(?:" + _ADTAG + r"|disclos\w*)",
    r"\b(?:caption|description)\s+only\b|\bonly\s+(?:use\s+#?ad\s+)?in\s+the\s+(?:caption|description)\b",
    r"\bnothing\s+(?:about\s+(?:the\s+)?ad\s+)?(?:in|on)\s+the\s+video\b",
    r"\b(?:don'?t|do not|never)\s+(?:say|mention)\b[^.\n]{0,20}?\bad\b[^.\n]{0,10}?\b(?:in|on)\s+the\s+(?:video|clip)\b",
]
# The disclosure itself is what gets a video rejected: "Posts with #ad will not be approved". Never followed.
DISCLOSURE_REJECTED = [_WITH_AD_REJECTED]
# Only in a brief: the same words can be innocent in a caption ("how to act natural on camera").
TONE_AD_BRIEF = [r"\bact\s+(?:natural|organic|normal)\b"]
# A sentence that names the disclosure as what is required asks for it, not against it: "Posts without
# #ad are rejected", "No #ad means not paid", "#ad is required". A sentence where the disclosure itself
# causes the rejection ("with #ad ... not approved", "looks like an ad ... rejected") is not one of these.
DISCLOSE_REQUIRED = [
    r"\b(?:without|no|missing|lacking|forget\w*|leave out|leaving out|skip\w*)\s+(?:an?\s+|the\s+|any\s+|a clear\s+)?"
    r"(?:" + _ADTAG + r"|" + _DISCWORD + r"|ad)\b[^.\n]{0,60}?(?:" + _REJECT + r"|\bmeans\s+(?:not paid|no pay|rejected))",
    r"(?:" + _ADTAG + r"|" + _DISCWORD + r")\s+(?:is|are)\s+(?:always\s+)?(?:required|mandatory|a must|compulsory)\b",
    r"\b(?:must|always|has to|have to)\s+(?:include|use|add|have|carry|show|start with)\s+(?:an?\s+|the\s+)?(?:"
    + _ADTAG + r"|" + _DISCWORD + r")",
    r"\b(?:don'?t|do not|doesn'?t|does not|fail(?:s|ing)? to|forget(?:s|ting)? to)\s+(?:include|add|use|put|show|turn on|"
    r"tick|have|carry)\b[^.\n]{0,40}?(?:" + _ADTAG + r"|" + _DISCWORD + r"|\bad\b)[^.\n]{0,60}?(?:" + _REJECT
    + r"|won'?t (?:be )?paid|not (?:be )?paid|isn'?t paid)",
]
# Words that name a disclosure, for the "read this sentence yourself" net.
DISCLOSURE_MENTION = r"(?:" + _ADTAG + r"|\b(?:ad|ads|advert\w*|disclos\w+|disclaimer|sponsor\w*|paid[- ]partnership|branded[- ]content|promotion(?:al)? content)\b)"
NEGATION_OR_REJECT = r"\b(?:no|not|never|don'?t|do not|without|avoid|skip|remove|hide|off|rejected|isn'?t|aren'?t|won'?t)\b"
# Brief text that forbids the disclosure on the video itself. The skill keeps it on screen anyway, so the
# brief and the skill disagree: the user asks the brand in writing or skips the campaign.
DISCLOSURE_CONFLICT = [
    r"\bno\s+(?:ad|disclosure|sponsor(?:ed|ship)?|promo(?:tional)?)\s+(?:text|label|overlay|banner|sticker|title|pill)s?\b",
    _NEG + r"\s+(?:put|show|burn|write|add|place|display)\s+(?:any\s+|the\s+)?[\"'“]?(?:ad|sponsored|disclosure)[\"'”]?\s+"
    r"(?:label\s+|text\s+)?(?:on|in|over|into)\s+(?:the\s+)?(?:video|clip|screen|footage)",
    r"\bno\s+on[- ]screen\s+(?:disclosure|label|ad)\b",
    r"\bno\s+burn(?:ed|t)[- ]in\s+(?:disclosure|label)",
]
# Asking for or arranging engagement: a permanent ban on the marketplaces and a platform rule break.
ENGAGEMENT_BAIT = [
    r"\bl4l\b", r"\bf4f\b", r"\bsub4sub\b", r"\bengagement\s+(?:group|pod|chat)s?\b",
    r"\bbuy(?:ing)?\s+(?:views|likes|followers|comments|shares)\b", r"\bview\s*bots?\b", r"\bbot(?:ted|ting)?\s+(?:views|likes)\b",
]
# In a caption these read as asking viewers to swap follows; often meant, sometimes quoted. A warning there.
ENGAGEMENT_SOFT = [r"\b(?:like|follow|sub)\s*(?:4|for)\s*(?:like|follow|sub)\b"]
# Only in a brief: location tricks. The word VPN in a caption ("the best VPN for travel") is fine.
LOCATION_TRICKS = [
    r"\b(?:use|using|with|via|through|turn on|get|need)\s+(?:a\s+|your\s+)?vpn\b",
    r"\bvpn\s+(?:to|for|set to|in)\s+(?:change|fake|spoof|appear|look|get|set|switch|the us|us|usa|america)\b",
    r"\b(?:fake|spoof|change)\s+(?:your\s+)?(?:location|country|region|ip)\b",
    r"\b(?:from|on|over|provide|provides|give|gives|offer|offers)\b[^.\n]{0,20}\bvpn\b",
]
# A sentence that bans something (the brief's own "no engagement groups") is not a request for it.
BANS_IT = r"\b(?:no|not|never|don'?t|do not|without|avoid|banned?|forbidden|prohibited|disallowed|zero|against)\b"

# ---- UGC: what the skill refuses in a brief, and the words that mark a claim in a script

# Posting from an account the brand owns, or one made up as a character: refused. The viewer can't tell
# a paid creator is talking, and the account isn't the creator's.
BRAND_ACCOUNT = [
    r"\bpost\s+(?:it\s+|them\s+|the videos?\s+)?(?:from|on|to)\s+(?:our|the brand'?s|an?\s+account\s+we\s+(?:give|provide|create|own|set up))\b",
    r"\b(?:we(?:'ll| will)?|the brand(?: will)?)\s+(?:give|provide|send|create|set up)\s+(?:you\s+)?(?:the\s+|a\s+|an\s+)?(?:login|log-in|account|accounts|page)s?\b",
    r"\blog\s?in(?:to)?\s+(?:to\s+)?(?:our|the brand'?s)\s+(?:account|page|profile)",
    r"\bbrand[- ]owned\s+(?:account|page|profile)s?\b",
    r"\b(?:new|fresh|separate)\s+account\b[^.\n]{0,40}\b(?:as|named|called|posing as|for)\s+(?:a\s+)?(?:character|customer|fan|girl|guy|student|mom|dad)\b",
    r"\b(?:as|play|playing|create|creating|post as|posting as|adopt|adopting|use|using|become)\s+(?:a|an|the|this|our)\s+"
    r"(?:\w+\s+){0,2}persona\b",
]
# Posting as someone the creator isn't: "post as a happy customer", "say you're a regular user", "pretend
# you're a fan". NO-GO: the brand is asked whether a disclosed video in the creator's own voice is fine.
PERSONA = [
    r"\b(?:say|pretend|claim|tell (?:people|viewers|them|your audience))\b[^.\n]{0,30}?\b(?:you(?:'re| are)|to be)\s+"
    r"(?:just\s+)?(?:a\s+|an\s+)?(?:real|regular|normal|random|genuine|actual|ordinary|happy)\s+(?:user|customer|buyer|person|fan|client)",
    r"\b(?:post|talk|speak|film|act|pose|present yourself)\s+(?:as|like)\s+(?:a|an|any)?\s*(?:happy|regular|real|normal|random|"
    r"ordinary|satisfied|genuine|everyday)?\s*(?:customer|user|buyer|fan|client|consumer|shopper)s?\b(?!\s+would)",
    r"\bpretend\b[^.\n]{0,40}\b(?:customer|user|bought|found|discovered|stumbled|fan)",
    r"\bmake\s+(?:viewers|people|them|your (?:audience|followers))\s+(?:think|believe)\b",
]
# The creator is asked to say what didn't happen: use they didn't have, results they didn't get.
FAKE_TESTIMONIAL = [
    r"\b(?:say|claim|tell|mention|act like)\b[^.\n]{0,30}?\byou(?:'ve| have)?\s+(?:been\s+)?(?:used|using|tried|bought|had)\b"
    r"[^.\n]{0,30}?\b(?:for|since)\s+(?:\w+\s+){0,2}(?:days?|weeks?|months?|years?)\b",
    r"\b(?:even if|whether or not|doesn'?t matter if|no matter if)\s+you(?:'ve| have)?\s+(?:not\s+|never\s+)?(?:actually\s+)?(?:used|tried|bought|tested)",
    r"\byou\s+(?:don'?t|do not)\s+(?:need|have)\s+to\s+(?:have\s+)?(?:actually\s+)?(?:use[ds]?|try|tried|buy|bought|test(?:ed)?)\b",
    r"\b(?:fake|made[- ]up|invented|scripted)\s+(?:review|testimonial|results?|before[- ]and[- ]after|story)",
    r"\b(?:write|post|leave)\s+(?:a\s+)?(?:5|five)[- ]star\s+review",
    r"\b(?:make up|invent)\s+(?:a\s+|your\s+)?(?:story|result|number|testimonial|review)",
]
# A discovery story the brief writes for the creator: "act like you just discovered it", "talk about it like
# you found it on your own". Not refused: it is an experience claim, kept only when it is how the creator
# really found it, otherwise reworded ("here's what <brand> does").
DISCOVERY = [
    r"\b(?:like|as if|as though)\s+(?:you|a (?:regular |normal |real )?user|someone)\s+(?:just\s+|have\s+just\s+)?(?:found|discovered|"
    r"stumbled|came across|came upon)\b",
    r"\bact\s+(?:like|as if|as though)\s+you\b",
    r"\b(?:just\s+)?(?:discovered|found|stumbled (?:on|upon|across))\s+(?:it|this|the app|the product|glowly|\w+)\s+(?:on your own|yourself|"
    r"organically|by accident|by chance)\b",
]
# Results or use the brief tells the creator to claim ("say it cleared your skin", "share your results after
# 30 days", "tell them you use it every day"): only if true. The checklist asks each one before GO.
DICTATED = [
    r"\b(?:say|tell|mention|share|show|talk about|explain|claim)\b[^.\n]{0,40}?\b(?:your|you(?:'ve| have)?)\s+(?:honest\s+)?"
    r"(?:results?|before[- ]and[- ]after|experience|progress|journey|transformation|favou?rite|routine|daily|used|use|love|"
    r"been using|tried)\b",
    r"\b(?:say|tell|mention|claim)\b[^.\n]{0,40}?\b(?:it|the \w+|this)\s+(?:cleared|fixed|changed|saved|helped|cured|improved|"
    r"transformed|removed|got rid)\b",
    r"\bafter\s+(?:\d+|a few|two|three|four)\s+(?:days?|weeks?|months?)\s+of\s+(?:using|use)\b",
    r"\bbefore[- ]and[- ]after\b",
    r"\b(?:the|an?)\s+app\s+you\s+use\s+every\s+(?:day|morning|night)\b",
]
# The brief allows or wants a generated person or voice. Required: refused, a real person films. Allowed
# ("AI UGC accepted", "you can use an avatar if you prefer"): a GO, the creator films as always.
AI_PRESENTER = [
    r"\b(?:ai|a\.i\.)[- ]?(?:generated\s+)?(?:avatar|actor|actress|presenter|influencer|spokesperson|creator|person|human|model|ugc|talking head)s?\b",
    r"\b(?:digital|virtual|synthetic)\s+(?:avatar|human|presenter|influencer|person|actor|creator)s?\b",
    r"\bvoice[- ]?clon\w*|\bclone\s+(?:your|a|the)\s+voice\b",
    r"\b(?:lip[- ]?sync(?:ed)?\s+(?:avatar|video)|face[- ]?swap\w*|deep\s?fake\w*)\b",
]
# A computer voice reading the script. The skill uses the creator's own voice: required is a NO-GO (ask
# whether a real voiceover is fine), allowed is a GO.
TTS_VOICE = [r"\btext[- ]to[- ]speech\b", r"\btts\b", r"\bai[- ]?(?:generated\s+)?voice(?:[- ]?over)?s?\b",
             r"\b(?:synthetic|computer|robot(?:ic)?|generated)\s+voice(?:[- ]?over)?s?\b"]
# Words that make an AI or TTS line an option, not a requirement.
PERMISSIVE = (r"\b(?:accept\w*|allow\w*|can use|may use|could use|are welcome|is welcome|welcome to|as well as|optional|"
              r"if you prefer|if you want|if you like|or real|either|ok(?:ay)?\s+(?:too|as well)|fine\s+(?:too|as well)|"
              r"not required|no problem)\b")
# Clean footage: no burned-in text on the video. Allowed: the skill leaves captions and the hook text off
# ("burned_text": "none" or "disclosure_only" in campaign.json) and discloses out loud, first in the caption
# and with the platform's own label.
NO_BURNED_TEXT = [
    r"\b(?:no|without|zero)\s+(?:any\s+)?(?:text|overlays?|stickers?|graphics?|banners?|captions?|subtitles?)(?:\s*(?:,|or|and)\s*"
    r"(?:text|overlays?|stickers?|graphics?|captions?|subtitles?))*\s+(?:burned\s+|burnt\s+)?(?:on|over|in|into)\s+(?:the\s+)?"
    r"(?:video|clip|screen|footage)",
    r"\bno\s+(?:text\s+)?overlays?\b", r"\bno\s+burn(?:ed|t)[- ]in\s+(?:text|captions?|subtitles?)",
    r"\b(?:don'?t|do not|never)\s+burn\s+in\s+(?:any\s+)?(?:text|captions?|subtitles?)",
    r"\bclean\s+(?:footage|video|clips?)\b[^.\n]{0,30}\bno\s+(?:text|stickers?|captions?)",
    r"\bno\s+(?:captions?|subtitles?)\s+on\s+the\s+video\b",
    r"\bno\s+on[- ]screen\s+(?:text|captions?)\b",
    r"\b(?:keep|leave)\s+the\s+(?:footage|video|clips?)\s+clean\b",
    r"\bno\s+(?:text|stickers?|captions?|subtitles?)\s*(?:,|or|and)\s*(?:text|stickers?|captions?|subtitles?)\b",
]
# Content about earning money. Flagged so every earnings claim in the video is checked: a money figure
# or "you can make" needs the brand's typical-earnings line, and get-rich-quick framing is never used.
MAKE_MONEY = [
    r"\b(?:make|making|earn|earning|made|earned)\s+(?:real\s+|extra\s+|easy\s+|passive\s+|some\s+|more\s+)?(?:money|cash|income|\$\s?\d)",
    r"\bpassive income\b", r"\bside hustle\b", r"\bearn\w*\s+(?:money\s+|extra\s+)?on\s+the\s+side\b", r"\bside income\b", r"\bget paid (?:to|for|from)\b", r"\bfinancial freedom\b",
    r"\bquit (?:your|my) (?:9|nine|day )", r"\$\s?\d[\d,.]*\s*(?:k\s*)?(?:a|per|/|in a|in one)\s*(?:day|week|month|year)\b",
    r"\b(?:income|payout|earnings)\s+(?:proof|screenshots?)\b", r"\bmoney[- ]making\b",
]
# TikTok's branded content policy: these can't be promoted in branded content at all ...
PROHIBITED_TOPICS = {
    "weight loss": r"\b(?:weight[- ]loss|lose weight|fat[- ]burn\w*|slimming|diet pills?|appetite suppress\w*)\b",
    "multi-level marketing": r"\b(?:mlm|multi[- ]level marketing|network marketing|downline)\b",
    "payday loans": r"\bpayday (?:loans?|lenders?)\b",
    "CBD": r"\bcbd\b",
    "political content": r"\b(?:vote for|election|candidate|political (?:ad|campaign|party))\b",
    "tobacco or vapes": r"\b(?:vape|vapes|vaping|e-?cig\w*|nicotine|tobacco)\b",
}
# ... and these only by invitation (TikTok One). Flagged for the creator to check, not refused.
RESTRICTED_TOPICS = {
    "gambling": r"\b(?:gambling|casino|betting|sportsbook|bet on)\b",
    "alcohol": r"\b(?:alcohol|beer|wine|vodka|whisk(?:e)?y|spirits brand)\b",
    "supplements or medicine": r"\b(?:supplements?|vitamins?|gummies|medication|medicine|pills?)\b",
    "financial services": r"\b(?:crypto\w*|forex|trading app|stock trading|invest(?:ing|ment) app|loans?|credit cards?)\b",
}
# A line that says the creator used something or got a result: it must be the creator's own, confirmed.
# Creators often drop the "I": "been obsessed with this for months", "now my lock screen", "my skin cleared".
EXPERIENCE_HINTS = (r"\b(?:i(?:'ve| have)?\s+(?:been\s+)?(?:using|used|tried|tested|bought|had|switched|opened|open|"
                    r"downloaded|installed)|i\s+(?:use|love|swear by|recommend|can'?t live without|can'?t stop)|"
                    r"(?:been|was|am|i'?m)\s+(?:obsessed|hooked|addicted)|obsessed with|been using|been loving|"
                    r"can'?t stop using|my\s+(?:favorite|favourite|go-?to|results?|new|daily)|now my|"
                    r"my\s+(?:lock ?screen|home ?screen|wallpaper|routine|mornings?|skin|sleep|hair|face|body|energy|"
                    r"mood|focus|anxiety|insomnia|weight|life|setup|desk|feed|bills?|savings?|income)|changed my|"
                    r"since i (?:started|switched|began|got)|every day since|"
                    r"every\s+(?:single\s+)?(?:day|morning|night|week)|for\s+(?:\d+|a few|two|three|four|several|six|"
                    r"months|weeks|years)\s*(?:days?|weeks?|months?|years?)?|for months|for years|"
                    r"i\s+(?:made|earned|saved|lost|gained|got paid|noticed)|helped me|saved me|works for me|"
                    r"cured my|fixed my|cleared (?:up )?my|use (?:this|it) (?:daily|every)|day \d+ of|"
                    r"been on (?:this|it)|we (?:use|love|swear by|tried)|obsessed|only \w*\s*(?:app|product|one|thing)?"
                    r"\s*i (?:trust|use)|lost \d+\s*(?:pounds|lbs|kg|kilos))\b")
FIRST_PERSON = r"\b(?:i|i'm|i've|i'd|i'll|im|ive|my|me|mine|myself)\b"
# First person that makes no claim ("let me show you", "watch me"), left out of the fail-closed check.
_BENIGN_FIRST = (r"\b(?:let me|watch me|show me|follow me|join me|with me|i'?m (?:going to|gonna) (?:show|tell|try)|"
                 r"i'?ll show|i want to show|here'?s (?:how|what) i)\b")


def _norm_quotes(text):
    return (text or "").replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')


def experience_hint(text):
    """The words that make a line about the speaker's own use or result, or None. "Every day" or "for
    three weeks" count only next to "I", "my" or "me": "it shows a new photo every day" is about the
    product, "I open it every day" is about the creator."""
    low = _norm_quotes(text).lower()
    for m in re.finditer(EXPERIENCE_HINTS, low):
        w = m.group(0)
        if w.startswith(("every", "for ")) and not re.search(FIRST_PERSON, low):
            continue
        return w
    return None


def first_person_claim(text):
    """First person that isn't just "let me show you": a line that talks about the speaker."""
    low = re.sub(_BENIGN_FIRST, " ", _norm_quotes(text).lower())
    m = re.search(r"\b(?:i|i've|i'd|im|ive|my|mine|myself|me)\b", low)
    return m.group(0) if m else None


# Words that make a line a claim about the product (checked against the brief's talking points).
CLAIM_HINTS = (r"\d|%|\b(?:best|fastest|cheapest|easiest|only|first|#1|number one|guarantee\w*|proven|clinically|free|"
               r"save[sd]?|faster|better|cheaper|more than|less than|cure[sd]?|heals?|results?|works?|never|always|"
               r"instantly|risk[- ]free|safe|unlimited|every|all your|no ads|award\w*|doctors?|dermatologists?|experts?|"
               r"recommend\w*|approved|certified|in (?:a|one|\d+) (?:day|week|month)s?|overnight|deeper|cleared?)\b")
# Absolute claims nobody can stand behind without the advertiser's proof, word for word in the brief.
ABSOLUTE_CLAIMS = (r"(?:\b(?:guarantee\w*|100\s?%|risk[- ]free|cure[sd]?|miracle|instant(?:ly)?\s+(?:results?|rich)|"
                   r"never fails?|no risk|get rich|clinically (?:proven|tested)|number one|(?:dermatologist|doctor)s?[- ]"
                   r"(?:approved|recommended|tested))\b|(?<![\w#])#1\b)")
# Earnings: any money figure or a promise of income. Allowed only with the brand's typical-earnings line.
EARNINGS_CLAIM = (r"(?:[$\u20ac\u00a3]\s?\d|\b\d[\d,.]*\s*(?:k\s*)?(?:dollars|bucks|euros?|quid)\b|"
                  r"\b(?:i|we)\s+(?:made|make|earned|earn|got paid|get paid)\b|"
                  r"\byou\s+(?:can|could|will|'ll|would)\s+(?:easily\s+)?(?:make|earn|get paid)\b|"
                  r"\bearn\s+up\s+to\b|\bpays?\s+(?:me|you)\s+\$)")
# Get-rich-quick framing: TikTok bans it in branded content, and it misleads under the FTC's rules on
# earnings claims. Never written into a script, a hook or a caption.
GET_RICH_QUICK = [r"\b(?:quick|easy|fast|free|instant)\s+(?:money|cash|income)\b", r"\bpassive income\b",
                  r"\bget rich\b", r"\bfinancial freedom\b", r"\bquit (?:your|my) (?:9|nine|day )",
                  r"\bin (?:just )?\d+\s*(?:minutes?|mins?) a day\b", r"\bwithout (?:any )?(?:work|effort)\b",
                  r"\bmoney while (?:you|i) sleep\b", r"\b(?:6|six|7|seven)[- ]figures?\b"]


def norm_text(text):
    """Text for matching banned phrases: NFKC, straight quotes, hyphens and slashes as spaces, lower case.
    "FREE-forever" and "won\u2019t" match "free forever" and "won't"."""
    import unicodedata
    t = unicodedata.normalize("NFKC", _norm_quotes(text))
    t = re.sub(r"[\-\u2010\u2011\u2012\u2013\u2014\u2015_/]", " ", t)
    return t.lower()


def phrase_words(text):
    """The words of a text for phrase matching, keeping a leading # ("#1" stays "#1", so "Day 1" is
    not "#1")."""
    return re.findall(r"#?[a-z0-9']+|#?[^\W\d_][\w']*", norm_text(text))


def has_banned(text, phrase):
    """A banned phrase's words in order in the text, case, quotes, hyphens and punctuation aside. One
    matcher for the script, the captions and what was said on camera."""
    want = phrase_words(phrase)
    if not want:
        return False
    hay = phrase_words(text)
    n = len(want)
    return any(hay[i:i + n] == want for i in range(len(hay) - n + 1))


# Words that plainly say a video is paid, in a sentence that is about this video: "this is an ad", "#ad",
# "Ad, but ...", "sponsored by <brand>", "paid partnership with", "<brand> is paying me". Incidental words
# never count: "ad" inside other words, "I saw an ad", "the pub", "my sponsor at the gym", "paid by card",
# "apps sponsored by big brands". Common EU and Latin American wordings too.
_AD_WORD = (r"(?:ad|advert|advertisement|anzeige|werbung|reclame|advertentie|publicidad|publicidade|publicit[eé]|"
            r"pubblicit[aà]|reklama|reklame|annonse|annons|mainos)")
_DISC_STRONG = (
    r"(?<![\w#])#(?:ad|ads|advert|anzeige|werbung|reclame|publi|publicidad|publicidade|pub|sponsored|paidpartnership|"
    r"werbepartnerschaft)\b"
    r"|\b(?:this|it|that|the video|this video|the post|this post|today'?s video)(?:'s|\s+is|\s+was)\s+(?:an?\s+|a\s+paid\s+)?"
    r"(?:" + _AD_WORD + r"|sponsored|paid\s+(?:ad|post|partnership|promotion))(?![\w-])"
    r"|^\W*(?:" + _AD_WORD + r"|publi|sponsored)\s*(?:[:,.!\u2013-]|$)"
    r"|^\W*(?:" + _AD_WORD + r"|sponsored)\s+(?:for|with|by|from)\b"
    r"|\b(?:this(?:\s+video|\s+post)?|it|video|post)(?:'s|\s+is|\s+was)?\s+sponsored\s+by\b|^\W*sponsored\s+by\b"
    r"|\b(?:is|are|'s)\s+sponsoring\s+(?:this|today'?s|the)\s+(?:video|post)\b"
    r"|\bpaid\s+(?:partnership|promotion|post|collab\w*|ad|advert\w*)\b"
    r"|\b(?:is|are|'s|was)\s+paying\s+(?:me|us)\b|\bpaid\s+(?:me|us)\s+to\b"
    r"|\b(?:i'?m|i am|we'?re|we are)\s+(?:being\s+)?paid\s+(?:to|for|by)\b"
    r"|\bpatrocinad[oa]s?\b|\bgesponsert\b|\bgesponsord\b|\bsponsoris[eé]e?s?\b|\bsponsorizzat[oa]\b"
    r"|\bbezahlte\s+partnerschaft\b|\bcolaboraci[oó]n\s+pagada\b|\bparceria\s+paga\b"
    r"|\bpartenariat\s+r[eé]mun[eé]r[eé]\b|\bwerbepartnerschaft\b"
    r"|\b(?:esto es|isto [eé]|c'est|das ist|dit is|questo [eè])\s+(?:una?\s+|eine?\s+|een\s+|de la\s+)?"
    r"(?:publicidad|publicidade|publicit[eé]|pub|werbung|anzeige|reclame|advertentie|pubblicit[aà])\b")
# A label on screen or in a caption may be the word alone: "Ad", "Sponsored", "Paid partnership", "Werbung".
_LABEL = (r"^\W*#?(?:" + _AD_WORD + r"|ads|sponsored|publi|paid\s+partnership|paid\s+promotion|bezahlte\s+partnerschaft|"
          r"werbepartnerschaft|patrocinado|gesponsert|gesponsord|sponsoris[eé]|sponsorizzato)(?![\w-])")
NEGATIONS = ("not", "no", "non", "never", "isn", "isnt", "nt", "isn't", "aren't", "wasn't", "nicht", "kein", "keine",
             "geen", "pas", "nao", "não", "nobody", "zero", "none", "nothing", "without", "hardly")
# Words just before an ad word that make it someone else's ad: "I saw an ad", "the ad on my lock screen".
_INCIDENTAL = ("saw", "seen", "see", "watch", "watched", "hate", "hated", "skip", "skipped", "remember", "another",
               "every", "block", "blocked", "blocker", "annoying", "those", "these", "their", "your", "my", "on")


def denies_ad(text):
    """The sentence says, or implies, that a paid video isn't paid: "not an ad", "nobody is paying me",
    "I'd post this anyway", "even if they didn't pay me"."""
    return bool(find_phrases(text, DENY_AD))


def says_paid(text, brand=None, label=False):
    """True when the text plainly says this video is paid. A sentence that also denies it never counts.
    label=True: an on-screen label or caption tag, where "Ad" or "Sponsored" alone is enough."""
    low = _norm_quotes(text).lower().strip()
    if not low or denies_ad(low):
        return False
    if label and re.search(_LABEL, low):
        return True
    pats = [_DISC_STRONG]
    if brand:
        b = re.escape(str(brand).lower())
        pats.append(r"\b(?:in\s+)?(?:paid\s+)?partner(?:ship|ed)?\s+with\s+" + b)
        pats.append(r"\b(?:an?\s+)?" + _AD_WORD + r"\s+(?:for|with|from|by)\s+" + b)
        pats.append(r"\b(?:sponsored|paid)\s+by\s+(?:the\s+)?" + b)
        pats.append(b + r"\s+(?:is|are)\s+(?:sponsoring|paying\s+for)\s+(?:this|today)")
    for pat in pats:
        for m in re.finditer(pat, low):
            before = re.findall(r"[\w']+", low[:m.start()])[-3:]
            if any(w in NEGATIONS or w.endswith("n't") for w in before):
                continue
            if not m.group(0).lstrip().startswith("#") and any(w in _INCIDENTAL for w in before[-2:]):
                continue
            return True
    return False


def split_sentences(words, gap=0.6):
    """Timed words ({"w", "start", "end"}) as sentences: [{"text", "start", "end"}], broken at . ? ! and
    at pauses, so a check sees the whole sentence a word sits in ("this is not an ad")."""
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        if nxt is None or str(w.get("w", ""))[-1:] in ".?!" or nxt["start"] - w["end"] > gap:
            out.append({"text": " ".join(str(x["w"]) for x in cur), "start": round(cur[0]["start"], 2),
                        "end": round(cur[-1]["end"], 2)})
            cur = []
    return out


def disclosing_part(text, brand=None):
    """The words of a disclosure line up to the end of the sentence that discloses ("Example Orbit is paying
    me to show you this." of a longer line), or None when the line never says it is paid."""
    said = ""
    for part in re.split(r"(?<=[.?!:])\s+", (text or "").strip()):
        before = said
        said = (said + " " + part).strip()
        if says_paid(part, brand) or says_paid(said, brand):
            # the disclosure is complete at the clause that says it ("Ad," of "Ad, but this could be
            # your lock screen"), as long as the whole sentence says it too
            words = part.split()
            for i in range(1, len(words)):
                pre = " ".join(words[:i])
                if says_paid(pre, brand) and words[i - 1][-1:] in ",;:":
                    return (before + " " + pre).strip()
            return said
    return None


def disclosure_targets(lines, hooks=(), brand=None):
    """What the video must say to disclose: the disclosing part of each script line of kind "disclosure",
    and any opening hook that discloses ("Ad, but this could be your lock screen")."""
    out = []
    for t in list(lines) + list(hooks):
        part = disclosing_part(t, brand) if isinstance(t, str) else None
        if part and part not in out:
            out.append(part)
    return out


def find_disclosure(sentences, targets, brand=None, match=0.7):
    """Where the script's own disclosure is said: the first run of 1 to 3 spoken sentences that holds 70% of a
    target's words and plainly says it is paid. {"start", "end", "text"} (end: the end of the sentence that
    completes the disclosure), or None. Incidental words ("I saw an ad", "the pub") never count, because the
    sentence must be the script's disclosure line, and a sentence that denies the ad never counts."""
    sents = [x for x in sentences or [] if isinstance(x, dict) and isinstance(x.get("text"), str)]
    for i in range(len(sents)):
        if denies_ad(sents[i]["text"]):
            continue
        for j in range(i, min(i + 3, len(sents))):
            if denies_ad(sents[j]["text"]):
                break
            text = " ".join(x["text"] for x in sents[i:j + 1])
            if not says_paid(text, brand):
                continue
            if any(overlap(t, text) >= match for t in targets):
                return {"start": sents[i]["start"], "end": sents[j]["end"], "text": text}
    return None


def spoken_disclosure_at(sentences, brand=None, targets=None):
    """The end of the spoken disclosure (seconds), or None. With targets (the script's disclosure line and
    any disclosing hook), only the script's own disclosure counts."""
    if targets is not None:
        f = find_disclosure(sentences, targets, brand)
        return f["end"] if f else None
    for x in sentences:
        if says_paid(x["text"], brand):
            return x["end"]
    return None


def strip_known(text, *known):
    """The text with known safe phrases taken out (the brand name, the brief's own call to action,
    the brand's typical-earnings line), so "link in bio" or "free" from the brief's own words don't
    read as the creator's claim."""
    out = _norm_quotes(text)
    for k in sorted((str(x) for x in known if isinstance(x, str) and x.strip()), key=len, reverse=True):
        out = re.sub(re.escape(_norm_quotes(k).strip().rstrip(".")), " ", out, flags=re.I)
    return out


def overlap(a, b):
    """Share of a's content words that are in b (0 to 1)."""
    wa = content_words(a)
    return len(wa & content_words(b)) / max(1, len(wa)) if wa else 1.0


def free_text_problems(text, campaign, confirmed=(), points=(), te_line=None, said=False, claims_only=False, lines=()):
    """What a caption, a title or a sentence said on camera claims that the script's rules don't
    allow: [(level, message)]. The same rules as the script: an experience claim only when it
    matches a confirmed line or hook; absolute claims only in the brief's own talking points;
    earnings claims only with the typical-earnings line; never get-rich-quick framing; never a
    do_not_say phrase; never a line that hides the ad."""
    c = campaign if isinstance(campaign, dict) else {}
    out = []
    for w in ([] if claims_only else c.get("do_not_say") or []):
        if isinstance(w, str) and has_banned(text, w):
            out.append(("error", f"the brief says never to say \"{w}\""))
    for snt, _ in ([] if claims_only else hide_ad_hits(text)):
        out.append(("error", f"\"{snt}\" hides or plays down that it's an ad"))
    for snt, _ in ([] if claims_only else find_phrases(text, ENGAGEMENT_BAIT)):
        out.append(("error", f"\"{snt}\" asks for bought or arranged engagement"))
    known = [c.get("brand"), c.get("cta"), te_line]
    probe = strip_known(text, *known)
    exp = experience_hint(probe)
    if exp and not any(overlap(probe, t) >= 0.6 for t in confirmed):
        out.append(("error", f"\"{exp}\" claims your own use or result" + (" and isn't in a confirmed line or hook"
                    if said else ". Only a line or hook the creator confirmed can say that") + ": cut it" +
                    (" or confirm the line it belongs to" if said else " or reword it")))
    m = re.search(ABSOLUTE_CLAIMS, probe.lower())
    if m and not any(m.group(0) in str(t).lower() for t in points):
        out.append(("error", f"\"{m.group(0)}\" needs proof the advertiser has, and the brief's talking points don't say "
                    "it"))
    g = find_phrases(probe, GET_RICH_QUICK)
    if g:
        out.append(("error", f"\"{g[0][0]}\" is get-rich-quick framing (TikTok bans it in branded content; the FTC "
                    "treats it as deceptive). Say plainly what the product does"))
    if claims_only:
        # a caption or a title: the same claim rules as a script line. A claim about the product needs a
        # talking point or a script line that says it; a claim about you, a line you confirmed
        bare = re.sub(r"(?:#|@)[\w.]+|https?://\S+|\b[\w.-]+\.(?:com|app|io|co)\S*", " ", probe)
        for snt in [x.strip() for x in re.split(r"(?<=[.?!])\s+|\n+", bare) if x.strip()]:
            if experience_hint(snt) and exp:
                continue   # already reported above
            fp = first_person_claim(snt) or (re.search(r"\b(?:we|we've|we're|our|us)\b", snt.lower()) or [None])[0]
            if fp and len(content_words(snt)) >= 1 and not any(overlap(snt, t) >= 0.6 for t in confirmed):
                out.append(("error", f"\"{snt}\" talks about you (\"{fp}\"). Only a line or hook the creator "
                            "confirmed can say that: reword it or confirm the line it belongs to"))
                continue
            if not re.search(CLAIM_HINTS, snt.lower()):
                continue
            backing = [str(t) for t in list(points) + list(lines) + list(confirmed) if t]
            union = " ".join(backing).lower()
            uw = set(words_of(union))
            lost = [m.group(0) for m in re.finditer(CLAIM_HINTS, snt.lower())
                    if not (m.group(0)[:1].isdigit() or m.group(0) in "%") and m.group(0) not in uw
                    and m.group(0) not in union]
            lost += [n for n in re.findall(r"\d+%?", snt) if n not in re.findall(r"\d+%?", union)]
            cw = content_words(snt)
            cover = len(cw & {w for w in uw if len(w) > 2}) / len(cw) if cw else 1.0
            if lost or cover < 0.6:
                what = lost[0] if lost else re.search(CLAIM_HINTS, snt.lower()).group(0)
                out.append(("error", f"\"{snt}\" makes a claim (\"{what}\") that no talking point or script line "
                            "says. Use the brief's own words or leave it out"))
    e = re.search(EARNINGS_CLAIM, probe.lower())
    if e:
        if not te_line:
            out.append(("error", f"\"{e.group(0).strip()}\" is an earnings claim, and the brand gave no typical-earnings "
                        "line. Leave money figures and income claims out"))
        elif not (te_line and overlap(te_line, text) >= 0.8) and not said:
            out.append(("warning", f"\"{e.group(0).strip()}\" is an earnings claim: the video must also say the "
                        f"typical-earnings line (\"{te_line}\")"))
    return out


NEGATION = r"n't\b|\b(?:not|never|no|nobody|nothing|none|without|cannot|neither|nor)\b"
FILLER_WORDS = {"okay", "yeah", "anyway", "alright", "right", "like", "literally", "honestly", "guys", "basically",
                "actually", "really", "well", "hey", "yes", "know", "mean", "thing", "stuff", "kind", "sort", "gonna"}


def negated(text):
    return bool(re.search(NEGATION, _norm_quotes(text or "").lower()))


def script_match(text, lines):
    """How closely one sentence matches the script: (share of its words, the best line). Compared with
    each line and each pair of neighbouring lines (a sentence can run over two), never with the whole
    script at once, so words picked from different lines don't add up to a match."""
    cw = content_words(text) - FILLER_WORDS
    if not cw:
        return 1.0, None
    cands = list(lines) + [a + " " + b for a, b in zip(lines, lines[1:])]
    best, best_line = 0.0, None
    for ln in cands:
        sc = len(cw & content_words(ln)) / len(cw)
        if sc > best:
            best, best_line = sc, ln
    return best, best_line


def text_sha(*parts):
    """A fingerprint of some text (a script line, a caption): a confirmation or a yes given for one
    wording is void when the wording changes."""
    h = hashlib.sha256()
    for p in parts:
        h.update(json.dumps(p, sort_keys=True, ensure_ascii=False).encode("utf-8", "surrogatepass"))
        h.update(b"\0")
    return h.hexdigest()


def words_of(text):
    return re.findall(r"[a-z0-9']+", (text or "").lower())


STOP = {"a", "an", "the", "of", "to", "for", "and", "that", "with", "on", "in", "is", "it", "its", "it's", "so", "but",
        "i", "or", "at", "as", "if", "by", "from", "my", "your", "our", "you", "we", "this", "be", "are", "was", "can",
        "just", "all", "me", "they", "their", "them", "do", "does", "has", "have", "will", "get", "into", "up", "out"}


def content_words(text):
    return {w for w in words_of(text) if w not in STOP and len(w) > 2}

_reading = [None]   # the file being read, for the last-resort message in guard()


def reading(path):
    _reading[0] = path


def die(msg):
    raise SystemExit("error: " + msg)


def guard(main):
    """Run a script's main(): any unexpected error becomes one clear line, not a traceback.
    Set UGC_DEBUG=1 to see the traceback."""
    try:
        main()
    except SystemExit:
        raise
    except KeyboardInterrupt:
        sys.exit("stopped. Run the same command again when you are ready")
    except Exception as e:
        if os.environ.get("UGC_DEBUG"):
            raise
        if isinstance(e, UnicodeEncodeError):
            sys.exit("error: a text holds half an emoji or a broken character (a cut-off copy). Retype that text")
        if isinstance(e, OSError):
            name = rel(str(e.filename)) if e.filename else "a file"
            sys.exit(f"error: can't read or write {name}: {e.strerror or e}. Check that it exists, that you "
                     "may write to that folder, and that no file there has the name of a folder this needs")
        where = (rel(str(_reading[0])) if _reading[0] else
                 "one of the files you gave (campaign.json, script.json, edit.json, job.json or a saved reply)")
        sys.exit(f"error: {where} has a value of the wrong kind somewhere (text where a number belongs, a list "
                 f"where one value belongs, or the reverse): {type(e).__name__}: {e}. "
                 "Set UGC_DEBUG=1 for details.")


def read_json(path, what=None):
    reading(path)
    try:
        with open(path, encoding="utf-8-sig") as fh:
            data = json.load(fh)
        reading(None)   # read cleanly: a later wrong value is not this file's fault
        return data
    except FileNotFoundError:
        die(f"{path} not found" + (f" ({what})" if what else ""))
    except IsADirectoryError:
        die(f"{path} is a folder, not a JSON file")
    except UnicodeDecodeError:
        die(f"{path} is not UTF-8 text (is it a JSON file?)")
    except json.JSONDecodeError as e:
        die(f"{path} is not valid JSON (line {e.lineno}, column {e.colno}): {e.msg}")
    except RecursionError:
        die(f"{path} has brackets nested far too deep to be one of this skill's files")


def write_json(path, data):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp = path + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=1)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def write_text(path, text):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def rel(path, start=None):
    try:
        r = os.path.relpath(path, start or os.getcwd())
    except ValueError:  # another drive on Windows
        return path.replace(os.sep, "/")
    if r.startswith(os.pardir + os.sep + os.pardir + os.sep):
        return os.path.abspath(path).replace(os.sep, "/")
    return r.replace(os.sep, "/")


def _mark(ch):
    return unicodedata.category(ch).startswith("M")


def slug(text):
    """A safe file name from any text: letters and digits of every script, lowercase, the rest
    becomes one dash."""
    out = []
    for ch in unicodedata.normalize("NFC", str(text)).lower():
        if ch.isalnum() or (out and out[-1] != "-" and _mark(ch)):
            out.append(ch)
        elif out and out[-1] != "-":
            out.append("-")
    s = "".join(out)[:80].strip("-")
    if not s:
        s = "x" + hashlib.sha1(str(text).encode("utf-8", "surrogatepass")).hexdigest()[:8]
    if s in WINDOWS_RESERVED:
        s += "-1"
    return s


def valid_id(text):
    """An id: lowercase letters and digits, single dashes between them, 80 at most."""
    return isinstance(text, str) and unicodedata.normalize("NFC", text) == slug(text)


@functools.lru_cache(maxsize=None)
def _sha256_cached(path, size, mtime):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def sha256(path):
    """The file's fingerprint: two files with the same one are the same edit, whatever their names."""
    st = os.stat(path)
    return _sha256_cached(os.path.abspath(path), st.st_size, st.st_mtime)


def need_ffmpeg():
    import shutil
    if not (shutil.which("ffmpeg") and shutil.which("ffprobe")):
        die("ffmpeg not found. Mac: brew install ffmpeg. Windows: winget install Gyan.FFmpeg (then open a "
            "new terminal). Linux: sudo apt install ffmpeg")


@functools.lru_cache(maxsize=None)
def ffmpeg_has(kind, name):
    """Whether this ffmpeg build has an encoder or filter."""
    r = subprocess.run(["ffmpeg", "-hide_banner", f"-{kind}"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return bool(re.search(rf"\s{re.escape(name)}\s", r.stdout))


def moov_first(path):
    """True when the MP4's index (moov) sits before the video data (mdat), which Instagram needs.
    None when the file isn't an MP4/MOV this can read."""
    try:
        with open(path, "rb") as fh:
            size = os.path.getsize(path)
            pos = 0
            while pos + 8 <= size:
                fh.seek(pos)
                head = fh.read(16)
                n = int.from_bytes(head[:4], "big")
                kind = head[4:8]
                if n == 1 and len(head) == 16:
                    n = int.from_bytes(head[8:16], "big")
                elif n == 0:
                    n = size - pos
                if kind == b"moov":
                    return True
                if kind == b"mdat":
                    return False
                if n < 8 or not kind.strip(b"\0").isalnum():
                    return None
                pos += n
    except OSError:
        return None
    return None


def probe(path, label=None):
    """Width and height as displayed (after rotation), fps, duration, codecs, colour, sound, size."""
    name = label or path
    if not os.path.exists(path):
        die(f"{name} not found")
    if os.path.isdir(path):
        die(f"{name} is a folder; give one video file")
    if not os.path.getsize(path):
        die(f"{name} is an empty file (0 bytes)")
    need_ffmpeg()
    r = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        d = json.loads(r.stdout or "{}")
    except json.JSONDecodeError:
        d = {}
    if not isinstance(d, dict):
        d = {}
    streams = d.get("streams") or []
    vs = [s for s in streams if s.get("codec_type") == "video" and not (s.get("disposition") or {}).get("attached_pic")]
    aus = [s for s in streams if s.get("codec_type") == "audio"]
    fmt = (d.get("format") or {}).get("format_name", "")
    if vs and (fmt == "image2" or fmt.endswith("_pipe")):
        die(f"{name} is an image, not a video")
    if not vs:
        die(f"{name}: no video in this file (is it a video?)")
    v = vs[0]
    w, h = int(v.get("width") or 0), int(v.get("height") or 0)
    if not w or not h:
        die(f"{name}: no video in this file (is it a video?)")
    rot = 0
    for sd in v.get("side_data_list") or []:
        if "rotation" in sd:
            try:
                rot = int(float(sd["rotation"]))
            except (TypeError, ValueError):
                pass
    try:
        rot = int(float((v.get("tags") or {}).get("rotate", rot)))
    except (TypeError, ValueError):
        pass
    if rot % 180:
        w, h = h, w

    def rate(txt):
        try:
            n, dd = (txt or "0/1").split("/")
            return float(n) / float(dd) if float(dd) else 0.0
        except (ValueError, ZeroDivisionError):
            return 0.0
    fps = rate(v.get("avg_frame_rate")) or rate(v.get("r_frame_rate"))
    if fps > 1000:
        fps = 0.0
    dur = 0.0
    for src in ((d.get("format") or {}).get("duration"), v.get("duration")):
        try:
            dur = float(src)
            break
        except (TypeError, ValueError):
            continue
    a = aus[0] if aus else {}
    try:
        a_rate = int(a.get("sample_rate") or 0)
    except ValueError:
        a_rate = 0
    try:
        channels = int(a.get("channels") or 0)
    except (TypeError, ValueError):
        channels = 0
    size = os.path.getsize(path)
    return {"width": w, "height": h, "fps": round(fps, 3), "duration": round(max(dur, 0.0), 3),
            "rate": v.get("r_frame_rate") or "30/1", "vcodec": v.get("codec_name"), "pix_fmt": v.get("pix_fmt"), "transfer": v.get("color_transfer"),
            "acodec": a.get("codec_name"), "audio": bool(aus), "audio_rate": a_rate, "channels": channels,
            "bytes": size, "mbps": round(size * 8 / dur / 1e6, 2) if dur else 0.0,
            "mp4": any(x in fmt for x in ("mp4", "mov")), "moov_first": moov_first(path)}


def size_text(n):
    return f"{n / GB:g} GB" if n >= GB and n % GB == 0 else f"{n / MB:.1f} MB"


def file_issues(info, platform, tiktok_max_s=None):
    """Problems one platform has with this file: a list of (level, message)."""
    L = LIMITS[platform]
    name = L["label"]
    out = []
    s, w, h = info["duration"], info["width"], info["height"]
    max_s = float(tiktok_max_s) if platform == "TIKTOK" and tiktok_max_s else L["max_s"]
    if not s:
        out.append(("error", "can't read this file's length; export it again as MP4"))
    elif s < L["min_s"]:
        out.append(("error", f"{s:.1f} s is shorter than the {name} minimum of {L['min_s']} s"))
    if platform == "YOUTUBE":
        if s > max_s or w > h:
            why = f"{s:.0f} s is over 3 minutes" if s > max_s else f"{w}x{h} is wider than it is tall"
            out.append(("error", f"{why}, so YouTube would publish it as a normal video, not a Short"))
    elif s > max_s:
        out.append(("error", f"{s:.0f} s is over the {name} limit of {max_s:.0f} s"))
    if info["bytes"] > L["bytes"]:
        out.append(("error", f"{size_text(info['bytes'])} is over the {name} limit of {size_text(L['bytes'])}"))
    fps = L.get("fps")
    if fps and info["fps"] and not fps[0] - 0.1 <= info["fps"] <= fps[1] + 0.5:
        out.append(("error", f"{info['fps']:g} frames a second; {name} accepts {fps[0]} to {fps[1]}"))
    if L.get("max_width") and w > L["max_width"]:
        out.append(("error", f"{w} px wide; {name} accepts up to {L['max_width']} px"))
    if L.get("max_side") and max(w, h) > L["max_side"]:
        out.append(("error", f"{w}x{h}; {name} accepts up to {L['max_side']} px per side"))
    if L.get("min_side") and min(w, h) < L["min_side"]:
        out.append(("error", f"{w}x{h}; {name} needs at least {L['min_side']} px per side"))
    if info["vcodec"] != "h264" and not (info["vcodec"] == "hevc" and not L.get("strict")):
        out.append(("error" if L.get("strict") else "warning",
                    f"video codec is {info['vcodec']}; H.264 is the one every platform takes"))
    if info["pix_fmt"] and not info["pix_fmt"].startswith(("yuv420p", "yuvj420p")):
        out.append(("error" if L.get("strict") else "warning", f"pixel format {info['pix_fmt']}; platforms expect yuv420p"))
    if info["transfer"] in HDR_TRANSFER:
        out.append(("error" if L.get("strict") else "warning", "HDR video; it can be rejected or look washed out"))
    if L.get("strict"):
        if not info["mp4"]:
            out.append(("error", f"{name} takes MP4 or MOV files only"))
        elif info["moov_first"] is False:
            out.append(("error", f"the file's index is at the end; {name} needs it at the start (\"fast start\")"))
        if info["audio"] and info["acodec"] != "aac":
            out.append(("error", f"audio codec is {info['acodec']}; {name} needs AAC"))
        if info["audio_rate"] > 48000:
            out.append(("error", f"audio is {info['audio_rate']} Hz; {name} accepts up to 48,000 Hz"))
        if info["mbps"] > 25:
            out.append(("error", f"{info['mbps']:g} Mbps; {name} accepts up to 25 Mbps"))
    if not info["audio"]:
        out.append(("warning", "no sound track"))
    return out


# ---- text: hashtags, handles, links and each platform's way of counting

URL_RE = re.compile(r"(?i:https?://|www\.)\S+"
                    r"|(?<![@\w.-])[A-Za-z0-9-]+\.(?:com|net|org|io|co|app|ai|dev|shop|store|me|ly|gg|tv)(?![A-Za-z0-9])(?:/\S*)?")


def hashtags(text):
    """Hashtags as the platforms read them: a # followed by letters or digits with at least one letter."""
    return [h for h in re.findall(r"(?<![\w&])#\w+", text or "") if any(c.isalpha() for c in h)]


def mentions(text):
    return re.findall(r"(?<![\w@.])@[A-Za-z0-9_](?:[A-Za-z0-9_.]*[A-Za-z0-9_])?", text or "")


def links(text):
    return [m.group(0).rstrip(".,;:!?)]}\"'") for m in URL_RE.finditer(text or "")]


def norm_link(u):
    """A link without scheme, www, case and trailing slash, so example.com/x and https://www.example.com/x/ match."""
    u = re.sub(r"(?i)^https?://", "", (u or "").strip())
    u = re.sub(r"(?i)^www\.", "", u)
    return u.rstrip("/").lower()


# Share-menu links carry tracking parameters (?igsh=, ?si=, ?is_from_webapp=1&sender_device=pc, utm_...).
TRACKING = re.compile(r"^(?:utm_\w*|igsh|igshid|si|is_from_webapp|sender_device|sender_web_id|_t|_r|_d|feature|"
                      r"share_\w*|ref|refer|referrer|source|web_id|tt_from|u_code|preview_pb|checksum|sec_uid|"
                      r"lang|embed_source|fbclid|gclid|mibextid|rdid|img_index|pp|app|t)$", re.I)


def post_key(url):
    """One key per post, whatever link the app's share menu gave: "TIKTOK:<video id>",
    "INSTAGRAM:<shortcode>", "YOUTUBE:<video id>", or for other links the host and path without
    tracking parameters. Ids keep their case (they are case-sensitive). A TikTok short link
    (vm.tiktok.com, /t/) gives "TIKTOK-SHORT:<code>": it can't be matched to a post, so ask for the
    full link."""
    import urllib.parse
    u = (url or "").strip()
    if not u:
        return ""
    if not re.match(r"(?i)^[a-z]+://", u):
        u = "https://" + u
    try:
        p = urllib.parse.urlsplit(u)
    except ValueError:
        return "URL:" + u
    host = (p.hostname or "").lower()
    bare = re.sub(r"^(?:www|m|mobile|web)\.", "", host)
    path = re.sub(r"/{2,}", "/", p.path or "/")
    if bare.endswith("tiktok.com"):
        if bare.startswith(("vm.", "vt.")) or path.startswith("/t/"):
            return "TIKTOK-SHORT:" + path.strip("/").split("/")[-1]
        m = re.search(r"/(?:video|photo|v)/([A-Za-z0-9_-]+)", path)
        if m:
            return "TIKTOK:" + m.group(1)
    if bare.endswith("instagram.com"):
        m = re.search(r"/(?:reels?|p|tv)/([A-Za-z0-9_-]+)", path)
        if m:
            return "INSTAGRAM:" + m.group(1)
    if bare == "youtu.be":
        vid = path.strip("/").split("/")[0]
        if vid:
            return "YOUTUBE:" + vid
    if bare.endswith("youtube.com"):
        m = re.search(r"/(?:shorts|live|embed|v)/([A-Za-z0-9_-]+)", path)
        if m:
            return "YOUTUBE:" + m.group(1)
        q = urllib.parse.parse_qs(p.query)
        if q.get("v"):
            return "YOUTUBE:" + q["v"][0]
    kept = [(k, v) for k, v in urllib.parse.parse_qsl(p.query, keep_blank_values=True) if not TRACKING.match(k)]
    tail = ("?" + urllib.parse.urlencode(sorted(kept))) if kept else ""
    return "URL:" + bare + path.rstrip("/") + tail


def short_link(url):
    """True for a share link that hides the post id (vm.tiktok.com/..., tiktok.com/t/...)."""
    return post_key(url).startswith("TIKTOK-SHORT:")


def text_length(platform, text):
    """Length the way this platform counts it."""
    text = text or ""
    if platform == "YOUTUBE":
        return len(text.encode("utf-8", "surrogatepass"))
    if platform == "TIKTOK":   # UTF-16 units: most emoji count 2
        return len(text.encode("utf-16-le", "surrogatepass")) // 2
    return len(text)


def find_phrases(text, patterns):
    """Every match of these patterns in a text: (the sentence it is in, the words that matched)."""
    hits = []
    flat = re.sub(r"[‘’]", "'", text or "")
    for pat in patterns:
        for m in re.finditer(pat, flat, flags=re.I):
            start = max(flat.rfind(".", 0, m.start()), flat.rfind("\n", 0, m.start())) + 1
            ends = [i for i in (flat.find(".", m.end()), flat.find("\n", m.end())) if i != -1]
            end = min(ends) + 1 if ends else len(flat)
            sentence = " ".join(flat[start:end].split()).lstrip("-*•> ").strip()
            if sentence not in (h[0] for h in hits):   # one line per sentence, however many patterns match it
                hits.append((sentence, m.group(0)))
    return hits


def hide_ad_hits(text, brief=False, skip=()):
    """Sentences that forbid, drop, hide or move the disclosure itself, or say a paid video isn't one. A
    sentence saying a video without the disclosure is rejected asks for the disclosure, so it isn't one.
    In a brief, the caption wording ("not an ad") counts only when the brief tells the creator to say it:
    "make it look like a regular post, not an ad" is a tone note, "say it's not an ad" is hiding."""
    if not brief:
        return [(s, m) for s, m in find_phrases(text, HIDE_AD) if not requires_disclosure(s)]
    hits = [(s, m) for s, m in find_phrases(text, HIDE_AD_CORE) if s not in skip and not requires_disclosure(s)]
    seen = {s for s, _ in hits}
    for s, m in find_phrases(text, DENY_AD):
        if s not in seen and s not in skip and re.search(_INSTRUCT, s, re.I) and not requires_disclosure(s) and \
                not find_phrases(s, TONE_AD):
            hits.append((s, m))
    return hits


def tone_hits(text, brief=True, skip=()):
    """Sentences about how the video should feel ("keep it natural, it shouldn't feel like an ad"):
    style direction, not a disclosure ban. Shown as tone notes; the disclosure stays."""
    pats = TONE_AD + (TONE_AD_BRIEF if brief else [])
    return [(s, m) for s, m in find_phrases(text, pats) if s not in skip and not requires_disclosure(s)]


def requires_disclosure(sentence):
    """True when the sentence names the disclosure as what is required ("Posts without #ad are
    rejected", "#ad is required"), and doesn't also make the disclosure the cause of a rejection."""
    flat = re.sub(r"[‘’]", "'", sentence or "")
    if not any(re.search(p, flat, re.I) for p in DISCLOSE_REQUIRED):
        return False
    return not any(re.search(p, flat, re.I) for p in DISCLOSURE_REJECTED)


def read_yourself(text, already=()):
    """Sentences of a brief that name a disclosure next to a negation or a rejection, and that the
    patterns neither flagged nor read as asking for the disclosure. The agent reads each one itself."""
    flat = re.sub(r"[‘’]", "'", text or "")
    out = []
    for raw in re.split(r"(?<=[.!?])\s+|\n", flat):
        s = " ".join(raw.split()).lstrip("-*•> ").strip()
        if not s or s in already or s in out:
            continue
        probe = re.sub(r"(?i)\b(?:no|zero|without|free of)\s+(?:more\s+)?ads\b|\bads?[- ]free\b|\bad[- ]?block\w*", " ", s)
        if re.search(DISCLOSURE_MENTION, probe, re.I) and re.search(NEGATION_OR_REJECT, probe, re.I) \
                and not requires_disclosure(s):
            out.append(s)
    return out


def asks_for(text, patterns):
    """Sentences that ask for one of these things. One that bans it ("no engagement groups") doesn't."""
    return [(s, m) for s, m in find_phrases(text, patterns) if not re.search(BANS_IT, s, re.I)]


def stamp(t):
    m, s = divmod(float(t), 60)
    return f"{int(m)}:{s:04.1f}"


# ---- time and money

_now_warned = [False]


def now_utc():
    """The clock the scripts use. UGC_NOW (an ISO time) fixes it for examples and tests."""
    fixed = os.environ.get("UGC_NOW")
    if fixed:
        t = parse_time(fixed)
        if t:
            if not _now_warned[0]:
                _now_warned[0] = True
                sys.stderr.write(f"warning: UGC_NOW is set, so the clock reads {iso(t)}, not the real time: deadlines, "
                                 "posting windows and 'yes' expiry all follow it. Unset it (unset UGC_NOW) for real "
                                 "campaigns\n")
            return t
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)


def _iso_clean(text):
    t = re.sub(r"\.\d+", "", text.strip())
    t = re.sub(r"^(\d{4}-\d{2}-\d{2}) (\d)", r"\1T\2", t)
    t = re.sub(r"[Zz]$", "+00:00", t)
    return re.sub(r"([+-]\d{2})(\d{2})$", r"\1:\2", t)   # +0100 -> +01:00 (Python 3.9 needs the colon)


def parse_time(text):
    """A stored ISO 8601 time ("2026-11-15T14:03:00Z" or with an offset; without one, UTC). None if not."""
    if not isinstance(text, str) or not text.strip():
        return None
    try:
        d = datetime.datetime.fromisoformat(_iso_clean(text))
    except ValueError:
        return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=datetime.timezone.utc)
    return d.astimezone(datetime.timezone.utc)


def load_zone(zone):
    """The ZoneInfo for an IANA name, or None when this computer can't load it (Windows needs
    pip install tzdata)."""
    if not zone or not isinstance(zone, str):
        return None
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(zone)
    except Exception:
        return None


def parse_user_time(text, zone=None):
    """A time the user typed: (time in UTC, the zone it was read in when it had no offset, problem).
    A time without an offset is the user's own clock time: read in `zone` (the job's timezone),
    else in this computer's zone. A date alone is refused (it would be midnight)."""
    if not isinstance(text, str) or not text.strip():
        return None, None, "give a time like 2026-11-16T09:05 (your clock) or 2026-11-16T14:05Z (UTC)"
    if re.fullmatch(r"\s*\d{4}-\d{2}-\d{2}\s*", text):
        return None, None, "give the time of day too, like 2026-11-16T09:05; a date alone would be read as midnight"
    try:
        d = datetime.datetime.fromisoformat(_iso_clean(text))
    except ValueError:
        return None, None, "give a time like 2026-11-16T09:05 (your clock) or 2026-11-16T14:05Z (UTC)"
    assumed = None
    if d.tzinfo is None:
        tz = load_zone(zone)
        if tz is not None:
            d, assumed = d.replace(tzinfo=tz), zone
        else:
            d = d.astimezone()   # this computer's own zone
            assumed = "this computer's time zone (" + (d.strftime("%Z") or "local") + ")"
    return d.astimezone(datetime.timezone.utc), assumed, None


def iso(t):
    return t.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def clock(t, zone=None):
    """A time as people read it: 'Mon 16 Nov 09:31 America/New_York (EST)', or in UTC when the zone
    is unknown. The abbreviation tells EDT from EST on the night the clocks go back."""
    tz = load_zone(zone)
    if tz is None:
        return t.astimezone(datetime.timezone.utc).strftime("%a %d %b %H:%M UTC")
    t = t.astimezone(tz)
    abbr = t.strftime("%Z")
    return t.strftime("%a %d %b %H:%M ") + zone + (f" ({abbr})" if abbr and abbr != zone else "")


def money(x, cur="USD"):
    sign = "$" if cur == "USD" else ""
    tail = "" if cur == "USD" else f" {cur}"
    return f"{sign}{x:,.2f}{tail}"


def payout(views, rate_per_1k, min_payout=0.0, cap=None, fee_pct=DEFAULT_FEE_PCT, min_views=0, cur="USD"):
    """(gross, paid after the fee, why) for one video at this many views. Below the campaign's
    minimum nothing is paid; above its cap the cap is paid. The campaign's own count decides."""
    views = max(0, int(views or 0))
    if min_views and views < min_views:
        return 0.0, 0.0, f"under the {min_views:,} view minimum"
    gross = views / 1000.0 * float(rate_per_1k or 0)
    why = ""
    if cap is not None and gross > cap:
        gross, why = float(cap), "capped"
    if min_payout and gross < min_payout:
        return gross, 0.0, f"under the {money(min_payout, cur)} minimum payout"
    return gross, round(gross * (1 - float(fee_pct) / 100.0), 2), why


COUNTRY = {"CA": "Canada", "AU": "Australia", "NZ": "New Zealand", "DE": "Germany", "FR": "France", "ES": "Spain",
           "IT": "Italy", "NL": "the Netherlands", "BR": "Brazil", "MX": "Mexico", "IN": "India", "IE": "Ireland",
           "GB": "the UK", "PH": "the Philippines"}


def place_name(geo):
    """'US' reads as 'the US' in a sentence; a country code becomes its name; a name stays as it is."""
    g = str(geo or "").strip()
    if g.upper() in COUNTRY:
        return COUNTRY[g.upper()]
    return f"the {g}" if g.upper() in ("US", "USA", "UK", "UAE", "NETHERLANDS", "PHILIPPINES") else g


def is_num(v, minimum=None):
    """A real, finite number (not true/false, not Infinity or NaN)."""
    import math
    ok = isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)
    return ok and (minimum is None or v >= minimum)


# Fields a brief often leaves out: null or a wrong value reads as the default (campaign.py reports the
# wrong value as an error), so no script ever does arithmetic with None.
CAMPAIGN_DEFAULTS = {"fee_pct": DEFAULT_FEE_PCT, "window_days": DEFAULT_WINDOW_DAYS, "days_live": DEFAULT_WINDOW_DAYS,
                     "submit_within_minutes": SUBMIT_MINUTES}


def with_defaults(c):
    """A copy of a campaign with every optional field filled in: the defaults above, "window_from"
    ("threshold": views count for window_days from the day the video crosses the payout threshold,
    as most marketplaces count; or "post"), "mode" ("post" or "deliver_files"), "currency" and
    "aspect"."""
    out = dict(c) if isinstance(c, dict) else {}
    for k, v in CAMPAIGN_DEFAULTS.items():
        if not is_num(out.get(k), 0):
            out[k] = v
    if out.get("window_from") not in ("threshold", "post"):
        out["window_from"] = "threshold"
    if out.get("mode") not in ("post", "deliver_files"):
        out["mode"] = "post"
    if not isinstance(out.get("currency"), str) or not out["currency"].strip():
        out["currency"] = "USD"
    if out.get("aspect") not in ("9:16", "any"):
        out["aspect"] = "9:16"
    return out


def terms(c, platform):
    """(rate per 1,000 views, minimum payout, cap per video, view minimum) for one platform: the
    platform's own numbers when the brief sets them per platform, else the campaign's."""
    plat = (c.get("platforms") or {}).get(platform) if isinstance(c.get("platforms"), dict) else None
    plat = plat if isinstance(plat, dict) else {}

    def pick(k):
        v = plat.get(k) if plat.get(k) is not None else c.get(k)
        return v if is_num(v, 0) else None
    rate = plat.get("rate_per_1k") if is_num(plat.get("rate_per_1k"), 0) else 0.0
    return float(rate), float(pick("min_payout") or 0), pick("cap_per_video"), int(pick("min_views") or 0)


def threshold_views(c, platform):
    """Views at which a video starts to pay on this platform (0 when there is no minimum)."""
    rate, mn, _, mv = terms(c, platform)
    need = int(mn / rate * 1000 + 0.999) if mn and rate else 0
    return max(mv, need)


# ---- the user's own files: one ledger and one accounts file for every campaign and folder

def user_home():
    """Where the ledger and the saved accounts live: UGC_CREATOR_HOME, else ~/.ugc-creator (the
    .ugc-creator folder in the user's home folder, on Windows too)."""
    home = os.environ.get("UGC_CREATOR_HOME")
    return os.path.abspath(os.path.expanduser(home)) if home else os.path.join(os.path.expanduser("~"), ".ugc-creator")


def ledger_path(override=None):
    """The one ledger of every post and submission, for every campaign, whatever folder it was made
    in: --ledger, else UGC_CREATOR_LEDGER, else <user_home>/ledger.json. One file is what lets the
    skill refuse an edit or a link already used for another campaign."""
    p = override or os.environ.get("UGC_CREATOR_LEDGER")
    return os.path.abspath(os.path.expanduser(p)) if p else os.path.join(user_home(), "ledger.json")


_LOADED = {}   # ledger path -> fingerprint of the file as it was read, so a save can't drop another session's write


def _file_fp(path):
    try:
        with open(path, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except FileNotFoundError:
        return None


def load_ledger(path=None):
    """ledger.json: {"posts": {"<postId>|<account>": {...}}, "submissions": [{...}], "campaigns":
    {id: the campaign's terms}}. A damaged file is an error and is left exactly as it is: it may be
    the only record of what went out."""
    path = path or ledger_path()
    _LOADED[os.path.abspath(path)] = _file_fp(path)
    if not os.path.exists(path):
        return {"posts": {}, "submissions": [], "campaigns": {}, "hours": [], "pending": {}}
    data = read_json(path, "the ledger")
    if (not isinstance(data, dict) or not isinstance(data.get("posts", {}), dict)
            or not isinstance(data.get("submissions", []), list)
            or not isinstance(data.get("campaigns", {}), dict)
            or not all(isinstance(v, dict) for v in data.get("posts", {}).values())
            or not all(isinstance(v, dict) and isinstance(v.get("url"), str) for v in data.get("submissions", []))):
        die(f"the ledger ({rel(path)}) is damaged: it must hold \"posts\" (one entry per post) and \"submissions\" (a "
            "list). It was left as it is. Repair it, or move it away if nothing in it was really posted")
    data.setdefault("posts", {})
    data.setdefault("submissions", [])
    data.setdefault("campaigns", {})
    if not isinstance(data.get("hours"), list):
        data["hours"] = []
    if not isinstance(data.get("pending"), dict):
        data["pending"] = {}
    reading(None)
    return data


def save_ledger(path, data):
    """Write the ledger under a lock file. When another session (a second agent, another campaign's
    script) wrote it after this one read it, nothing is written: run the command again, it reads the
    new ledger first. That way no post or submission is ever lost."""
    import time
    path = os.path.abspath(path or ledger_path())
    os.makedirs(os.path.dirname(path), exist_ok=True)
    lock = path + ".lock"
    for _ in range(100):
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            break
        except FileExistsError:
            try:
                if time.time() - os.path.getmtime(lock) > 60:   # left behind by a script that was stopped
                    os.remove(lock)
                    continue
            except OSError:
                pass
            time.sleep(0.1)
    else:
        die(f"the ledger ({rel(path)}) is being written by another session. Wait a moment and run this again")
    try:
        if path in _LOADED and _file_fp(path) != _LOADED[path]:
            die(f"the ledger ({rel(path)}) changed while this ran (another session wrote to it). Nothing was written; "
                "run the same command again")
        write_json(path, data)
        _LOADED[path] = _file_fp(path)
    finally:
        try:
            os.remove(lock)
        except OSError:
            pass


def proof_path(lpath=None):
    """The proof log: proof.csv next to the ledger, one file for every campaign (each row names its
    campaign), so earnings and proof never depend on the folder a command runs in."""
    return os.path.join(os.path.dirname(os.path.abspath(lpath or ledger_path())), "proof.csv")


def unwrap_reply(data):
    """A tool reply saved as the MCP envelope ({"content": [{"type": "text", "text": "{...json...}"}]})
    becomes the JSON inside it. Anything else comes back as it was."""
    if isinstance(data, dict) and isinstance(data.get("content"), list) and not data.get("socialAccountPosts"):
        parsed = []
        for part in data["content"]:
            if isinstance(part, dict) and isinstance(part.get("text"), str):
                try:
                    v = json.loads(part["text"])
                except ValueError:
                    continue
                if isinstance(v, (dict, list)):
                    parsed.append(v)
        if len(parsed) == 1:
            return parsed[0]
        if parsed:
            return parsed
    return data


def load_saved_accounts():
    """The accounts the user saved once (<user_home>/accounts.json): {"accounts": [{name, platform,
    handle, the comment/duet/stitch and YouTube choices, audience}]}. [] when none. They are only ever
    shown as suggestions; nothing from this file goes into a post unless the agent writes it into
    job.json after the user confirms it."""
    path = os.path.join(user_home(), "accounts.json")
    if not os.path.exists(path):
        return []
    data = read_json(path, "your saved accounts")
    reading(None)
    accs = data.get("accounts") if isinstance(data, dict) else None
    return [a for a in accs if isinstance(a, dict) and isinstance(a.get("name"), str)] if isinstance(accs, list) else []


def account_key(a):
    """"TIKTOK|example.creator": an account is the same account only when platform and handle both
    match (names like "TikTok" are reused across accounts). None without both."""
    if not isinstance(a, dict):
        return None
    p, h = a.get("platform"), a.get("handle")
    if not (isinstance(p, str) and p.strip() and isinstance(h, str) and h.strip().lstrip("@").strip()):
        return None
    return p.strip().upper() + "|" + h.strip().lstrip("@").strip().casefold()


def placeholder_id(sid):
    s = str(sid).strip().lower()
    return s.startswith("<") or s in ("", "id", "...", "socialaccountid", "todo") or s.startswith(("your", "xxx"))


def post_items(data, depth=0):
    """Every per-post entry in a saved WoopSocial reply (posts_get, social_account_posts_list or
    social_account_posts_list_analytics), wherever the reply nests them: the dicts that carry an
    externalPostUrl or a socialAccountId with a delivery status or metrics."""
    found = []
    if depth > 6:
        return found
    if isinstance(data, list):
        for x in data:
            found += post_items(x, depth + 1)
    elif isinstance(data, dict):
        if isinstance(data.get("externalPostUrl"), str) or (
                isinstance(data.get("socialAccountId"), str) and ("deliveryStatus" in data or "metrics" in data)):
            found.append(data)
        else:
            for v in data.values():
                if isinstance(v, (list, dict)):
                    found += post_items(v, depth + 1)
    return found


# ---------- media fingerprints: a re-export or a new container of the same video ----------

FP_VERSION = 1


def media_fp(path, sha=None):
    """A fingerprint that survives a re-export, a new container or a resize: the loudness of every
    half second ("a") and a 64-bit difference hash of one frame a second ("v"). Cached by the file's
    sha256 under <user_home>/fp-cache. None when ffmpeg can't read the file."""
    import array
    sha = sha or sha256(path)
    cache = os.path.join(user_home(), "fp-cache", f"{sha}.json")
    try:
        with open(cache, encoding="utf-8") as fh:
            fp = json.load(fh)
        if fp.get("version") == FP_VERSION:
            return fp
    except (OSError, ValueError, AttributeError):
        pass
    fp = {"version": FP_VERSION, "a": [], "v": []}
    try:
        r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", "8000", "-f", "s16le", "-"],
                           capture_output=True, timeout=600)
        pcm = array.array("h")
        pcm.frombytes(r.stdout[:len(r.stdout) // 2 * 2])
        if sys.byteorder == "big":
            pcm.byteswap()
        for i in range(0, len(pcm) - 3999, 4000):
            chunk = pcm[i:i + 4000]
            rms = (sum(x * x for x in chunk[::4]) / 1000.0) ** 0.5
            fp["a"].append(int(round(20 * __import__("math").log10(max(rms, 1.0)))))
        r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-an", "-vf", "fps=1,scale=9:8:flags=area,format=gray",
                            "-f", "rawvideo", "-"], capture_output=True, timeout=600)
        raw = r.stdout
        for i in range(0, len(raw) - 71, 72):
            px = raw[i:i + 72]
            bits = 0
            for y in range(8):
                for x in range(8):
                    bits = (bits << 1) | (1 if px[y * 9 + x] > px[y * 9 + x + 1] else 0)
            fp["v"].append(f"{bits:016x}")
    except (OSError, subprocess.SubprocessError):
        return None
    if not fp["a"] and not fp["v"]:
        return None
    try:
        os.makedirs(os.path.dirname(cache), exist_ok=True)
        write_json(cache, fp)
    except OSError:
        pass
    return fp


def fp_same(a, b):
    """True when two fingerprints are the same video (or the same take): the frames match second by
    second, and so does the sound, at the same start or a second or two apart (a trimmed head)."""
    if not (isinstance(a, dict) and isinstance(b, dict)):
        return False
    va, vb = a.get("v") or [], b.get("v") or []
    aa, ab = a.get("a") or [], b.get("a") or []
    n_long = max(len(va), len(vb), len(aa) // 2, len(ab) // 2, 1)
    n_short = min(len(va), len(vb)) if va and vb else min(len(aa), len(ab)) // 2
    if n_short < 3 or n_short < 0.8 * n_long:
        return False

    def frames_ok(shift, limit):
        pairs = [(va[i], vb[i + shift]) for i in range(len(va)) if 0 <= i + shift < len(vb)]
        if len(pairs) < 3:
            return False
        close = sum(1 for x, y in pairs if bin(int(x, 16) ^ int(y, 16)).count("1") <= limit)
        return close >= 0.8 * len(pairs)

    def sound_ok(shift):
        pairs = [(aa[i], ab[i + shift]) for i in range(len(aa)) if 0 <= i + shift < len(ab)]
        loud = [(x, y) for x, y in pairs if max(x, y) > 20]
        if len(loud) < 4:
            return None   # no sound to compare
        d = sorted(x - y for x, y in loud)
        med = d[len(d) // 2]   # a re-export may be louder or quieter overall
        return sum(1 for x, y in loud if abs(x - y - med) <= 3) >= 0.85 * len(loud)

    for sh in (0, 1, -1, 2, -2):
        s_ok = sound_ok(sh * 2)
        if s_ok is True and (not (va and vb) or frames_ok(sh, 14)):
            return True
        if s_ok is None and va and vb and frames_ok(sh, 6):
            return True
    return False


def locked_update(path, change, what="the file"):
    """Read a JSON object, change it and write it back under a lock file, so two runs at once (two
    uploads in parallel) never drop each other's entry. change(data) edits the dict in place."""
    import time
    path = os.path.abspath(path)
    lock = path + ".lock"
    for _ in range(100):
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            break
        except FileExistsError:
            try:
                if time.time() - os.path.getmtime(lock) > 60:
                    os.remove(lock)
                    continue
            except OSError:
                pass
            time.sleep(0.1)
    else:
        die(f"{what} ({rel(path)}) is being written by another run. Wait a moment and run this again")
    try:
        data = {}
        if os.path.isfile(path):
            try:
                with open(path, encoding="utf-8") as fh:
                    data = json.load(fh)
            except (OSError, ValueError):
                data = {}
        if not isinstance(data, dict):
            data = {}
        change(data)
        write_json(path, data)
        return data
    finally:
        try:
            os.remove(lock)
        except OSError:
            pass


def upload_record(full):
    """What upload_parts.py recorded for this exact file in uploaded.json next to it: {"sha256",
    "uploadSessionId", "mediaId", ...}, or None when this file (as it is now) was never uploaded."""
    rp = os.path.join(os.path.dirname(os.path.abspath(full)), "uploaded.json")
    try:
        with open(rp, encoding="utf-8") as fh:
            rec = json.load(fh)
    except (OSError, ValueError):
        return None
    got = rec.get(os.path.basename(full)) if isinstance(rec, dict) else None
    if not isinstance(got, dict) or got.get("sha256") != sha256(full):
        return None
    return got
