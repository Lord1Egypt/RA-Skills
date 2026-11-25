# When a run goes wrong

## A task stays queued

Keep polling that task with `beatra.tasks.get`. Finished pictures stay deliverable.

## The create response never came back

Retry the identical payload and the same `client_request_id`. If the task id disappeared, list tasks and match the frozen request first.

## The price on the card looks wrong

Read `beatra.models.list` again and show the number it just returned.

## A still left the family

One `beatra.images.edit` on that still restores the poster's subject and palette. Own card, own id. If it is still apart, deliver it beside the poster and stop.
