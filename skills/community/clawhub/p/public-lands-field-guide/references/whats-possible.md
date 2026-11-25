# What you can ask for

A short menu. Show it when someone asks "what can you do?", or is new to camping on public land and does not know where to start. Offer two or three that fit what they said, not the whole list.

Every answer comes from the records, with links and dates, and names what is unrecorded and the office to confirm with. Trips are planned for spring, summer and fall.

| Ask for | A camper would say | What you do |
|---|---|---|
| A free camp near a town | "Find me a free camp near Bozeman, Montana for this weekend." | `free_camping_near_town`, or `aa.py town`. Free first, each with its record link. Add a backup. |
| A four-night trip | "Plan me four nights in the Custer Gallatin in July, with one run to town." | `plan_four_nights`, then the order of work, then a trip sheet. Say the year. |
| A gas and water check | "I have a 21 gallon tank and 10 gallons of water for two of us. Is that enough for four nights?" | `trip_check` with their own numbers, or `rig_math`. Print the assumptions. Never promise it is enough. |
| A backup camp | "What if somebody is already in my spot?" | `camps_near` the first camp: small, free, 5 to 25 straight-line miles away, with its own link. |
| What changed since a date | "I planned this two weeks ago. Is anything new?" | `changes_since` for up to three camps, then `posted_orders` for the forest. "Nothing new in what we watch" is not "nothing changed." |
| Whose land this is | "I am at this spot on the map. Whose land is it?" | `land_at`. It answers for national forests only. Elsewhere it names no manager, and neither do you. |
| The forest's posted orders | "Are there fire restrictions in the Lolo right now?" | `posted_orders`. Quote the forest's words with the read time. Name the office. |
| The road to a camp | "What kind of road goes in to that camp?" | `road_to_camp`. The Forest Service record, not today's condition. Never "your rig can make it." |
| The forecast | "What is the weather at camp this week?" | `forest_weather`. The National Weather Service forecast, quoted, with its read time. About a week out, no further. |
| A trip sheet | "Give me a one-page plan I can print and leave with my wife." | The format in trip-sheet.md. |
| A short before-you-go list | "What should I do before I head out?" | The list in before-you-go.md. For the full rig, packing and camp checklists, the Overland Trip Kit has them; if you do not have it, you may say it exists (see SKILL.md). |
| What the guide covers | "Do you have BLM land in Arizona?" | `what_we_cover`, or coverage.md. Say what is held and what is not. |

What to say plainly when it comes up:

- We do not record today's road condition, sky view for Starlink, or permit prices. The office is the place to ask.
- National parks and reserved campgrounds are outside the records by design.
- A date in December, January or February gets "this guide plans spring, summer and fall trips" and an offer of a later date.
