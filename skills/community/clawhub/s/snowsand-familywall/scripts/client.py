"""
FamilyWall API Client

Based on reverse-engineering of the FamilyWall API at https://api.familywall.com
Authentication is session-based using JSESSIONID cookies.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from urllib.parse import urlencode

try:
    import requests
except ImportError:
    # Use urllib as fallback
    import urllib.request
    import urllib.parse
    import http.cookiejar

    requests = None


class FamilyWallClient:
    """Client for interacting with the FamilyWall API."""

    BASE_URL = "https://api.familywall.com/api"
    PARTNER_SCOPE = "Family"

    def __init__(self, timezone=None):
        self.timezone = timezone or "America/Chicago"
        self.jsessionid = None
        self.account_id = None
        self.family_id = None
        self._session = None

        if requests:
            self._session = requests.Session()
            self._session.headers.update({
                "accept": "application/json, text/javascript, */*; q=0.01",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Referer": "https://www.familywall.com/",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            })

    def _api_call(self, endpoint, params=None, method="POST"):
        """Make an API call to FamilyWall."""
        if params is None:
            params = {}
        params["partnerScope"] = self.PARTNER_SCOPE

        url = f"{self.BASE_URL}/{endpoint}"
        body = urlencode(params, doseq=True)

        headers = {}
        if self.jsessionid:
            headers["tokencsrf"] = self.jsessionid
            headers["Cookie"] = f"JSESSIONID={self.jsessionid}"

        if requests and self._session:
            try:
                resp = self._session.post(url, data=body, headers=headers, timeout=30)
                if resp.status_code == 200:
                    try:
                        return resp.json()
                    except json.JSONDecodeError:
                        return {"raw": resp.text}
                else:
                    return {"error": f"HTTP {resp.status_code}", "body": resp.text[:500]}
            except Exception as e:
                return {"error": str(e)}
        else:
            # Fallback to urllib
            try:
                req = urllib.request.Request(url, data=body.encode("utf-8"), method=method)
                req.add_header("accept", "application/json, text/javascript, */*; q=0.01")
                req.add_header("content-type", "application/x-www-form-urlencoded; charset=UTF-8")
                req.add_header("Referer", "https://www.familywall.com/")
                if self.jsessionid:
                    req.add_header("tokencsrf", self.jsessionid)
                    req.add_header("Cookie", f"JSESSIONID={self.jsessionid}")

                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = resp.read().decode("utf-8")
                    try:
                        return json.loads(data)
                    except json.JSONDecodeError:
                        return {"raw": data}
            except Exception as e:
                return {"error": str(e)}

    def login(self, email, password):
        """Authenticate with FamilyWall."""
        params = {
            "a01call": "log2get",
            "transactional": "true",
            "a00generateAutologinToken": "true",
            "a00identifier": email,
            "a00password": password,
        }

        result = self._api_call("log2in", params)
        if not result:
            return False

        login_info = result.get("a00", {}).get("r", {}).get("r", {})
        if not login_info or "accountId" not in login_info:
            # Check for error
            error = result.get("a00", {}).get("ex", {}).get("ex", {})
            if error:
                print(json.dumps({"error": error.get("message", "Login failed")}), file=sys.stderr)
            return False

        self.account_id = login_info["accountId"]
        self.jsessionid = login_info.get("tokenCsrf")

        # Check if user has a family
        if login_info.get("hasFamily") == "true":
            # Get family ID
            families = result.get("a02", {}).get("r", {}).get("r", [])
            if families:
                self.family_id = families[0].get("family_id")

        return True

    def get_all_family(self):
        """Get all family data including members, profiles, settings, threads."""
        params = {
            "a01call": "prfgetProfiles",
            "a02call": "famlistfamily",
            "a03call": "settingsgetperfamily",
            "a04call": "famshowincominginvite",
            "a05call": "imthreadlist",
            "a05isLoggedFamily": "false",
            "a06call": "accgetstate",
            "a06deviceId": "openclaw-agent",
            "a06modelType": "WebFirebase",
            "a06applicationVersion": "",
            "a06timezone": self.timezone,
        }

        result = self._api_call("accgetallfamily", params)

        # Extract family_id if we don't have it
        if result and not self.family_id:
            families = result.get("a02", {}).get("r", {}).get("r", [])
            if families:
                self.family_id = families[0].get("family_id")

        return result

    # --- Calendar / Events ---

    def get_events(self, days=7, start=None, end=None):
        """Get calendar events for a date range."""
        if not start:
            start = datetime.now().strftime("%Y-%m-%dT00:00:00.000Z")
        if not end:
            end_date = datetime.now() + timedelta(days=days)
            end = end_date.strftime("%Y-%m-%dT23:59:59.000Z")

        params = {
            "a00from": start,
            "a00to": end,
        }

        result = self._api_call("evtlistinterval", params)
        if not result:
            return None

        # Check for error
        if "ex" in result.get("a00", {}):
            return {"error": result["a00"]["ex"]}

        events_raw = result.get("a00", {}).get("r", {}).get("r", [])
        events = []
        for e in events_raw:
            events.append({
                "id": e.get("metaId") or e.get("eventId"),
                "title": e.get("text"),
                "description": e.get("description"),
                "start": e.get("startDate"),
                "end": e.get("endDate"),
                "allDay": e.get("allDay"),
                "location": e.get("where"),
                "recurrence": e.get("recurrency"),
                "authorId": e.get("accountId"),
                "color": e.get("color"),
                "calendarId": e.get("calendarId"),
            })

        return events

    def create_event(self, title, start, end, description=None, location=None, all_day=False):
        """Create a calendar event."""
        params = {
            "a00text": title,
            "a00startDate": start,
            "a00endDate": end,
        }

        if description:
            params["a00description"] = description
        if location:
            params["a00where"] = location
        if all_day:
            params["a00allDay"] = "true"

        result = self._api_call("evtcreate", params)
        if not result:
            return None

        if "ex" in result.get("a00", {}):
            return {"error": result["a00"]["ex"]}

        return result.get("a00", {}).get("r", {}).get("r")

    def delete_event(self, event_id):
        """Delete a calendar event."""
        params = {"a00eventId": event_id}
        result = self._api_call("evtdelete", params)
        if not result:
            return None
        if "ex" in result.get("a00", {}):
            return {"error": result["a00"]["ex"]}
        return result.get("a00", {}).get("r", {}).get("r")

    # --- Shopping Lists / Tasks ---

    def get_lists(self):
        """Get all shopping/task lists."""
        result = self._api_call("taskgettasklists", {})
        if not result:
            return None

        if "ex" in result.get("a00", {}):
            return {"error": result["a00"]["ex"]}

        lists_raw = result.get("a00", {}).get("r", {}).get("r", [])
        lists = []
        for lst in lists_raw:
            lists.append({
                "id": lst.get("metaId"),
                "name": lst.get("name"),
                "type": lst.get("type") or lst.get("taskListType"),
                "itemCount": lst.get("itemCount"),
                "checkedCount": lst.get("checkedCount"),
                "color": lst.get("color"),
            })

        return lists

    def get_list_items(self, list_id):
        """Get items from a specific list."""
        params = {"a00listId": list_id}
        result = self._api_call("tasklist", params)
        if not result:
            return None

        if "ex" in result.get("a00", {}):
            return {"error": result["a00"]["ex"]}

        items_raw = result.get("a00", {}).get("r", {}).get("r", [])
        items = []
        for item in items_raw:
            items.append({
                "id": item.get("metaId") or item.get("taskId"),
                "text": item.get("text"),
                "complete": item.get("complete"),
                "quantity": item.get("quantity"),
                "authorId": item.get("accountId"),
                "categories": [c.get("name") for c in item.get("categories", [])],
                "creationDate": item.get("creationDate"),
            })

        return {
            "list_id": list_id,
            "items": items,
        }

    def add_list_item(self, list_id, name, quantity=None):
        """Add an item to a list."""
        params = {
            "a00taskListId": list_id,
            "a00text": name,
        }
        if quantity:
            params["a00quantity"] = quantity

        result = self._api_call("taskcreate", params)
        if not result:
            return None

        if "ex" in result.get("a00", {}):
            return {"error": result["a00"]["ex"]}

        return result.get("a00", {}).get("r", {}).get("r")

    def check_list_item(self, item_id, checked=True):
        """Mark a list item as checked/unchecked."""
        params = {
            "a00taskId": item_id,
            "a00complete": "true" if checked else "false",
        }

        result = self._api_call("taskmark", params)
        if not result:
            return None

        if "ex" in result.get("a00", {}):
            return {"error": result["a00"]["ex"]}

        return result.get("a00", {}).get("r", {}).get("r")

    def create_list(self, name, list_type="SHOPPING"):
        """Create a new list."""
        params = {
            "a00name": name,
            "a00taskListType": list_type,
        }

        result = self._api_call("taskcreatelist", params)
        if not result:
            return None

        if "ex" in result.get("a00", {}):
            return {"error": result["a00"]["ex"]}

        return result.get("a00", {}).get("r", {}).get("r")

    # --- Messaging ---

    def get_threads(self):
        """Get IM threads."""
        params = {"a00isLoggedFamily": "false"}
        result = self._api_call("imthreadlist", params)
        if not result:
            return None

        if "ex" in result.get("a00", {}):
            return {"error": result["a00"]["ex"]}

        threads_raw = result.get("a00", {}).get("r", {}).get("r", [])
        threads = []
        for t in threads_raw:
            participants = []
            for p in t.get("participants", []):
                participants.append({
                    "accountId": p.get("accountId"),
                    "firstName": p.get("accountFirstname"),
                })
            threads.append({
                "id": t.get("metaId"),
                "participants": participants,
                "unreadCount": t.get("unreadCount"),
                "messageCount": t.get("messageCount"),
                "lastMessage": t.get("lastMessage"),
            })

        return threads

    def get_messages(self, thread_id, limit=20):
        """Get messages from a thread, including media attachments."""
        params = {
            "a00threadId": thread_id,
            "a00limit": str(limit),
        }

        result = self._api_call("immessagelist2", params)
        if not result:
            return None

        if "ex" in result.get("a00", {}):
            return {"error": result["a00"]["ex"]}

        data = result.get("a00", {}).get("r", {}).get("r", {})
        # immessagelist2 returns {size, datas, count, start}
        if isinstance(data, dict):
            messages_raw = data.get("datas", [])
        elif isinstance(data, list):
            messages_raw = data
        else:
            messages_raw = []

        messages = []
        for m in messages_raw:
            msg = {
                "id": m.get("metaId"),
                "text": m.get("text"),
                "authorId": m.get("fromId") or m.get("authorAccountId"),
                "authorName": m.get("authorFirstname"),
                "date": m.get("creationDate"),
                "type": m.get("type"),
            }

            # Parse media attachments
            raw_medias = m.get("medias", [])
            if raw_medias:
                msg["medias"] = []
                for media in raw_medias:
                    msg["medias"].append({
                        "mediaId": media.get("mediaId") or media.get("metaId"),
                        "name": media.get("name"),
                        "mimeType": media.get("mimeType"),
                        "size": media.get("datasize"),
                        "pictureUrl": media.get("pictureUrl"),
                        "resolutionX": media.get("resolutionX"),
                        "resolutionY": media.get("resolutionY"),
                        "durationMs": media.get("durationMs"),
                        "readystate": media.get("readystate"),
                    })

            messages.append(msg)

        return messages

    def send_message(self, thread_id, text):
        """Send a message to a thread."""
        params = {
            "a00threadId": thread_id,
            "a00text": text,
        }

        result = self._api_call("imsend", params)
        if not result:
            return None

        if "ex" in result.get("a00", {}):
            return {"error": result["a00"]["ex"]}

        return result.get("a00", {}).get("r", {}).get("r")

    # --- Media Download ---

    def download_media(self, media_url, output_path):
        """Download a media file from a FamilyWall pictureUrl.

        Args:
            media_url: The pictureUrl from a media object.
            output_path: Local path to save the file.

        Returns:
            dict with file path, size, and content_type on success; error dict on failure.
        """
        if not media_url:
            return {"error": "No media URL provided"}

        headers = {
            "Referer": "https://www.familywall.com/",
        }
        if self.jsessionid:
            headers["tokencsrf"] = self.jsessionid
            headers["Cookie"] = f"JSESSIONID={self.jsessionid}"

        # Ensure output directory exists
        out_dir = os.path.dirname(output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        if requests and self._session:
            try:
                resp = self._session.get(media_url, headers=headers, timeout=60, stream=True)
                if resp.status_code != 200:
                    return {"error": f"HTTP {resp.status_code}", "body": resp.text[:500]}

                content_type = resp.headers.get("Content-Type", "application/octet-stream")
                total = 0
                with open(output_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                        total += len(chunk)

                return {
                    "path": output_path,
                    "size": total,
                    "content_type": content_type,
                }
            except Exception as e:
                return {"error": str(e)}
        else:
            # Fallback to urllib
            try:
                req = urllib.request.Request(media_url, method="GET")
                for k, v in headers.items():
                    req.add_header(k, v)

                with urllib.request.urlopen(req, timeout=60) as resp:
                    content_type = resp.headers.get("Content-Type", "application/octet-stream")
                    data = resp.read()
                    with open(output_path, "wb") as f:
                        f.write(data)

                    return {
                        "path": output_path,
                        "size": len(data),
                        "content_type": content_type,
                    }
            except Exception as e:
                return {"error": str(e)}

    def get_media_from_message(self, thread_id, message_id=None, limit=20):
        """Get media attachments from messages in a thread.

        Args:
            thread_id: Thread ID to search.
            message_id: Optional specific message ID to filter.
            limit: Max messages to scan.

        Returns:
            List of media dicts with download URLs and metadata.
        """
        messages = self.get_messages(thread_id, limit=limit)
        if not messages or isinstance(messages, dict) and "error" in messages:
            return messages

        all_media = []
        for msg in messages:
            if message_id and msg.get("id") != message_id:
                continue
            for media in msg.get("medias", []):
                media["messageId"] = msg.get("id")
                media["messageText"] = msg.get("text")
                media["messageDate"] = msg.get("date")
                media["authorId"] = msg.get("authorId")
                all_media.append(media)

        return all_media

    # --- Location ---

    def get_locations(self):
        """Get family member locations."""
        result = self._api_call("locgetpositions2", {})
        if not result:
            return None

        if "ex" in result.get("a00", {}):
            return {"error": result["a00"]["ex"]}

        locations_raw = result.get("a00", {}).get("r", {}).get("r", [])
        locations = []
        if isinstance(locations_raw, list):
            for loc in locations_raw:
                locations.append({
                    "accountId": loc.get("accountId"),
                    "firstName": loc.get("firstName"),
                    "latitude": loc.get("latitude"),
                    "longitude": loc.get("longitude"),
                    "accuracy": loc.get("accuracy"),
                    "date": loc.get("date"),
                    "address": loc.get("address"),
                })
        elif isinstance(locations_raw, dict):
            # Might return a dict keyed by account ID
            for key, loc in locations_raw.items():
                locations.append({
                    "accountId": loc.get("accountId", key),
                    "firstName": loc.get("firstName"),
                    "latitude": loc.get("latitude"),
                    "longitude": loc.get("longitude"),
                    "accuracy": loc.get("accuracy"),
                    "date": loc.get("date"),
                    "address": loc.get("address"),
                })

        return locations

    # --- Wall / Feed ---

    def get_wall(self, limit=20, offset=0):
        """Get family wall/feed posts."""
        params = {
            "a00limit": str(limit),
            "a00offset": str(offset),
        }

        result = self._api_call("wallactivityget", params)
        if not result:
            return None

        if "ex" in result.get("a00", {}):
            return {"error": result["a00"]["ex"]}

        posts_raw = result.get("a00", {}).get("r", {}).get("r", [])
        posts = []
        for p in posts_raw:
            post = {
                "id": p.get("metaId"),
                "type": p.get("type"),
                "text": p.get("description") or p.get("tagline"),
                "authorId": p.get("authorAccountId"),
                "authorName": p.get("authorFirstname"),
                "date": p.get("creationDate"),
                "comments": p.get("commentCount"),
                "likes": p.get("likeCount"),
            }

            # Include media attachments if present
            raw_medias = p.get("medias", [])
            if raw_medias:
                post["medias"] = []
                for media in raw_medias:
                    post["medias"].append({
                        "mediaId": media.get("mediaId") or media.get("metaId"),
                        "name": media.get("name"),
                        "mimeType": media.get("mimeType"),
                        "size": media.get("datasize"),
                        "pictureUrl": media.get("pictureUrl"),
                        "resolutionX": media.get("resolutionX"),
                        "resolutionY": media.get("resolutionY"),
                        "durationMs": media.get("durationMs"),
                        "readystate": media.get("readystate"),
                    })

            posts.append(post)

        return posts
