#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from reddit_scraper import scrape_all
from stock_data import fetch_stock_data, find_european_equivalents

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"

console = Console()
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

TOP_N_TICKERS = 20


def extract_top_picks(analysis: str) -> list[str]:
    picks: list[str] = []
    for match in re.finditer(r"\*\*TOP PICK:\s*\$?(\w+)\*\*|\*\*RUNNER-UP:\s*\$?(\w+)\*\*|\*\*WILDCARD[^*]*:\s*\$?(\w+)\*\*", analysis):
        ticker = match.group(1) or match.group(2) or match.group(3)
        if ticker:
            picks.append(ticker)
    return picks


from contextlib import contextmanager


@contextmanager
def suppress_stderr():
    old_stderr = sys.stderr
    sys.stderr = open(os.devnull, "w")
    try:
        yield
    finally:
        sys.stderr.close()
        sys.stderr = old_stderr


def print_euro_equivalents(analysis: str):
    picks = extract_top_picks(analysis)
    if not picks:
        return

    console.print("\n[yellow]Looking up European equivalents...[/yellow]")

    table = Table(title="European Stock Equivalents")
    table.add_column("US Ticker", style="cyan")
    table.add_column("Euro Ticker", style="green")
    table.add_column("Exchange")
    table.add_column("Price", justify="right")
    table.add_column("Currency")

    found_any = False
    for us_ticker in picks:
        with suppress_stderr():
            euro_results = find_european_equivalents(us_ticker)
        if euro_results:
            found_any = True
            for er in euro_results:
                table.add_row(
                    f"${us_ticker}",
                    er["ticker"],
                    er["exchange"],
                    f"{er['price']:.2f}",
                    er["currency"],
                )
        else:
            table.add_row(f"${us_ticker}", "—", "—", "—", "—")

    if found_any:
        console.print(table)
    else:
        console.print("[dim]No European equivalents found.[/dim]")


def build_context(reddit_data: dict, stock_data: dict, euro: bool = False) -> str:
    ticker_counts = reddit_data["ticker_counts"]
    top_tickers = list(ticker_counts.keys())[:TOP_N_TICKERS]

    lines = [
        f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}",
        f"Total Reddit Posts Analyzed: {len(reddit_data['posts'])}",
        "",
        "=== STOCK DATA ===",
    ]

    for ticker in top_tickers:
        sd = stock_data.get(ticker)
        if not sd:
            continue
        mentions = ticker_counts.get(ticker, 0)
        cap_str = f"${sd['market_cap']/1e9:.1f}B" if sd["market_cap"] else "N/A"
        target_str = f"${sd['target_mean']:.2f}" if sd.get("target_mean") else "N/A"
        short_str = f"{sd['short_pct']*100:.1f}%" if sd.get("short_pct") else "N/A"

        lines.append(
            f"${ticker} ({sd['short_name']}): "
            f"Price=${sd['price']:.2f}, "
            f"MktCap={cap_str}, "
            f"Sector={sd['sector']}, "
            f"1WkChange={sd['week_change_pct']:+.2f}%, "
            f"P/E={sd.get('pe_ratio', 'N/A')}, "
            f"FwdP/E={sd.get('forward_pe', 'N/A')}, "
            f"Beta={sd.get('beta', 'N/A')}, "
            f"50dMA={sd.get('fifty_day_avg', 'N/A')}, "
            f"200dMA={sd.get('two_hundred_day_avg', 'N/A')}, "
            f"Recommendation={sd['recommendation']}, "
            f"AnalystTarget={target_str}, "
            f"ShortFloat={short_str}, "
            f"VolRatio={sd['volume_ratio']}, "
            f"RedditMentions={mentions}"
        )

    lines.append("")
    lines.append("=== REDDIT MENTION RANKING ===")
    for ticker, count in list(ticker_counts.items())[:TOP_N_TICKERS]:
        lines.append(f"  ${ticker}: {count} mentions")

    if euro:
        lines.append("")
        lines.append("=== NOTE ===")
        lines.append("The user wants European exchange equivalents included in the analysis.")
        lines.append("At the end of your response, add a '**European Equivalents**' section listing the top pick's")
        lines.append("most liquid European ticker (usually .DE for Xetra) and any relevant secondary listings.")

    return "\n".join(lines)


def run_analysis(context: str) -> str:
    system_prompt = (
        "You are a senior quantitative analyst at a top hedge fund. "
        "Your specialty is combining social media sentiment analysis with "
        "fundamental and technical data to identify short-term trading opportunities. "
        "You are pragmatic, data-driven, and concise. "
        "Output your analysis in clear sections with specific reasoning."
    )

    user_prompt = f"""Analyze the following data and determine which single stock has the highest probability of delivering the best return over the NEXT 7 DAYS (1 week).

Consider:
1. Reddit hype/momentum (rising mentions = potential catalyst)
2. Recent price action and technical setup
3. Valuation (P/E, forward P/E)
4. Short squeeze potential (high short float + high Reddit interest)
5. Volume anomalies (unusual volume = institutional or retail interest)
6. Analyst sentiment and price targets
7. Sector momentum

Output format (be concise, use these sections):

**TOP PICK: $TICKER**
- Rationale: (2-3 sentences on why this is the best 1-week play)

**RUNNER-UP: $TICKER**
- Rationale: (1-2 sentences)

**WILDCARD (High Risk/Reward): $TICKER**
- Rationale: (1-2 sentences)

**Risk Factors to Watch:**
- (2-3 bullet points of macro/sector risks this week)

**Confidence Score: X/10**
- (1 sentence)

DATA:
{context}"""

    console.print("\n[yellow]Sending data to Deepseek for analysis...[/yellow]\n")

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            max_tokens=1200,
        )
        return response.choices[0].message.content or "(no response)"
    except Exception as e:
        return f"Error calling Deepseek API: {e}"


def print_stock_table(stock_data: dict, ticker_counts: dict):
    table = Table(title="Stock Data Snapshot")
    table.add_column("Ticker", style="cyan")
    table.add_column("Price", justify="right")
    table.add_column("1Wk Chg", justify="right")
    table.add_column("Mkt Cap", justify="right")
    table.add_column("P/E", justify="right")
    table.add_column("Beta", justify="right")
    table.add_column("Reddit Mentions", justify="right")
    table.add_column("Rec", justify="center")

    for ticker in list(ticker_counts.keys())[:TOP_N_TICKERS]:
        sd = stock_data.get(ticker)
        if not sd:
            continue
        cap_str = f"${sd['market_cap']/1e9:.1f}B" if sd["market_cap"] else "N/A"
        pe_str = f"{sd['pe_ratio']:.1f}" if sd.get("pe_ratio") else "N/A"
        beta_str = f"{sd['beta']:.2f}" if sd.get("beta") else "N/A"
        change_color = "green" if sd["week_change_pct"] >= 0 else "red"

        table.add_row(
            f"${ticker}",
            f"${sd['price']:.2f}",
            f"[{change_color}]{sd['week_change_pct']:+.2f}%[/{change_color}]",
            cap_str,
            pe_str,
            beta_str,
            str(ticker_counts.get(ticker, 0)),
            sd["recommendation"],
        )

    console.print(table)


def main():
    parser = argparse.ArgumentParser(
        description="Reddit Stonks Analyzer — scrape Reddit + AI stock picks"
    )
    parser.add_argument(
        "-e", "--euro",
        action="store_true",
        help="Show European exchange equivalents for top picks",
    )
    parser.add_argument(
        "-p", "--posts",
        type=int,
        default=50,
        help="Posts per subreddit (default: 50)",
    )
    args = parser.parse_args()

    if not DEEPSEEK_API_KEY:
        console.print(
            "[red]Error:[/red] DEEPSEEK_API_KEY not set. "
            "Copy .env.example to .env and add your key."
        )
        sys.exit(1)

    console.print(Panel.fit(
        "[bold green]Reddit Stonks Analyzer[/bold green]\n"
        "Scrapes Reddit stock pages + AI analysis for best 1-week return",
        border_style="green",
    ))

    reddit_data = scrape_all(limit_per_sub=args.posts)

    top_tickers = list(reddit_data["ticker_counts"].keys())[:TOP_N_TICKERS]
    stock_data = fetch_stock_data(top_tickers)

    print_stock_table(stock_data, reddit_data["ticker_counts"])

    context = build_context(reddit_data, stock_data, euro=args.euro)
    analysis = run_analysis(context)

    console.print(Panel.fit(
        analysis,
        title="[bold]AI Analysis - Best Stock for Next 7 Days[/bold]",
        border_style="yellow",
    ))

    if args.euro:
        print_euro_equivalents(analysis)

    disclaimer = (
        "DISCLAIMER: This is AI-generated analysis for entertainment/educational "
        "purposes only. Not financial advice. Past performance does not guarantee "
        "future results. Always do your own research before investing."
    )
    console.print(f"\n[dim]{disclaimer}[/dim]")


if __name__ == "__main__":
    main()
