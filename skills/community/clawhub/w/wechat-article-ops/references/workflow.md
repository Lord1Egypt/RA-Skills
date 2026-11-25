# WeChat article

The titles, the article, the digest, the share blurb, and the four-slot note are free.

## Pictures

- Cover: 2.35:1. Title stays in the article unless the user asks for it on the picture.
- Section pictures: square, one per section they confirm, illustrating that section.
- Moments: 1:1, the same subject and palette as the cover.

`beatra.images.generate` opens the cover only when there is no brand image. After that, `beatra.images.transform` carries the cover, or the uploaded brand image, into the other frames.

Title on the cover is one `beatra.images.edit`: the exact title on a clear band, the picture unchanged. If the characters come back wrong, one text-free edit, then deliver the title beside the picture and stop.

## Spoken opening

Only when the user wants the article heard. `beatra.voices.list`, then one `beatra.speech.synthesize` of the opening, about thirty seconds. It is a slot on the materials card, not a second conversation.

## Worked article

Topic: how a neighborhood bakery times its sourdough. Reader: people who walk home past the shop. Three titles, one article with a digest, a two-sentence share blurb, four posting slots. Cover at 2.35:1 from a photo of the loaf, two section pictures and one Moments square transformed from that cover, no title burned in.
