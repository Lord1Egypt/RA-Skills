#!/usr/bin/env python3
"""
Zoom API client for creating, retrieving, listing, and deleting Zoom meetings.
Uses Server-to-Server OAuth flow for authentication.
"""

import json
import os
import sys
import io
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import requests

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


class ZoomAPIError(Exception):
    """Custom exception for Zoom API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, details: Optional[dict] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ZoomClient:
    """Zoom API client using Server-to-Server OAuth."""
    
    BASE_URL = "https://api.zoom.us/v2"
    TOKEN_URL = "https://zoom.us/oauth/token"
    CREDENTIAL_PATH = Path.home() / ".openclaw" / "credentials" / "zoom.json"
    
    def __init__(self, credentials: Optional[dict] = None):
        """
        Initialize Zoom client.
        
        Args:
            credentials: Optional dict with account_id, client_id, client_secret.
                        If not provided, loads from credential file.
        """
        if credentials:
            self.credentials = credentials
        else:
            self.credentials = self._load_credentials()
        
        self._access_token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None
    
    def _load_credentials(self) -> dict:
        """Load credentials from the credential file."""
        if not self.CREDENTIAL_PATH.exists():
            raise ZoomAPIError(
                f"Credential file not found: {self.CREDENTIAL_PATH}",
                details={"path": str(self.CREDENTIAL_PATH)}
            )
        
        try:
            with open(self.CREDENTIAL_PATH, "r") as f:
                creds = json.load(f)
            
            required = ["account_id", "client_id", "client_secret"]
            missing = [k for k in required if k not in creds]
            if missing:
                raise ZoomAPIError(
                    f"Missing required credentials: {', '.join(missing)}",
                    details={"missing": missing}
                )
            
            return creds
        except json.JSONDecodeError as e:
            raise ZoomAPIError(
                f"Invalid JSON in credential file: {e}",
                details={"error": str(e)}
            )
    
    def _get_access_token(self) -> str:
        """
        Obtain or refresh access token using Server-to-Server OAuth.
        
        Returns:
            Access token string.
        """
        # Check if we have a valid cached token
        if self._access_token and self._token_expires_at:
            if datetime.now() < self._token_expires_at:
                return self._access_token
        
        # Request new token
        try:
            response = requests.post(
                self.TOKEN_URL,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "account_credentials",
                    "account_id": self.credentials["account_id"]
                },
                auth=(
                    self.credentials["client_id"],
                    self.credentials["client_secret"]
                ),
                timeout=30
            )
            
            if response.status_code != 200:
                raise ZoomAPIError(
                    "Failed to obtain access token",
                    status_code=response.status_code,
                    details={"response": response.text}
                )
            
            token_data = response.json()
            self._access_token = token_data["access_token"]
            # Token expires in 3600 seconds by default, cache with buffer
            expires_in = token_data.get("expires_in", 3600)
            self._token_expires_at = datetime.now().replace(
                second=datetime.now().second,
                microsecond=0
            )
            from datetime import timedelta
            self._token_expires_at += timedelta(seconds=expires_in - 300)
            
            return self._access_token
            
        except requests.RequestException as e:
            raise ZoomAPIError(
                f"Network error while obtaining token: {e}",
                details={"error": str(e)}
            )
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict] = None,
        json_data: Optional[dict] = None
    ) -> dict:
        """
        Make HTTP request to Zoom API.
        
        Args:
            method: HTTP method (GET, POST, DELETE)
            endpoint: API endpoint (without base URL)
            params: Query parameters
            json_data: JSON body for POST/PUT requests
            
        Returns:
            Parsed JSON response.
        """
        url = f"{self.BASE_URL}{endpoint}"
        headers = {"Authorization": f"Bearer {self._get_access_token()}"}
        
        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                params=params,
                json=json_data,
                timeout=30
            )
            
            if response.status_code == 401:
                # Token might be expired, try refreshing once
                self._access_token = None
                headers["Authorization"] = f"Bearer {self._get_access_token()}"
                response = requests.request(
                    method,
                    url,
                    headers=headers,
                    params=params,
                    json=json_data,
                    timeout=30
                )
            
            if response.status_code >= 400:
                error_data = {}
                try:
                    error_data = response.json()
                except:
                    pass
                
                raise ZoomAPIError(
                    error_data.get("errorMessage", f"API error: {response.status_code}"),
                    status_code=response.status_code,
                    details=error_data
                )
            
            if response.status_code == 204:
                return {}
            
            return response.json()
            
        except requests.RequestException as e:
            raise ZoomAPIError(
                f"Network error: {e}",
                details={"error": str(e)}
            )
    
    def create_meeting(
        self,
        topic: str,
        start_time: Optional[str] = None,
        duration: int = 40,
        timezone: str = "Asia/Almaty"
    ) -> dict:
        """
        Create a new Zoom meeting.

        Args:
            topic: Meeting topic/title
            start_time: ISO 8601 format datetime string. Defaults to now.
            duration: Meeting duration in minutes. Defaults to 40.
            timezone: Timezone for the meeting. Defaults to Asia/Aqtobe.

        Returns:
            Meeting details including id, join_url, password.
        """
        if start_time is None:
            # Get current time in the specified timezone
            try:
                import pytz
                tz_obj = pytz.timezone(timezone)
                local_now = datetime.now(tz_obj)
                start_time = local_now.strftime("%Y-%m-%dT%H:%M:%S")
            except Exception:
                # Fallback for any timezone errors
                start_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        
        payload = {
            "topic": topic,
            "type": 2,  # Scheduled meeting
            "start_time": start_time,
            "duration": duration,
            "timezone": timezone,
            "settings": {
                "join_before_host": True,
                "mute_upon_entry": False,
                "waiting_room": False
            }
        }
        
        response = self._request("POST", "/users/me/meetings", json_data=payload)

        # Convert UTC start_time from API to local timezone for display
        api_start_time = response.get("start_time", start_time)
        display_start_time = api_start_time
        try:
            import pytz
            # Parse UTC time from API (formats: 2026-03-05T15:51:33Z or 2026-03-05T15:51:33.000000Z)
            utc_time_str = api_start_time.split('.')[0]  # Remove microseconds if present
            if utc_time_str.endswith('Z'):
                utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%SZ")
                utc_time = pytz.utc.localize(utc_time)
                local_tz = pytz.timezone(timezone)
                local_time = utc_time.astimezone(local_tz)
                display_start_time = local_time.strftime("%Y-%m-%dT%H:%M:%S %Z")
        except Exception as e:
            # Keep original time if conversion fails
            pass

        return {
            "meeting_id": str(response.get("id", "")),
            "join_url": response.get("join_url", ""),
            "password": response.get("password", ""),
            "topic": response.get("topic", topic),
            "start_time": display_start_time,
            "duration": response.get("duration", duration),
            "timezone": response.get("timezone", timezone)
        }
    
    def get_meeting(self, meeting_id: str) -> dict:
        """
        Retrieve meeting details.
        
        Args:
            meeting_id: Zoom meeting ID.
            
        Returns:
            Meeting details.
        """
        response = self._request("GET", f"/meetings/{meeting_id}")
        
        return {
            "meeting_id": str(response.get("id", meeting_id)),
            "join_url": response.get("join_url", ""),
            "password": response.get("password", ""),
            "topic": response.get("topic", ""),
            "start_time": response.get("start_time", ""),
            "duration": response.get("duration", 0),
            "timezone": response.get("timezone", ""),
            "status": response.get("status", "")
        }
    
    def list_meetings(self, user_id: str = "me") -> list:
        """
        List all meetings for a user.
        
        Args:
            user_id: User ID or 'me' for authenticated user.
            
        Returns:
            List of meeting summaries.
        """
        response = self._request("GET", f"/users/{user_id}/meetings")
        
        meetings = response.get("meetings", [])
        return [
            {
                "meeting_id": str(m.get("id", "")),
                "topic": m.get("topic", ""),
                "start_time": m.get("start_time", ""),
                "duration": m.get("duration", 0),
                "join_url": m.get("join_url", "")
            }
            for m in meetings
        ]
    
    def delete_meeting(self, meeting_id: str) -> dict:
        """
        Delete a Zoom meeting.
        
        Args:
            meeting_id: Zoom meeting ID.
            
        Returns:
            Confirmation response.
        """
        self._request("DELETE", f"/meetings/{meeting_id}")
        
        return {
            "success": True,
            "meeting_id": meeting_id,
            "message": f"Meeting {meeting_id} deleted successfully"
        }


def format_output(result: dict, action: str) -> str:
    """
    Format API result as human-readable output.

    Args:
        result: API response dict
        action: The action performed

    Returns:
        Formatted string output.
    """
    if action == "create_meeting":
        lines = [
            "✅ Meeting created!",
            "",
            f"📋 Topic: {result.get('topic', 'Untitled')}",
            f"🆔 Meeting ID: {result.get('meeting_id', 'N/A')}",
            f"🔗 Join: {result.get('join_url', 'N/A')}",
            f"🔑 Password: {result.get('password', 'N/A')}",
            f"⏰ Start: {result.get('start_time', 'N/A')}",
            f"⏱ Duration: {result.get('duration', 40)} min",
            f"🌍 Timezone: {result.get('timezone', 'N/A')}"
        ]
        return "\n".join(lines)

    elif action == "get_meeting":
        lines = [
            "📋 Meeting Details",
            "",
            f"📋 Topic: {result.get('topic', 'Untitled')}",
            f"🆔 ID: {result.get('meeting_id', 'N/A')}",
            f"🔗 Join: {result.get('join_url', 'N/A')}",
            f"🔑 Password: {result.get('password', 'N/A')}",
            f"⏰ Start: {result.get('start_time', 'N/A')}",
            f"⏱ Duration: {result.get('duration', 0)} min",
            f"🌍 Timezone: {result.get('timezone', 'N/A')}",
            f"📊 Status: {result.get('status', 'N/A')}"
        ]
        return "\n".join(lines)

    elif action == "list_meetings":
        if not result:
            return "📭 No meetings found."
        lines = [f"📅 Found {len(result)} meeting(s)", ""]
        for i, meeting in enumerate(result, 1):
            lines.append(f"{i}. {meeting.get('topic', 'Untitled')}")
            lines.append(f"   ID: {meeting.get('meeting_id', 'N/A')}")
            lines.append(f"   Start: {meeting.get('start_time', 'N/A')}")
            lines.append(f"   Duration: {meeting.get('duration', 0)} min")
            lines.append("")
        return "\n".join(lines)

    elif action == "delete_meeting":
        return f"✅ Meeting {result.get('meeting_id', 'N/A')} deleted."

    else:
        return json.dumps(result, indent=2)


def main():
    """CLI entry point for testing."""
    # Check if JSON input is provided via stdin or as argument
    json_input = None
    
    # Try to read JSON from stdin (for piped input)
    if not sys.stdin.isatty():
        try:
            stdin_data = sys.stdin.read().strip()
            if stdin_data:
                json_input = json.loads(stdin_data)
        except json.JSONDecodeError:
            pass
    
    # Or check for --json argument
    if "--json" in sys.argv:
        json_idx = sys.argv.index("--json")
        if json_idx + 1 < len(sys.argv):
            try:
                json_input = json.loads(sys.argv[json_idx + 1])
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON: {e}")
                sys.exit(1)
    
    client = ZoomClient()

    try:
        if json_input:
            # JSON mode - process action from JSON
            action = json_input.get("action", "")
            
            if action == "create_meeting":
                topic = json_input.get("topic", "Untitled Meeting")
                start_time = json_input.get("start_time")
                duration = json_input.get("duration", 40)
                timezone = json_input.get("timezone", "Asia/Almaty")
                result = client.create_meeting(topic, start_time, duration, timezone)
                print(format_output(result, "create_meeting"))
                
            elif action == "get_meeting":
                meeting_id = json_input.get("meeting_id", "")
                if not meeting_id:
                    print("Error: meeting_id required in JSON")
                    sys.exit(1)
                result = client.get_meeting(meeting_id)
                print(format_output(result, "get_meeting"))
                
            elif action == "list_meetings":
                user_id = json_input.get("user_id", "me")
                result = client.list_meetings(user_id)
                print(format_output(result, "list_meetings"))
                
            elif action == "delete_meeting":
                meeting_id = json_input.get("meeting_id", "")
                if not meeting_id:
                    print("Error: meeting_id required in JSON")
                    sys.exit(1)
                result = client.delete_meeting(meeting_id)
                print(format_output(result, "delete_meeting"))
                
            else:
                print(f"Error: Unknown action '{action}'")
                print("Supported actions: create_meeting, get_meeting, list_meetings, delete_meeting")
                sys.exit(1)
        else:
            # CLI mode - positional arguments
            if len(sys.argv) < 2:
                print("Usage:")
                print("  python zoom_api.py <action> [args...]")
                print("  python zoom_api.py --json '<json_object>'")
                print("Actions: create, get, list, delete")
                sys.exit(1)

            action = sys.argv[1]
            
            if action == "create":
                topic = sys.argv[2] if len(sys.argv) > 2 else "Test Meeting"
                result = client.create_meeting(topic)
                print(format_output(result, "create_meeting"))
            elif action == "get":
                meeting_id = sys.argv[2] if len(sys.argv) > 2 else ""
                if not meeting_id:
                    print("Error: meeting_id required")
                    sys.exit(1)
                result = client.get_meeting(meeting_id)
                print(format_output(result, "get_meeting"))
            elif action == "list":
                result = client.list_meetings()
                print(format_output(result, "list_meetings"))
            elif action == "delete":
                meeting_id = sys.argv[2] if len(sys.argv) > 2 else ""
                if not meeting_id:
                    print("Error: meeting_id required")
                    sys.exit(1)
                result = client.delete_meeting(meeting_id)
                print(format_output(result, "delete_meeting"))
            else:
                print(f"Unknown action: {action}")
                sys.exit(1)

    except ZoomAPIError as e:
        print(f"Error: {e.message}")
        if e.details:
            print(f"Details: {json.dumps(e.details, indent=2)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
