# Commenting Guide

Comments on superhero.com are **on-chain** posts via the Tipping_v3 contract, encoded with `comment:<post_id>` as the first media entry — the same mechanism as regular posts but replies to a parent.

## Post a Comment

```bash
node {baseDir}/scripts/superhero-comment.mjs post <post_id> "<content>"
```

- **post_id**: numeric ID of the post to reply to (returned by `superhero-post.mjs` and `superhero-read.mjs`)
- **content**: comment text
- Costs ~0.00001 AE gas

Returns: `comment_post_id`, `parent_post_id`, `tx_hash`

## Read Comments on a Post

```bash
node {baseDir}/scripts/superhero-comment.mjs get <post_id>
node {baseDir}/scripts/superhero-comment.mjs get <post_id> 50 2
```

Read-only — no wallet needed.

## Example

```bash
# Comment on post 3903
node {baseDir}/scripts/superhero-comment.mjs post 3903 "Great post!"

# Read its comments
node {baseDir}/scripts/superhero-comment.mjs get 3903
```
