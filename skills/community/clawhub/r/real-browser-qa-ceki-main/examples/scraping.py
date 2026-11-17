"""Scraping a site with anti-bot protection using a real browser."""
import asyncio

from ceki_browser import Browser


async def main():
    async with Browser(token="YOUR_TOKEN") as br:
        async with await br.session(
            mode="incognito",
            domain_hints=["news.ycombinator.com"],
            geo="US",
        ) as s:
            await s.navigate("https://news.ycombinator.com")

            items = await s.query_all(
                "a.titlelink",
                attributes=["textContent", "href"],
                limit=30,
            )
            for el in items.elements:
                print(f"{el.get('textContent')} — {el.get('href')}")

            page_html = await s.get_html("body", outer=False)
            print(f"\nPage HTML size: {len(page_html.html)} chars")

            screenshot = await s.screenshot(format="png")
            print(f"Screenshot: {len(screenshot.data)} base64 chars")


if __name__ == "__main__":
    asyncio.run(main())
