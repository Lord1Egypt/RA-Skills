import logging
import asyncio
from datetime import date, datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from simmer_client import (
    fetch_weather_markets, get_market_context, execute_trade,
    get_agent_info, get_positions,
)
from noaa import get_noaa_forecast
from openmeteo import get_openmeteo_forecast
from wunderground import get_wunderground_forecast
from ai_analyzer import analyze_with_ai
from strategy import compute_confidence
from city_map import resolve_city
from config import TRADE_AMOUNT, CONFIDENCE_THRESHOLD, SIMMER_VENUE

logger = logging.getLogger(__name__)

NUM_MARKETS_SHOWN = 4


def build_main_keyboard(markets: list[dict]) -> InlineKeyboardMarkup:
    keyboard = []
    for i, market in enumerate(markets[:NUM_MARKETS_SHOWN]):
        question_short = market.get("question", f"Market {i+1}")
        if len(question_short) > 45:
            question_short = question_short[:42] + "..."
        keyboard.append([
            InlineKeyboardButton(
                f"🔮 Predict {i+1} & Bet — {question_short}",
                callback_data=f"predict_{i}"
            )
        ])
    keyboard.append([InlineKeyboardButton("📊 Agent Status", callback_data="status")])
    return InlineKeyboardMarkup(keyboard)


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        markets = await fetch_weather_markets(limit=NUM_MARKETS_SHOWN + 5)
        active = [m for m in markets if m.get("status") == "active"]
        if not active:
            active = markets

        context.bot_data["cached_markets"] = active

        msg = "🤖 *Simmer Weather Trading Bot*\n\n"
        msg += f"Found *{len(active)}* active weather markets.\n"
        msg += "Select a market to analyze and trade:\n\n"

        for i, m in enumerate(active[:NUM_MARKETS_SHOWN]):
            prob = m.get("current_probability")
            prob_str = f"{prob:.0%}" if isinstance(prob, float) else "N/A"
            msg += f"*{i+1}.* {m.get('question', 'Unknown')[:80]}\n"
            msg += f"   YES price: {prob_str}\n\n"

        keyboard = build_main_keyboard(active)
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)

    except Exception as e:
        logger.exception("Error in /start")
        await update.message.reply_text(
            f"❌ Failed to fetch markets from Simmer:\n`{str(e)[:300]}`",
            parse_mode=ParseMode.MARKDOWN
        )


async def handle_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("⏳ Fetching agent status...")
    try:
        agent = await get_agent_info()
        positions = await get_positions()

        balance = agent.get("balance", "N/A")
        agent_id = agent.get("agent_id", agent.get("id", "N/A"))

        msg = "📊 *Agent Status*\n\n"
        msg += f"🆔 Agent ID: `{agent_id}`\n"
        msg += f"💰 Balance: `{balance}`\n"
        msg += f"🏦 Venue: `{SIMMER_VENUE}`\n\n"

        if positions:
            msg += f"📈 *Open Positions ({len(positions)}):*\n"
            for pos in positions[:5]:
                mkt = pos.get("market_question", pos.get("question", "Unknown"))[:50]
                shares = pos.get("shares", pos.get("quantity", "?"))
                side = pos.get("side", "YES")
                msg += f"  • {mkt}\n    {side}: {shares} shares\n"
        else:
            msg += "📈 *Open Positions:* None\n"

        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        logger.exception("Error in /status")
        await update.message.reply_text(
            f"❌ Error fetching status:\n`{str(e)[:300]}`",
            parse_mode=ParseMode.MARKDOWN
        )


async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "status":
        await query.message.reply_text("⏳ Fetching agent status...")
        try:
            agent = await get_agent_info()
            positions = await get_positions()

            balance = agent.get("balance", "N/A")
            agent_id = agent.get("agent_id", agent.get("id", "N/A"))

            msg = "📊 *Agent Status*\n\n"
            msg += f"🆔 Agent ID: `{agent_id}`\n"
            msg += f"💰 Balance: `{balance}`\n"
            msg += f"🏦 Venue: `{SIMMER_VENUE}`\n\n"

            if positions:
                msg += f"📈 *Open Positions ({len(positions)}):*\n"
                for pos in positions[:5]:
                    mkt = pos.get("market_question", pos.get("question", "Unknown"))[:50]
                    shares = pos.get("shares", pos.get("quantity", "?"))
                    side = pos.get("side", "YES")
                    msg += f"  • {mkt}\n    {side}: {shares} shares\n"
            else:
                msg += "📈 *Open Positions:* None\n"

            await query.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            await query.message.reply_text(f"❌ Error: `{str(e)[:200]}`", parse_mode=ParseMode.MARKDOWN)
        return

    if not data.startswith("predict_"):
        return

    try:
        market_index = int(data.split("_")[1])
    except (IndexError, ValueError):
        await query.message.reply_text("❌ Invalid button data.")
        return

    await query.message.reply_text(
        f"⏳ Fetching fresh markets and running full analysis for market #{market_index + 1}...\n"
        "This may take 1–2 minutes (3 live forecasts + NVIDIA FourcastNet atmospheric model)."
    )

    await _run_prediction_pipeline(query, market_index)


async def _run_prediction_pipeline(query, market_index: int) -> None:
    try:
        markets = await fetch_weather_markets(limit=NUM_MARKETS_SHOWN + 5)
        active = [m for m in markets if m.get("status") == "active"]
        if not active:
            active = markets
    except Exception as e:
        await query.message.reply_text(
            f"❌ Failed to fetch markets from Simmer API.\n\nError: `{str(e)[:300]}`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    if market_index >= len(active):
        await query.message.reply_text(
            f"❌ Not enough markets available. Only {len(active)} active markets found, "
            f"but you selected #{market_index + 1}."
        )
        return

    market = active[market_index]
    question = market.get("question", "Unknown")
    logger.info(f"Pipeline: processing market index {market_index}: {question}")

    if not market.get("id"):
        await query.message.reply_text(
            f"❌ Market #{market_index + 1} has no ID. Cannot proceed.\n\nMarket: {question}"
        )
        return

    if market.get("min_temp") is None or market.get("max_temp") is None:
        await query.message.reply_text(
            f"❌ Could not parse temperature bucket from market question.\n\n"
            f"Question: `{question}`\n\n"
            f"Parsed min_temp={market.get('min_temp')} max_temp={market.get('max_temp')}.\n"
            f"The market question format may not be supported yet.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    if market.get("city") is None:
        await query.message.reply_text(
            f"❌ Could not identify a city from market question.\n\n"
            f"Question: `{question}`\n\n"
            f"Add the city to city_map.py if needed.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    try:
        city_data = resolve_city(market["city"])
    except ValueError as e:
        await query.message.reply_text(
            f"❌ City resolution failed: {str(e)}",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    target_date = market.get("date")
    if target_date is None:
        target_date = date.today()
        logger.warning(f"No date parsed from market question, defaulting to today: {target_date}")

    await query.message.reply_text(
        f"📍 Market: {question[:80]}\n"
        f"🏙️ City: {market['city']} | 📅 Date: {target_date} | 🌡️ Bucket: {market['min_temp']}–{market['max_temp']}°F\n\n"
        f"⏳ Step 1/4: Fetching Simmer context..."
    )

    try:
        simmer_context = await get_market_context(market["id"])
    except Exception as e:
        await query.message.reply_text(
            f"❌ *Simmer Context API failed.*\n\nError: `{str(e)[:300]}`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    await query.message.reply_text("⏳ Step 2/4: Fetching 3 live weather forecasts (NOAA + Open-Meteo + Wunderground)...")

    noaa_temp = None
    openmeteo_temp = None
    wunderground_temp = None
    forecast_errors = []

    try:
        noaa_temp = await get_noaa_forecast(city_data["lat"], city_data["lon"], target_date)
        logger.info(f"NOAA result: {noaa_temp}°F")
    except Exception as e:
        forecast_errors.append(f"NOAA: {str(e)[:200]}")
        logger.error(f"NOAA failed: {e}")

    try:
        openmeteo_temp = await get_openmeteo_forecast(
            city_data["lat"], city_data["lon"], target_date, timezone=city_data.get("timezone", "auto")
        )
        logger.info(f"Open-Meteo result: {openmeteo_temp}°F")
    except Exception as e:
        forecast_errors.append(f"Open-Meteo: {str(e)[:200]}")
        logger.error(f"Open-Meteo failed: {e}")

    try:
        wunderground_temp = await get_wunderground_forecast(city_data["wunderground"], target_date)
        logger.info(f"Wunderground result: {wunderground_temp}°F")
    except Exception as e:
        forecast_errors.append(f"Wunderground: {str(e)[:200]}")
        logger.error(f"Wunderground failed: {e}")

    if forecast_errors:
        errors_formatted = "\n".join(f"• {e}" for e in forecast_errors)
        await query.message.reply_text(
            f"❌ *TRADE SKIPPED — Forecast API failure(s)*\n\n"
            f"📍 Market: {question[:80]}\n\n"
            f"The following APIs failed:\n{errors_formatted}\n\n"
            f"All three forecasts (NOAA, Open-Meteo, Wunderground) are required.\n"
            f"No trade was placed.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    await query.message.reply_text(
        f"📡 Forecasts received:\n"
        f"  • NOAA: {noaa_temp}°F\n"
        f"  • Open-Meteo: {openmeteo_temp}°F\n"
        f"  • Wunderground: {wunderground_temp}°F\n\n"
        f"⏳ Step 3/4: Submitting to NVIDIA FourcastNet atmospheric model (may take ~1 min)..."
    )

    try:
        ai_result = await analyze_with_ai(
            market=market,
            context=simmer_context,
            noaa_temp=noaa_temp,
            openmeteo_temp=openmeteo_temp,
            wunderground_temp=wunderground_temp,
        )
    except Exception as e:
        await query.message.reply_text(
            f"❌ *TRADE SKIPPED — FourcastNet analysis failed*\n\n"
            f"📍 Market: {question[:80]}\n\n"
            f"NVIDIA FourcastNet error: `{str(e)[:300]}`\n\n"
            f"No trade was placed.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    await query.message.reply_text("⏳ Step 4/4: Computing confidence score and making final decision...")

    confidence = compute_confidence(
        noaa=noaa_temp,
        openmeteo=openmeteo_temp,
        wunderground=wunderground_temp,
        min_temp=market["min_temp"],
        max_temp=market["max_temp"],
        context=simmer_context,
        ai_result=ai_result,
    )

    consensus = round((noaa_temp + openmeteo_temp + wunderground_temp) / 3)
    spread = max(noaa_temp, openmeteo_temp, wunderground_temp) - min(noaa_temp, openmeteo_temp, wunderground_temp)
    inside_bucket = market["min_temp"] <= consensus <= market["max_temp"]
    sources_agree = spread <= 1
    prob = market.get("current_probability")
    prob_str = f"{prob:.0%}" if isinstance(prob, float) else "N/A"
    edge_pct = simmer_context.get("edge", {}).get("edge_pct", "N/A")
    slippage = simmer_context.get("slippage_estimate", "N/A")
    time_to_res = simmer_context.get("time_to_resolution", "N/A")

    if confidence == CONFIDENCE_THRESHOLD and ai_result.get("verdict") == "TRADE":
        reasoning = (
            f"NOAA={noaa_temp}°F, OpenMeteo={openmeteo_temp}°F, Wunderground={wunderground_temp}°F — "
            f"all within ±1°F. Bucket [{market['min_temp']}-{market['max_temp']}°F]. "
            f"Confidence 100%. FourcastNet verdict: TRADE. Reason: {ai_result.get('reason', '')}"
        )

        try:
            trade_result = await execute_trade(
                market_id=market["id"],
                reasoning=reasoning,
            )
        except Exception as e:
            await query.message.reply_text(
                f"⚠️ *TRADE FAILED — API error during execution*\n\n"
                f"📍 Market: {question[:80]}\n\n"
                f"Conditions were met (confidence=100%, AI=TRADE) but the trade API failed:\n"
                f"`{str(e)[:300]}`\n\n"
                f"No trade was placed.",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        success = trade_result.get("success", True)
        trade_id = trade_result.get("trade_id", trade_result.get("id", "N/A"))
        shares = trade_result.get("shares_bought", trade_result.get("shares", "N/A"))
        cost = trade_result.get("cost", TRADE_AMOUNT)
        new_price = trade_result.get("new_price", trade_result.get("price", "N/A"))
        fully_filled = trade_result.get("fully_filled", True)
        trade_warnings = trade_result.get("warnings", [])
        error_msg = trade_result.get("error", None)

        if not success or error_msg:
            await query.message.reply_text(
                f"⚠️ *TRADE REJECTED BY SIMMER*\n\n"
                f"📍 Market: {question[:80]}\n\n"
                f"Simmer rejected the trade:\n`{error_msg or 'No error message returned'}`\n\n"
                f"No shares were purchased.",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        bucket_icon = "✅" if inside_bucket else "❌"
        agree_icon = "✅" if sources_agree else "❌"

        msg = (
            f"🚨 *TRADE EXECUTED*\n\n"
            f"📍 *Market:* {question[:80]}\n"
            f"🔗 *Market ID:* `{market['id']}`\n"
            f"🌐 *Venue:* Simmer ($SIM)\n\n"
            f"📡 *Live Forecast:*\n"
            f"   • NOAA:          `{noaa_temp}°F`\n"
            f"   • Open-Meteo:   `{openmeteo_temp}°F`\n"
            f"   • Wunderground: `{wunderground_temp}°F`\n"
            f"   • Consensus:    `{consensus}°F` "
            f"{bucket_icon} {'Inside' if inside_bucket else 'Outside'} bucket [{market['min_temp']}–{market['max_temp']}°F]\n\n"
            f"🤖 *NVIDIA FourcastNet Verdict:* TRADE\n"
            f"   Predicted Temp:   `{ai_result.get('predicted_temp')}°F`\n"
            f"   Sources Agree:    {agree_icon} (spread={spread}°F)\n"
            f"   Bucket Match:     ✅ ({consensus} inside [{market['min_temp']}–{market['max_temp']}])\n"
            f"   Simmer Edge:      ✅ TRADE recommended\n"
            f"   FC Reason:        {ai_result.get('reason', 'N/A')}\n\n"
            f"📊 *Confidence Score:* 100%\n\n"
            f"💵 *Action:* BUY YES\n"
            f"💰 *Amount:* ${cost} SIM\n"
            f"📈 *Shares Bought:* {shares}\n"
            f"💲 *New Market Price:* {new_price}\n"
            f"🧾 *Trade ID:* `{trade_id}`\n"
            f"✔️ *Fully Filled:* {'Yes' if fully_filled else 'No'}\n"
        )

        if trade_warnings:
            msg += f"\n⚠️ *Warnings:* {', '.join(str(w) for w in trade_warnings)}"

        await query.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

    else:
        verdict = ai_result.get("verdict", "SKIP")
        reason = ai_result.get("reason", "No reason provided by AI")
        bucket_icon = "✅" if inside_bucket else "❌"
        agree_icon = "✅" if sources_agree else "❌"

        skip_reasons = []
        if not sources_agree:
            skip_reasons.append(f"Forecast spread is {spread}°F (maximum allowed: 1°F)")
        if not inside_bucket:
            skip_reasons.append(
                f"Consensus {consensus}°F is NOT inside bucket [{market['min_temp']}–{market['max_temp']}°F] "
                f"(off by {min(abs(consensus - market['min_temp']), abs(consensus - market['max_temp']))}°F)"
            )
        edge_rec = simmer_context.get("edge", {}).get("recommendation", "SKIP")
        if edge_rec != "TRADE":
            skip_reasons.append(f"Simmer edge recommendation is {edge_rec}, not TRADE")
        if confidence < CONFIDENCE_THRESHOLD:
            skip_reasons.append(f"Confidence score is {confidence}%, required: {CONFIDENCE_THRESHOLD}%")
        if verdict != "TRADE":
            skip_reasons.append(f"AI verdict is {verdict}: {reason}")

        reasons_formatted = "\n".join(f"   • {r}" for r in skip_reasons) if skip_reasons else f"   • {reason}"

        msg = (
            f"❌ *TRADE SKIPPED*\n\n"
            f"📍 *Market:* {question[:80]}\n\n"
            f"📡 *Live Forecast:*\n"
            f"   • NOAA:          `{noaa_temp}°F`\n"
            f"   • Open-Meteo:   `{openmeteo_temp}°F`\n"
            f"   • Wunderground: `{wunderground_temp}°F`\n"
            f"   • Consensus:    `{consensus}°F` "
            f"{bucket_icon} {'Inside' if inside_bucket else 'NOT inside'} bucket [{market['min_temp']}–{market['max_temp']}°F]\n\n"
            f"🤖 *NVIDIA FourcastNet Verdict:* {verdict}\n"
            f"   Predicted Temp:   `{ai_result.get('predicted_temp')}°F`\n"
            f"   Sources Agree:    {agree_icon} (spread={spread}°F)\n"
            f"   Bucket Match:     {bucket_icon} ({consensus}°F {'inside' if inside_bucket else 'outside'} [{market['min_temp']}–{market['max_temp']}])\n"
            f"   FC Reason:        {reason}\n\n"
            f"📊 *Confidence Score:* {confidence}%\n"
            f"🚫 *Required:* {CONFIDENCE_THRESHOLD}%\n\n"
            f"*Exact reasons for skip:*\n{reasons_formatted}\n\n"
            f"No trade was placed."
        )

        await query.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
