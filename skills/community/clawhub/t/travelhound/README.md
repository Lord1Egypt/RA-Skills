# TravelHound — Find Cheap Flights & Hotels Before You Book

> Compare Google Flights, Skyscanner, Kayak, Booking.com, Agoda, Trip.com side by side. Get a Buy/Wait verdict. Stack OTA coupon codes.

[![clawhub](https://img.shields.io/badge/clawhub-travelhound-blue)](https://clawhub.ai/skills/travelhound)
[![version](https://img.shields.io/badge/version-1.1.3-green)](https://clawhub.ai/skills/travelhound)
[![license](https://img.shields.io/badge/license-MIT--0-lightgrey)](LICENSE)

## What it does

TravelHound is an [OpenClaw](https://openclaw.ai) skill that does for flights and hotels what [BuyWise](https://github.com/jiajiaoy/BuyWise) does for products: compares real prices across platforms, checks whether now is the right time to book, finds promo codes, and gives you a clear verdict.

**Flight comparison** — Google Flights + Skyscanner + Kayak + Trip.com, with Kayak's *Buy now / Wait* forecast  
**Hotel comparison** — Booking.com + Agoda + Hotels.com + Trip.com, with OTA coupon stacking  
**Full trip planner** — flights + hotels in one report with total budget estimate  
**Destination intelligence** — visa requirements, exchange rate trend, safety advisories, latest news  
**OTA coupon stacking** — calls [CouponClaw](https://github.com/jiajiaoy/CouponClaw) to find promo codes for Booking.com, Agoda, Trip.com  
**News check** — calls [NewsToday](https://github.com/jiajiaoy/NewsToday) for destination-relevant headlines (political situation, weather, local events)

## Data sources

| Platform | Type | Strength |
|---|---|---|
| Google Flights | Flights | Best aggregator; price insights; date flexibility view |
| Skyscanner | Flights | Lowest fares incl. budget carriers; flexible origin |
| Kayak | Flights + Hotels | Price Forecast (Buy / Wait) + price history chart |
| Trip.com / 携程 | Flights + Hotels | Best rates for Asian routes; Chinese carrier coverage |
| Booking.com | Hotels | Widest global inventory; Genius discounts |
| Agoda | Hotels | Best rates for Southeast and East Asia |
| Hotels.com | Hotels | 10-night loyalty reward |

## Installation

```bash
openclaw install travelhound
```

## Usage

```bash
# Full trip planner: flights + hotels + destination intel
openclaw run travelhound trip "Tokyo" --from "London" --date 2026-08-01 --nights 7 --budget mid

# Flights only
openclaw run travelhound flights "London" "Tokyo" --date 2026-08-01 --return 2026-08-08

# Hotels only
openclaw run travelhound hotels "Tokyo" --checkin 2026-08-01 --checkout 2026-08-08 --budget mid

# Budget options
# --budget budget | mid | luxury
# --class economy | business | first
# --lang zh | en
```

## Ecosystem

Part of the **OpenClaw Smart Consumer** skill suite:

```
NewsToday ←→ TravelHound → CouponClaw
                 ↑
            TrendRadar (trending destinations)
```

| Skill | How it connects |
|---|---|
| **TravelHound** | Travel pricing ← you are here |
| [CouponClaw](https://github.com/jiajiaoy/CouponClaw) | OTA promo codes stacked on top of platform prices |
| [NewsToday](https://github.com/jiajiaoy/NewsToday) | Destination news (visa changes, safety, events) |
| [BuyWise](https://github.com/jiajiaoy/BuyWise) | Same buy/wait decision logic, applied to products |

## Keywords

cheap flights · flight comparison · best time to book flights · flight price prediction · Google Flights · Skyscanner · Kayak · cheap hotels · hotel comparison · Booking.com · Agoda · budget travel · travel hacks · OTA coupon · visa requirements · exchange rate · 机票 · 酒店 · 旅行攻略 · 特价机票 · 穷游 · 自由行

---

Built for [OpenClaw](https://openclaw.ai) · Published on [clawhub.ai/skills/travelhound](https://clawhub.ai/skills/travelhound)
