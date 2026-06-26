# Query parameters

Support lightweight natural-language parameters inside the search query.

## Count
Examples:
- 3 images
- 2 pics
- 5 images

Meaning:
- preferred result count
- default 1 for high confidence, 3 for medium-confidence candidate mode
- cap at 5

## Intent override
Examples:
- official
- meme
- avatar
- wallpaper
- hd wallpaper

Meaning:
- if an explicit parameter exists, override auto-detected intent

## Orientation / style preferences
Examples:
- landscape
- portrait
- hd
- 4k

Meaning:
- adjust ranking and quality preferences
- do not treat these as the core entity

## Practical rule

Parse parameters first, then search the cleaned core query.
Return both:
- parsed parameters
- cleaned core query
