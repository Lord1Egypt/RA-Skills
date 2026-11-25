# When a run goes wrong

## A task stays queued

Keep polling that task with `beatra.tasks.get`. Submit the same shot again only after this task has failed, and then with a new card.

## The create response never came back

Retry the identical payload and the same `client_request_id`. If the task id disappeared, call `beatra.tasks.list`, then `beatra.tasks.get`, and match the frozen request before that retry.

## The price on the card looks wrong

Read `beatra.models.list` again, or `beatra.social.tools.get` for a lookup, and show the number it just returned.

## The product in the still is not the photo

One `beatra.images.edit` uses that still as the base and asks to restore the product from the uploaded photo's shape and color. Own card, own id. If it is still wrong, deliver the still beside the photo and stop.
