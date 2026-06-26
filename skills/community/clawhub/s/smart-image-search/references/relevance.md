# Relevance ranking for image search

When multiple image candidates are available, do not blindly send the first one.

## Goal

Pick the image that is most likely to match the user's intended concept, meme, person, mascot, or object.

## Ranking heuristics

Score higher when:
- the page title, alt text, filename, or surrounding text contains the exact query
- the source domain looks semantically related to the query
- the candidate appears in multiple engines
- the image dimensions are reasonable and not tiny thumbnails
- the image URL or page URL contains meaningful query words

Score lower when:
- the result is obviously unrelated clickbait/news drift
- the result is a generic stock image
- the result is a duplicate thumbnail or sprite
- the result comes from a very noisy aggregation page with weak query match

## Query normalization

Before matching:
- preserve the original query
- also create a compact version without spaces
- split obvious tokens by spaces for Chinese mixed with Latin words
- treat common suffix words like `图`, `图片`, `表情包`, `头像`, `壁纸` as weak modifiers, not the main entity

## Practical decision rule

1. Gather top candidates from all available engines.
2. Compute a simple relevance score.
3. Prefer the highest-score candidate over the literal first result.
4. If confidence is weak, send 2-3 candidates instead of pretending there is one perfect match.
