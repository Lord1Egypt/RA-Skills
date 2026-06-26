#!/usr/bin/env python3
"""
FamilyWall CLI - OpenClaw Skill
Interact with the FamilyWall family organization platform.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta

# Add the scripts directory to path for local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from client import FamilyWallClient


def get_client():
    """Create and authenticate a FamilyWall client from environment variables."""
    email = os.environ.get("FAMILYWALL_EMAIL")
    password = os.environ.get("FAMILYWALL_PASSWORD")

    if not email or not password:
        print(json.dumps({"error": "FAMILYWALL_EMAIL and FAMILYWALL_PASSWORD must be set"}))
        sys.exit(1)

    client = FamilyWallClient()
    success = client.login(email, password)
    if not success:
        print(json.dumps({"error": "Failed to authenticate with FamilyWall"}))
        sys.exit(1)

    return client


def cmd_status(args):
    """Show account and family status."""
    client = get_client()
    data = client.get_all_family()
    if not data:
        print(json.dumps({"error": "Failed to get family data"}))
        return

    result = {
        "account_id": client.account_id,
        "family": None,
        "members": [],
        "settings": None,
    }

    # Family info
    families = data.get("a02", {}).get("r", {}).get("r", [])
    if families:
        fam = families[0]
        result["family"] = {
            "name": fam.get("name"),
            "family_id": fam.get("family_id"),
        }
        members = fam.get("members", [])
        for m in members:
            identifiers = m.get("identifiers", [])
            email_id = next((i["value"] for i in identifiers if i.get("type") == "Email"), None)
            result["members"].append({
                "firstName": m.get("firstName"),
                "email": email_id,
                "role": m.get("role"),
                "accountId": m.get("accountId"),
            })

    # Settings
    settings = data.get("a03", {}).get("r", {}).get("r")
    if settings:
        result["settings"] = {
            "geolocSharing": settings.get("geolocSharing"),
            "calendarFirstDayOfWeek": settings.get("calendarFirstDayOfWeek"),
            "defaultReminderValue": settings.get("defaultReminderValue"),
        }

    print(json.dumps(result, indent=2))


def cmd_members(args):
    """List family members."""
    client = get_client()
    data = client.get_all_family()
    if not data:
        print(json.dumps({"error": "Failed to get family data"}))
        return

    families = data.get("a02", {}).get("r", {}).get("r", [])
    if not families:
        print(json.dumps({"error": "No family found"}))
        return

    members = []
    for m in families[0].get("members", []):
        identifiers = m.get("identifiers", [])
        email_id = next((i["value"] for i in identifiers if i.get("type") == "Email"), None)
        phone_id = next((i["value"] for i in identifiers if i.get("type") == "Msisdn"), None)
        members.append({
            "firstName": m.get("firstName"),
            "email": email_id,
            "phone": phone_id,
            "role": m.get("role"),
            "accountId": m.get("accountId"),
            "lastLoginDate": m.get("lastLoginDate"),
            "color": m.get("color"),
        })

    print(json.dumps(members, indent=2))


# --- Calendar / Events ---

def cmd_events_list(args):
    """List upcoming calendar events."""
    client = get_client()
    days = args.days if args.days else 7
    events = client.get_events(days=days)
    if events is None:
        print(json.dumps({"error": "Failed to get events"}))
        return
    print(json.dumps(events, indent=2))


def cmd_events_create(args):
    """Create a calendar event."""
    client = get_client()
    result = client.create_event(
        title=args.title,
        start=args.start,
        end=args.end,
        description=args.description,
        location=args.location,
        all_day=args.allday,
    )
    if result is None:
        print(json.dumps({"error": "Failed to create event"}))
        return
    print(json.dumps(result, indent=2))


def cmd_events_delete(args):
    """Delete a calendar event."""
    client = get_client()
    result = client.delete_event(args.event_id)
    if result is None:
        print(json.dumps({"error": "Failed to delete event"}))
        return
    print(json.dumps({"deleted": True, "event_id": args.event_id}))


# --- Shopping Lists / Tasks ---

def cmd_lists(args):
    """List all shopping/task lists."""
    client = get_client()
    lists = client.get_lists()
    if lists is None:
        print(json.dumps({"error": "Failed to get lists"}))
        return
    print(json.dumps(lists, indent=2))


def cmd_list_items(args):
    """Get items from a specific list."""
    client = get_client()
    items = client.get_list_items(args.list_id)
    if items is None:
        print(json.dumps({"error": "Failed to get list items"}))
        return
    print(json.dumps(items, indent=2))


def cmd_list_add_item(args):
    """Add an item to a list."""
    client = get_client()
    result = client.add_list_item(args.list_id, args.name, quantity=args.quantity)
    if result is None:
        print(json.dumps({"error": "Failed to add item"}))
        return
    print(json.dumps(result, indent=2))


def cmd_list_check_item(args):
    """Mark a list item as checked/purchased."""
    client = get_client()
    result = client.check_list_item(args.item_id, checked=not args.uncheck)
    if result is None:
        print(json.dumps({"error": "Failed to update item"}))
        return
    print(json.dumps(result, indent=2))


def cmd_list_create(args):
    """Create a new list."""
    client = get_client()
    result = client.create_list(args.name, list_type=args.type)
    if result is None:
        print(json.dumps({"error": "Failed to create list"}))
        return
    print(json.dumps(result, indent=2))


# --- Messaging ---

def cmd_threads(args):
    """List IM threads."""
    client = get_client()
    threads = client.get_threads()
    if threads is None:
        print(json.dumps({"error": "Failed to get threads"}))
        return
    print(json.dumps(threads, indent=2))


def cmd_messages(args):
    """Get messages from a thread."""
    client = get_client()
    messages = client.get_messages(args.thread_id, limit=args.limit)
    if messages is None:
        print(json.dumps({"error": "Failed to get messages"}))
        return
    print(json.dumps(messages, indent=2))


def cmd_send_message(args):
    """Send a message to a thread."""
    client = get_client()
    result = client.send_message(args.thread_id, args.text)
    if result is None:
        print(json.dumps({"error": "Failed to send message"}))
        return
    print(json.dumps(result, indent=2))


# --- Media ---

def cmd_media_list(args):
    """List media attachments from a thread."""
    client = get_client()
    media = client.get_media_from_message(
        args.thread_id,
        message_id=args.message_id,
        limit=args.limit,
    )
    if media is None:
        print(json.dumps({"error": "Failed to get media"}))
        return
    print(json.dumps(media, indent=2))


def cmd_media_download(args):
    """Download a media file."""
    client = get_client()

    output = args.output
    if not output:
        # If downloading by URL, derive filename from URL or use generic
        if args.url:
            output = args.url.rsplit("/", 1)[-1].split("?")[0] or "download"
        elif args.media_id:
            output = args.media_id.replace("/", "_")
        else:
            output = "download"

    # If we have a direct URL, download it
    if args.url:
        result = client.download_media(args.url, output)
        print(json.dumps(result, indent=2))
        return

    # If we have a media_id and thread_id, find the URL
    if args.media_id and args.thread_id:
        all_media = client.get_media_from_message(args.thread_id, limit=50)
        if isinstance(all_media, dict) and "error" in all_media:
            print(json.dumps(all_media, indent=2))
            return

        target = None
        for m in (all_media or []):
            if m.get("mediaId") == args.media_id:
                target = m
                break

        if not target:
            print(json.dumps({"error": f"Media {args.media_id} not found in thread {args.thread_id}"}))
            return

        # Use original filename if output wasn't explicitly set
        if not args.output and target.get("name"):
            output = target["name"]

        result = client.download_media(target["pictureUrl"], output)
        print(json.dumps(result, indent=2))
        return

    print(json.dumps({"error": "Provide --url or both --media-id and --thread-id"}))


def cmd_media_download_all(args):
    """Download all media from a thread."""
    client = get_client()
    all_media = client.get_media_from_message(
        args.thread_id,
        message_id=args.message_id,
        limit=args.limit,
    )

    if isinstance(all_media, dict) and "error" in all_media:
        print(json.dumps(all_media, indent=2))
        return

    if not all_media:
        print(json.dumps({"message": "No media found", "count": 0}))
        return

    output_dir = args.output_dir or "."
    os.makedirs(output_dir, exist_ok=True)

    results = []
    for media in all_media:
        url = media.get("pictureUrl")
        if not url:
            continue

        filename = media.get("name") or media.get("mediaId", "file").replace("/", "_")
        # Avoid collisions by prepending media ID
        mid = (media.get("mediaId") or "").replace("/", "_")
        safe_name = f"{mid}_{filename}" if mid else filename
        out_path = os.path.join(output_dir, safe_name)

        result = client.download_media(url, out_path)
        result["mediaId"] = media.get("mediaId")
        result["mimeType"] = media.get("mimeType")
        result["originalName"] = media.get("name")
        results.append(result)

    print(json.dumps({"downloaded": len(results), "files": results}, indent=2))


# --- Meal Planner ---

def cmd_meals_list(args):
    """List meal plan for a date range."""
    client = get_client()
    meals = client.get_meal_plan(start=args.start, end=args.end, days=args.days)
    if meals is None:
        print(json.dumps({"error": "Failed to get meal plan"}))
        return
    print(json.dumps(meals, indent=2))


def cmd_meals_add(args):
    """Add a meal to the plan."""
    client = get_client()
    result = client.add_meal(args.name, args.date, meal_type=args.type)
    if result is None:
        print(json.dumps({"error": "Failed to add meal"}))
        return
    print(json.dumps(result, indent=2))


def cmd_recipe_create(args):
    """Create a recipe."""
    client = get_client()
    result = client.create_recipe(
        name=args.name,
        ingredients=args.ingredients,
        instructions=args.instructions,
        prep_time=args.prep_time,
        cook_time=args.cook_time,
        serves=args.serves,
        description=args.description,
    )
    if result is None:
        print(json.dumps({"error": "Failed to create recipe"}))
        return
    print(json.dumps(result, indent=2))


def cmd_recipe_from_url(args):
    """Create a recipe from a URL."""
    client = get_client()
    result = client.create_recipe_from_url(args.url, category=args.category)
    if result is None:
        print(json.dumps({"error": "Failed to create recipe from URL"}))
        return
    print(json.dumps(result, indent=2))


def cmd_recipe_categories(args):
    """List recipe categories."""
    client = get_client()
    categories = client.get_recipe_categories()
    if categories is None:
        print(json.dumps({"error": "Failed to get categories"}))
        return
    print(json.dumps(categories, indent=2))


# --- Location ---

def cmd_locations(args):
    """Get family member locations."""
    client = get_client()
    locations = client.get_locations()
    if locations is None:
        print(json.dumps({"error": "Failed to get locations"}))
        return
    print(json.dumps(locations, indent=2))


# --- Wall / Feed ---

def cmd_wall(args):
    """Get family wall/feed."""
    client = get_client()
    wall = client.get_wall(limit=args.limit)
    if wall is None:
        print(json.dumps({"error": "Failed to get wall"}))
        return
    print(json.dumps(wall, indent=2))


def main():
    parser = argparse.ArgumentParser(description="FamilyWall CLI for OpenClaw")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Status
    subparsers.add_parser("status", help="Show account and family status")

    # Members
    subparsers.add_parser("members", help="List family members")

    # Events
    events_parser = subparsers.add_parser("events", help="Calendar events")
    events_sub = events_parser.add_subparsers(dest="events_command")

    events_list = events_sub.add_parser("list", help="List upcoming events")
    events_list.add_argument("--days", type=int, default=7, help="Number of days ahead")

    events_create = events_sub.add_parser("create", help="Create a new event")
    events_create.add_argument("title", help="Event title")
    events_create.add_argument("--start", required=True, help="Start datetime (ISO format)")
    events_create.add_argument("--end", required=True, help="End datetime (ISO format)")
    events_create.add_argument("--description", help="Event description")
    events_create.add_argument("--location", help="Event location")
    events_create.add_argument("--allday", action="store_true", help="All-day event")

    events_delete = events_sub.add_parser("delete", help="Delete an event")
    events_delete.add_argument("event_id", help="Event ID to delete")

    # Lists
    lists_parser = subparsers.add_parser("lists", help="Shopping/task lists")
    lists_sub = lists_parser.add_subparsers(dest="lists_command")

    lists_sub.add_parser("list", help="List all lists")

    list_items = lists_sub.add_parser("items", help="Get items from a list")
    list_items.add_argument("list_id", help="List ID")

    list_add = lists_sub.add_parser("add", help="Add item to a list")
    list_add.add_argument("list_id", help="List ID")
    list_add.add_argument("name", help="Item name")
    list_add.add_argument("--quantity", help="Item quantity")

    list_check = lists_sub.add_parser("check", help="Check/uncheck an item")
    list_check.add_argument("item_id", help="Item ID")
    list_check.add_argument("--uncheck", action="store_true", help="Uncheck instead of check")

    list_create = lists_sub.add_parser("create", help="Create a new list")
    list_create.add_argument("name", help="List name")
    list_create.add_argument("--type", default="SHOPPING", help="List type (SHOPPING or TODO)")

    # Messaging
    msg_parser = subparsers.add_parser("messages", help="Family messaging")
    msg_sub = msg_parser.add_subparsers(dest="msg_command")

    msg_sub.add_parser("threads", help="List message threads")

    msg_read = msg_sub.add_parser("read", help="Read messages from a thread")
    msg_read.add_argument("thread_id", help="Thread ID")
    msg_read.add_argument("--limit", type=int, default=20, help="Number of messages")

    msg_send = msg_sub.add_parser("send", help="Send a message")
    msg_send.add_argument("thread_id", help="Thread ID")
    msg_send.add_argument("text", help="Message text")

    # Media
    media_parser = subparsers.add_parser("media", help="Media downloading")
    media_sub = media_parser.add_subparsers(dest="media_command")

    media_list = media_sub.add_parser("list", help="List media in a thread")
    media_list.add_argument("thread_id", help="Thread ID")
    media_list.add_argument("--message-id", help="Filter to specific message ID")
    media_list.add_argument("--limit", type=int, default=20, help="Max messages to scan")

    media_dl = media_sub.add_parser("download", help="Download a media file")
    media_dl.add_argument("--url", help="Direct media pictureUrl")
    media_dl.add_argument("--media-id", help="Media ID (requires --thread-id)")
    media_dl.add_argument("--thread-id", help="Thread ID (used with --media-id)")
    media_dl.add_argument("-o", "--output", help="Output file path")

    media_dl_all = media_sub.add_parser("download-all", help="Download all media from a thread")
    media_dl_all.add_argument("thread_id", help="Thread ID")
    media_dl_all.add_argument("--message-id", help="Filter to specific message ID")
    media_dl_all.add_argument("--output-dir", default=".", help="Output directory")
    media_dl_all.add_argument("--limit", type=int, default=50, help="Max messages to scan")

    # Meals
    meals_parser = subparsers.add_parser("meals", help="Meal planner")
    meals_sub = meals_parser.add_subparsers(dest="meals_command")

    meals_list = meals_sub.add_parser("list", help="List meal plan")
    meals_list.add_argument("--days", type=int, default=7, help="Number of days ahead")
    meals_list.add_argument("--start", help="Start date (YYYY-MM-DD)")
    meals_list.add_argument("--end", help="End date (YYYY-MM-DD)")

    meals_add = meals_sub.add_parser("add", help="Add a meal to the plan")
    meals_add.add_argument("name", help="Dish name")
    meals_add.add_argument("--date", required=True, help="Date (YYYY-MM-DD)")
    meals_add.add_argument("--type", default="DINNER", help="Meal type: BREAKFAST, LUNCH, DINNER, SNACK")

    # Recipes
    recipe_parser = subparsers.add_parser("recipes", help="Recipe management")
    recipe_sub = recipe_parser.add_subparsers(dest="recipe_command")

    recipe_sub.add_parser("categories", help="List recipe categories")

    recipe_create = recipe_sub.add_parser("create", help="Create a recipe")
    recipe_create.add_argument("name", help="Recipe name")
    recipe_create.add_argument("--ingredients", help="Ingredients (newline-separated)")
    recipe_create.add_argument("--instructions", help="Instructions")
    recipe_create.add_argument("--prep-time", type=int, help="Prep time in minutes")
    recipe_create.add_argument("--cook-time", type=int, help="Cook time in minutes")
    recipe_create.add_argument("--serves", type=int, help="Number of servings")
    recipe_create.add_argument("--description", help="Description")

    recipe_url = recipe_sub.add_parser("from-url", help="Create recipe from URL")
    recipe_url.add_argument("url", help="Recipe URL to scrape")
    recipe_url.add_argument("--category", help="Category")

    # Location
    subparsers.add_parser("locations", help="Get family member locations")

    # Wall
    wall_parser = subparsers.add_parser("wall", help="Get family wall/feed")
    wall_parser.add_argument("--limit", type=int, default=20, help="Number of posts")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "status":
        cmd_status(args)
    elif args.command == "members":
        cmd_members(args)
    elif args.command == "events":
        if not args.events_command or args.events_command == "list":
            cmd_events_list(args)
        elif args.events_command == "create":
            cmd_events_create(args)
        elif args.events_command == "delete":
            cmd_events_delete(args)
    elif args.command == "lists":
        if not args.lists_command or args.lists_command == "list":
            cmd_lists(args)
        elif args.lists_command == "items":
            cmd_list_items(args)
        elif args.lists_command == "add":
            cmd_list_add_item(args)
        elif args.lists_command == "check":
            cmd_list_check_item(args)
        elif args.lists_command == "create":
            cmd_list_create(args)
    elif args.command == "messages":
        if not args.msg_command or args.msg_command == "threads":
            cmd_threads(args)
        elif args.msg_command == "read":
            cmd_messages(args)
        elif args.msg_command == "send":
            cmd_send_message(args)
    elif args.command == "media":
        if not args.media_command or args.media_command == "list":
            if not hasattr(args, 'thread_id') or not args.thread_id:
                media_parser.print_help()
                sys.exit(1)
            cmd_media_list(args)
        elif args.media_command == "download":
            cmd_media_download(args)
        elif args.media_command == "download-all":
            cmd_media_download_all(args)
    elif args.command == "meals":
        if not args.meals_command or args.meals_command == "list":
            cmd_meals_list(args)
        elif args.meals_command == "add":
            cmd_meals_add(args)
    elif args.command == "recipes":
        if not args.recipe_command or args.recipe_command == "categories":
            cmd_recipe_categories(args)
        elif args.recipe_command == "create":
            cmd_recipe_create(args)
        elif args.recipe_command == "from-url":
            cmd_recipe_from_url(args)
    elif args.command == "locations":
        cmd_locations(args)
    elif args.command == "wall":
        cmd_wall(args)


if __name__ == "__main__":
    main()
