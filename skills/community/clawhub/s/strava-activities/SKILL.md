---
name: strava-activities
description: Track and manage Strava workouts, athlete stats, routes, segments, and club activities via the Strava API. Use this skill when users want to log activities, review athletic performance, explore routes, or manage club data in Strava.
---

# Strava

![Strava](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/strava.svg)

Track and manage Strava activities, athlete data, routes, segments, and club activity from chat via the Strava API.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=strava-activities) for hosted connection flows and credentials so you do not need to configure Strava API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Strava |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Strava |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Strava API     │
│   (User Chat)   │     │   (OAuth)    │     │                  │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Strava    │                       │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │  Strava  │
   │  File    │           │ Auth     │           │  Account │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Strava again."

## Quick Start

```bash
# Get athlete profile
clawlink_call_tool --tool "strava_get_athlete" --params '{}'

# List recent activities
clawlink_call_tool --tool "strava_list_activities" --params '{"limit": 10}'

# Get activity details
clawlink_call_tool --tool "strava_get_activity" --params '{"activity_id": "ACTIVITY_ID"}'
```

## Authentication

All Strava tool calls are authenticated automatically by ClawLink using the user's connected Strava account OAuth token.

**No API token is required in chat.** ClawLink stores the OAuth token securely and injects it into every Strava API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=strava and connect Strava.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `strava` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration strava
```

**Response:** Returns the live tool catalog for Strava.

### Reconnect

If Strava tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=strava
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration strava`

## Security & Permissions

- Access is scoped to the Strava account connected during OAuth setup and the scopes granted.
- **Write operations (create activity, upload files, update settings) require explicit user confirmation.**
- Activity upload requires the user to own the data being uploaded.
- Club management operations may require club admin privileges.

## Tool Reference

### Athlete

| Tool | Description | Mode |
|------|-------------|------|
| `strava_get_athlete` | Get the authenticated athlete's profile | Read |
| `strava_update_athlete` | Update athlete settings (sport type, timezone) | Write |
| `strava_get_athlete_stats` | Get athlete statistics (distance, pace, heart rate zones) | Read |
| `strava_get_athlete_zones` | Get heart rate and power zones | Read |
| `strava_get_athlete_clubs` | List clubs the athlete is a member of | Read |

### Activities

| Tool | Description | Mode |
|------|-------------|------|
| `strava_list_activities` | List the athlete's activities with pagination | Read |
| `strava_get_activity` | Get details for a specific activity | Read |
| `strava_create_activity` | Create a manual activity entry | Write |
| `strava_update_activity` | Update an activity's name, description, or privacy | Write |
| `strava_delete_activity` | Delete an activity permanently | Write |
| `strava_get_activity_zones` | Get splits and heart rate/power zones for an activity | Read |
| `strava_get_activity_laps` | Get lap data for an activity | Read |
| `strava_get_activity_streams` | Get GPS, heart rate, power streams for an activity | Read |
| `strava_upload_activity_photo` | Attach a photo to an activity | Write |

### Activity Comments & Kudos

| Tool | Description | Mode |
|------|-------------|------|
| `strava_list_activity_comments` | List comments on an activity | Read |
| `strava_create_activity_comment` | Add a comment to an activity | Write |
| `strava_list_activity_kudos` | List kudos given to an activity | Read |
| `strava_give_kudos_to_activity` | Give kudos to an activity | Write |
| `strava_delete_kudos_from_activity` | Remove kudos from an activity | Write |

### Routes

| Tool | Description | Mode |
|------|-------------|------|
| `strava_list_routes` | List the athlete's saved routes | Read |
| `strava_get_route` | Get details and segments for a route | Read |
| `strava_create_route` | Create a new route | Write |
| `strava_update_route` | Update a route's name or description | Write |
| `strava_delete_route` | Delete a route | Write |

### Segments

| Tool | Description | Mode |
|------|-------------|------|
| `strava_get_segment` | Get a segment's leaderboard and details | Read |
| `strava_list_segment_efforts` | List efforts on a segment by an athlete | Read |
| `strava_get_segment_effort` | Get a specific segment effort | Read |
| `strava_explore_segments` | Explore segments in a geographic area | Read |
| `strava_star_segment` | Star/favorite a segment | Write |
| `strava_unstar_segment` | Remove a star from a segment | Write |
| `strava_list_starred_segments` | List the athlete's starred segments | Read |

### Clubs

| Tool | Description | Mode |
|------|-------------|------|
| `strava_get_club` | Get a club's profile | Read |
| `strava_list_club_activities` | List recent activities in a club | Read |
| `strava_list_club_members` | List members of a club | Read |
| `strava_join_club` | Request to join a club | Write |
| `strava_leave_club` | Leave a club | Write |

### Gear & Equipment

| Tool | Description | Mode |
|------|-------------|------|
| `strava_get_equipment` | Get details for a piece of equipment | Read |
| `strava_create_equipment` | Add new equipment (bike, shoes) | Write |
| `strava_update_equipment` | Update equipment name or retired status | Write |
| `strava_delete_equipment` | Delete equipment | Write |
| `strava_list_athlete_equipment` | List all equipment for an athlete | Read |

### Uploads

| Tool | Description | Mode |
|------|-------------|------|
| `strava_upload_file` | Upload a FIT, GPX, or TCX activity file | Write |
| `strava_get_upload_status` | Check the status of an activity upload | Read |

## Code Examples

### Get athlete stats

```bash
clawlink_call_tool --tool "strava_get_athlete_stats" \
  --params '{"athlete_id": "ATHLETE_ID"}'
```

### List recent activities

```bash
clawlink_call_tool --tool "strava_list_activities" \
  --params '{
    "limit": 10,
    "after": 1704067200
  }'
```

### Get activity details

```bash
clawlink_call_tool --tool "strava_get_activity" \
  --params '{
    "activity_id": "ACTIVITY_ID"
  }'
```

### Explore segments in an area

```bash
clawlink_call_tool --tool "strava_explore_segments" \
  --params '{
    "bounds": [37.8, -122.5, 37.9, -122.4],
    "activity_type": "running"
  }'
```

### Star a segment

```bash
clawlink_call_tool --tool "strava_star_segment" \
  --params '{
    "segment_id": "SEGMENT_ID"
  }'
```

### Get club activities

```bash
clawlink_call_tool --tool "strava_list_club_activities" \
  --params '{
    "club_id": "CLUB_ID",
    "limit": 20
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Strava is connected.
2. Call `clawlink_list_tools --integration strava` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `strava`.
5. If no Strava tools appear, direct the user to https://claw-link.dev/dashboard?add=strava.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → explore → describe                           │
│                                                             │
│  Example: List activities → Get activity streams → Analyze │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → call                       │
│                                                             │
│  Example: Preview activity upload → User approves → Upload │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, get, and explore operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Activity uploads (FIT, GPX, TCX) are processed asynchronously — check upload status with `strava_get_upload_status`.
- Segment explore uses bounding box coordinates: `[southwest_lat, southwest_lng, northeast_lat, northeast_lng]`.
- Activity privacy controls may hide some data from API responses for private activities.
- Upload file size limits apply — compressed FIT files are preferred over raw GPX for large activities.
- Heart rate and power data availability depends on the device used to record the activity.
- Activity types include: `run`, `ride`, `swim`, `workout`, `hike`, `walk`, and others.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration strava`. |
| Missing connection | Strava is not connected. Direct the user to https://claw-link.dev/dashboard?add=strava. |
| `Activity not found` | The activity ID does not exist or belongs to another athlete. |
| `Segment not found` | The segment ID does not exist in Strava's database. |
| `Upload in progress` | The file upload is still being processed. Check status with `strava_get_upload_status`. |
| `Upload failed` | The file format is invalid or the upload processing failed. |
| `403 Forbidden` | The connected account lacks permission for this operation. |
| `Rate limited` | Too many requests — wait before retrying. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Upload Fails

1. Confirm the file is a valid FIT, GPX, or TCX format.
2. Check the file size — very large files may fail to process.
3. Wait and poll `strava_get_upload_status` — processing can take several seconds for large files.
4. Verify the activity data is valid (GPS coordinates, timestamps).

## Resources

- [Strava API Documentation](https://developers.strava.com/docs/reference/)
- [Strava API Overview](https://developers.strava.com/)
- [Strava Authentication](https://developers.strava.com/docs/auth/)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=strava-activities
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=strava-activities)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)