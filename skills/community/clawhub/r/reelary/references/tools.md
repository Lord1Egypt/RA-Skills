# Reelary MCP tools

All tools talk to the Reelary app running locally on the user's Mac or Windows PC. Nothing is uploaded.

| Tool | Use it to |
|---|---|
| reelary_status | Check the app is ready: plan (free/pro), indexed folders, running jobs, export limits |
| reelary_list_folders | See which folders are in the library |
| reelary_add_folder | Add and index a folder (background job, free and unlimited) |
| reelary_remove_folder | Drop a folder from the index (files stay on disk) |
| reelary_search | Find clips/photos by meaning; returns path + start/end seconds; `include_thumbnails` to see them |
| reelary_rough_cut | Script -> draft: one scene per line, best clip + 2 alternatives each |
| reelary_save_project | Save a draft as a project the user can open in the editor |
| reelary_open_in_app | Show the window, optionally on a project, for hand edits |
| reelary_export_video | Render MP4 (background job). Free: 720p, watermark, 60s max, 5/month |
| reelary_export_nle | FCPXML / XML / EDL for Premiere, Final Cut, DaVinci Resolve (Pro) |
| reelary_job_status | Poll an index or export job |
| reelary_list_people / reelary_person_clips | Face search (Pro) |
| reelary_list_places | Where footage was shot, from GPS (Pro) |

Search results are dynamic segments: consecutive matching frames of one video merged into one range. Quote times as mm:ss and keep full paths.
