# WordPress.com access policy

An access policy limits which endpoints WordPress.com connections may call through Maton. WordPress.com doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/wordpress#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for WordPress.com: its 228 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create wordpress --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "rest/v1.1/sites/{id}"},
    {"method": "GET", "path": "wp/v2/sites/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/post-counts/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/posts"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/posts/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/posts/{id}/likes"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/posts/{id}/likes/mine"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/posts/{id}/reblogs/mine"},
    {"method": "POST", "path": "rest/v1.1/sites/{id}/posts/{id}/related"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/posts/{id}/replies"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/posts/{id}/subscribers"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/posts/{id}/subscribers/mine"},
    {"method": "GET", "path": "wp/v2/sites/{id}/posts"},
    {"method": "GET", "path": "wp/v2/sites/{id}/posts/{id}"},
    {"method": "GET", "path": "wp/v2/sites/{id}/posts/{id}/autosaves"},
    {"method": "GET", "path": "wp/v2/sites/{id}/posts/{id}/autosaves/{id}"},
    {"method": "GET", "path": "wp/v2/sites/{id}/posts/{id}/revisions"},
    {"method": "GET", "path": "wp/v2/sites/{id}/posts/{id}/revisions/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/dropdown-pages"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/page-templates"},
    {"method": "GET", "path": "wp/v2/sites/{id}/pages"},
    {"method": "GET", "path": "wp/v2/sites/{id}/pages/{id}"},
    {"method": "GET", "path": "wp/v2/sites/{id}/pages/{id}/autosaves"},
    {"method": "GET", "path": "wp/v2/sites/{id}/pages/{id}/autosaves/{id}"},
    {"method": "GET", "path": "wp/v2/sites/{id}/pages/{id}/revisions"},
    {"method": "GET", "path": "wp/v2/sites/{id}/pages/{id}/revisions/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/post-types"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/post-types/{id}/taxonomies"},
    {"method": "GET", "path": "wp/v2/sites/{id}/statuses"},
    {"method": "GET", "path": "wp/v2/sites/{id}/statuses/{id}"},
    {"method": "GET", "path": "wp/v2/sites/{id}/types"},
    {"method": "GET", "path": "wp/v2/sites/{id}/types/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/comment-counts"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/comment-history/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/comments"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/comments-tree"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/comments/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/comments/{id}/likes"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/comments/{id}/likes/mine"},
    {"method": "GET", "path": "wp/v2/sites/{id}/comments"},
    {"method": "GET", "path": "wp/v2/sites/{id}/comments/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/categories"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/categories/{id}"},
    {"method": "GET", "path": "wp/v2/sites/{id}/categories"},
    {"method": "GET", "path": "wp/v2/sites/{id}/categories/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/tags"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/tags/{id}"},
    {"method": "GET", "path": "wp/v2/sites/{id}/tags"},
    {"method": "GET", "path": "wp/v2/sites/{id}/tags/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/taxonomies/{id}/terms"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/taxonomies/{id}/terms/{id}"},
    {"method": "GET", "path": "wp/v2/sites/{id}/taxonomies"},
    {"method": "GET", "path": "wp/v2/sites/{id}/taxonomies/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/media"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/media/{id}"},
    {"method": "GET", "path": "wp/v2/sites/{id}/media"},
    {"method": "GET", "path": "wp/v2/sites/{id}/media/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/users"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/users/{id}"},
    {"method": "GET", "path": "rest/v1.1/users/suggest"},
    {"method": "GET", "path": "rest/v1.1/users/{id}"},
    {"method": "GET", "path": "rest/v1.1/users/{id}/posts"},
    {"method": "GET", "path": "wp/v2/sites/{id}/users"},
    {"method": "GET", "path": "wp/v2/sites/{id}/users/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/followers"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/followers/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/follows"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/follows/mine"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/archives"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/author/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/clicks"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/clicks/emails/summary"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/clicks/emails/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/clicks/emails/{id}/client"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/clicks/emails/{id}/country"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/clicks/emails/{id}/device"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/clicks/emails/{id}/link"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/clicks/emails/{id}/rate"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/clicks/emails/{id}/user-content-link"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/comment-followers"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/comments"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/country-views"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/devices/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/emails/summary"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/file-downloads"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/followers"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/highlights"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/location-views/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/opens/emails/summary"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/opens/emails/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/opens/emails/{id}/client"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/opens/emails/{id}/country"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/opens/emails/{id}/device"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/opens/emails/{id}/rate"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/post/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/publicize"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/referrers"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/referrers/spam"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/search-terms"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/streak"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/summary"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/tags"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/top-authors"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/top-posts"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/ua-queries"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/utm/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/utm/{id}/top_posts"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/video-plays"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/video/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/views-by/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/stats/views/posts"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/menus"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/menus/{id}"},
    {"method": "GET", "path": "wp/v2/sites/{id}/menu-items"},
    {"method": "GET", "path": "wp/v2/sites/{id}/menu-items/{id}"},
    {"method": "GET", "path": "wp/v2/sites/{id}/menu-locations"},
    {"method": "GET", "path": "wp/v2/sites/{id}/menu-locations/{id}"},
    {"method": "GET", "path": "wp/v2/sites/{id}/menus"},
    {"method": "GET", "path": "wp/v2/sites/{id}/menus/{id}"},
    {"method": "GET", "path": "wp/v2/sites/{id}/navigation"},
    {"method": "GET", "path": "wp/v2/sites/{id}/navigation/{id}"},
    {"method": "GET", "path": "wp/v2/sites/{id}/navigation/{id}/autosaves"},
    {"method": "GET", "path": "wp/v2/sites/{id}/navigation/{id}/autosaves/{id}"},
    {"method": "GET", "path": "wp/v2/sites/{id}/navigation/{id}/revisions"},
    {"method": "GET", "path": "wp/v2/sites/{id}/navigation/{id}/revisions/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/widgets"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/widgets/{id}"},
    {"method": "GET", "path": "wp/v2/sites/{id}/sidebars"},
    {"method": "GET", "path": "wp/v2/sites/{id}/sidebars/{id}"},
    {"method": "GET", "path": "wp/v2/sites/{id}/widget-types"},
    {"method": "GET", "path": "wp/v2/sites/{id}/widget-types/{id}"},
    {"method": "GET", "path": "wp/v2/sites/{id}/widgets"},
    {"method": "GET", "path": "wp/v2/sites/{id}/widgets/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/headers/mine"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/headers/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/themes"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/themes/mine"},
    {"method": "GET", "path": "rest/v1.1/themes"},
    {"method": "GET", "path": "rest/v1.1/themes/{id}"},
    {"method": "GET", "path": "wp/v2/sites/{id}/themes"},
    {"method": "GET", "path": "wp/v2/sites/{id}/themes/{id}"},
    {"method": "GET", "path": "wp/v2/sites/{id}/template-parts/**"},
    {"method": "GET", "path": "wp/v2/sites/{id}/templates/**"},
    {"method": "GET", "path": "wp/v2/sites/{id}/block-patterns/categories"},
    {"method": "GET", "path": "wp/v2/sites/{id}/block-patterns/patterns"},
    {"method": "GET", "path": "wp/v2/sites/{id}/block-types/**"},
    {"method": "GET", "path": "wp/v2/sites/{id}/blocks"},
    {"method": "GET", "path": "wp/v2/sites/{id}/blocks/{id}"},
    {"method": "GET", "path": "wp/v2/sites/{id}/blocks/{id}/autosaves"},
    {"method": "GET", "path": "wp/v2/sites/{id}/blocks/{id}/autosaves/{id}"},
    {"method": "GET", "path": "wp/v2/sites/{id}/blocks/{id}/revisions"},
    {"method": "GET", "path": "wp/v2/sites/{id}/blocks/{id}/revisions/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/embeds"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/shortcodes"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/sharing-buttons"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/publicize-connections"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/publicize-connections/{id}"},
    {"method": "POST", "path": "rest/v1.1/sites/{id}/search"},
    {"method": "GET", "path": "wp/v2/sites/{id}/search"},
    {"method": "GET", "path": "wp/v2/sites/{id}/settings"},
    {"method": "GET", "path": "wp/v2/sites/{id}/plugins"},
    {"method": "GET", "path": "wp/v2/sites/{id}/plugins/{id}"},
    {"method": "GET", "path": "wp/v2/sites/{id}/feedback"},
    {"method": "GET", "path": "wp/v2/sites/{id}/feedback/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/imports"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/imports/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/wordads/earnings"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/wordads/settings"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/wordads/stats"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/wordads/tos"},
    {"method": "GET", "path": "rest/v1.1/jetpack-blogs"},
    {"method": "GET", "path": "rest/v1.1/jetpack-blogs/{id}"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/automated-transfers/status"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/sync/status"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/translations"},
    {"method": "GET", "path": "rest/v1.1/sites/{id}/updates"},
    {"method": "GET", "path": "rest/v1.1/me"},
    {"method": "GET", "path": "rest/v1.1/me/billing-history"},
    {"method": "GET", "path": "rest/v1.1/me/connected-applications"},
    {"method": "GET", "path": "rest/v1.1/me/connected-applications/{id}"},
    {"method": "GET", "path": "rest/v1.1/me/keyring-connections"},
    {"method": "GET", "path": "rest/v1.1/me/keyring-connections/{id}"},
    {"method": "GET", "path": "rest/v1.1/me/likes"},
    {"method": "GET", "path": "rest/v1.1/me/mailboxes"},
    {"method": "GET", "path": "rest/v1.1/me/posts"},
    {"method": "GET", "path": "rest/v1.1/me/preferences"},
    {"method": "GET", "path": "rest/v1.1/me/publicize-connections"},
    {"method": "GET", "path": "rest/v1.1/me/publicize-connections/{id}"},
    {"method": "GET", "path": "rest/v1.1/me/settings"},
    {"method": "POST", "path": "rest/v1.1/me/settings/password/validate"},
    {"method": "GET", "path": "rest/v1.1/me/settings/profile-links"},
    {"method": "GET", "path": "rest/v1.1/me/sites"},
    {"method": "GET", "path": "rest/v1.1/me/sites/compact"},
    {"method": "GET", "path": "rest/v1.1/me/sites/features"},
    {"method": "GET", "path": "rest/v1.1/me/sites/plugins"},
    {"method": "GET", "path": "rest/v1.1/me/two-step"},
    {"method": "GET", "path": "rest/v1/notifications"},
    {"method": "GET", "path": "rest/v1/notifications/{id}"},
    {"method": "GET", "path": "rest/v1.1/read/email-settings"},
    {"method": "GET", "path": "rest/v1.1/read/feed"},
    {"method": "GET", "path": "rest/v1.1/read/feed/{id}"},
    {"method": "GET", "path": "rest/v1.1/read/following"},
    {"method": "GET", "path": "rest/v1.1/read/following/mine"},
    {"method": "GET", "path": "rest/v1.1/read/liked"},
    {"method": "GET", "path": "rest/v1.1/read/lists/{id}"},
    {"method": "GET", "path": "rest/v1.1/read/menu"},
    {"method": "GET", "path": "rest/v1.1/read/recommendations/mine"},
    {"method": "GET", "path": "rest/v1.1/read/sites/{id}/posts/{id}"},
    {"method": "GET", "path": "rest/v1.1/read/subscriptions-count"},
    {"method": "GET", "path": "rest/v1.1/read/tags"},
    {"method": "GET", "path": "rest/v1.1/read/tags/alphabetic"},
    {"method": "GET", "path": "rest/v1.1/read/tags/{id}"},
    {"method": "GET", "path": "rest/v1.1/read/tags/{id}/mine"},
    {"method": "GET", "path": "rest/v1.1/read/tags/{id}/posts"},
    {"method": "GET", "path": "rest/v1.1/read/trending/tags"},
    {"method": "GET", "path": "rest/v1.1/manual_payment/{id}"},
    {"method": "GET", "path": "rest/v1.1/freshly-pressed"},
    {"method": "GET", "path": "rest/v1.1/insights"},
    {"method": "GET", "path": "rest/v1.1/insights/{id}"},
    {"method": "GET", "path": "rest/v1.1/meta/external-services"},
    {"method": "GET", "path": "rest/v1.1/meta/external-services/{id}"},
    {"method": "GET", "path": "rest/v1.1/meta/sharing-buttons"},
    {"method": "GET", "path": "rest/v1.1/support/alternates/{id}/posts/{id}"},
    {"method": "GET", "path": "rest/v1.1/videos/{id}"},
    {"method": "GET", "path": "rest/v1.1/videos/{id}/chapters"},
    {"method": "GET", "path": "rest/v1.1/videos/{id}/playlist/{id}"},
    {"method": "GET", "path": "rest/v1.1/videos/{id}/poster"}
  ],
  "deny": []
}
```

## Endpoints

The WordPress.com endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | rest/v1.1/sites/{id} | read | sites | Get information about a site. |
| GET | wp/v2/sites/{id} | read | sites | Get the WP REST API v2 index for a site (available routes). |
| GET | rest/v1.1/sites/{id}/post-counts/{id} | read | posts | Get number of posts in the post type groups by post status. |
| GET | rest/v1.1/sites/{id}/posts | read | posts | Get a list of matching posts. |
| POST | rest/v1.1/sites/{id}/posts/delete | write | posts | Delete multiple posts. |
| POST | rest/v1.1/sites/{id}/posts/new | write | posts | Create a post. |
| POST | rest/v1.1/sites/{id}/posts/restore | write | posts | Restore multiple posts. |
| GET | rest/v1.1/sites/{id}/posts/{id} | read | posts | Get a single post (by ID). |
| POST | rest/v1.1/sites/{id}/posts/{id} | write | posts | Edit a post. |
| POST | rest/v1.1/sites/{id}/posts/{id}/delete | write | posts | Delete a post. |
| GET | rest/v1.1/sites/{id}/posts/{id}/likes | read | posts | Get a list of the likes for a post. |
| GET | rest/v1.1/sites/{id}/posts/{id}/likes/mine | read | posts | Get the current user's like status for a post. |
| POST | rest/v1.1/sites/{id}/posts/{id}/likes/mine/delete | write | posts | Unlike a post. |
| POST | rest/v1.1/sites/{id}/posts/{id}/likes/new | write | posts | Like a post. |
| GET | rest/v1.1/sites/{id}/posts/{id}/reblogs/mine | read | posts | Get reblog status for a post. |
| POST | rest/v1.1/sites/{id}/posts/{id}/reblogs/new | write | posts | Reblog a post. |
| POST | rest/v1.1/sites/{id}/posts/{id}/related | read | posts | Find posts related to a post (a query sent as POST). |
| GET | rest/v1.1/sites/{id}/posts/{id}/replies | read | posts | Get a list of recent comments on a post. |
| POST | rest/v1.1/sites/{id}/posts/{id}/replies/new | write | posts | Create a comment on a post. |
| POST | rest/v1.1/sites/{id}/posts/{id}/restore | write | posts | Restore a post or page from the trash to its previous status. |
| GET | rest/v1.1/sites/{id}/posts/{id}/subscribers | read | posts | Get a list of the specified post's subscribers. |
| GET | rest/v1.1/sites/{id}/posts/{id}/subscribers/mine | read | posts | Get subscription status of the specified post for the current user. |
| POST | rest/v1.1/sites/{id}/posts/{id}/subscribers/mine/delete | write | posts | Unsubscribe the current user from the specified post. |
| POST | rest/v1.1/sites/{id}/posts/{id}/subscribers/mine/update | write | posts | Subscribe current user to be notified of the specified post's comments. |
| POST | rest/v1.1/sites/{id}/posts/{id}/subscribers/new | write | posts | Subscribe current user to be notified of the specified post's comments. |
| GET | wp/v2/sites/{id}/posts | read | posts | List posts (WP REST API v2). |
| POST | wp/v2/sites/{id}/posts | write | posts | Create a post (WP REST API v2). |
| GET | wp/v2/sites/{id}/posts/{id} | read | posts | Get a post (WP REST API v2). |
| POST | wp/v2/sites/{id}/posts/{id} | write | posts | Update a post (WP REST API v2). |
| PUT | wp/v2/sites/{id}/posts/{id} | write | posts | Update a post (WP REST API v2). |
| PATCH | wp/v2/sites/{id}/posts/{id} | write | posts | Update a post (WP REST API v2). |
| DELETE | wp/v2/sites/{id}/posts/{id} | write | posts | Delete a post (WP REST API v2). |
| GET | wp/v2/sites/{id}/posts/{id}/autosaves | read | posts | List the autosaves of a post (WP REST API v2). |
| POST | wp/v2/sites/{id}/posts/{id}/autosaves | write | posts | Create an autosave of a post (WP REST API v2). |
| GET | wp/v2/sites/{id}/posts/{id}/autosaves/{id} | read | posts | Get one autosave of a post (WP REST API v2). |
| GET | wp/v2/sites/{id}/posts/{id}/revisions | read | posts | List the revisions of a post (WP REST API v2). |
| GET | wp/v2/sites/{id}/posts/{id}/revisions/{id} | read | posts | Get one revision of a post (WP REST API v2). |
| DELETE | wp/v2/sites/{id}/posts/{id}/revisions/{id} | write | posts | Delete a revision of a post (WP REST API v2). |
| GET | rest/v1.1/sites/{id}/dropdown-pages | read | pages | Get a list of pages to be displayed as options in a select-a-page-dropdown. |
| GET | rest/v1.1/sites/{id}/page-templates | read | pages | Get a list of page templates supported by a site. |
| GET | wp/v2/sites/{id}/pages | read | pages | List pages (WP REST API v2). |
| POST | wp/v2/sites/{id}/pages | write | pages | Create a page (WP REST API v2). |
| GET | wp/v2/sites/{id}/pages/{id} | read | pages | Get a page (WP REST API v2). |
| POST | wp/v2/sites/{id}/pages/{id} | write | pages | Update a page (WP REST API v2). |
| PUT | wp/v2/sites/{id}/pages/{id} | write | pages | Update a page (WP REST API v2). |
| PATCH | wp/v2/sites/{id}/pages/{id} | write | pages | Update a page (WP REST API v2). |
| DELETE | wp/v2/sites/{id}/pages/{id} | write | pages | Delete a page (WP REST API v2). |
| GET | wp/v2/sites/{id}/pages/{id}/autosaves | read | pages | List the autosaves of a page (WP REST API v2). |
| POST | wp/v2/sites/{id}/pages/{id}/autosaves | write | pages | Create an autosave of a page (WP REST API v2). |
| GET | wp/v2/sites/{id}/pages/{id}/autosaves/{id} | read | pages | Get one autosave of a page (WP REST API v2). |
| GET | wp/v2/sites/{id}/pages/{id}/revisions | read | pages | List the revisions of a page (WP REST API v2). |
| GET | wp/v2/sites/{id}/pages/{id}/revisions/{id} | read | pages | Get one revision of a page (WP REST API v2). |
| DELETE | wp/v2/sites/{id}/pages/{id}/revisions/{id} | write | pages | Delete a revision of a page (WP REST API v2). |
| GET | rest/v1.1/sites/{id}/post-types | read | post-types | Get a list of post types available for a site. |
| GET | rest/v1.1/sites/{id}/post-types/{id}/taxonomies | read | post-types | Get a list of taxonomies associated with a post type. |
| GET | wp/v2/sites/{id}/statuses | read | post-types | List post statuses (WP REST API v2). |
| GET | wp/v2/sites/{id}/statuses/{id} | read | post-types | Get a post status (WP REST API v2). |
| GET | wp/v2/sites/{id}/types | read | post-types | List post types (WP REST API v2). |
| GET | wp/v2/sites/{id}/types/{id} | read | post-types | Get a post type (WP REST API v2). |
| GET | rest/v1.1/sites/{id}/comment-counts | read | comments | Get comment counts for each available status. |
| GET | rest/v1.1/sites/{id}/comment-history/{id} | read | comments | Get the audit history for given comment. |
| GET | rest/v1.1/sites/{id}/comments | read | comments | Get a list of recent comments. |
| GET | rest/v1.1/sites/{id}/comments-tree | read | comments | Get a comments tree for site. |
| GET | rest/v1.1/sites/{id}/comments/{id} | read | comments | Get a single comment. |
| POST | rest/v1.1/sites/{id}/comments/{id} | write | comments | Edit a comment. |
| POST | rest/v1.1/sites/{id}/comments/{id}/delete | write | comments | Delete a comment. |
| GET | rest/v1.1/sites/{id}/comments/{id}/likes | read | comments | Get the likes for a comment. |
| GET | rest/v1.1/sites/{id}/comments/{id}/likes/mine | read | comments | Get your like status for a comment. |
| POST | rest/v1.1/sites/{id}/comments/{id}/likes/mine/delete | write | comments | Remove your like from a comment. |
| POST | rest/v1.1/sites/{id}/comments/{id}/likes/new | write | comments | Like a comment. |
| POST | rest/v1.1/sites/{id}/comments/{id}/replies/new | write | comments | Create a comment as a reply to another comment. |
| GET | wp/v2/sites/{id}/comments | read | comments | List comments (WP REST API v2). |
| POST | wp/v2/sites/{id}/comments | write | comments | Create a comment (WP REST API v2). |
| GET | wp/v2/sites/{id}/comments/{id} | read | comments | Get a comment (WP REST API v2). |
| POST | wp/v2/sites/{id}/comments/{id} | write | comments | Update a comment (WP REST API v2). |
| PUT | wp/v2/sites/{id}/comments/{id} | write | comments | Update a comment (WP REST API v2). |
| PATCH | wp/v2/sites/{id}/comments/{id} | write | comments | Update a comment (WP REST API v2). |
| DELETE | wp/v2/sites/{id}/comments/{id} | write | comments | Delete a comment (WP REST API v2). |
| GET | rest/v1.1/sites/{id}/categories | read | categories | Get a list of a site's categories. |
| POST | rest/v1.1/sites/{id}/categories/new | write | categories | Create a new category. |
| GET | rest/v1.1/sites/{id}/categories/{id} | read | categories | Get information about a single category. |
| POST | rest/v1.1/sites/{id}/categories/{id} | write | categories | Edit a category. |
| POST | rest/v1.1/sites/{id}/categories/{id}/delete | write | categories | Delete a category. |
| GET | wp/v2/sites/{id}/categories | read | categories | List categories (WP REST API v2). |
| POST | wp/v2/sites/{id}/categories | write | categories | Create a category (WP REST API v2). |
| GET | wp/v2/sites/{id}/categories/{id} | read | categories | Get a category (WP REST API v2). |
| POST | wp/v2/sites/{id}/categories/{id} | write | categories | Update a category (WP REST API v2). |
| PUT | wp/v2/sites/{id}/categories/{id} | write | categories | Update a category (WP REST API v2). |
| PATCH | wp/v2/sites/{id}/categories/{id} | write | categories | Update a category (WP REST API v2). |
| DELETE | wp/v2/sites/{id}/categories/{id} | write | categories | Delete a category (WP REST API v2). |
| GET | rest/v1.1/sites/{id}/tags | read | tags | Get a list of a site's tags. |
| POST | rest/v1.1/sites/{id}/tags/new | write | tags | Create a new tag. |
| GET | rest/v1.1/sites/{id}/tags/{id} | read | tags | Get information about a single tag. |
| POST | rest/v1.1/sites/{id}/tags/{id} | write | tags | Edit a tag. |
| POST | rest/v1.1/sites/{id}/tags/{id}/delete | write | tags | Delete a tag. |
| GET | wp/v2/sites/{id}/tags | read | tags | List tags (WP REST API v2). |
| POST | wp/v2/sites/{id}/tags | write | tags | Create a tag (WP REST API v2). |
| GET | wp/v2/sites/{id}/tags/{id} | read | tags | Get a tag (WP REST API v2). |
| POST | wp/v2/sites/{id}/tags/{id} | write | tags | Update a tag (WP REST API v2). |
| PUT | wp/v2/sites/{id}/tags/{id} | write | tags | Update a tag (WP REST API v2). |
| PATCH | wp/v2/sites/{id}/tags/{id} | write | tags | Update a tag (WP REST API v2). |
| DELETE | wp/v2/sites/{id}/tags/{id} | write | tags | Delete a tag (WP REST API v2). |
| GET | rest/v1.1/sites/{id}/taxonomies/{id}/terms | read | taxonomies | Get a list of a site's terms by taxonomy. |
| POST | rest/v1.1/sites/{id}/taxonomies/{id}/terms/new | write | taxonomies | Create a new term. |
| GET | rest/v1.1/sites/{id}/taxonomies/{id}/terms/{id} | read | taxonomies | Get information about a single term. |
| POST | rest/v1.1/sites/{id}/taxonomies/{id}/terms/{id} | write | taxonomies | Edit a term. |
| POST | rest/v1.1/sites/{id}/taxonomies/{id}/terms/{id}/delete | write | taxonomies | Delete a term. |
| GET | wp/v2/sites/{id}/taxonomies | read | taxonomies | List taxonomies (WP REST API v2). |
| GET | wp/v2/sites/{id}/taxonomies/{id} | read | taxonomies | Get a taxonomy (WP REST API v2). |
| GET | rest/v1.1/sites/{id}/media | read | media | Get a list of items in the media library. |
| POST | rest/v1.1/sites/{id}/media/new | write | media | Upload a new piece of media. |
| GET | rest/v1.1/sites/{id}/media/{id} | read | media | Get a single media item (by ID). |
| POST | rest/v1.1/sites/{id}/media/{id} | write | media | Edit basic information about a media item. |
| POST | rest/v1.1/sites/{id}/media/{id}/delete | write | media | Delete a piece of media. |
| POST | rest/v1.1/sites/{id}/media/{id}/edit | write | media | Edit a media item. |
| GET | wp/v2/sites/{id}/media | read | media | List media items (WP REST API v2). |
| POST | wp/v2/sites/{id}/media | write | media | Create a media item (WP REST API v2). |
| GET | wp/v2/sites/{id}/media/{id} | read | media | Get a media item (WP REST API v2). |
| POST | wp/v2/sites/{id}/media/{id} | write | media | Update a media item (WP REST API v2). |
| PUT | wp/v2/sites/{id}/media/{id} | write | media | Update a media item (WP REST API v2). |
| PATCH | wp/v2/sites/{id}/media/{id} | write | media | Update a media item (WP REST API v2). |
| DELETE | wp/v2/sites/{id}/media/{id} | write | media | Delete a media item (WP REST API v2). |
| POST | wp/v2/sites/{id}/media/{id}/edit | write | media | Apply image edits to a media item (WP REST API v2). |
| POST | wp/v2/sites/{id}/media/{id}/finalize | write | media | Finalize an uploaded media item (WP REST API v2). |
| POST | wp/v2/sites/{id}/media/{id}/post-process | write | media | Run post-processing on an uploaded media item (WP REST API v2). |
| POST | wp/v2/sites/{id}/media/{id}/sideload | write | media | Sideload a file onto a media item (WP REST API v2). |
| POST | rest/v1.1/sites/{id}/invites/new | write | users | Invite one or more users to your site. |
| GET | rest/v1.1/sites/{id}/users | read | users | List the users of a site. |
| GET | rest/v1.1/sites/{id}/users/{id} | read | users | Get details of a user of a site by ID or login. |
| POST | rest/v1.1/sites/{id}/users/{id} | write | users | Update details of a user of a site. |
| POST | rest/v1.1/sites/{id}/users/{id}/delete | write | users | Deletes or removes a user of a site. |
| GET | rest/v1.1/users/suggest | read | users | Get a list of possible users to suggest for @mentions. |
| GET | rest/v1.1/users/{id} | read | users | Get metadata about a user. |
| GET | rest/v1.1/users/{id}/posts | read | users | Get a list of published posts authored by a specified user across their public sites, ordered by date in descending order. |
| GET | wp/v2/sites/{id}/users | read | users | List site users (WP REST API v2). |
| POST | wp/v2/sites/{id}/users | write | users | Create a user (WP REST API v2). |
| GET | wp/v2/sites/{id}/users/{id} | read | users | Get a user (WP REST API v2). |
| POST | wp/v2/sites/{id}/users/{id} | write | users | Update a user (WP REST API v2). |
| PUT | wp/v2/sites/{id}/users/{id} | write | users | Update a user (WP REST API v2). |
| PATCH | wp/v2/sites/{id}/users/{id} | write | users | Update a user (WP REST API v2). |
| DELETE | wp/v2/sites/{id}/users/{id} | write | users | Delete a user (WP REST API v2). |
| GET | rest/v1.1/sites/{id}/followers | read | followers | View a site's followers. |
| GET | rest/v1.1/sites/{id}/followers/{id} | read | followers | View a site's follower or subscriber. |
| GET | rest/v1.1/sites/{id}/follows | read | followers | List a site's followers in reverse chronological order. |
| GET | rest/v1.1/sites/{id}/follows/mine | read | followers | Get blog following status for the current user. |
| POST | rest/v1.1/sites/{id}/follows/mine/delete | write | followers | Unfollow a blog. |
| POST | rest/v1.1/sites/{id}/follows/new | write | followers | Follow a blog. |
| GET | rest/v1.1/sites/{id}/stats | read | stats | Get a site's stats. |
| GET | rest/v1.1/sites/{id}/stats/archives | read | stats | View a site's archives. |
| GET | rest/v1.1/sites/{id}/stats/author/{id} | read | stats | View an author's views, likes and comments. |
| GET | rest/v1.1/sites/{id}/stats/clicks | read | stats | View a site's outbound clicks. |
| GET | rest/v1.1/sites/{id}/stats/clicks/emails/summary | read | stats | View the total number of email clicks for each post. |
| GET | rest/v1.1/sites/{id}/stats/clicks/emails/{id} | read | stats | View chart stats related to email clicks by period. |
| GET | rest/v1.1/sites/{id}/stats/clicks/emails/{id}/client | read | stats | View email clicks by client. |
| GET | rest/v1.1/sites/{id}/stats/clicks/emails/{id}/country | read | stats | View email clicks by country. |
| GET | rest/v1.1/sites/{id}/stats/clicks/emails/{id}/device | read | stats | View email clicks by device. |
| GET | rest/v1.1/sites/{id}/stats/clicks/emails/{id}/link | read | stats | View email clicks by link. |
| GET | rest/v1.1/sites/{id}/stats/clicks/emails/{id}/rate | read | stats | View email clicks rate by post. |
| GET | rest/v1.1/sites/{id}/stats/clicks/emails/{id}/user-content-link | read | stats | View email clicks by user content link. |
| GET | rest/v1.1/sites/{id}/stats/comment-followers | read | stats | View a site's comment followers. |
| GET | rest/v1.1/sites/{id}/stats/comments | read | stats | View a site's top comment authors and most-commented posts. |
| GET | rest/v1.1/sites/{id}/stats/country-views | read | stats | View a site's views by country. |
| GET | rest/v1.1/sites/{id}/stats/devices/{id} | read | stats | Fetch site's Device properties statistics. |
| GET | rest/v1.1/sites/{id}/stats/emails/summary | read | stats | View the total number of email opens and clicks for each post. |
| GET | rest/v1.1/sites/{id}/stats/file-downloads | read | stats | View a site's file downloads. |
| GET | rest/v1.1/sites/{id}/stats/followers | read | stats | View a site's followers. |
| GET | rest/v1.1/sites/{id}/stats/highlights | read | stats | View highlight metrics from the last seven days. |
| GET | rest/v1.1/sites/{id}/stats/location-views/{id} | read | stats | View a site's views by country, region and city. |
| GET | rest/v1.1/sites/{id}/stats/opens/emails/summary | read | stats | View the total number of email opens for each post. |
| GET | rest/v1.1/sites/{id}/stats/opens/emails/{id} | read | stats | View multiple stats related to email opens by post. |
| GET | rest/v1.1/sites/{id}/stats/opens/emails/{id}/client | read | stats | View email opens stats by client. |
| GET | rest/v1.1/sites/{id}/stats/opens/emails/{id}/country | read | stats | View email opens stats by country. |
| GET | rest/v1.1/sites/{id}/stats/opens/emails/{id}/device | read | stats | View email opens stats by device. |
| GET | rest/v1.1/sites/{id}/stats/opens/emails/{id}/rate | read | stats | View email opens rate by post. |
| GET | rest/v1.1/sites/{id}/stats/post/{id} | read | stats | View a post's views. |
| GET | rest/v1.1/sites/{id}/stats/publicize | read | stats | View a site's publicize follower counts. |
| GET | rest/v1.1/sites/{id}/stats/referrers | read | stats | View a site's referrers. |
| GET | rest/v1.1/sites/{id}/stats/referrers/spam | read | stats | List referrers marked as spam. |
| POST | rest/v1.1/sites/{id}/stats/referrers/spam/delete | write | stats | Unreport a referrer as spam. |
| POST | rest/v1.1/sites/{id}/stats/referrers/spam/new | write | stats | Report a referrer as spam. |
| GET | rest/v1.1/sites/{id}/stats/search-terms | read | stats | View search terms used to find the site. |
| GET | rest/v1.1/sites/{id}/stats/streak | read | stats | Get stats for Calendar Heatmap. |
| GET | rest/v1.1/sites/{id}/stats/summary | read | stats | View a site's summarized views, visitors, likes and comments. |
| GET | rest/v1.1/sites/{id}/stats/tags | read | stats | View a site's views by tags and categories. |
| GET | rest/v1.1/sites/{id}/stats/top-authors | read | stats | View a site's top authors. |
| GET | rest/v1.1/sites/{id}/stats/top-posts | read | stats | View a site's top posts and pages by views. |
| GET | rest/v1.1/sites/{id}/stats/ua-queries | read | stats | Run an allowlisted Unified Analytics query template for a site and return its rows. |
| GET | rest/v1.1/sites/{id}/stats/utm/{id} | read | stats | Fetch site's UTM param statistics. |
| GET | rest/v1.1/sites/{id}/stats/utm/{id}/top_posts | read | stats | Fetch top posts for a given UTM parameter value. |
| GET | rest/v1.1/sites/{id}/stats/video-plays | read | stats | View a site's video plays. |
| GET | rest/v1.1/sites/{id}/stats/video/{id} | read | stats | View the details of a single video. |
| GET | rest/v1.1/sites/{id}/stats/views-by/{id} | read | stats | Fetch a site's views over a range of days, folded into a fixed dimension. |
| GET | rest/v1.1/sites/{id}/stats/views/posts | read | stats | View the total number of views for each post. |
| GET | rest/v1.1/sites/{id}/menus | read | menus | Get a list of all navigation menus. |
| POST | rest/v1.1/sites/{id}/menus/new | write | menus | Create a new navigation menu. |
| GET | rest/v1.1/sites/{id}/menus/{id} | read | menus | Get a single navigation menu. |
| POST | rest/v1.1/sites/{id}/menus/{id} | write | menus | Update a navigation menu. |
| POST | rest/v1.1/sites/{id}/menus/{id}/delete | write | menus | Delete a navigation menu. |
| GET | wp/v2/sites/{id}/menu-items | read | menus | List menu items (WP REST API v2). |
| POST | wp/v2/sites/{id}/menu-items | write | menus | Create a menu item (WP REST API v2). |
| GET | wp/v2/sites/{id}/menu-items/{id} | read | menus | Get a menu item (WP REST API v2). |
| POST | wp/v2/sites/{id}/menu-items/{id} | write | menus | Update a menu item (WP REST API v2). |
| PUT | wp/v2/sites/{id}/menu-items/{id} | write | menus | Update a menu item (WP REST API v2). |
| PATCH | wp/v2/sites/{id}/menu-items/{id} | write | menus | Update a menu item (WP REST API v2). |
| DELETE | wp/v2/sites/{id}/menu-items/{id} | write | menus | Delete a menu item (WP REST API v2). |
| GET | wp/v2/sites/{id}/menu-locations | read | menus | List menu locations (WP REST API v2). |
| GET | wp/v2/sites/{id}/menu-locations/{id} | read | menus | Get a menu location (WP REST API v2). |
| GET | wp/v2/sites/{id}/menus | read | menus | List navigation menus (WP REST API v2). |
| POST | wp/v2/sites/{id}/menus | write | menus | Create a navigation menu (WP REST API v2). |
| GET | wp/v2/sites/{id}/menus/{id} | read | menus | Get a navigation menu (WP REST API v2). |
| POST | wp/v2/sites/{id}/menus/{id} | write | menus | Update a navigation menu (WP REST API v2). |
| PUT | wp/v2/sites/{id}/menus/{id} | write | menus | Update a navigation menu (WP REST API v2). |
| PATCH | wp/v2/sites/{id}/menus/{id} | write | menus | Update a navigation menu (WP REST API v2). |
| DELETE | wp/v2/sites/{id}/menus/{id} | write | menus | Delete a navigation menu (WP REST API v2). |
| GET | wp/v2/sites/{id}/navigation | read | menus | List navigation block menus (WP REST API v2). |
| POST | wp/v2/sites/{id}/navigation | write | menus | Create a navigation block menu (WP REST API v2). |
| GET | wp/v2/sites/{id}/navigation/{id} | read | menus | Get a navigation block menu (WP REST API v2). |
| POST | wp/v2/sites/{id}/navigation/{id} | write | menus | Update a navigation block menu (WP REST API v2). |
| PUT | wp/v2/sites/{id}/navigation/{id} | write | menus | Update a navigation block menu (WP REST API v2). |
| PATCH | wp/v2/sites/{id}/navigation/{id} | write | menus | Update a navigation block menu (WP REST API v2). |
| DELETE | wp/v2/sites/{id}/navigation/{id} | write | menus | Delete a navigation block menu (WP REST API v2). |
| GET | wp/v2/sites/{id}/navigation/{id}/autosaves | read | menus | List the autosaves of a navigation block menu (WP REST API v2). |
| POST | wp/v2/sites/{id}/navigation/{id}/autosaves | write | menus | Create an autosave of a navigation block menu (WP REST API v2). |
| GET | wp/v2/sites/{id}/navigation/{id}/autosaves/{id} | read | menus | Get one autosave of a navigation block menu (WP REST API v2). |
| GET | wp/v2/sites/{id}/navigation/{id}/revisions | read | menus | List the revisions of a navigation block menu (WP REST API v2). |
| GET | wp/v2/sites/{id}/navigation/{id}/revisions/{id} | read | menus | Get one revision of a navigation block menu (WP REST API v2). |
| DELETE | wp/v2/sites/{id}/navigation/{id}/revisions/{id} | write | menus | Delete a revision of a navigation block menu (WP REST API v2). |
| GET | rest/v1.1/sites/{id}/widgets | read | widgets | Retrieve the active and inactive widgets for a site. |
| POST | rest/v1.1/sites/{id}/widgets/new | write | widgets | Activate a widget on a site. |
| GET | rest/v1.1/sites/{id}/widgets/{id} | read | widgets | Retrieve a widget on a site by its ID. |
| POST | rest/v1.1/sites/{id}/widgets/{id} | write | widgets | Update a widget on a site by its ID. |
| POST | rest/v1.1/sites/{id}/widgets/{id}/delete | write | widgets | Deactivate a widget on a site by its ID. Will delete if already deactivated. |
| GET | wp/v2/sites/{id}/sidebars | read | widgets | List widget areas (WP REST API v2). |
| GET | wp/v2/sites/{id}/sidebars/{id} | read | widgets | Get a widget area (WP REST API v2). |
| POST | wp/v2/sites/{id}/sidebars/{id} | write | widgets | Update a widget area (WP REST API v2). |
| PUT | wp/v2/sites/{id}/sidebars/{id} | write | widgets | Update a widget area (WP REST API v2). |
| PATCH | wp/v2/sites/{id}/sidebars/{id} | write | widgets | Update a widget area (WP REST API v2). |
| GET | wp/v2/sites/{id}/widget-types | read | widgets | List widget types (WP REST API v2). |
| GET | wp/v2/sites/{id}/widget-types/{id} | read | widgets | Get a widget type (WP REST API v2). |
| GET | wp/v2/sites/{id}/widgets | read | widgets | List widgets (WP REST API v2). |
| POST | wp/v2/sites/{id}/widgets | write | widgets | Create a widget (WP REST API v2). |
| GET | wp/v2/sites/{id}/widgets/{id} | read | widgets | Get a widget (WP REST API v2). |
| POST | wp/v2/sites/{id}/widgets/{id} | write | widgets | Update a widget (WP REST API v2). |
| PUT | wp/v2/sites/{id}/widgets/{id} | write | widgets | Update a widget (WP REST API v2). |
| PATCH | wp/v2/sites/{id}/widgets/{id} | write | widgets | Update a widget (WP REST API v2). |
| DELETE | wp/v2/sites/{id}/widgets/{id} | write | widgets | Delete a widget (WP REST API v2). |
| GET | rest/v1.1/sites/{id}/headers/mine | read | themes | Get the custom header options for a site. |
| POST | rest/v1.1/sites/{id}/headers/mine | write | themes | Set the custom header options for a site. |
| GET | rest/v1.1/sites/{id}/headers/{id} | read | themes | Get the custom header options for a site with a particular theme. |
| GET | rest/v1.1/sites/{id}/themes | read | themes | Get information about a theme on WordPress.com. |
| GET | rest/v1.1/sites/{id}/themes/mine | read | themes | Get the active theme of a site. |
| POST | rest/v1.1/sites/{id}/themes/mine | write | themes | Change the active theme of a site. |
| GET | rest/v1.1/themes | read | themes | Get a list of all available themes on WordPress.com. |
| GET | rest/v1.1/themes/{id} | read | themes | Get a theme on WordPress.com. |
| GET | wp/v2/sites/{id}/themes | read | themes | List themes (WP REST API v2). |
| GET | wp/v2/sites/{id}/themes/{id} | read | themes | Get a theme (WP REST API v2). |
| GET | `wp/v2/sites/{id}/template-parts/**` | read | templates | List or get template parts, their revisions and autosaves; IDs contain slashes (WP REST API v2). |
| POST | `wp/v2/sites/{id}/template-parts/**` | write | templates | Create, update or delete template parts (WP REST API v2). |
| PUT | `wp/v2/sites/{id}/template-parts/**` | write | templates | Create, update or delete template parts (WP REST API v2). |
| PATCH | `wp/v2/sites/{id}/template-parts/**` | write | templates | Create, update or delete template parts (WP REST API v2). |
| DELETE | `wp/v2/sites/{id}/template-parts/**` | write | templates | Create, update or delete template parts (WP REST API v2). |
| GET | `wp/v2/sites/{id}/templates/**` | read | templates | List or get templates, their revisions and autosaves; IDs contain slashes (WP REST API v2). |
| POST | `wp/v2/sites/{id}/templates/**` | write | templates | Create, update or delete templates (WP REST API v2). |
| PUT | `wp/v2/sites/{id}/templates/**` | write | templates | Create, update or delete templates (WP REST API v2). |
| PATCH | `wp/v2/sites/{id}/templates/**` | write | templates | Create, update or delete templates (WP REST API v2). |
| DELETE | `wp/v2/sites/{id}/templates/**` | write | templates | Create, update or delete templates (WP REST API v2). |
| GET | wp/v2/sites/{id}/block-patterns/categories | read | blocks | List block pattern categories (WP REST API v2). |
| GET | wp/v2/sites/{id}/block-patterns/patterns | read | blocks | List registered block patterns (WP REST API v2). |
| GET | wp/v2/sites/{id}/block-renderer/{id} | write | blocks | Render a dynamic block server-side; kept out of read because it executes block code with caller-supplied attributes. |
| POST | wp/v2/sites/{id}/block-renderer/{id} | write | blocks | Render a dynamic block server-side with attributes sent in the body. |
| GET | `wp/v2/sites/{id}/block-types/**` | read | blocks | List or get registered block types (WP REST API v2). |
| GET | wp/v2/sites/{id}/blocks | read | blocks | List synced patterns (reusable blocks) (WP REST API v2). |
| POST | wp/v2/sites/{id}/blocks | write | blocks | Create a synced pattern (reusable block) (WP REST API v2). |
| GET | wp/v2/sites/{id}/blocks/{id} | read | blocks | Get a synced pattern (reusable block) (WP REST API v2). |
| POST | wp/v2/sites/{id}/blocks/{id} | write | blocks | Update a synced pattern (reusable block) (WP REST API v2). |
| PUT | wp/v2/sites/{id}/blocks/{id} | write | blocks | Update a synced pattern (reusable block) (WP REST API v2). |
| PATCH | wp/v2/sites/{id}/blocks/{id} | write | blocks | Update a synced pattern (reusable block) (WP REST API v2). |
| DELETE | wp/v2/sites/{id}/blocks/{id} | write | blocks | Delete a synced pattern (reusable block) (WP REST API v2). |
| GET | wp/v2/sites/{id}/blocks/{id}/autosaves | read | blocks | List the autosaves of a synced pattern (WP REST API v2). |
| POST | wp/v2/sites/{id}/blocks/{id}/autosaves | write | blocks | Create an autosave of a synced pattern (WP REST API v2). |
| GET | wp/v2/sites/{id}/blocks/{id}/autosaves/{id} | read | blocks | Get one autosave of a synced pattern (WP REST API v2). |
| GET | wp/v2/sites/{id}/blocks/{id}/revisions | read | blocks | List the revisions of a synced pattern (WP REST API v2). |
| GET | wp/v2/sites/{id}/blocks/{id}/revisions/{id} | read | blocks | Get one revision of a synced pattern (WP REST API v2). |
| DELETE | wp/v2/sites/{id}/blocks/{id}/revisions/{id} | write | blocks | Delete a revision of a synced pattern (WP REST API v2). |
| GET | rest/v1.1/sites/{id}/embeds | read | embeds | Get a list of embeds available on a site. |
| GET | rest/v1.1/sites/{id}/embeds/render | write | embeds | Render an embed for a URL; kept out of read because the site fetches the caller-supplied URL from a third party. |
| GET | rest/v1.1/sites/{id}/shortcodes | read | embeds | Get a list of shortcodes available on a site. |
| GET | rest/v1.1/sites/{id}/shortcodes/render | write | embeds | Render a shortcode on the site; kept out of read because it executes arbitrary shortcode handlers server-side. |
| GET | rest/v1.1/sites/{id}/sharing-buttons | read | sharing-buttons | Get a list of a site's sharing buttons. |
| POST | rest/v1.1/sites/{id}/sharing-buttons | write | sharing-buttons | Edit all sharing buttons for a site. |
| GET | rest/v1.1/sites/{id}/publicize-connections | read | publicize-connections | Get a list of publicize connections that are associated with the specified site. |
| POST | rest/v1.1/sites/{id}/publicize-connections/new | write | publicize-connections | Create a new publicize connection that is associated with the specified site. |
| GET | rest/v1.1/sites/{id}/publicize-connections/{id} | read | publicize-connections | Get a single publicize connection that is associated with the specified site. |
| POST | rest/v1.1/sites/{id}/publicize-connections/{id} | write | publicize-connections | Update a single publicize connection belonging to the specified site. |
| POST | rest/v1.1/sites/{id}/publicize-connections/{id}/delete | write | publicize-connections | Delete the specified publicize connection. |
| POST | rest/v1.1/sites/{id}/search | read | search | Search a site's content with an Elasticsearch query (a query sent as POST). |
| GET | wp/v2/sites/{id}/search | read | search | Search posts, pages, terms and other content (WP REST API v2). |
| GET | wp/v2/sites/{id}/settings | read | settings | Get the site settings (WP REST API v2). |
| POST | wp/v2/sites/{id}/settings | write | settings | Update the site settings (WP REST API v2). |
| PUT | wp/v2/sites/{id}/settings | write | settings | Update the site settings (WP REST API v2). |
| PATCH | wp/v2/sites/{id}/settings | write | settings | Update the site settings (WP REST API v2). |
| GET | wp/v2/sites/{id}/plugins | read | plugins | List installed plugins (WP REST API v2). |
| POST | wp/v2/sites/{id}/plugins | write | plugins | Create a plugin (install, activate or deactivate) (WP REST API v2). |
| GET | wp/v2/sites/{id}/plugins/{id} | read | plugins | Get a plugin (install, activate or deactivate) (WP REST API v2). |
| POST | wp/v2/sites/{id}/plugins/{id} | write | plugins | Update a plugin (install, activate or deactivate) (WP REST API v2). |
| PUT | wp/v2/sites/{id}/plugins/{id} | write | plugins | Update a plugin (install, activate or deactivate) (WP REST API v2). |
| PATCH | wp/v2/sites/{id}/plugins/{id} | write | plugins | Update a plugin (install, activate or deactivate) (WP REST API v2). |
| DELETE | wp/v2/sites/{id}/plugins/{id} | write | plugins | Delete a plugin (install, activate or deactivate) (WP REST API v2). |
| GET | wp/v2/sites/{id}/feedback | read | forms | List form responses (WP REST API v2). |
| POST | wp/v2/sites/{id}/feedback | write | forms | Create a form response (WP REST API v2). |
| GET | wp/v2/sites/{id}/feedback/{id} | read | forms | Get a form response (WP REST API v2). |
| POST | wp/v2/sites/{id}/feedback/{id} | write | forms | Update a form response (WP REST API v2). |
| PUT | wp/v2/sites/{id}/feedback/{id} | write | forms | Update a form response (WP REST API v2). |
| PATCH | wp/v2/sites/{id}/feedback/{id} | write | forms | Update a form response (WP REST API v2). |
| DELETE | wp/v2/sites/{id}/feedback/{id} | write | forms | Delete a form response (WP REST API v2). |
| GET | rest/v1.1/sites/{id}/imports | read | imports | Get information about any current imports for this site. |
| POST | rest/v1.1/sites/{id}/imports/library/new | write | imports | Prepare an import for this site. |
| POST | rest/v1.1/sites/{id}/imports/new | write | imports | Prepare an import for this site. |
| GET | rest/v1.1/sites/{id}/imports/{id} | read | imports | Get information about the state of an import. |
| POST | rest/v1.1/sites/{id}/imports/{id} | write | imports | Update the import for a site. |
| POST | rest/v1.1/sites/{id}/wordads/approve | write | wordads | Request streamlined approval to join the WordAds program. |
| GET | rest/v1.1/sites/{id}/wordads/earnings | read | wordads | Get detailed WordAds earnings information about a site. |
| GET | rest/v1.1/sites/{id}/wordads/settings | read | wordads | Get detailed WordAds settings information about a site. |
| POST | rest/v1.1/sites/{id}/wordads/settings | write | wordads | Update WordAds settings for a site. |
| GET | rest/v1.1/sites/{id}/wordads/stats | read | wordads | Get WordAds stats for a site. |
| GET | rest/v1.1/sites/{id}/wordads/tos | read | wordads | Get WordAds TOS information about a site. |
| POST | rest/v1.1/sites/{id}/wordads/tos | write | wordads | Update WordAds TOS setting for a site. |
| GET | rest/v1.1/jetpack-blogs | read | jetpack | Get a list of your Jetpack-enabled blogs. |
| GET | rest/v1.1/jetpack-blogs/{id} | read | jetpack | Get Jetpack settings. |
| POST | rest/v1.1/jetpack-blogs/{id} | write | jetpack | Update Jetpack settings. |
| POST | rest/v1.1/jetpack-blogs/{id}/mine/delete | write | jetpack | Disconnect a Jetpack-enabled blog from a WordPress.com user. |
| POST | rest/v1.1/jetpack-blogs/{id}/source/{id}/migrate | write | jetpack | Migrate followers from a WordPress.com blog to a Jetpack-enabled blog. |
| GET | rest/v1.1/jetpack-blogs/{id}/test-connection | write | jetpack | Test the connection to a Jetpack site; kept out of read because it makes WordPress.com call out to the site. |
| GET | rest/v1.1/sites/{id}/automated-transfers/status | read | jetpack | Returns the current status of Automated Transfer for a site. |
| POST | rest/v1.1/sites/{id}/protect/recovery/confirm | write | jetpack | A site confirms that a user can bypass jetpack to try to login and login. |
| POST | rest/v1.1/sites/{id}/protect/recovery/request | write | jetpack | A user request an email containing a recovery url that they can use to bypass a Protect blockage. |
| GET | rest/v1.1/sites/{id}/protect/recovery/validate/{id} | write | jetpack | Validate an emailed Protect recovery token; a GET that is part of a login-bypass flow. |
| POST | rest/v1.1/sites/{id}/sync/now | write | jetpack | Force immediate sync of top items on a queue. |
| GET | rest/v1.1/sites/{id}/sync/status | read | jetpack | Status of the current full sync or the previous full sync. |
| GET | rest/v1.1/sites/{id}/translations | read | jetpack | Gets info about a Jetpack blog's core installation. |
| POST | rest/v1.1/sites/{id}/translations | write | jetpack | Toggle automatic core updates for a Jetpack blog. |
| POST | rest/v1.1/sites/{id}/translations/update | write | jetpack | Update All Translations installation on a Jetpack blog. |
| GET | rest/v1.1/sites/{id}/updates | read | jetpack | Get counts for available updates. |
| GET | rest/v1.1/me | read | me | Get metadata about the current user. |
| GET | rest/v1.1/me/billing-history | read | me | Get list of current user's billing history and upcoming charges. |
| GET | rest/v1.1/me/connected-applications | read | me | Get current user's connected applications. |
| GET | rest/v1.1/me/connected-applications/{id} | read | me | Get one of current user's connected applications. |
| POST | rest/v1.1/me/connected-applications/{id}/delete | write | me | Delete one of current user's connected application access tokens. |
| GET | rest/v1.1/me/keyring-connections | read | me | Get a list of all the keyring connections associated with the current user. |
| GET | rest/v1.1/me/keyring-connections/{id} | read | me | Get a single Keyring connection that the current user has setup. |
| POST | rest/v1.1/me/keyring-connections/{id}/delete | write | me | Delete the Keyring connection (and associated token) with the provided ID. Also deletes all associated publicize connections. |
| GET | rest/v1.1/me/likes | read | me | Get a list of the current user's likes. |
| GET | rest/v1.1/me/mailboxes | read | me | List all email mailboxes the current user has access to across all manageable sites. |
| GET | rest/v1.1/me/posts | read | me | Get a list of posts across all the user's sites. |
| GET | rest/v1.1/me/preferences | read | me | Get the current user's settings. |
| POST | rest/v1.1/me/preferences | write | me | Update the current user's preferences. |
| GET | rest/v1.1/me/publicize-connections | read | me | Get a list of publicize connections that the current user has set up. |
| GET | rest/v1.1/me/publicize-connections/{id} | read | me | Get a single publicize connection that the current user has set up. |
| POST | rest/v1.1/me/publicize-connections/{id} | write | me | Update a single publicize connection belonging to the current user. |
| POST | rest/v1.1/me/publicize-connections/{id}/delete | write | me | Delete the specified publicize connection. |
| GET | rest/v1.1/me/settings | read | me | Get the current user's settings. |
| POST | rest/v1.1/me/settings | write | me | Update the current user's settings. |
| POST | rest/v1.1/me/settings/password/validate | read | me | Check the strength of a candidate password; nothing is saved. |
| GET | rest/v1.1/me/settings/profile-links | read | me | Get current user's profile links. |
| POST | rest/v1.1/me/settings/profile-links/new | write | me | Add a link to current user's profile. |
| POST | rest/v1.1/me/settings/profile-links/{id}/delete | write | me | Delete a link from current user's profile. |
| GET | rest/v1.1/me/sites | read | me | Get a list of the current user's sites. |
| GET | rest/v1.1/me/sites/compact | read | me | Not in use. |
| GET | rest/v1.1/me/sites/features | read | me | Get a list of the current user's sites features. |
| GET | rest/v1.1/me/sites/plugins | read | me | Get a list of the current user's sites plugins. |
| GET | rest/v1.1/me/two-step | read | me | Get information about current user's two factor configuration. |
| POST | rest/v1.1/me/two-step/sms/new | write | me | Sends a two-step code via SMS to the current user. |
| POST | rest/v1.1/notifications/read | write | notifications | Mark a set of notifications as read. |
| POST | rest/v1.1/notifications/seen | write | notifications | Set the timestamp of the most recently seen notification. |
| GET | rest/v1/notifications | read | notifications | List the current user's notifications (v1 path; v1.1 only documents the mark-read calls). |
| POST | rest/v1/notifications/read | write | notifications | Mark a set of notifications as read (v1 path). |
| POST | rest/v1/notifications/seen | write | notifications | Set the timestamp of the most recently seen notification (v1 path). |
| GET | rest/v1/notifications/{id} | read | notifications | Get a single notification (v1 path). |
| GET | rest/v1.1/read/email-settings | read | reader | Returns the email settings. |
| POST | rest/v1.1/read/email-settings | write | reader | Reader email settings endpoint called with POST; documented as returning settings but accepts new values. |
| GET | rest/v1.1/read/feed | read | reader | Get the ID and subscribe URL of one or more matching feeds by domain or URL. |
| GET | rest/v1.1/read/feed/{id} | read | reader | Get details about a feed. |
| GET | rest/v1.1/read/following | read | reader | Get a list of posts from the blogs a user follows. |
| GET | rest/v1.1/read/following/mine | read | reader | Get a list of the feeds the user is following. |
| POST | rest/v1.1/read/following/mine/delete | write | reader | Unfollow the specified blog. |
| POST | rest/v1.1/read/following/mine/new | write | reader | Follow the specified blog. |
| GET | rest/v1.1/read/liked | read | reader | Get a list of posts from the blogs a user likes. |
| GET | rest/v1.1/read/lists/{id} | read | reader | Get an array of Reader lists by user slug. |
| GET | rest/v1.1/read/menu | read | reader | Get default reader menu. |
| GET | rest/v1.1/read/recommendations/mine | read | reader | Get a list of blog recommendations for the current user. |
| GET | rest/v1.1/read/sites/{id}/posts/{id} | read | reader | Get a single post (by ID). |
| GET | rest/v1.1/read/subscriptions-count | read | reader | Returns the number of blog, comment and pending subscriptions. |
| GET | rest/v1.1/read/tags | read | reader | Get a list of tags subscribed to by the user. |
| GET | rest/v1.1/read/tags/alphabetic | read | reader | Get a filtered list of top tags, grouped by letter. |
| GET | rest/v1.1/read/tags/{id} | read | reader | Get details about a specified tag. |
| GET | rest/v1.1/read/tags/{id}/mine | read | reader | Get the subscribed status of the user to a given tag. |
| POST | rest/v1.1/read/tags/{id}/mine/delete | write | reader | Unsubscribe from a tag. |
| POST | rest/v1.1/read/tags/{id}/mine/new | write | reader | Subscribe to a new tag. |
| GET | rest/v1.1/read/tags/{id}/posts | read | reader | Get a list of posts from a tag. |
| GET | rest/v1.1/read/trending/tags | read | reader | Get a list of trending tags. |
| GET | wp/v2/sites/{id}/wp-abilities/v1/abilities/{id}/run | write | abilities | Run a registered ability; an RPC-style call that can change the site whatever the method. |
| POST | wp/v2/sites/{id}/wp-abilities/v1/abilities/{id}/run | write | abilities | Run a registered ability; an RPC-style call that can change the site whatever the method. |
| PUT | wp/v2/sites/{id}/wp-abilities/v1/abilities/{id}/run | write | abilities | Run a registered ability; an RPC-style call that can change the site whatever the method. |
| PATCH | wp/v2/sites/{id}/wp-abilities/v1/abilities/{id}/run | write | abilities | Run a registered ability; an RPC-style call that can change the site whatever the method. |
| DELETE | wp/v2/sites/{id}/wp-abilities/v1/abilities/{id}/run | write | abilities | Run a registered ability; an RPC-style call that can change the site whatever the method. |
| GET | rest/v1.1/batch | write | batch | Run several GET endpoints in one call; kept out of read because the inner URLs are not checked, so it can reach any GET. |
| POST | rest/v1.1/manual_payment | write | billing | Pay a manual payment. |
| GET | rest/v1.1/manual_payment/{id} | read | billing | Return a payment object containing a collection of items that need to be paid for together. |
| GET | rest/v1.1/freshly-pressed | read | freshly-pressed | Get a list of Freshly Pressed posts. |
| GET | rest/v1.1/insights | read | insights | Get a list of stats/metrics/insights that the current user has access to. |
| GET | rest/v1.1/insights/{id} | read | insights | Get raw data for a particular graph. |
| POST | rest/v1.1/marketing/survey | write | marketing | Submit a marketing survey. |
| GET | rest/v1.1/meta/external-services | read | meta | Get a list of third-party services that WordPress.com or Jetpack sites can integrate with via keyring. |
| GET | rest/v1.1/meta/external-services/{id} | read | meta | Get information about a single external service that WordPress.com or Jetpack sites can integrate with via keyring. |
| GET | rest/v1.1/meta/sharing-buttons | read | meta | Get a list of external services for which sharing buttons are supported. |
| GET | rest/v1.1/support/alternates/{id}/posts/{id} | read | support | Get alternates for support article (by ID). |
| GET | rest/v1.1/videos/{id} | read | videos | Get the metadata for a specified VideoPress video. |
| GET | rest/v1.1/videos/{id}/chapters | read | videos | Get the chapters for a specified VideoPress video. |
| GET | rest/v1.1/videos/{id}/playlist/{id} | read | videos | Get the poster for a specified VideoPress video. |
| GET | rest/v1.1/videos/{id}/poster | read | videos | Get the poster for a specified VideoPress video. |
| POST | rest/v1.1/videos/{id}/poster | write | videos | Upload and set a poster for a specified VideoPress video. |
| POST | rest/v1.1/videos/{id}/tracks | write | videos | Upload a subtitle/caption track for a specified VideoPress video. |
| POST | rest/v1.1/videos/{id}/tracks/delete | write | videos | Delete an existing subtitle/caption track for a specified VideoPress video. |
