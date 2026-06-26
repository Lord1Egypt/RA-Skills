import logging

logger = logging.getLogger(__name__)


def compute_confidence(
    noaa: int,
    openmeteo: int,
    wunderground: int,
    min_temp: int,
    max_temp: int,
    context: dict,
    ai_result: dict,
) -> int:
    """
    Computes a confidence score 0–100.
    ai_result now comes from NVIDIA FourcastNet (a 4th atmospheric model forecast).
    Trade only executes if score == 100.
    """
    score = 0
    breakdown = []

    if abs(noaa - openmeteo) <= 1:
        score += 12
        breakdown.append(f"NOAA vs OpenMeteo agree (|{noaa}-{openmeteo}|<=1): +12")
    else:
        breakdown.append(f"NOAA vs OpenMeteo disagree (|{noaa}-{openmeteo}|={abs(noaa-openmeteo)}): +0")

    if abs(noaa - wunderground) <= 1:
        score += 12
        breakdown.append(f"NOAA vs Wunderground agree (|{noaa}-{wunderground}|<=1): +12")
    else:
        breakdown.append(f"NOAA vs Wunderground disagree (|{noaa}-{wunderground}|={abs(noaa-wunderground)}): +0")

    if abs(openmeteo - wunderground) <= 1:
        score += 11
        breakdown.append(f"OpenMeteo vs Wunderground agree (|{openmeteo}-{wunderground}|<=1): +11")
    else:
        breakdown.append(f"OpenMeteo vs Wunderground disagree (|{openmeteo}-{wunderground}|={abs(openmeteo-wunderground)}): +0")

    consensus = round((noaa + openmeteo + wunderground) / 3)
    if min_temp <= consensus <= max_temp:
        score += 25
        breakdown.append(f"Consensus {consensus}°F inside [{min_temp}–{max_temp}°F]: +25")
    else:
        breakdown.append(f"Consensus {consensus}°F outside [{min_temp}–{max_temp}°F]: +0")

    edge_rec = context.get("edge", {}).get("recommendation", None)
    if edge_rec == "TRADE":
        score += 20
        breakdown.append(f"Simmer edge recommendation=TRADE: +20")
    else:
        breakdown.append(f"Simmer edge recommendation={edge_rec} (no user probability set): +0")

    hours = context.get("time_to_resolution", 999)
    if isinstance(hours, (int, float)) and hours <= 24:
        score += 10
        breakdown.append(f"Time to resolution {hours}h <=24h: +10")
    else:
        breakdown.append(f"Time to resolution {hours}h >24h: +0")

    pre_ai_score = score
    breakdown.append(f"Pre-FourcastNet score: {pre_ai_score}")

    fc_verdict = ai_result.get("verdict") == "TRADE"
    fc_inside = ai_result.get("inside_bucket") is True
    fc_sources = ai_result.get("sources_agree") is True

    if fc_verdict and fc_inside and fc_sources:
        score = 100
        breakdown.append("FourcastNet full confirmation (all conditions true): score locked to 100")
    else:
        breakdown.append(
            f"FourcastNet did NOT fully confirm: verdict={ai_result.get('verdict')}, "
            f"inside_bucket={ai_result.get('inside_bucket')}, "
            f"sources_agree={ai_result.get('sources_agree')}"
        )

    final_score = min(score, 100)
    logger.info(f"Confidence score: {final_score}\n" + "\n".join(f"  {b}" for b in breakdown))
    return final_score
