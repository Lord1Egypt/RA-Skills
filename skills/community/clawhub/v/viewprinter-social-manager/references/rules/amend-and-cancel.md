# amend-and-cancel: What can still change, and what cannot be recalled

## Priority: HIGH

## What goes wrong

A post is reported as cancelled when part of it is already going out, or an
amendment is attempted on a post that is frozen and the failure is a surprise.

## Read first

`posts_list` shows posts with the state of each destination, or one post given
its `post_id`. Call it before changing anything; `posts_save` takes the
`post_id` from there, both to amend and to cancel.

## Amending

**The caption and destinations can only change while every destination is
still pending.** Once any destination has started publishing, only the time can
change — new words mean a new post. Passing `account_ids` or `groups` replaces
the destination list entirely.

Changing `scheduled_at` re-aims delivery. There is no separate publish step.

## Cancelling

`posts_save` with the `post_id` and `cancel: true`. **It cannot recall what is
already going out.** Destinations that have not started are cancelled; any
mid-publish come back in `still_going`.

Report that honestly. "Cancelled" when two of five are already live is a lie the
user will discover on their own feed.

## Context

- Deleting media a pending post depends on is a different way to break a post.
  See `media-upload` for the delete warning.
