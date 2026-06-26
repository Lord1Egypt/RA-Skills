#!/usr/bin/env python3
from datetime import datetime, date

def days_until(expiry):
    if not expiry:
        return None
    try:
        d = datetime.fromisoformat(expiry).date()
        return (d - date.today()).days
    except ValueError:
        return None

def calculate_quality_score(proxy):
    score = 50

    status = proxy.get("status")
    if status == "active":
        score += 15
    elif status == "inactive":
        score -= 15

    success_rate = proxy.get("success_rate")
    if success_rate is not None:
        try:
            sr = float(success_rate)
            if sr >= 95:
                score += 20
            elif sr >= 85:
                score += 10
            elif sr < 70:
                score -= 15
        except (TypeError, ValueError):
            pass

    latency = proxy.get("avg_latency_ms")
    if latency is not None:
        try:
            lat = int(latency)
            if lat <= 150:
                score += 10
            elif lat <= 300:
                score += 5
            elif lat > 800:
                score -= 10
        except (TypeError, ValueError):
            pass

    expiry = days_until(proxy.get("expires_on"))
    if expiry is not None:
        if expiry < 0:
            score -= 50
        elif expiry <= 3:
            score -= 15
        elif expiry <= 14:
            score -= 5

    if proxy.get("rotation") == "sticky":
        score += 3

    return max(0, min(100, int(score)))

def fit_score(proxy, region=None, protocol=None, rotation=None, max_latency_ms=None):
    score = 0

    if proxy.get("status") != "active":
        return -9999

    expiry = days_until(proxy.get("expires_on"))
    if expiry is not None and expiry < 0:
        return -9999

    if region:
        if (proxy.get("region") or "").lower() == region.lower():
            score += 25
        else:
            score -= 20

    if protocol:
        if (proxy.get("protocol") or "").lower() == protocol.lower():
            score += 20
        else:
            score -= 15

    if rotation:
        if (proxy.get("rotation") or "").lower() == rotation.lower():
            score += 15
        else:
            score -= 10

    latency = proxy.get("avg_latency_ms")
    if max_latency_ms is not None and latency is not None:
        try:
            if int(latency) <= int(max_latency_ms):
                score += 15
            else:
                score -= 20
        except (TypeError, ValueError):
            pass

    score += int(proxy.get("quality_score", 0) / 2)
    return score
