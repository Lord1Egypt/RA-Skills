# When a run goes wrong

## A task stays queued

Keep polling that task with `beatra.tasks.get`. The titles are already usable.

## The create response never came back

Retry the identical payload and the same `client_request_id`. If the task id disappeared, call `beatra.tasks.list`, then `beatra.tasks.get`, and match the frozen request first.

## The price on the card looks wrong

Read `beatra.models.list` or `beatra.social.tools.get` again and show the number it just returned.

## The title on the cover is wrong

One `beatra.images.edit` sets the exact title and keeps the picture. Own card, own id. If the characters are still wrong, deliver the cover and the title as text and stop.
