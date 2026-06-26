---
name: this-week-in-nyc
description: Find things to do in New York City this week.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🗽"
    requires:
      bins:
        - curl
        - puppeteer
---

# This Week in NYC

## Purpose
Put together a fun and unique list of events that are happening in and around New York City this week that fit the user's interests.

## Workflow

### 1. Requirements
Assume that the user is only looking for events that happen between 5pm-10pm on the weekday. No time restrictions for Friday night and weekends.

Ask the user if there is any particular interest or activity they want to especially look out for.

### 2. Check Event Sources

Based on user preferences, check these NYC event sources:

**Film & Cinema:**
- Anthology Film Archives (https://www.anthologyfilmarchives.org/film_screenings/calendar) - Experimental, avant-garde, and classic cinema
- Metrograph (https://metrograph.com/) - Independent and repertory cinema in Lower East Side
- Alamo Drafthouse NYC (https://drafthouse.com/nyc/theater/lower-manhattan) - Genre films, special screenings, and eat-in theater

**Community & Activism:**
- Times Up (https://times-up.org/calendar/) - Bike rides, community events, and activist gatherings
- ABC No Rio (https://www.abcnorio.org/events/events.html) - Punk shows, art exhibitions, and radical community events
- Fifth Estate (https://www.fifthestate.org/contact-fifth-estate/writers-guidelines/) - Anarchist publication and event collective

**Performing Arts & Music:**
- Ars Nova (https://arsnovanyc.com/upcoming-events/) - Experimental theater, comedy, and music

**Educational:**
- Nerd Nite NYC (https://nyc.nerdnite.com/) - Monthly talks on science, history, and weird topics in bar settings
- Lectures on tap (https://www.eventbrite.com/cc/lectures-on-tap-nyc-april-2026-4823839) - Professors giving lectures at breweriesC 

**Library Events:**
- New York Public Library (https://www.nypl.org/) - Author talks, workshops, exhibitions, and free cultural programs

**General Event Aggregators:**
- Meetup NYC (https://www.meetup.com/find/?location=us--ny--New%20York&source=EVENTS) - Community groups and interest-based meetups
- Eventbrite - Concerts, workshops, nightlife, and ticketed events
- The Skint (https://www.theskint.com/) - Free and cheap events across all categories
- Secret NYC (https://secretnyc.co/things-to-do/) - Hidden gems, pop-ups, and lesser-known activities
- Fever Up (https://feverup.com/en/new-york) - Curated events, immersive experiences, and unique activities
- Atlas Obscura (https://www.atlasobscura.com/things-to-do/new-york) - Unusual attractions, tours, and experiences
- Design My Night (https://www.designmynight.com/new-york) - Nightlife, bars, restaurants, and party planning
- NYC.gov Events (https://www.nyc.gov/main/events/?) - Official city events, festivals, and public programs
- Untapped Cities (https://www.untappedcities.com/tag/things-to-do/) - Insider guides and off-the-beaten-path NYC activities

### 3. Present Results

Format results with:
- Event name and venue
- Date/time
- Location and neighborhood
- Price (or "Free")
- Brief description highlighting what makes it interesting
- Link to event page or RSVP

## Instructions

### Searching Websites

When checking these sources:
1. Use `curl` or `puppeteer` to fetch event pages when available
2. Look for date, time, location, and price information
3. Extract event descriptions and highlight key details
4. Provide direct links to RSVP or buy tickets

## Constraints

- Only suggest events actually happening this week
- Verify event pages are current (some venues may have irregular schedules)
- For venues requiring tickets/RSVP, include booking links
- Don't suggest sold-out events unless specifically noted as such
- Include accessibility information when available

## Output Format

Structure recommendations as:

```markdown
# NYC Activities this week

### [Event Name]
- **When:** [Day, date, time]
- **Where:** [Venue name], [Address], [Neighborhood]
- **Cost:** [Price or "Free" or "Donation-based"]
- **Getting there:** [Nearest subway station]
- **What:** [1-2 sentence description]
- **Link:** [URL to event page]

[Repeat format above]

## Pro Tips
- [Insider tips about the venues, RSVP requirements, etc.]
- [Alternative suggestions if primary options are sold out]
- [Neighborhood recommendations for before/after the event]
- [etc]
```

## Special Notes

### Irregular Schedules
- **Nerd Nite NYC**: Typically monthly, check site for exact dates
- **ABC No Rio**: Schedule can be sporadic, always verify current info

### Booking Ahead
- Anthology Film Archives and Metrograph: Popular screenings sell out fast
- Alamo Drafthouse: Reserve seats online, especially for special events
- NYPL events: Some programs require registration

### Neighborhood Clusters
- **Lower East Side**: Metrograph, ABC No Rio, many bars/restaurants nearby
- **East Village**: Anthology Film Archives, Ars Nova, tons of nightlife
- **Lower Manhattan**: Alamo Drafthouse near Stone Street historic district

### Community Etiquette
- Times Up bike rides: All skill levels welcome, follow group ride rules
- ABC No Rio: Donation-based, cash at door
- Free library events: Often first-come first-served seating
