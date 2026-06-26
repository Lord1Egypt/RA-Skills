import json
import os
import json
import requests
import argparse
import sys
from datetime import datetime

TOKEN_CACHE = "/tmp/seesaw_token.json"

class SeesawClient:
    def __init__(self, base_url=None, api_key=None, api_secret=None):
        self.base_url = base_url or os.getenv("SEESAW_BASE_URL", "http://localhost:3000/v1")
        self.api_key = api_key or os.getenv("SEESAW_API_KEY")
        self.api_secret = api_secret or os.getenv("SEESAW_API_SECRET")
        self.token = self._load_token()

    def _load_token(self):
        if os.path.exists(TOKEN_CACHE):
            try:
                with open(TOKEN_CACHE, 'r') as f:
                    data = json.load(f)
                    return data.get("token")
            except (json.JSONDecodeError, IOError):
                pass
        return None

    def _save_token(self, token):
        self.token = token
        try:
            with open(TOKEN_CACHE, 'w') as f:
                json.dump({"token": token}, f)
        except IOError:
            pass

    def login(self):
        if not self.api_key or not self.api_secret:
            raise ValueError("SEESAW_API_KEY and SEESAW_API_SECRET must be set")
        
        url = f"{self.base_url}/auth/agent-login"
        payload = {"api_key": self.api_key, "api_secret": self.api_secret}
        try:
            resp = requests.post(url, json=payload, timeout=10)
            if not resp.ok: print(f"Error Body: {resp.text}")
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Login failed: {e}")
        
        token = resp.json().get("token")
        self._save_token(token)
        return token

    def _request(self, method, path, **kwargs):
        if not self.token:
            self.login()
        
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {self.token}"
        kwargs["headers"] = headers
        if "timeout" not in kwargs:
            kwargs["timeout"] = 15
        
        url = f"{self.base_url}/{path.lstrip('/')}"
        try:
            resp = requests.request(method, url, **kwargs)
            
            if resp.status_code == 401:
                self.login()
                headers["Authorization"] = f"Bearer {self.token}"
                resp = requests.request(method, url, **kwargs)
                
            if not resp.ok: print(f"Error Body: {resp.text}")
            resp.raise_for_status()
            try:
                return resp.json()
            except ValueError:
                return resp.text
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Request to {path} failed: {e}")

    # ========== MARKETS ==========
    def list_markets(self, page=1, limit=20, status="active", category_id=None, sort=None):
        params = {"page": page, "limit": limit, "status": status}
        if category_id:
            params["category_id"] = category_id
        if sort:
            params["sort"] = sort
        return self._request("GET", "markets", params=params)

    def get_market(self, market_id):
        return self._request("GET", f"markets/{market_id}")

    def get_market_activity(self, market_id, page=1, limit=20):
        params = {"page": page, "limit": limit}
        return self._request("GET", f"markets/{market_id}/activity", params=params)

    def get_price_history(self, market_id):
        return self._request("GET", f"markets/{market_id}/price-history")

    def get_traders(self, market_id, page=1, limit=20):
        params = {"page": page, "limit": limit}
        return self._request("GET", f"markets/{market_id}/traders", params=params)

    # ========== TRADE ==========
    def get_quote(self, market_id, option_id, amount, action="buy"):
        params = {
            "prediction_id": market_id,
            "option_id": option_id,
            "amount": amount,
            "action": action
        }
        return self._request("GET", "trade/quote", params=params)

    def buy(self, market_id, option_id, amount):
        if amount <= 0:
            return {"error": "Buy amount must be greater than 0", "status": "skipped"}
        payload = {
            "prediction_id": market_id,
            "option_id": option_id,
            "amount": str(amount)
        }
        return self._request("POST", "trade/buy", json=payload)

    def sell(self, market_id, option_id, shares):
        if shares <= 0:
            return {"error": "Sell shares must be greater than 0", "status": "skipped"}
        payload = {
            "prediction_id": market_id,
            "option_id": option_id,
            "shares": str(shares)
        }
        return self._request("POST", "trade/sell", json=payload)

    def claim_settlement(self, market_id):
        return self._request("POST", "trade/claim", json={"prediction_id": market_id})

    def get_positions(self, page=1, limit=20):
        params = {"page": page, "limit": limit}
        return self._request("GET", "trade/positions", params=params)

    def get_trade_history(self, page=1, limit=20):
        params = {"page": page, "limit": limit}
        return self._request("GET", "trade/history", params=params)

    # ========== WALLET ==========
    def get_balance(self):
        profile = self._request("GET", "auth/me")
        if isinstance(profile, dict):
            return {"credits": profile.get("credits", 0)}
        return profile

    def get_transactions(self, page=1, limit=20):
        params = {"page": page, "limit": limit}
        return self._request("GET", "wallet/transactions", params=params)

    def get_credit_history(self, page=1, limit=20):
        params = {"page": page, "limit": limit}
        return self._request("GET", "wallet/credit-history", params=params)

    def get_monthly_card_status(self):
        return self._request("GET", "wallet/monthly-card/status")

    # ========== USER ==========
    def get_profile(self, user_id):
        return self._request("GET", f"users/{user_id}")

    def get_default_avatars(self):
        return self._request("GET", "users/default-avatars")

    def update_avatar(self, avatar_url):
        return self._request("PUT", "users/me/avatar", json={"avatar_url": avatar_url})

    def update_profile(self, nickname=None, avatar_url=None):
        payload = {}
        if nickname:
            payload["nickname"] = nickname
        if avatar_url:
            payload["avatar_url"] = avatar_url
        return self._request("PATCH", "users/me", json=payload)

    def get_leaderboard(self, page=1, limit=20, timeframe="all"):
        params = {"page": page, "limit": limit, "timeframe": timeframe}
        return self._request("GET", "users/leaderboard", params=params)

    def get_followers(self, user_id, page=1, limit=20):
        params = {"page": page, "limit": limit}
        return self._request("GET", f"users/{user_id}/followers", params=params)

    def get_following(self, user_id, page=1, limit=20):
        params = {"page": page, "limit": limit}
        return self._request("GET", f"users/{user_id}/following", params=params)

    def get_favorites(self, user_id, page=1, limit=20):
        params = {"type": "favorite", "page": page, "limit": limit}
        return self._request("GET", f"users/{user_id}/markets", params=params)

    def follow(self, user_id):
        return self._request("POST", f"users/{user_id}/follow")

    def unfollow(self, user_id):
        return self._request("DELETE", f"users/{user_id}/follow")

    def block(self, user_id):
        return self._request("POST", f"users/{user_id}/block")

    def unblock(self, user_id):
        return self._request("DELETE", f"users/{user_id}/block")

    # ========== SOCIAL ==========
    def get_comments(self, market_id, page=1, limit=20):
        params = {"page": page, "limit": limit}
        return self._request("GET", f"markets/{market_id}/comments", params=params)

    def add_comment(self, market_id, content):
        payload = {"content": content}
        return self._request("POST", f"markets/{market_id}/comments", json=payload)

    def delete_comment(self, market_id, comment_id):
        return self._request("DELETE", f"markets/{market_id}/comments/{comment_id}")

    def favorite(self, market_id):
        return self._request("POST", f"markets/{market_id}/favorite")

    def unfavorite(self, market_id):
        return self._request("DELETE", f"markets/{market_id}/favorite")

    # ========== CHALLENGES ==========
    def list_challenges(self):
        return self._request("GET", "challenges")

    def claim_challenge(self, challenge_id):
        return self._request("POST", f"challenges/{challenge_id}/claim")

    # ========== ORACLE ==========
    def get_oracle_status(self, prediction_id):
        return self._request("GET", f"oracle/status/{prediction_id}")

    def assert_result(self, prediction_id, option_id):
        payload = {"prediction_id": prediction_id, "option_id": option_id}
        return self._request("POST", "oracle/assert", json=payload)

    def dispute_result(self, prediction_id, option_id):
        payload = {"prediction_id": prediction_id, "option_id": option_id}
        return self._request("POST", "oracle/dispute", json=payload)

    def vote(self, prediction_id, option_id):
        payload = {"prediction_id": prediction_id, "option_id": option_id}
        return self._request("POST", "oracle/vote", json=payload)

    def settle(self, prediction_id, winner_option_id):
        return self._request("POST", "oracle/settle", json={"prediction_id": prediction_id, "winner_option_id": winner_option_id})

    # ========== CATEGORIES ==========
    def list_categories(self):
        return self._request("GET", "categories")

    # ========== UPLOAD ==========
    def get_presigned_url(self, content_type="image/jpeg", file_extension="jpg"):
        params = {"content_type": content_type, "file_extension": file_extension}
        return self._request("GET", "upload/presigned-url", params=params)

    def upload_file(self, upload_url, file_path, content_type):
        with open(file_path, 'rb') as f:
            resp = requests.put(upload_url, data=f, headers={"Content-Type": content_type})
            if not resp.ok: print(f"Error Body: {resp.text}")
            resp.raise_for_status()
        return True

    # ========== MARKET CREATION ==========
    def create_market(self, title, options, initial_probabilities, end_time, description=None, image_urls=None):
        payload = {
            "title": title,
            "options": options,
            "initial_probabilities": initial_probabilities,
            "end_time": end_time
        }
        if description: payload["description"] = description
        if image_urls: payload["image_urls"] = image_urls
        return self._request("POST", "markets", json=payload)

    # ========== SHARE ==========
    def create_share_link(self, market_id, image_url=None, share_source=None, share_target=None):
        """
        Create a share link for a topic/market.
        
        Returns a dict (CreateShareLinkResponse) with:
          - share_id (str): 分享链接 ID
          - share_url (str): 完整的分享链接 URL
          - title (str, optional): 分享标题（微信用标题+副标题，朋友圈用标题）
          - subtitle (str, optional): 分享副标题（仅微信使用）
        """
        payload = {"market_id": market_id}
        if image_url:
            payload["image_url"] = image_url
        if share_source:
            payload["share_source"] = share_source
        if share_target:
            payload["share_target"] = share_target
        return self._request("POST", "share/create", json=payload)


def main():
    parser = argparse.ArgumentParser(description="SeeSaw Prediction Market CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # ========== WALLET ==========
    subparsers.add_parser("balance", help="Get wallet balance")
    
    p_tx = subparsers.add_parser("transactions", help="Get transaction history")
    p_tx.add_argument("--page", type=int, default=1)
    p_tx.add_argument("--limit", type=int, default=20)

    p_credit = subparsers.add_parser("credit-history", help="Get credit history")
    p_credit.add_argument("--page", type=int, default=1)
    p_credit.add_argument("--limit", type=int, default=20)

    subparsers.add_parser("monthly-card-status", help="Get monthly card status")

    # ========== MARKETS ==========
    p_list = subparsers.add_parser("list-markets", help="List prediction markets")
    p_list.add_argument("--page", type=int, default=1)
    p_list.add_argument("--limit", type=int, default=20)
    p_list.add_argument("--status", default="active")
    p_list.add_argument("--category", dest="category_id")

    p_get = subparsers.add_parser("get-market", help="Get market details")
    p_get.add_argument("id", help="Market ID")

    p_activity = subparsers.add_parser("market-activity", help="Get market activity")
    p_activity.add_argument("market_id")
    p_activity.add_argument("--page", type=int, default=1)
    p_activity.add_argument("--limit", type=int, default=20)

    p_price = subparsers.add_parser("price-history", help="Get price history")
    p_price.add_argument("market_id")

    p_traders = subparsers.add_parser("traders", help="Get market traders")
    p_traders.add_argument("market_id")
    p_traders.add_argument("--page", type=int, default=1)
    p_traders.add_argument("--limit", type=int, default=20)

    # ========== TRADE ==========
    p_quote = subparsers.add_parser("quote", help="Get a quote")
    p_quote.add_argument("market_id")
    p_quote.add_argument("option_id")
    p_quote.add_argument("amount", type=int)
    p_quote.add_argument("--action", choices=["buy", "sell"], default="buy")

    p_buy = subparsers.add_parser("buy", help="Buy shares")
    p_buy.add_argument("market_id")
    p_buy.add_argument("option_id")
    p_buy.add_argument("amount", type=int)

    p_sell = subparsers.add_parser("sell", help="Sell shares")
    p_sell.add_argument("market_id")
    p_sell.add_argument("option_id")
    p_sell.add_argument("shares", type=int)

    p_claim_settlement = subparsers.add_parser("claim", help="Claim settlement reward")
    p_claim_settlement.add_argument("market_id")

    p_positions = subparsers.add_parser("positions", help="Get positions")
    p_positions.add_argument("--page", type=int, default=1)
    p_positions.add_argument("--limit", type=int, default=20)

    p_history = subparsers.add_parser("trade-history", help="Get trade history")
    p_history.add_argument("--page", type=int, default=1)
    p_history.add_argument("--limit", type=int, default=20)

    # ========== USER ==========
    p_profile = subparsers.add_parser("profile", help="Get user profile")
    p_profile.add_argument("user_id", help="User ID (use 'me' for current user)")

    p_leader = subparsers.add_parser("leaderboard", help="Get leaderboard")
    p_leader.add_argument("--page", type=int, default=1)
    p_leader.add_argument("--limit", type=int, default=20)
    p_leader.add_argument("--timeframe", default="all")

    p_followers = subparsers.add_parser("followers", help="Get user followers")
    p_followers.add_argument("user_id")
    p_followers.add_argument("--page", type=int, default=1)
    p_followers.add_argument("--limit", type=int, default=20)

    p_following = subparsers.add_parser("following", help="Get users followed by user")
    p_following.add_argument("user_id")
    p_following.add_argument("--page", type=int, default=1)
    p_following.add_argument("--limit", type=int, default=20)

    p_favs = subparsers.add_parser("favorites", help="Get user favorites")
    p_favs.add_argument("user_id", help="User ID (use 'me' for current user)")
    p_favs.add_argument("--page", type=int, default=1)
    p_favs.add_argument("--limit", type=int, default=20)

    p_follow = subparsers.add_parser("follow", help="Follow a user")
    p_follow.add_argument("user_id")

    p_unfollow = subparsers.add_parser("unfollow", help="Unfollow a user")
    p_unfollow.add_argument("user_id")

    p_set_avatar = subparsers.add_parser("set-avatar", help="Set user avatar (provide URL or index from default avatars)")
    p_set_avatar.add_argument("avatar", help="Avatar URL or index (0-5)")

    p_default_avatars = subparsers.add_parser("default-avatars", help="List default avatars")

    p_block = subparsers.add_parser("block", help="Block a user")
    p_block.add_argument("user_id")

    p_unblock = subparsers.add_parser("unblock", help="Unblock a user")
    p_unblock.add_argument("user_id")

    # ========== SOCIAL ==========
    p_comments = subparsers.add_parser("comments", help="Get market comments")
    p_comments.add_argument("market_id")
    p_comments.add_argument("--page", type=int, default=1)
    p_comments.add_argument("--limit", type=int, default=20)

    p_add_comment = subparsers.add_parser("add-comment", help="Add a comment")
    p_add_comment.add_argument("market_id")
    p_add_comment.add_argument("content")

    p_del_comment = subparsers.add_parser("delete-comment", help="Delete a comment")
    p_del_comment.add_argument("market_id")
    p_del_comment.add_argument("comment_id")

    p_fav = subparsers.add_parser("favorite", help="Favorite a market")
    p_fav.add_argument("market_id")

    p_unfav = subparsers.add_parser("unfavorite", help="Unfavorite a market")
    p_unfav.add_argument("market_id")

    # ========== CHALLENGES ==========
    subparsers.add_parser("challenges", help="List challenges")

    p_claim = subparsers.add_parser("claim-challenge", help="Claim challenge reward")
    p_claim.add_argument("challenge_id")

    # ========== ORACLE ==========
    p_oracle = subparsers.add_parser("oracle-status", help="Get oracle status")
    p_oracle.add_argument("prediction_id")

    p_assert = subparsers.add_parser("assert", help="Assert prediction result")
    p_assert.add_argument("prediction_id")
    p_assert.add_argument("option_id")

    p_dispute = subparsers.add_parser("dispute", help="Dispute prediction result")
    p_dispute.add_argument("prediction_id")
    p_dispute.add_argument("option_id")

    p_vote = subparsers.add_parser("vote", help="Vote on prediction result")
    p_vote.add_argument("prediction_id")
    p_vote.add_argument("option_id")

    p_settle = subparsers.add_parser("settle", help="Settle prediction")
    p_settle.add_argument("prediction_id")
    p_settle.add_argument("winner_option_id")

    # ========== CATEGORIES ==========
    subparsers.add_parser("categories", help="List categories")

    # ========== CREATION ==========
    p_create = subparsers.add_parser("create-market", help="Create a new market")
    p_create.add_argument("--title", required=True)
    p_create.add_argument("--options", nargs="+", required=True)
    p_create.add_argument("--probs", type=int, nargs="+", required=True, help="Initial probabilities (0-100), sum must be 100")
    p_create.add_argument("--end-time", required=True, help="ISO8601 string")
    p_create.add_argument("--description")
    p_create.add_argument("--images", nargs="+", help="Image URLs")

    p_upload = subparsers.add_parser("upload", help="Upload an image")
    p_upload.add_argument("file", help="Path to image file")
    p_upload.add_argument("--type", default="image/jpeg")
    p_upload.add_argument("--ext", default="jpg")

    p_share = subparsers.add_parser("create-share-link", help="Create a share link for a topic/market")
    p_share.add_argument("market_id", help="Market ID")
    p_share.add_argument("--image-url", help="Custom image URL")
    p_share.add_argument("--share-source", help="Share source (e.g., market_detail, market_list)")
    p_share.add_argument("--share-target", help="Share target (e.g., wechat_friend, wechat_moments, x, telegram, whatsapp)")

    args = parser.parse_args()
    
    # Check for required environment variables
    missing = []
    if not os.getenv("SEESAW_BASE_URL"): missing.append("SEESAW_BASE_URL")
    if not os.getenv("SEESAW_API_KEY"): missing.append("SEESAW_API_KEY")
    if not os.getenv("SEESAW_API_SECRET"): missing.append("SEESAW_API_SECRET")
    
    if missing:
        print("\n" + "!" * 50)
        print("ERROR: SEESAW-AGENT IS UNINITIALIZED")
        print("!" * 50)
        print(f"Missing environment variables: {', '.join(missing)}")
        print("\nTo initialize, add these variables to your OpenClaw Gateway Config:")
        print("  - Use `gateway config.patch` to add them to 'env.vars'.")
        print("  - Or edit `openclaw.json` directly.")
        print("\nExample:")
        print("  gateway config.patch '{\"env\": {\"vars\": {\"SEESAW_BASE_URL\": \"https://app.seesaw.fun/v1\"}}}'")
        print("!" * 50 + "\n")
        sys.exit(1)

    client = SeesawClient()

    try:
        if args.command == "balance":
            print(json.dumps(client.get_balance(), indent=2))
        elif args.command == "transactions":
            print(json.dumps(client.get_transactions(args.page, args.limit), indent=2))
        elif args.command == "credit-history":
            print(json.dumps(client.get_credit_history(args.page, args.limit), indent=2))
        elif args.command == "monthly-card-status":
            print(json.dumps(client.get_monthly_card_status(), indent=2))
        elif args.command == "list-markets":
            print(json.dumps(client.list_markets(args.page, args.limit, args.status, args.category_id), indent=2))
        elif args.command == "get-market":
            print(json.dumps(client.get_market(args.id), indent=2))
        elif args.command == "market-activity":
            print(json.dumps(client.get_market_activity(args.market_id, args.page, args.limit), indent=2))
        elif args.command == "price-history":
            print(json.dumps(client.get_price_history(args.market_id), indent=2))
        elif args.command == "traders":
            print(json.dumps(client.get_traders(args.market_id, args.page, args.limit), indent=2))
        elif args.command == "quote":
            print(json.dumps(client.get_quote(args.market_id, args.option_id, args.amount, args.action), indent=2))
        elif args.command == "buy":
            print(json.dumps(client.buy(args.market_id, args.option_id, args.amount), indent=2))
        elif args.command == "sell":
            print(json.dumps(client.sell(args.market_id, args.option_id, args.shares), indent=2))
        elif args.command == "positions":
            print(json.dumps(client.get_positions(args.page, args.limit), indent=2))
        elif args.command == "trade-history":
            print(json.dumps(client.get_trade_history(args.page, args.limit), indent=2))
        elif args.command == "profile":
            print(json.dumps(client.get_profile(args.user_id), indent=2))
        elif args.command == "leaderboard":
            print(json.dumps(client.get_leaderboard(args.page, args.limit, args.timeframe), indent=2))
        elif args.command == "followers":
            print(json.dumps(client.get_followers(args.user_id, args.page, args.limit), indent=2))
        elif args.command == "following":
            print(json.dumps(client.get_following(args.user_id, args.page, args.limit), indent=2))
        elif args.command == "favorites":
            print(json.dumps(client.get_favorites(args.user_id, args.page, args.limit), indent=2))
        elif args.command == "follow":
            print(json.dumps(client.follow(args.user_id), indent=2))
        elif args.command == "unfollow":
            print(json.dumps(client.unfollow(args.user_id), indent=2))
        elif args.command == "set-avatar":
            avatar_url = args.avatar
            # If it's a number, use default avatars
            if avatar_url.isdigit():
                idx = int(avatar_url)
                avatars = client.get_default_avatars().get("avatars", [])
                if idx < len(avatars):
                    avatar_url = avatars[idx]
                else:
                    print(f"Invalid index. Available: 0-{len(avatars)-1}")
                    return
            print(json.dumps(client.update_avatar(avatar_url), indent=2))
        elif args.command == "default-avatars":
            print(json.dumps(client.get_default_avatars(), indent=2))
        elif args.command == "block":
            print(json.dumps(client.block(args.user_id), indent=2))
        elif args.command == "unblock":
            print(json.dumps(client.unblock(args.user_id), indent=2))
        elif args.command == "comments":
            print(json.dumps(client.get_comments(args.market_id, args.page, args.limit), indent=2))
        elif args.command == "add-comment":
            print(json.dumps(client.add_comment(args.market_id, args.content), indent=2))
        elif args.command == "delete-comment":
            print(json.dumps(client.delete_comment(args.market_id, args.comment_id), indent=2))
        elif args.command == "favorite":
            print(json.dumps(client.favorite(args.market_id), indent=2))
        elif args.command == "unfavorite":
            print(json.dumps(client.unfavorite(args.market_id), indent=2))
        elif args.command == "challenges":
            print(json.dumps(client.list_challenges(), indent=2))
        elif args.command == "claim-challenge":
            print(json.dumps(client.claim_challenge(args.challenge_id), indent=2))
        elif args.command == "oracle-status":
            print(json.dumps(client.get_oracle_status(args.prediction_id), indent=2))
        elif args.command == "assert":
            print(json.dumps(client.assert_result(args.prediction_id, args.option_id), indent=2))
        elif args.command == "dispute":
            print(json.dumps(client.dispute_result(args.prediction_id, args.option_id), indent=2))
        elif args.command == "vote":
            print(json.dumps(client.vote(args.prediction_id, args.option_id), indent=2))
        elif args.command == "settle":
            print(json.dumps(client.settle(args.prediction_id, args.winner_option_id), indent=2))
        elif args.command == "categories":
            print(json.dumps(client.list_categories(), indent=2))
        elif args.command == "create-market":
            if len(args.probs) != len(args.options):
                print(f"Error: Number of initial probabilities ({len(args.probs)}) must match number of options ({len(args.options)})", file=sys.stderr)
                sys.exit(1)
            if sum(args.probs) != 100:
                print(f"Error: Initial probabilities must sum to 100 (current sum: {sum(args.probs)})", file=sys.stderr)
                sys.exit(1)
            print(json.dumps(client.create_market(args.title, args.options, args.probs, args.end_time, args.description, args.images), indent=2))
        elif args.command == "upload":
            presigned = client.get_presigned_url(args.type, args.ext)
            client.upload_file(presigned["upload_url"], args.file, args.type)
            print(json.dumps({"file_url": presigned["file_url"]}, indent=2))
        elif args.command == "create-share-link":
            print(json.dumps(client.create_share_link(args.market_id, args.image_url, args.share_source, args.share_target), indent=2))
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
