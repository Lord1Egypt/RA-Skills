# When a run goes wrong

## A task stays queued

Keep polling that task with `beatra.tasks.get`. The article is already usable.

## The create response never came back

Retry the identical payload and the same `client_request_id`. If the task id disappeared, call `beatra.tasks.list`, then `beatra.tasks.get`, and match the frozen request before that retry.

## The price on the card looks wrong

Read `beatra.models.list` again and show the number it just returned.

## The cover title is misspelled

One `beatra.images.edit` sets the exact title and keeps the picture. Own card, own id. If the characters are still wrong, deliver the picture with the title written beside it and stop.
