# Command Families

Primary docs:

- WP-CLI commands index: <https://developer.wordpress.org/cli/commands/>
- WP-CLI handbook: <https://make.wordpress.org/cli/handbook/>

Use this file to get to the right namespace quickly.

## Core And Installation

- `core`
- `config`
- `db`
- `eval`
- `eval-file`
- `package`
- `cli`
- `info`

Common tasks:

- check version
- install or update core
- verify checksums
- inspect config constants
- export or import the database

## Code And Dependencies

- `plugin`
- `theme`
- `language`

Common tasks:

- list installed code
- activate, deactivate, install, uninstall, update
- inspect update availability

## Content And Taxonomy

- `post`
- `post-type`
- `post-meta`
- `comment`
- `comment-meta`
- `term`
- `term-meta`
- `category`
- `tag`
- `media`
- `attachment`
- `menu`
- `menu-item`
- `widget`

Common tasks:

- list or edit content
- assign taxonomy
- regenerate thumbnails
- manage menus and widgets

## Users And Permissions

- `user`
- `user-meta`
- `role`
- `cap`
- `super-admin`

Common tasks:

- create or update users
- reset passwords
- grant or revoke capabilities
- manage multisite super admins

## Runtime And Site Settings

- `option`
- `transient`
- `cron`
- `rewrite`
- `cache`
- `embed`
- `search-replace`

Common tasks:

- inspect home and site URL
- flush rewrites
- inspect cron events
- run search and replace safely

## Multisite

- `site`
- `network`
- `super-admin`

Always confirm the target site context:

- pass `--url=<site-url>` when needed
- do not assume the main site is the only site

## Practical Rule

If you know the noun but not the command:

1. run `scripts/list-commands.sh`
2. run `scripts/list-commands.sh --group <group>`
3. switch to the live help text before guessing subcommand names
