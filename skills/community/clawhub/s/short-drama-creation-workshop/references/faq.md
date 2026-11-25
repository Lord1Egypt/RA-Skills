# When a run goes wrong

## A task stays queued

Keep polling that task with `beatra.tasks.get`. `queued` and `running` mean wait. Submit the same shot again only after this task has failed, and then with a new card.

## The create response never came back

Retry the identical payload and the same `client_request_id`. If the task id is what disappeared, call `beatra.tasks.list`, then `beatra.tasks.get`, and match the frozen request before that retry.

## The price on the card looks wrong

Read `beatra.models.list` again for that capability and show the number it just returned. A price from an earlier beat is not this beat's price.

## The still came back as the wrong person

Leave the accepted reference in place. One `beatra.images.edit` uses the wrong still as the base and asks only for the face, wardrobe, or prop that drifted. That repair is its own card and its own id. If the repair is still wrong, deliver both stills and the bible row, and stop.
