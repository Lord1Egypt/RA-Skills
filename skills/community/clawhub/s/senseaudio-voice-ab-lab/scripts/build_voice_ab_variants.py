#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


TONE_LABELS = {
    "trust": "信任感",
    "warm": "亲和感",
    "urgent": "紧迫感",
    "direct": "直接转化",
}

REGIONAL_LABELS = {
    "neutral": "标准普通话口吻",
    "north_direct": "北方利落口吻",
    "south_gentle": "南方柔和口吻",
    "taiwan_soft": "台式温柔口吻",
}


def normalize_sentence(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[。.!?！？]+$", "", text)
    return text


def join_sentence(text: str) -> str:
    text = normalize_sentence(text)
    return f"{text}。" if text else ""


def regionalize(text: str, regional_style: str) -> str:
    if regional_style == "neutral":
        return text
    if regional_style == "north_direct":
        replacements = {
            "可以先看看": "直接看看",
            "很适合": "真挺适合",
            "现在入手": "现在上就行",
            "如果你": "你要是",
        }
    elif regional_style == "south_gentle":
        replacements = {
            "直接看看": "可以先看看",
            "别错过": "可以抓紧看看",
            "现在上就行": "现在入手会更合适",
            "很适合": "会比较适合",
        }
    elif regional_style == "taiwan_soft":
        replacements = {
            "很适合": "真的很适合",
            "会更合适": "会比较适合",
            "用起来会更舒服": "用起来真的会比较舒服",
            "可以先看看": "可以先看一下",
            "先点进来看看适不适合你": "可以先点进来看看是不是适合你",
            "别错过": "这波其实蛮值得把握",
            "现在入手": "现在入手会比较划算",
        }
    else:
        replacements = {}
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text


def build_copy(
    product: str,
    audience: str,
    key_message: str,
    offer: str,
    cta: str,
    proof: str,
    tone: str,
    regional_style: str,
) -> tuple[str, str]:
    product = normalize_sentence(product)
    audience = normalize_sentence(audience)
    key_message = normalize_sentence(key_message)
    offer = normalize_sentence(offer)
    cta = normalize_sentence(cta)
    proof = normalize_sentence(proof)

    offer_sentence = join_sentence(offer) if offer else ""
    proof_sentence = join_sentence(proof) if proof else ""

    if tone == "trust":
        text = (
            f"如果你更看重稳妥和省心，这款给{audience}准备的{product}会更合适。"
            f"{join_sentence(key_message)}"
            f"{proof_sentence}"
            f"{offer_sentence}"
            f"{join_sentence(cta)}"
        )
        hypothesis = "更适合高客单、需要信任背书的转化场景。"
    elif tone == "warm":
        text = (
            f"给{audience}说一个更实在的选择，这款{product}用起来会更舒服。"
            f"{join_sentence(key_message)}"
            f"{offer_sentence}"
            f"{join_sentence(cta)}"
        )
        hypothesis = "更适合私域、社群、熟人推荐和低压转化场景。"
    elif tone == "urgent":
        text = (
            f"想入手{product}的话，这波时间点刚刚好。"
            f"{offer_sentence}"
            f"{join_sentence(key_message)}"
            f"{join_sentence(cta)}"
        )
        hypothesis = "更适合促销期、直播前、限时活动和短视频投流。"
    else:
        text = (
            f"{product}直接看重点。"
            f"{join_sentence(key_message)}"
            f"{offer_sentence}"
            f"{join_sentence(cta)}"
        )
        hypothesis = "更适合信息流、强转化素材和低耐心受众。"

    text = regionalize(text, regional_style)
    return text, hypothesis


def estimate_points(text: str) -> int:
    visible = [ch for ch in text if not ch.isspace()]
    return sum(2 if "\u4e00" <= ch <= "\u9fff" else 1 for ch in visible)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build spoken A/B variants from one commercial brief.")
    parser.add_argument("--campaign-name", default="")
    parser.add_argument("--product", default="")
    parser.add_argument("--audience", default="")
    parser.add_argument("--key-message", default="")
    parser.add_argument("--offer", default="")
    parser.add_argument("--cta", default="")
    parser.add_argument("--proof", default="")
    parser.add_argument("--tones", default="trust,warm,urgent,direct")
    parser.add_argument("--regional-styles", default="neutral")
    parser.add_argument("--brief-json", default="")
    parser.add_argument("--out-json", required=True)
    args = parser.parse_args()

    brief = {}
    if args.brief_json:
        brief = json.loads(Path(args.brief_json).read_text(encoding="utf-8"))

    campaign_name = args.campaign_name or brief.get("campaign_name", "")
    product = args.product or brief.get("product", "")
    audience = args.audience or brief.get("audience", "")
    key_message = args.key_message or brief.get("key_message", "")
    offer = args.offer or brief.get("offer", "")
    cta = args.cta or brief.get("cta", "")
    proof = args.proof or brief.get("proof", "")

    missing = []
    for key, value in (
        ("campaign_name", campaign_name),
        ("product", product),
        ("audience", audience),
        ("key_message", key_message),
        ("cta", cta),
    ):
        if not str(value).strip():
            missing.append(key)
    if missing:
        raise SystemExit(
            "Missing required fields: {}. Pass them as flags or via --brief-json.".format(", ".join(missing))
        )

    tones = [x.strip() for x in args.tones.split(",") if x.strip()]
    regionals = [x.strip() for x in args.regional_styles.split(",") if x.strip()]

    variants = []
    idx = 1
    for regional in regionals:
        for tone in tones:
            text, hypothesis = build_copy(
                product,
                audience,
                key_message,
                offer,
                cta,
                proof,
                tone,
                regional,
            )
            variant = {
                "variant_id": f"V{idx:02d}",
                "tone": tone,
                "tone_label": TONE_LABELS.get(tone, tone),
                "regional_style": regional,
                "regional_label": REGIONAL_LABELS.get(regional, regional),
                "hypothesis": hypothesis,
                "text": text,
                "estimated_points": estimate_points(text),
            }
            variants.append(variant)
            idx += 1

    result = {
        "campaign_name": campaign_name,
        "same_voice_required": True,
        "product": product,
        "audience": audience,
        "key_message": key_message,
        "offer": offer,
        "cta": cta,
        "proof": proof,
        "tones": tones,
        "regional_styles": regionals,
        "source": brief.get("source") if brief else "manual_flags",
        "source_transcript": brief.get("source_transcript", ""),
        "variants": variants,
    }

    out = Path(args.out_json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
