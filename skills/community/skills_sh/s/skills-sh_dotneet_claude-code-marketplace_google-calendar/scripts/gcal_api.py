#!/usr/bin/env python3
import argparse
import json
import os
import pathlib
import sys
from typing import Any, Dict, Optional

from google.auth.transport.requests import AuthorizedSession, Request
from google.oauth2.credentials import Credentials

CALENDAR_BASE_URL = "https://www.googleapis.com/calendar/v3"
TASKS_BASE_URL = "https://tasks.googleapis.com/tasks/v1"
DEFAULT_CALENDAR_SCOPES = ["https://www.googleapis.com/auth/calendar"]
DEFAULT_TASKS_SCOPES = ["https://www.googleapis.com/auth/tasks"]


def load_json_input(raw: Optional[str], path: Optional[str]) -> Optional[Dict[str, Any]]:
    if raw and path:
        raise ValueError("Use only one of --body/--params or --body-file/--params-file")
    if path:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    if raw:
        return json.loads(raw)
    return None


def load_credentials(token_path: str, scopes: Optional[list]) -> Credentials:
    resolved = pathlib.Path(token_path).expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Token file not found: {resolved}")
    creds = Credentials.from_authorized_user_file(str(resolved), scopes=scopes)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        resolved.write_text(creds.to_json())
    return creds


def session_from_token(token_path: str, scopes: Optional[list]) -> AuthorizedSession:
    creds = load_credentials(token_path, scopes)
    return AuthorizedSession(creds)


def request(
    session: AuthorizedSession,
    method: str,
    path: str,
    params: Optional[Dict[str, Any]],
    body: Any,
    base_url: str = CALENDAR_BASE_URL,
) -> Any:
    if path.startswith("http://") or path.startswith("https://"):
        url = path
    else:
        if not path.startswith("/"):
            path = "/" + path
        url = base_url + path

    response = session.request(method=method, url=url, params=params, json=body)
    content_type = response.headers.get("Content-Type", "")

    if response.status_code >= 400:
        if "application/json" in content_type:
            error_payload = response.json()
        else:
            error_payload = {"error": response.text}
        raise RuntimeError(f"HTTP {response.status_code}: {json.dumps(error_payload, indent=2)}")

    if response.status_code == 204:
        return {"status": "deleted"}

    if "application/json" in content_type:
        return response.json()
    return {"text": response.text}


def time_object(value: str, time_zone: Optional[str]) -> Dict[str, str]:
    if "T" in value:
        obj = {"dateTime": value}
        if time_zone and ("Z" not in value and "+" not in value and "-" not in value[10:]):
            obj["timeZone"] = time_zone
        return obj
    return {"date": value}


def parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes", "y"}:
        return True
    if normalized in {"false", "0", "no", "n"}:
        return False
    raise argparse.ArgumentTypeError("Expected a boolean value (true/false).")


def add_common_auth_args(parser: argparse.ArgumentParser, default_scopes: Optional[list] = None) -> None:
    parser.add_argument(
        "--token",
        default=os.environ.get(
            "GCAL_TOKEN_PATH",
            os.path.expanduser("~/.config/google-calendar/token.json"),
        ),
        help="Path to OAuth token JSON.",
    )
    if default_scopes is None:
        default_scopes = DEFAULT_CALENDAR_SCOPES
    parser.add_argument(
        "--scopes",
        nargs="*",
        default=default_scopes,
        help="OAuth scopes (space separated).",
    )


def cmd_call(args: argparse.Namespace) -> Any:
    params = load_json_input(args.params, args.params_file)
    body = load_json_input(args.body, args.body_file)
    session = session_from_token(args.token, args.scopes)
    return request(session, args.method.upper(), args.path, params, body)


def cmd_list_calendars(args: argparse.Namespace) -> Any:
    session = session_from_token(args.token, args.scopes)
    params = {}
    if args.min_access_role:
        params["minAccessRole"] = args.min_access_role
    if args.max_results:
        params["maxResults"] = args.max_results
    if args.page_token:
        params["pageToken"] = args.page_token
    return request(session, "GET", "/users/me/calendarList", params, None)


def cmd_list_events(args: argparse.Namespace) -> Any:
    session = session_from_token(args.token, args.scopes)
    params: Dict[str, Any] = {
        "timeMin": args.time_min,
        "timeMax": args.time_max,
    }
    if args.q:
        params["q"] = args.q
    if args.single_events:
        params["singleEvents"] = True
    if args.order_by:
        params["orderBy"] = args.order_by
    if args.max_results:
        params["maxResults"] = args.max_results
    if args.time_zone:
        params["timeZone"] = args.time_zone
    if args.page_token:
        params["pageToken"] = args.page_token
    if args.fields:
        params["fields"] = args.fields

    path = f"/calendars/{args.calendar_id}/events"
    return request(session, "GET", path, params, None)


def cmd_get_event(args: argparse.Namespace) -> Any:
    session = session_from_token(args.token, args.scopes)
    params = {"fields": args.fields} if args.fields else None
    path = f"/calendars/{args.calendar_id}/events/{args.event_id}"
    return request(session, "GET", path, params, None)


def cmd_create_event(args: argparse.Namespace) -> Any:
    session = session_from_token(args.token, args.scopes)
    body = load_json_input(args.body, args.body_file)
    if body is None:
        if not args.summary or not args.start or not args.end:
            raise ValueError("--summary, --start, and --end are required unless --body is provided")
        body = {
            "summary": args.summary,
            "start": time_object(args.start, args.time_zone),
            "end": time_object(args.end, args.time_zone),
        }
        if args.location:
            body["location"] = args.location
        if args.description:
            body["description"] = args.description
        if args.attendees:
            body["attendees"] = [{"email": email} for email in args.attendees.split(",") if email]
        if args.recurrence:
            body["recurrence"] = args.recurrence

    path = f"/calendars/{args.calendar_id}/events"
    params = {"sendUpdates": args.send_updates} if args.send_updates else None
    return request(session, "POST", path, params, body)


def cmd_update_event(args: argparse.Namespace) -> Any:
    session = session_from_token(args.token, args.scopes)
    body = load_json_input(args.body, args.body_file)
    if body is None:
        body = {}
        if args.summary:
            body["summary"] = args.summary
        if args.start:
            body["start"] = time_object(args.start, args.time_zone)
        if args.end:
            body["end"] = time_object(args.end, args.time_zone)
        if args.location:
            body["location"] = args.location
        if args.description:
            body["description"] = args.description
        if args.attendees:
            body["attendees"] = [{"email": email} for email in args.attendees.split(",") if email]
        if args.recurrence:
            body["recurrence"] = args.recurrence

    if not body:
        raise ValueError("Provide fields to update or pass --body/--body-file")

    path = f"/calendars/{args.calendar_id}/events/{args.event_id}"
    params = {"sendUpdates": args.send_updates} if args.send_updates else None
    return request(session, "PATCH", path, params, body)


def cmd_delete_event(args: argparse.Namespace) -> Any:
    session = session_from_token(args.token, args.scopes)
    path = f"/calendars/{args.calendar_id}/events/{args.event_id}"
    params = {"sendUpdates": args.send_updates} if args.send_updates else None
    return request(session, "DELETE", path, params, None)


def cmd_freebusy(args: argparse.Namespace) -> Any:
    session = session_from_token(args.token, args.scopes)
    items = [{"id": cal_id} for cal_id in args.calendars.split(",") if cal_id]
    body = {
        "timeMin": args.time_min,
        "timeMax": args.time_max,
        "items": items,
    }
    if args.time_zone:
        body["timeZone"] = args.time_zone
    return request(session, "POST", "/freeBusy", None, body)


def cmd_list_tasklists(args: argparse.Namespace) -> Any:
    session = session_from_token(args.token, args.scopes)
    params: Dict[str, Any] = {}
    if args.max_results:
        params["maxResults"] = args.max_results
    if args.page_token:
        params["pageToken"] = args.page_token
    if args.fields:
        params["fields"] = args.fields
    return request(session, "GET", "/users/@me/lists", params, None, TASKS_BASE_URL)


def cmd_get_tasklist(args: argparse.Namespace) -> Any:
    session = session_from_token(args.token, args.scopes)
    params = {"fields": args.fields} if args.fields else None
    path = f"/users/@me/lists/{args.tasklist}"
    return request(session, "GET", path, params, None, TASKS_BASE_URL)


def cmd_create_tasklist(args: argparse.Namespace) -> Any:
    session = session_from_token(args.token, args.scopes)
    body = load_json_input(args.body, args.body_file)
    if body is None:
        if not args.title:
            raise ValueError("--title is required unless --body is provided")
        body = {"title": args.title}
    return request(session, "POST", "/users/@me/lists", None, body, TASKS_BASE_URL)


def cmd_update_tasklist(args: argparse.Namespace) -> Any:
    session = session_from_token(args.token, args.scopes)
    body = load_json_input(args.body, args.body_file)
    if body is None:
        body = {}
        if args.title:
            body["title"] = args.title
    if not body:
        raise ValueError("Provide fields to update or pass --body/--body-file")
    path = f"/users/@me/lists/{args.tasklist}"
    return request(session, "PATCH", path, None, body, TASKS_BASE_URL)


def cmd_delete_tasklist(args: argparse.Namespace) -> Any:
    session = session_from_token(args.token, args.scopes)
    path = f"/users/@me/lists/{args.tasklist}"
    return request(session, "DELETE", path, None, None, TASKS_BASE_URL)


def task_body_from_args(args: argparse.Namespace) -> Dict[str, Any]:
    body: Dict[str, Any] = {}
    if args.title:
        body["title"] = args.title
    if args.notes:
        body["notes"] = args.notes
    if args.due:
        body["due"] = args.due
    if args.status:
        body["status"] = args.status
    if args.completed:
        body["completed"] = args.completed
    return body


def cmd_list_tasks(args: argparse.Namespace) -> Any:
    session = session_from_token(args.token, args.scopes)
    params: Dict[str, Any] = {}
    if args.completed_max:
        params["completedMax"] = args.completed_max
    if args.completed_min:
        params["completedMin"] = args.completed_min
    if args.due_max:
        params["dueMax"] = args.due_max
    if args.due_min:
        params["dueMin"] = args.due_min
    if args.max_results:
        params["maxResults"] = args.max_results
    if args.page_token:
        params["pageToken"] = args.page_token
    if args.show_completed is not None:
        params["showCompleted"] = "true" if args.show_completed else "false"
    if args.show_deleted is not None:
        params["showDeleted"] = "true" if args.show_deleted else "false"
    if args.show_hidden is not None:
        params["showHidden"] = "true" if args.show_hidden else "false"
    if args.show_assigned is not None:
        params["showAssigned"] = "true" if args.show_assigned else "false"
    if args.updated_min:
        params["updatedMin"] = args.updated_min
    if args.fields:
        params["fields"] = args.fields
    path = f"/lists/{args.tasklist}/tasks"
    return request(session, "GET", path, params, None, TASKS_BASE_URL)


def cmd_get_task(args: argparse.Namespace) -> Any:
    session = session_from_token(args.token, args.scopes)
    params = {"fields": args.fields} if args.fields else None
    path = f"/lists/{args.tasklist}/tasks/{args.task_id}"
    return request(session, "GET", path, params, None, TASKS_BASE_URL)


def cmd_create_task(args: argparse.Namespace) -> Any:
    session = session_from_token(args.token, args.scopes)
    body = load_json_input(args.body, args.body_file)
    if body is None:
        if not args.title:
            raise ValueError("--title is required unless --body is provided")
        body = task_body_from_args(args)
    params: Dict[str, Any] = {}
    if args.parent:
        params["parent"] = args.parent
    if args.previous:
        params["previous"] = args.previous
    path = f"/lists/{args.tasklist}/tasks"
    return request(session, "POST", path, params, body, TASKS_BASE_URL)


def cmd_update_task(args: argparse.Namespace) -> Any:
    session = session_from_token(args.token, args.scopes)
    body = load_json_input(args.body, args.body_file)
    if body is None:
        body = task_body_from_args(args)
    if not body:
        raise ValueError("Provide fields to update or pass --body/--body-file")
    path = f"/lists/{args.tasklist}/tasks/{args.task_id}"
    return request(session, "PATCH", path, None, body, TASKS_BASE_URL)


def cmd_delete_task(args: argparse.Namespace) -> Any:
    session = session_from_token(args.token, args.scopes)
    path = f"/lists/{args.tasklist}/tasks/{args.task_id}"
    return request(session, "DELETE", path, None, None, TASKS_BASE_URL)


def cmd_move_task(args: argparse.Namespace) -> Any:
    session = session_from_token(args.token, args.scopes)
    params: Dict[str, Any] = {}
    if args.parent:
        params["parent"] = args.parent
    if args.previous:
        params["previous"] = args.previous
    if args.destination_tasklist:
        params["destinationTasklist"] = args.destination_tasklist
    path = f"/lists/{args.tasklist}/tasks/{args.task_id}/move"
    return request(session, "POST", path, params, None, TASKS_BASE_URL)


def cmd_clear_tasks(args: argparse.Namespace) -> Any:
    session = session_from_token(args.token, args.scopes)
    path = f"/lists/{args.tasklist}/clear"
    return request(session, "POST", path, None, None, TASKS_BASE_URL)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Google Calendar + Tasks API CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    call_parser = subparsers.add_parser("call", help="Call an arbitrary Calendar API endpoint")
    add_common_auth_args(call_parser)
    call_parser.add_argument("method", help="HTTP method (GET/POST/PATCH/DELETE)")
    call_parser.add_argument("path", help="API path, e.g., /calendars/primary/events")
    call_parser.add_argument("--params", help="Query params as JSON string")
    call_parser.add_argument("--params-file", help="Path to query params JSON file")
    call_parser.add_argument("--body", help="Request body as JSON string")
    call_parser.add_argument("--body-file", help="Path to request body JSON file")
    call_parser.set_defaults(func=cmd_call)

    list_cal_parser = subparsers.add_parser("list-calendars", help="List calendars")
    add_common_auth_args(list_cal_parser)
    list_cal_parser.add_argument("--min-access-role", help="Filter by minimum access role")
    list_cal_parser.add_argument("--max-results", type=int, help="Max results")
    list_cal_parser.add_argument("--page-token", help="Page token")
    list_cal_parser.set_defaults(func=cmd_list_calendars)

    list_events_parser = subparsers.add_parser("list-events", help="List events")
    add_common_auth_args(list_events_parser)
    list_events_parser.add_argument("--calendar-id", required=True, help="Calendar ID (or 'primary')")
    list_events_parser.add_argument("--time-min", required=True, help="RFC3339 start time")
    list_events_parser.add_argument("--time-max", required=True, help="RFC3339 end time")
    list_events_parser.add_argument("--q", help="Free text search query")
    list_events_parser.add_argument("--single-events", action="store_true", help="Expand recurring events")
    list_events_parser.add_argument("--order-by", help="Order by (e.g., startTime)")
    list_events_parser.add_argument("--max-results", type=int, help="Max results")
    list_events_parser.add_argument("--time-zone", help="IANA timezone")
    list_events_parser.add_argument("--page-token", help="Page token")
    list_events_parser.add_argument("--fields", help="Partial response fields")
    list_events_parser.set_defaults(func=cmd_list_events)

    get_event_parser = subparsers.add_parser("get-event", help="Get an event")
    add_common_auth_args(get_event_parser)
    get_event_parser.add_argument("--calendar-id", required=True, help="Calendar ID")
    get_event_parser.add_argument("--event-id", required=True, help="Event ID")
    get_event_parser.add_argument("--fields", help="Partial response fields")
    get_event_parser.set_defaults(func=cmd_get_event)

    create_parser = subparsers.add_parser("create-event", help="Create an event")
    add_common_auth_args(create_parser)
    create_parser.add_argument("--calendar-id", required=True, help="Calendar ID")
    create_parser.add_argument("--summary", help="Event title")
    create_parser.add_argument("--start", help="Start time (RFC3339 or date)")
    create_parser.add_argument("--end", help="End time (RFC3339 or date)")
    create_parser.add_argument("--time-zone", help="Timezone if start/end lack offset")
    create_parser.add_argument("--location", help="Location")
    create_parser.add_argument("--description", help="Description")
    create_parser.add_argument("--attendees", help="Comma-separated attendee emails")
    create_parser.add_argument("--recurrence", action="append", help="Repeat rule (RRULE:...)", default=[])
    create_parser.add_argument("--send-updates", help="all|externalOnly|none")
    create_parser.add_argument("--body", help="Request body as JSON string")
    create_parser.add_argument("--body-file", help="Path to request body JSON file")
    create_parser.set_defaults(func=cmd_create_event)

    update_parser = subparsers.add_parser("update-event", help="Update an event")
    add_common_auth_args(update_parser)
    update_parser.add_argument("--calendar-id", required=True, help="Calendar ID")
    update_parser.add_argument("--event-id", required=True, help="Event ID")
    update_parser.add_argument("--summary", help="Event title")
    update_parser.add_argument("--start", help="Start time (RFC3339 or date)")
    update_parser.add_argument("--end", help="End time (RFC3339 or date)")
    update_parser.add_argument("--time-zone", help="Timezone if start/end lack offset")
    update_parser.add_argument("--location", help="Location")
    update_parser.add_argument("--description", help="Description")
    update_parser.add_argument("--attendees", help="Comma-separated attendee emails")
    update_parser.add_argument("--recurrence", action="append", help="Repeat rule (RRULE:...)", default=[])
    update_parser.add_argument("--send-updates", help="all|externalOnly|none")
    update_parser.add_argument("--body", help="Request body as JSON string")
    update_parser.add_argument("--body-file", help="Path to request body JSON file")
    update_parser.set_defaults(func=cmd_update_event)

    delete_parser = subparsers.add_parser("delete-event", help="Delete an event")
    add_common_auth_args(delete_parser)
    delete_parser.add_argument("--calendar-id", required=True, help="Calendar ID")
    delete_parser.add_argument("--event-id", required=True, help="Event ID")
    delete_parser.add_argument("--send-updates", help="all|externalOnly|none")
    delete_parser.set_defaults(func=cmd_delete_event)

    freebusy_parser = subparsers.add_parser("freebusy", help="Free/busy query")
    add_common_auth_args(freebusy_parser)
    freebusy_parser.add_argument("--calendars", required=True, help="Comma-separated calendar IDs")
    freebusy_parser.add_argument("--time-min", required=True, help="RFC3339 start time")
    freebusy_parser.add_argument("--time-max", required=True, help="RFC3339 end time")
    freebusy_parser.add_argument("--time-zone", help="IANA timezone")
    freebusy_parser.set_defaults(func=cmd_freebusy)

    list_tasklists_parser = subparsers.add_parser("list-tasklists", help="List task lists")
    add_common_auth_args(list_tasklists_parser, DEFAULT_TASKS_SCOPES)
    list_tasklists_parser.add_argument("--max-results", type=int, help="Max results")
    list_tasklists_parser.add_argument("--page-token", help="Page token")
    list_tasklists_parser.add_argument("--fields", help="Partial response fields")
    list_tasklists_parser.set_defaults(func=cmd_list_tasklists)

    get_tasklist_parser = subparsers.add_parser("get-tasklist", help="Get a task list")
    add_common_auth_args(get_tasklist_parser, DEFAULT_TASKS_SCOPES)
    get_tasklist_parser.add_argument("--tasklist", required=True, help="Task list ID")
    get_tasklist_parser.add_argument("--fields", help="Partial response fields")
    get_tasklist_parser.set_defaults(func=cmd_get_tasklist)

    create_tasklist_parser = subparsers.add_parser("create-tasklist", help="Create a task list")
    add_common_auth_args(create_tasklist_parser, DEFAULT_TASKS_SCOPES)
    create_tasklist_parser.add_argument("--title", help="Task list title")
    create_tasklist_parser.add_argument("--body", help="Request body as JSON string")
    create_tasklist_parser.add_argument("--body-file", help="Path to request body JSON file")
    create_tasklist_parser.set_defaults(func=cmd_create_tasklist)

    update_tasklist_parser = subparsers.add_parser("update-tasklist", help="Update a task list")
    add_common_auth_args(update_tasklist_parser, DEFAULT_TASKS_SCOPES)
    update_tasklist_parser.add_argument("--tasklist", required=True, help="Task list ID")
    update_tasklist_parser.add_argument("--title", help="Task list title")
    update_tasklist_parser.add_argument("--body", help="Request body as JSON string")
    update_tasklist_parser.add_argument("--body-file", help="Path to request body JSON file")
    update_tasklist_parser.set_defaults(func=cmd_update_tasklist)

    delete_tasklist_parser = subparsers.add_parser("delete-tasklist", help="Delete a task list")
    add_common_auth_args(delete_tasklist_parser, DEFAULT_TASKS_SCOPES)
    delete_tasklist_parser.add_argument("--tasklist", required=True, help="Task list ID")
    delete_tasklist_parser.set_defaults(func=cmd_delete_tasklist)

    list_tasks_parser = subparsers.add_parser("list-tasks", help="List tasks in a task list")
    add_common_auth_args(list_tasks_parser, DEFAULT_TASKS_SCOPES)
    list_tasks_parser.add_argument("--tasklist", required=True, help="Task list ID")
    list_tasks_parser.add_argument("--completed-max", help="RFC3339 completion time upper bound")
    list_tasks_parser.add_argument("--completed-min", help="RFC3339 completion time lower bound")
    list_tasks_parser.add_argument("--due-max", help="RFC3339 due time upper bound")
    list_tasks_parser.add_argument("--due-min", help="RFC3339 due time lower bound")
    list_tasks_parser.add_argument("--max-results", type=int, help="Max results")
    list_tasks_parser.add_argument("--page-token", help="Page token")
    list_tasks_parser.add_argument("--show-completed", type=parse_bool, help="true/false")
    list_tasks_parser.add_argument("--show-deleted", type=parse_bool, help="true/false")
    list_tasks_parser.add_argument("--show-hidden", type=parse_bool, help="true/false")
    list_tasks_parser.add_argument("--show-assigned", type=parse_bool, help="true/false")
    list_tasks_parser.add_argument("--updated-min", help="RFC3339 updated time lower bound")
    list_tasks_parser.add_argument("--fields", help="Partial response fields")
    list_tasks_parser.set_defaults(func=cmd_list_tasks)

    get_task_parser = subparsers.add_parser("get-task", help="Get a task")
    add_common_auth_args(get_task_parser, DEFAULT_TASKS_SCOPES)
    get_task_parser.add_argument("--tasklist", required=True, help="Task list ID")
    get_task_parser.add_argument("--task-id", required=True, help="Task ID")
    get_task_parser.add_argument("--fields", help="Partial response fields")
    get_task_parser.set_defaults(func=cmd_get_task)

    create_task_parser = subparsers.add_parser("create-task", help="Create a task")
    add_common_auth_args(create_task_parser, DEFAULT_TASKS_SCOPES)
    create_task_parser.add_argument("--tasklist", required=True, help="Task list ID")
    create_task_parser.add_argument("--title", help="Task title")
    create_task_parser.add_argument("--notes", help="Task notes")
    create_task_parser.add_argument("--due", help="RFC3339 due time")
    create_task_parser.add_argument("--status", help="Task status (needsAction|completed)")
    create_task_parser.add_argument("--completed", help="RFC3339 completion time")
    create_task_parser.add_argument("--parent", help="Parent task ID")
    create_task_parser.add_argument("--previous", help="Previous sibling task ID")
    create_task_parser.add_argument("--body", help="Request body as JSON string")
    create_task_parser.add_argument("--body-file", help="Path to request body JSON file")
    create_task_parser.set_defaults(func=cmd_create_task)

    update_task_parser = subparsers.add_parser("update-task", help="Update a task")
    add_common_auth_args(update_task_parser, DEFAULT_TASKS_SCOPES)
    update_task_parser.add_argument("--tasklist", required=True, help="Task list ID")
    update_task_parser.add_argument("--task-id", required=True, help="Task ID")
    update_task_parser.add_argument("--title", help="Task title")
    update_task_parser.add_argument("--notes", help="Task notes")
    update_task_parser.add_argument("--due", help="RFC3339 due time")
    update_task_parser.add_argument("--status", help="Task status (needsAction|completed)")
    update_task_parser.add_argument("--completed", help="RFC3339 completion time")
    update_task_parser.add_argument("--body", help="Request body as JSON string")
    update_task_parser.add_argument("--body-file", help="Path to request body JSON file")
    update_task_parser.set_defaults(func=cmd_update_task)

    delete_task_parser = subparsers.add_parser("delete-task", help="Delete a task")
    add_common_auth_args(delete_task_parser, DEFAULT_TASKS_SCOPES)
    delete_task_parser.add_argument("--tasklist", required=True, help="Task list ID")
    delete_task_parser.add_argument("--task-id", required=True, help="Task ID")
    delete_task_parser.set_defaults(func=cmd_delete_task)

    move_task_parser = subparsers.add_parser("move-task", help="Move a task")
    add_common_auth_args(move_task_parser, DEFAULT_TASKS_SCOPES)
    move_task_parser.add_argument("--tasklist", required=True, help="Task list ID")
    move_task_parser.add_argument("--task-id", required=True, help="Task ID")
    move_task_parser.add_argument("--parent", help="New parent task ID")
    move_task_parser.add_argument("--previous", help="New previous sibling task ID")
    move_task_parser.add_argument("--destination-tasklist", help="Destination task list ID")
    move_task_parser.set_defaults(func=cmd_move_task)

    clear_tasks_parser = subparsers.add_parser("clear-tasks", help="Clear completed tasks")
    add_common_auth_args(clear_tasks_parser, DEFAULT_TASKS_SCOPES)
    clear_tasks_parser.add_argument("--tasklist", required=True, help="Task list ID")
    clear_tasks_parser.set_defaults(func=cmd_clear_tasks)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        result = args.func(args)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
