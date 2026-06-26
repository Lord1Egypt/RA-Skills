# SF Supervisorial Districts Reference

## Current Board (2026)

| District | Supervisor | Neighborhoods |
|----------|-----------|---------------|
| D1 | Connie Chan | Richmond, Inner/Outer Richmond, Sea Cliff, Jordan Park |
| D2 | Stephen Sherrill | Marina, Cow Hollow, Pacific Heights, Presidio Heights |
| D3 | Danny Sauter | North Beach, Chinatown, Telegraph Hill, Russian Hill, Fisherman's Wharf |
| D4 | Alan Wong | Sunset, Inner/Outer Sunset, Parkside |
| D5 | Bilal Mahmood | NOPA, Western Addition, Haight, Hayes Valley, Lower Haight, Alamo Square, Cole Valley, Duboce |
| D6 | Matt Dorsey | SoMa, Tenderloin, Civic Center, Mid-Market |
| D7 | Myrna Melgar | West Portal, Forest Hill, Twin Peaks, Diamond Heights, Glen Park, Miraloma Park |
| D8 | Rafael Mandelman (President) | Castro, Noe Valley, Corona Heights, Eureka Valley, Duboce Triangle |
| D9 | Jackie Fielder | Mission, Bernal Heights, Portola |
| D10 | Shamann Walton | Bayview, Hunters Point, Visitacion Valley, Excelsior, Crocker Amazon |
| D11 | Chyanne Chen | Excelsior, Ingleside, Oceanview, Outer Mission |

## Key Committees (2026)

| Committee | Chair | Members | Schedule |
|-----------|-------|---------|----------|
| Land Use and Transportation | Melgar | Chen, Mahmood | Monday 1:30 PM |
| Budget and Appropriations | Chan | Dorsey, Sauter, Walton, Mandelman | Wednesday 1:30 PM |
| Budget and Finance | Chan | Dorsey, Sauter | Wednesday 10:00 AM |
| Government Audit and Oversight | Fielder | Sauter, Sherrill | 1st & 3rd Thursday 10:00 AM |
| Public Safety and Neighborhood Services | Dorsey | Mahmood, Wong | 2nd & 4th Thursday 10:00 AM |
| Rules Committee | Walton | Sherrill, Mandelman | Monday 10:00 AM |

Full Board meets every other Tuesday at 2:00 PM.

## How SF Land Use Works (quick reference)

1. **Introduction** — Supervisor introduces ordinance/resolution at full Board
2. **Committee referral** — Usually sent to Land Use and Transportation (or relevant committee)
3. **Committee hearing** — Public comment, amendments, vote to recommend or kill
4. **Full Board first reading** — Ordinances require two readings (resolutions only one)
5. **Full Board second reading / final passage** — Becomes law if Mayor signs (or doesn't veto within 10 days)

Planning Commission runs parallel to this for zoning/development items — their approval/denial feeds into the Board process.

## Scraping Notes

**Just use curl** — both Legistar and sfmta.com return full HTML to curl without JavaScript. No headless browser needed.

```bash
# Legistar calendar
curl -s "https://sfgov.legistar.com/Calendar.aspx" | grep -i "MeetingDetail"

# SFMTA public notices
curl -s "https://www.sfmta.com/public-notices" | grep -i "engineering-public-hearing"

# SFMTA hearing page → find PDF link
curl -s "https://www.sfmta.com/notices/engineering-public-hearing-meeting-april-32026" | grep -o '/media/[0-9]*/download[^"]*'

# Download PDF
curl -sL "https://www.sfmta.com/media/44732/download?inline" -o agenda.pdf

# Extract text from PDF (pdfplumber in Python, or pdftotext CLI)
pdftotext agenda.pdf -   # stdout
python3 -c "import pdfplumber; [print(p.extract_text()) for p in pdfplumber.open('agenda.pdf').pages]"

# Quick grep for district after extraction
curl -sL "https://www.sfmta.com/media/44732/download?inline" | pdftotext - - | grep -A5 "District 5"
```

**Legistar URL patterns:**
- **Calendar**: `https://sfgov.legistar.com/Calendar.aspx`
- **Meeting detail URLs require GUIDs** — get them from the calendar page HTML, don't construct manually
- **Minutes PDFs**: `View.ashx?M=M&ID={meeting_id}&GUID={guid}`
- **Agenda PDFs**: `View.ashx?M=A&ID={meeting_id}&GUID={guid}`
- **Legislation attachments**: `View.ashx?M=F&ID={attachment_id}&GUID={guid}` — IDs must be scraped from LegislationDetail page
- Planning Commission uses `sfplanning.org` (JS-rendered, harder to scrape — not currently supported)

## Participation: How to Engage

- **Public comment at meetings**: Sign up at sfbos.org or show up in person (City Hall, Room 250)
- **Written comment**: Email bos@sfgov.org or mail City Hall Room 244
- **Contact your supervisor**: sfbos.org/supervisors
- **Watch live**: SFGovTV Cable Channel 26 or sfgovtv.org
- **Meeting schedule**: sfgov.legistar.com/Calendar.aspx
