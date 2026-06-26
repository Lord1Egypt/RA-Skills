"""Entry point: python -m redditrank_tui"""
from redditrank_tui.app import RedditRankApp

def main():
    app = RedditRankApp()
    app.run()

if __name__ == "__main__":
    main()
