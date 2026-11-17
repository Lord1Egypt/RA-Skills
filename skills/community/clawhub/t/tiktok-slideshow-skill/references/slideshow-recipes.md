# Slideshow recipes for app marketing

Each recipe is 5 to 6 slides, one text block per slide, the app by slide 3. Brackets are filled
with the user's real details.

**Works without the user's own stories:** relatable scenario, tension then release, tiny
tutorial, be honest.
**Needs real stories:** someone else and a conflict, honest test, mistake list, before and after.

## 1. Relatable scenario (the default)

The viewer recognizes their own moment. Claims nothing about the user.

| Slide | Text |
|---|---|
| 1 | [category] apps when you [small, common failure]: |
| 2 | [what the usual app does to you then, felt] |
| 3 | [App]: [what it does instead, in plain words] (full-screen screenshot) |
| 4 | [what that changes for the viewer] |
| 5 | be honest. [question about the viewer's own experience] |

## 2. Someone else, conflict, reveal

Needs a real story. When it is real, this is one of the strongest formats.

| Slide | Text |
|---|---|
| 1 | my [person] said [their doubt] |
| 2 | so I showed them [what the app made or did] (screenshot or phone in hand) |
| 3 | [their reaction, in their words] |
| 4 | [the detail that changed their mind] |
| 5 | [question: whose side are you on?] |

## 3. Tension then release

| Slide | Text |
|---|---|
| 1 | [the moment the problem hurts] |
| 2 | [it gets worse / the usual fix fails] |
| 3 | then [App] (full-screen screenshot) |
| 4 | [the relief, specific] |
| 5 | [question] |

## 4. Honest test (needs real testing)

| Slide | Text |
|---|---|
| 1 | I tried [N] [category] apps for [time] |
| 2 | the one I kept: [App] (screenshot) |
| 3 | why: [the one thing it does differently] |
| 4 | the others: [one fair line each] |
| 5 | which one are you using? |

The app is the answer on slide 2. Only apps the user really tried, described fairly.

## 5. Mistake list (needs real experience)

| Slide | Text |
|---|---|
| 1 | [N] mistakes I made [doing X] |
| 2 | the one that cost me most: [what happened] |
| 3 | what I use now: [App] (screenshot) |
| 4 | the other mistakes, one line each |
| 5 | which one have you made? |

## 6. Tiny tutorial

| Slide | Text |
|---|---|
| 1 | how to [do X] in [short time] |
| 2 to 4 | step [n]: [action] (screenshot of that step in the app) |
| 5 | save this for later. [question] |

## Caption template

```
[main search phrase in natural words, first]
[one line of context]
[question]
#[specific tag] #[specific tag]
```

Example:

```
habit tracker without streaks, finally
miss a day and nothing resets
be honest, how many habit apps have you deleted?
#habittracker #productivityapps
```

## Worked example: a habit tracker (relatable scenario)

`examples/habit-app-slides.json`, photos in `examples/photos/` (one Pexels shoot: one person, one
bedroom, one light):

```json
{
  "theme": {"style": "highlight", "strip": "black"},
  "slides": [
    {"text": "habit apps when you miss ONE day:", "image": "photos/bed-phone.jpg", "position": "center"},
    {"text": "fell asleep once.\nstreak: 0", "image": "photos/bed-asleep.jpg", "position": "center"},
    {"text": "plodd: miss a day,\nnothing resets", "image": "screens/plodd-today.png", "layout": "fullscreen"},
    {"text": "5 out of 7 days still counts", "image": "photos/bed-morning.jpg", "position": "bottom"},
    {"text": "be honest. how many habit apps have you deleted?", "image": "photos/bed-scrolling.jpg", "position": "bottom"}
  ]
}
```

The app ("plodd") and its screen are made up for the example; in a real post it is the real app.

## Publish block (fill before asking for a yes)

| Field | Value |
|---|---|
| Account | [@account] |
| Slides | [N] JPEGs, 1080x1920 (TikTok), 1080x1350 (Instagram, separate post) |
| Caption | [caption] |
| TikTok mode | TikTok inbox draft (MEDIA_UPLOAD) or direct (DIRECT_POST, privacy [value]) |
| AI images | [yes: label in TikTok / caption disclosure for direct posts, or no] |
| When | [date and time, user's timezone] |
