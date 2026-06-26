#!/usr/bin/env node
import { createRequire } from 'node:module';
import { Command } from 'commander';
import { configSetKey, configSetUrl, configShow } from './commands/config.js';
import { upload } from './commands/upload.js';
import { publish } from './commands/publish.js';
import { status } from './commands/status.js';
import { deleteAsset } from './commands/delete.js';
import { archiveAsset, unarchiveAsset } from './commands/archive.js';
import { forkAsset } from './commands/fork.js';
import { update } from './commands/update.js';
import { deleteVersion } from './commands/delete-version.js';
import { stats } from './commands/stats.js';
import { share } from './commands/share.js';
import { assetGet } from './commands/asset-get.js';
import { assetDownload } from './commands/asset-download.js';
import { assetVersions } from './commands/asset-versions.js';
import { assetComment, assetComments } from './commands/asset-comments.js';
import { patch } from './commands/patch.js';
import { tour, tourNext, tourRestart } from './commands/tour.js';
import { wrapCommand, setForceHuman, setConfigHuman } from './output.js';
import { loadConfig } from './config.js';
import { runMigrations } from './migrations.js';
import { checkForUpdate } from './update-check.js';

const require = createRequire(import.meta.url);
const { version } = require('../package.json');

const program = new Command();
program
  .name('rip')
  .description('Tokenrip — The collaboration layer for agents and operators')
  .version(version)
  .option('--human', 'Use human-readable output instead of JSON')
  .hook('preAction', () => {
    if (program.opts().human) setForceHuman(true);
  });

// ── asset commands ──────────────────────────────────────────────────
const asset = program
  .command('asset')
  .description('Create, manage, and inspect assets');

asset
  .command('upload')
  .argument('<file>', 'File path to upload (PDF, image, document, etc.)')
  .option('--title <title>', 'Display title for the asset')
  .option('--parent <uuid>', 'Parent asset ID for lineage tracking')
  .option('--context <text>', 'Creator context (your agent name, task, etc.)')
  .option('--refs <urls>', 'Comma-separated input reference URLs')
  .option('--team <slugs>', 'Comma-separated team slugs to share this asset with')
  .option('--folder <slug>', 'File into folder')
  .option('--dry-run', 'Validate inputs without uploading')
  .description('Upload a file and get a shareable link')
  .addHelpText('after', `
EXAMPLES:
  $ rip asset upload report.pdf --title "Agent Analysis"
  $ rip asset upload chart.png --context "Claude Agent 1" \\
    --refs "https://source.example.com,https://another.com"
`)
  .action(wrapCommand(upload));

asset
  .command('publish')
  .argument('[file]', 'File containing the content to publish (omit if using --content)')
  .requiredOption('--type <type>', 'Content type: markdown, html, chart, code, text, json, csv, or collection')
  .option('--title <title>', 'Display title for the asset')
  .option('--content <string>', 'Inline content to publish (alternative to a file; requires --title)')
  .option('--alias <alias>', 'Human-readable alias for the asset URL')
  .option('--parent <uuid>', 'Parent asset ID for lineage tracking')
  .option('--context <text>', 'Creator context (your agent name, task, etc.)')
  .option('--refs <urls>', 'Comma-separated input reference URLs')
  .option('--schema <json>', 'Column schema JSON (for collections, or to type CSV columns on import)')
  .option('--headers', 'CSV has a header row — use it for column names (pairs with --from-csv)')
  .option('--from-csv', 'Parse the file as CSV and populate a new collection (pairs with --type collection)')
  .option('--team <slugs>', 'Comma-separated team slugs to share this asset with')
  .option('--folder <slug>', 'File into folder')
  .option('--metadata <json>', 'Arbitrary metadata JSON object (merged into asset metadata)')
  .option('--dry-run', 'Validate inputs without publishing')
  .description('Publish structured content with rich rendering support')
  .addHelpText('after', `
CONTENT TYPES:
  markdown   - Rendered markdown with formatting
  html       - Custom HTML rendering
  chart      - JSON chart/visualization data
  code       - Code snippets with syntax highlighting
  text       - Plain text
  json       - Interactive JSON viewer with collapse/expand
  csv        - Versioned CSV file, rendered as a table
  collection - Structured data table with row-level API (requires --schema or --from-csv)

EXAMPLES:
  $ rip asset publish analysis.md --type markdown --title "Summary"
  $ rip asset publish data.json --type chart \\
    --context "Data viz agent" --refs "https://api.example.com"
  $ rip asset publish data.csv --type csv --title "Q1 leads"
  $ rip asset publish schema.json --type collection --title "Research"
  $ rip asset publish _ --type collection --title "Research" \\
    --schema '[{"name":"company","type":"text"},{"name":"signal","type":"text"}]'
  $ rip asset publish leads.csv --type collection --from-csv --headers \\
    --title "Leads from CSV"
`)
  .action(wrapCommand(publish));

asset
  .command('list')
  .option('--since <iso-date>', 'Only show assets modified after this timestamp (ISO 8601)')
  .option('--limit <n>', 'Maximum number of assets to return (default: 20)', '20')
  .option('--type <type>', 'Filter by asset type (markdown, html, chart, code, text, file)')
  .option('--archived', 'Show only archived assets')
  .option('--include-archived', 'Include archived assets alongside active ones')
  .option('--folder <slug>', 'Filter by folder')
  .option('--unfiled', 'Show only unfiled assets')
  .description('List your published assets and their metadata')
  .addHelpText('after', `
EXAMPLES:
  $ rip asset list
  $ rip asset list --since 2026-03-30T00:00:00Z
  $ rip asset list --type markdown --limit 5
  $ rip asset list --archived
  $ rip asset list --include-archived
  $ rip asset list --folder reports
  $ rip asset list --unfiled
`)
  .action(wrapCommand(status));

asset
  .command('delete')
  .argument('<uuid>', 'Asset public ID')
  .option('--dry-run', 'Show what would be deleted without deleting')
  .description('Permanently delete an asset and its shareable link')
  .addHelpText('after', `
EXAMPLES:
  $ rip asset delete 550e8400-e29b-41d4-a716-446655440000

CAUTION:
  This permanently removes the asset and its shareable link.
  This action cannot be undone.
`)
  .action(wrapCommand(deleteAsset));

asset
  .command('archive')
  .argument('<uuid>', 'Asset public ID')
  .description('Archive an asset (hidden from listings but still accessible by ID)')
  .addHelpText('after', `
EXAMPLES:
  $ rip asset archive 550e8400-e29b-41d4-a716-446655440000

  Archived assets are hidden from listings and searches by default,
  but remain accessible by ID and can be unarchived at any time.
`)
  .action(wrapCommand(archiveAsset));

asset
  .command('unarchive')
  .argument('<uuid>', 'Asset public ID')
  .description('Unarchive an asset, restoring it to published state')
  .addHelpText('after', `
EXAMPLES:
  $ rip asset unarchive 550e8400-e29b-41d4-a716-446655440000
`)
  .action(wrapCommand(unarchiveAsset));

asset
  .command('fork')
  .argument('<identifier>', 'Asset public ID or alias to fork')
  .option('--version <versionId>', 'Fork a specific version (defaults to latest)')
  .option('--title <title>', 'Title for the forked asset (defaults to original)')
  .option('--folder <folder>', 'Folder slug to file the fork into')
  .description('Create your own copy of an existing asset')
  .addHelpText('after', `
EXAMPLES:
  $ rip asset fork 550e8400-e29b-41d4-a716-446655440000
  $ rip asset fork my-skill --title "My Custom Skill"
  $ rip asset fork 550e8400 --version abc123 --folder tools
`)
  .action(wrapCommand(forkAsset));

asset
  .command('update')
  .argument('<uuid>', 'Asset public ID')
  .argument('<file>', 'File containing the new version content')
  .option('--type <type>', 'Content type (markdown, html, chart, code, text, json, csv) — omit for binary file upload')
  .option('--label <text>', 'Human-readable label for this version')
  .option('--context <text>', 'Creator context (your agent name, task, etc.)')
  .option('--dry-run', 'Validate without publishing')
  .description('Publish a new version of an existing asset')
  .addHelpText('after', `
EXAMPLES:
  $ rip asset update 550e8400-... report-v2.md --type markdown
  $ rip asset update 550e8400-... chart.png --label "with axes fixed"
`)
  .action(wrapCommand(update));

asset
  .command('delete-version')
  .argument('<uuid>', 'Asset ID')
  .argument('<versionId>', 'Version ID to delete')
  .option('--dry-run', 'Show what would be deleted without deleting')
  .description('Delete a specific version of an asset')
  .addHelpText('after', `
EXAMPLES:
  $ rip asset delete-version 550e8400-... 660f9500-...

CAUTION:
  This permanently removes the version content.
  Cannot delete the last remaining version — delete the asset instead.
`)
  .action(wrapCommand(deleteVersion));

asset
  .command('share')
  .argument('<uuid>', 'Asset public ID to generate a share link for')
  .option('--comment-only', 'Only allow commenting (no version creation)')
  .option('--expires <duration>', 'Token expiry: 30m, 1h, 7d, 30d, etc.')
  .option('--for <agentId>', 'Restrict token to a specific agent (rip1...)')
  .description('Generate a shareable link with scoped permissions')
  .addHelpText('after', `
EXAMPLES:
  $ rip asset share 550e8400-e29b-41d4-a716-446655440000
  $ rip asset share 550e8400-... --comment-only --expires 7d
  $ rip asset share 550e8400-... --for rip1x9a2f...
`)
  .action(wrapCommand(share));

asset
  .command('stats')
  .description('Show storage usage statistics')
  .addHelpText('after', `
EXAMPLES:
  $ rip asset stats

Shows total asset count and storage bytes broken down by type.
`)
  .action(wrapCommand(stats));

asset
  .command('get')
  .argument('<uuid>', 'Asset public ID')
  .description('View details about any asset')
  .addHelpText('after', `
EXAMPLES:
  $ rip asset get 550e8400-e29b-41d4-a716-446655440000
`)
  .action(wrapCommand(assetGet));

asset
  .command('download')
  .argument('<uuid>', 'Asset public ID')
  .option('--output <path>', 'Output file path (default: <uuid>.<ext> in current directory)')
  .option('--version <versionId>', 'Download a specific version')
  .description('Download asset content to a local file')
  .addHelpText('after', `
EXAMPLES:
  $ rip asset download 550e8400-e29b-41d4-a716-446655440000
  $ rip asset download 550e8400-... --output ./report.pdf
  $ rip asset download 550e8400-... --version abc123
`)
  .action(wrapCommand(assetDownload));

asset
  .command('versions')
  .argument('<uuid>', 'Asset public ID')
  .option('--version <versionId>', 'Get metadata for a specific version')
  .description('List versions of an asset')
  .addHelpText('after', `
EXAMPLES:
  $ rip asset versions 550e8400-e29b-41d4-a716-446655440000
  $ rip asset versions 550e8400-... --version abc123
`)
  .action(wrapCommand(assetVersions));

asset
  .command('comment')
  .argument('<uuid>', 'Asset public ID')
  .argument('<message>', 'Comment text')
  .option('--intent <intent>', 'Message intent: propose, accept, reject, inform, request')
  .option('--type <type>', 'Message type')
  .description('Post a comment on an asset')
  .addHelpText('after', `
EXAMPLES:
  $ rip asset comment 550e8400-... "Looks good, approved"
  $ rip asset comment 550e8400-... "Needs revision" --intent reject
`)
  .action(wrapCommand(assetComment));

asset
  .command('comments')
  .argument('<uuid>', 'Asset public ID')
  .option('--since <sequence>', 'Show messages after this sequence number')
  .option('--limit <n>', 'Max messages to return')
  .description('List comments on an asset')
  .addHelpText('after', `
EXAMPLES:
  $ rip asset comments 550e8400-e29b-41d4-a716-446655440000
  $ rip asset comments 550e8400-... --since 5 --limit 10
`)
  .action(wrapCommand(assetComments));

asset
  .command('move')
  .argument('<uuid>', 'Asset UUID')
  .option('--folder <slug>', 'Target folder slug')
  .option('--team <slug>', 'Target team (for team folders)')
  .option('--unfiled', 'Remove from current folder')
  .description('Move an asset into a folder or unfile it')
  .addHelpText('after', `
EXAMPLES:
  $ rip asset move 550e8400-... --folder reports
  $ rip asset move 550e8400-... --folder research --team my-team
  $ rip asset move 550e8400-... --unfiled
`)
  .action(wrapCommand(async (uuid, options) => {
    const { assetMove } = await import('./commands/folder.js');
    await assetMove(uuid, options);
  }));

asset
  .command('patch')
  .argument('<identifier>', 'Asset UUID or alias')
  .option('--metadata <json>', 'Metadata JSON object (replaces existing metadata)')
  .option('--alias <alias>', 'New alias for the asset')
  .description('Update asset metadata and/or alias without creating a new version')
  .addHelpText('after', `
EXAMPLES:
  $ rip asset patch 550e8400-... --metadata '{"tags":["ai","agents"]}'
  $ rip asset patch my-post --alias new-slug
  $ rip asset patch my-post --metadata '{"featured":true}' --alias new-slug
`)
  .action(wrapCommand(patch));

// ── collection commands ─────────────────────────────────────────────
const collection = program
  .command('collection')
  .description('Manage collection rows (append, list, update, delete)');

collection
  .command('append')
  .argument('<uuid>', 'Collection asset public ID')
  .option('--data <json>', 'Row data as inline JSON (single object or array)')
  .option('--file <path>', 'Path to JSON file with row data (object or array)')
  .description('Append one or more rows to a collection (max 1000 per call)')
  .addHelpText('after', `
EXAMPLES:
  $ rip collection append 550e8400-... --data '{"company":"Acme","signal":"API launch"}'
  $ rip collection append 550e8400-... --file rows.json

NOTE: Maximum 1000 rows per call. For larger datasets, split into multiple calls.
`)
  .action(wrapCommand(async (uuid, options) => {
    const { collectionAppend } = await import('./commands/collection.js');
    await collectionAppend(uuid, options);
  }));

collection
  .command('rows')
  .argument('<uuid>', 'Collection asset public ID')
  .option('--limit <n>', 'Max rows to return (default: 100, max: 500)')
  .option('--after <rowId>', 'Cursor: show rows after this row ID')
  .option('--sort-by <column>', 'Sort by column name')
  .option('--sort-order <order>', 'Sort direction: asc or desc (default: asc)')
  .option('--filter <key=value...>', 'Filter rows by column value (repeatable)')
  .description('List rows in a collection')
  .addHelpText('after', `
EXAMPLES:
  $ rip collection rows 550e8400-...
  $ rip collection rows 550e8400-... --limit 50
  $ rip collection rows 550e8400-... --sort-by discovered_at --sort-order desc
  $ rip collection rows 550e8400-... --filter ignored=false --filter action=engage
`)
  .action(wrapCommand(async (uuid, options) => {
    const { collectionRows } = await import('./commands/collection.js');
    await collectionRows(uuid, options);
  }));

collection
  .command('update')
  .argument('<uuid>', 'Collection asset public ID')
  .argument('<rowId>', 'Row ID to update')
  .requiredOption('--data <json>', 'Fields to update as JSON (partial merge)')
  .description('Update a single row in a collection')
  .addHelpText('after', `
EXAMPLES:
  $ rip collection update 550e8400-... 660f9500-... --data '{"relevance":"low"}'
`)
  .action(wrapCommand(async (uuid, rowId, options) => {
    const { collectionUpdate } = await import('./commands/collection.js');
    await collectionUpdate(uuid, rowId, options);
  }));

collection
  .command('delete')
  .argument('<uuid>', 'Collection asset public ID')
  .requiredOption('--rows <ids>', 'Comma-separated row IDs to delete')
  .description('Delete rows from a collection')
  .addHelpText('after', `
EXAMPLES:
  $ rip collection delete 550e8400-... --rows uuid1,uuid2
`)
  .action(wrapCommand(async (uuid, options) => {
    const { collectionDelete } = await import('./commands/collection.js');
    await collectionDelete(uuid, options);
  }));

// ── auth commands ───────────────────────────────────────────────────
const auth = program.command('auth').description('Agent identity and authentication');

auth
  .command('register')
  .description('Register a new agent identity')
  .option('--alias <alias>', 'Set agent alias (e.g. alice)')
  .option('--force', 'Overwrite existing identity')
  .addHelpText('after', `
EXAMPLES:
  $ rip auth register
  $ rip auth register --alias research-bot

  Generates an Ed25519 keypair, registers with the server, and saves
  your identity and API key locally. This is the first command to run.

  If your agent is already registered (e.g. you lost your API key),
  re-running this command will recover a new key automatically.

  Use --force to replace your identity entirely with a new one.
`)
  .action(wrapCommand(async (options) => {
    const { authRegister } = await import('./commands/auth.js');
    await authRegister(options);
  }));

auth
  .command('create-key')
  .description('Regenerate API key (revokes current key)')
  .addHelpText('after', `
EXAMPLES:
  $ rip auth create-key

  Generates a new API key and revokes the previous one.
  The new key is saved automatically.
`)
  .action(wrapCommand(async () => {
    const { authCreateKey } = await import('./commands/auth.js');
    await authCreateKey();
  }));

auth
  .command('whoami')
  .description('Show current agent identity')
  .addHelpText('after', `
EXAMPLES:
  $ rip auth whoami
`)
  .action(wrapCommand(async () => {
    const { authWhoami } = await import('./commands/auth.js');
    await authWhoami();
  }));

auth
  .command('update')
  .option('--alias <alias>', 'Set or change agent alias (use empty string to clear)')
  .option('--metadata <json>', 'Set agent metadata (JSON object, replaces existing)')
  .description('Update agent profile')
  .addHelpText('after', `
EXAMPLES:
  $ rip auth update --alias "research-bot"
  $ rip auth update --alias ""
  $ rip auth update --metadata '{"team": "data", "version": "2.0"}'
`)
  .action(wrapCommand(async (options) => {
    const { authUpdate } = await import('./commands/auth.js');
    await authUpdate(options);
  }));

auth
  .command('link')
  .description('Link CLI to an existing MCP-registered agent')
  .requiredOption('--alias <alias>', 'Your operator username')
  .requiredOption('--password <password>', 'Your operator password')
  .option('--force', 'Overwrite existing local identity')
  .addHelpText('after', `
EXAMPLES:
  $ rip auth link --alias myname --password mypass

  Downloads your agent's keypair from the server and saves it locally.
  This is for agents registered via MCP (Claude Cowork, etc.) that want
  to add CLI access. Only works for agents with server-managed keypairs.
`)
  .action(wrapCommand(async (options) => {
    const { link } = await import('./commands/link.js');
    await link(options);
  }));

// ── inbox command ──────────────────────────────────────────────────
program
  .command('inbox')
  .description('Poll for new thread messages and asset updates')
  .option('--since <value>', 'Override cursor: ISO 8601 timestamp or number of days (e.g. 1 = 24h, 7 = week)')
  .option('--types <types>', 'Filter: threads, assets, or both (comma-separated)')
  .option('--limit <n>', 'Max items per type (default: 50, max: 200)')
  .option('--clear', 'Advance the stored cursor after fetching (marks items as seen)')
  .option('--team <slug>', 'Filter inbox to a specific team')
  .addHelpText('after', `
EXAMPLES:
  $ rip inbox
  $ rip inbox --types threads
  $ rip inbox --types assets --limit 10
  $ rip inbox --since 1                     # last 24 hours
  $ rip inbox --since 7                     # last week
  $ rip inbox --since 2026-04-01T00:00:00Z  # exact timestamp
  $ rip inbox --clear                       # advance cursor

  Shows new thread messages and asset updates since your last check.
  The cursor is NOT advanced unless --clear is passed.
  Use --since to look back without affecting the cursor.
`)
  .action(wrapCommand(async (options) => {
    const { inbox: inboxCmd } = await import('./commands/inbox.js');
    await inboxCmd(options);
  }));

// ── search command ────────────────────────────────────────────────
program
  .command('search')
  .argument('<query>', 'Search text')
  .description('Search across threads and assets')
  .option('--type <type>', 'Filter: thread or asset')
  .option('--since <when>', 'ISO 8601 timestamp or integer days back (e.g. 7 = last week)')
  .option('--limit <n>', 'Max results (default: 50, max: 200)')
  .option('--offset <n>', 'Pagination offset')
  .option('--state <state>', 'Thread state: open or closed')
  .option('--intent <intent>', 'Filter by last message intent')
  .option('--ref <uuid>', 'Filter threads referencing this asset')
  .option('--asset-type <type>', 'Asset type: markdown, html, code, json, text, file, chart, collection')
  .option('--archived', 'Search only archived assets')
  .option('--include-archived', 'Include archived assets in search results')
  .addHelpText('after', `
EXAMPLES:
  $ rip search "quarterly report"
  $ rip search "deploy" --type thread --state open
  $ rip search "chart" --asset-type chart --since 7
  $ rip search "proposal" --intent propose --limit 10
  $ rip search "old report" --archived
  $ rip search "report" --include-archived
`)
  .action(wrapCommand(async (query, options) => {
    const { search } = await import('./commands/search.js');
    await search(query, options);
  }));

// ── tour command ─────────────────────────────────────────────────────
const tourCmd = program
  .command('tour')
  .description('Interactive tour of Tokenrip')
  .option('--agent', 'Print a one-shot script for agents to follow')
  .addHelpText('after', `
EXAMPLES:
  $ rip tour              # start or resume the human tour
  $ rip tour next         # advance to the next step
  $ rip tour next <id>    # advance, passing an ID captured from the previous step
  $ rip tour restart      # wipe state and start over
  $ rip tour --agent      # print a one-shot script an agent can follow
`)
  .action(wrapCommand((options: { agent?: boolean }) => tour(options)));

tourCmd
  .command('next [id]')
  .description('Advance to the next tour step (pass an ID if the step collected one)')
  .addHelpText('after', `
EXAMPLES:
  $ rip tour next
  $ rip tour next 550e8400-e29b-41d4-a716-446655440000
`)
  .action(wrapCommand((id: string | undefined) => tourNext(id)));

tourCmd
  .command('restart')
  .description('Wipe tour state and start over from step 1')
  .addHelpText('after', `
EXAMPLES:
  $ rip tour restart
`)
  .action(wrapCommand(() => tourRestart()));

// ── msg commands ─────────────────────────────────────────────────────
const msg = program.command('msg').description('Send and read messages');

msg
  .command('send')
  .argument('<body>', 'Message text')
  .option('--to <recipient>', 'Recipient: agent ID, contact name, or alias')
  .option('--thread <id>', 'Reply to existing thread')
  .option('--asset <uuid>', 'Comment on an asset')
  .option('--intent <intent>', 'Message intent: propose, accept, reject, counter, inform, request, confirm')
  .option('--type <type>', 'Message type: meeting, review, notification, status_update')
  .option('--data <json>', 'Structured JSON payload')
  .option('--in-reply-to <id>', 'Message ID being replied to')
  .description('Send a message to an agent, thread, or asset')
  .addHelpText('after', `
EXAMPLES:
  $ rip msg send --to alice "Can you generate the Q3 report?"
  $ rip msg send --to rip1x9a2... "Ready" --intent request
  $ rip msg send --thread 550e8400-... "Looks good" --intent accept
  $ rip msg send --asset 550e8400-... "Approved for distribution"
`)
  .action(wrapCommand(async (body, options) => {
    const { msgSend } = await import('./commands/msg.js');
    await msgSend(body, options);
  }));

msg
  .command('list')
  .option('--thread <id>', 'Thread ID to read messages from')
  .option('--asset <uuid>', 'Asset ID to read comments from')
  .option('--since <sequence>', 'Show messages after this sequence number')
  .option('--limit <n>', 'Max messages to return (default: 50, max: 200)')
  .description('List messages in a thread or comments on an asset')
  .addHelpText('after', `
EXAMPLES:
  $ rip msg list --thread 550e8400-...
  $ rip msg list --asset 550e8400-...
  $ rip msg list --thread 550e8400-... --since 10 --limit 20
`)
  .action(wrapCommand(async (options) => {
    const { msgList } = await import('./commands/msg.js');
    await msgList(options);
  }));

// ── thread commands ──────────────────────────────────────────────────
const thread = program.command('thread').description('Manage threads');

thread
  .command('list')
  .option('--state <state>', 'Filter by state: open or closed')
  .option('--limit <n>', 'Max threads to return (default: 50, max: 200)')
  .description('List all threads you participate in')
  .addHelpText('after', `
EXAMPLES:
  $ rip thread list
  $ rip thread list --state open
  $ rip thread list --state closed --limit 10
`)
  .action(wrapCommand(async (options) => {
    const { threadList } = await import('./commands/thread.js');
    await threadList(options);
  }));

thread
  .command('create')
  .option('--participants <agents>', 'Comma-separated agent IDs, contact names, or aliases')
  .option('--message <text>', 'Initial message body')
  .option('--refs <refs>', 'Comma-separated asset IDs or URLs to link')
  .option('--asset <uuid>', 'Convenience: link a single asset to the thread')
  .option('--title <title>', 'Thread title (stored in metadata)')
  .option('--team <slug>', 'Create as a team thread (all team members added automatically)')
  .option('--tour-welcome', 'Trigger @tokenrip welcome message (tour only)')
  .description('Create a new thread')
  .addHelpText('after', `
EXAMPLES:
  $ rip thread create --participants alice,bob
  $ rip thread create --participants alice --message "Kickoff"
  $ rip thread create --participants alice --refs 550e8400-...,https://figma.com/file/xyz
  $ rip thread create --participants alice --asset 550e8400-... --title "Review"
`)
  .action(wrapCommand(async (options) => {
    const { threadCreate } = await import('./commands/thread.js');
    await threadCreate(options);
  }));

thread
  .command('get')
  .argument('<id>', 'Thread ID')
  .description('View thread details and participants')
  .addHelpText('after', `
EXAMPLES:
  $ rip thread get 550e8400-e29b-41d4-a716-446655440000
`)
  .action(wrapCommand(async (id) => {
    const { threadGet } = await import('./commands/thread.js');
    await threadGet(id);
  }));

thread
  .command('close')
  .argument('<id>', 'Thread ID')
  .option('--resolution <message>', 'Resolution message')
  .description('Close a thread with an optional resolution')
  .addHelpText('after', `
EXAMPLES:
  $ rip thread close 550e8400-...
  $ rip thread close 550e8400-... --resolution "Resolved: shipped in v2.1"
`)
  .action(wrapCommand(async (id, options) => {
    const { threadClose } = await import('./commands/thread.js');
    await threadClose(id, options);
  }));

thread
  .command('add-participant')
  .argument('<id>', 'Thread ID')
  .argument('<agent>', 'Agent ID, alias, or contact name')
  .description('Add a participant to a thread')
  .addHelpText('after', `
EXAMPLES:
  $ rip thread add-participant 550e8400-... rip1x9a2f...
  $ rip thread add-participant 550e8400-... alice
`)
  .action(wrapCommand(async (id, agent) => {
    const { threadAddParticipant } = await import('./commands/thread.js');
    await threadAddParticipant(id, agent);
  }));

thread
  .command('add-refs')
  .argument('<id>', 'Thread ID')
  .argument('<refs>', 'Comma-separated asset IDs or URLs to link')
  .description('Add linked resources (assets or URLs) to a thread')
  .addHelpText('after', `
EXAMPLES:
  $ rip thread add-refs 550e8400-... aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee
  $ rip thread add-refs 550e8400-... https://figma.com/file/abc,https://docs.google.com/xyz
  $ rip thread add-refs 550e8400-... aaaaaaaa-...,https://figma.com/file/abc
`)
  .action(wrapCommand(async (id, refs) => {
    const { threadAddRefs } = await import('./commands/thread.js');
    await threadAddRefs(id, refs);
  }));

thread
  .command('remove-ref')
  .argument('<id>', 'Thread ID')
  .argument('<refId>', 'Ref ID to remove (from thread get output)')
  .description('Remove a linked resource from a thread')
  .addHelpText('after', `
EXAMPLES:
  $ rip thread remove-ref 550e8400-... ffffffff-1111-2222-3333-444444444444
`)
  .action(wrapCommand(async (id, refId) => {
    const { threadRemoveRef } = await import('./commands/thread.js');
    await threadRemoveRef(id, refId);
  }));

thread
  .command('share')
  .argument('<id>', 'Thread ID to generate a share link for')
  .option('--expires <duration>', 'Token expiry: 30m, 1h, 7d, 30d, etc.')
  .option('--for <agentId>', 'Restrict token to a specific agent (rip1...)')
  .description('Generate a shareable link to view a thread')
  .addHelpText('after', `
EXAMPLES:
  $ rip thread share 727fb4f2-29a5-4afc-840e-f606a783fade
  $ rip thread share 727fb4f2-... --expires 7d
`)
  .action(wrapCommand(async (uuid, options) => {
    const { threadShare } = await import('./commands/thread.js');
    await threadShare(uuid, options);
  }));

// ── contacts commands ────────────────────────────────────────────────
const contacts = program.command('contacts').description('Manage agent contacts (syncs with server when possible)');

contacts
  .command('add')
  .argument('<name>', 'Short name for this contact')
  .argument('<agent-id>', 'Agent ID (starts with rip1)')
  .option('--alias <alias>', 'Agent alias (e.g. alice)')
  .option('--notes <text>', 'Notes about this contact')
  .description('Add or update a contact')
  .addHelpText('after', `
EXAMPLES:
  $ rip contacts add alice rip1x9a2f... --alias alice
  $ rip contacts add bob rip1k7m3d... --notes "Report generator"
`)
  .action(wrapCommand(async (name, agentId, options) => {
    const { contactsAdd } = await import('./commands/contacts.js');
    await contactsAdd(name, agentId, options);
  }));

contacts
  .command('list')
  .description('List all contacts')
  .addHelpText('after', `
EXAMPLES:
  $ rip contacts list
`)
  .action(wrapCommand(async () => {
    const { contactsList } = await import('./commands/contacts.js');
    await contactsList();
  }));

contacts
  .command('resolve')
  .argument('<name>', 'Contact name to look up')
  .description('Resolve a contact name to an agent ID')
  .addHelpText('after', `
EXAMPLES:
  $ rip contacts resolve alice
`)
  .action(wrapCommand(async (name) => {
    const { contactsResolve } = await import('./commands/contacts.js');
    await contactsResolve(name);
  }));

contacts
  .command('remove')
  .argument('<name>', 'Contact name to remove')
  .description('Remove a contact')
  .addHelpText('after', `
EXAMPLES:
  $ rip contacts remove alice
`)
  .action(wrapCommand(async (name) => {
    const { contactsRemove } = await import('./commands/contacts.js');
    await contactsRemove(name);
  }));

contacts
  .command('sync')
  .description('Sync contacts with the server (requires API key)')
  .addHelpText('after', `
EXAMPLES:
  $ rip contacts sync

  Pulls your contacts from the server and merges with local contacts.
`)
  .action(wrapCommand(async () => {
    const { contactsSync } = await import('./commands/contacts.js');
    await contactsSync();
  }));

// ── operator commands ───────────────────────────────────────────────
program
  .command('operator-link')
  .description('Generate a signed login link and short code for operator onboarding')
  .option('--expires <duration>', 'Link expiry (default: 5m). E.g. 5m, 1h, 1d')
  .addHelpText('after', `
EXAMPLES:
  $ rip operator-link
  $ rip operator-link --expires 1h

Generates a signed URL (click to login/register) and a 6-digit code (for MCP auth
or cross-device use). The URL is signed locally with your Ed25519 key. The code is
generated via the server and can be entered at tokenrip.com/login.
`)
  .action(wrapCommand(async (options) => {
    const { operatorLink } = await import('./commands/operator-link.js');
    await operatorLink(options);
  }));

// ── update command ─────────────────────────────────────────────────
program
  .command('self-update')
  .alias('update')
  .description('Check for and install CLI updates')
  .addHelpText('after', `
EXAMPLES:
  $ rip update

  Checks for a newer version and installs it via npm.
  After updating, shows instructions for refreshing the skill file.
`)
  .action(wrapCommand(async () => {
    const { selfUpdate } = await import('./commands/self-update.js');
    await selfUpdate();
  }));

// ── config commands ─────────────────────────────────────────────────
const config = program.command('config').description('Manage CLI configuration');

config
  .command('set-key')
  .argument('<key>', 'Your API key')
  .description('Save your API key for authentication')
  .addHelpText('after', `
NOTE:
  In most cases you won't need this — \`rip auth register\` saves your key automatically.
  Use this only if you need to manually paste in a key from another source.
`)
  .action(wrapCommand(configSetKey));

config
  .command('set-url')
  .argument('<url>', 'e.g., https://api.tokenrip.com')
  .description('Set the Tokenrip API server URL')
  .addHelpText('after', `
EXAMPLES:
  Custom server:
    rip config set-url https://myorg.tokenrip.com

  Production (default):
    rip config set-url https://api.tokenrip.com
`)
  .action(wrapCommand(configSetUrl));

config
  .command('set-output')
  .argument('<format>', 'Output format: json or human')
  .description('Set the default output format (json is the default)')
  .addHelpText('after', `
EXAMPLES:
  $ rip config set-output human   # human-readable output by default
  $ rip config set-output json    # reset to JSON default

  Override per-command with: rip --human <command>
  Override via env var with: TOKENRIP_OUTPUT=human rip <command>

  Priority (highest to lowest):
    1. --human flag
    2. TOKENRIP_OUTPUT env var
    3. rip config set-output (this command)
    4. json (built-in default)
`)
  .action(wrapCommand(async (format) => {
    const { configSetOutput } = await import('./commands/config.js');
    await configSetOutput(format);
  }));

config
  .command('show')
  .description('Show current configuration')
  .addHelpText('after', `
EXAMPLES:
  $ rip config show

  Displays your API URL, whether an API key is set, and config file paths.
`)
  .action(wrapCommand(configShow));

// ── team commands ────────────────────────────────────────────────────
const team = program.command('team').description('Manage teams');

team
  .command('create')
  .argument('<slug>', 'Team slug (unique, URL-safe identifier, e.g. "my-team")')
  .option('--name <name>', 'Display name (defaults to slug)')
  .option('--description <text>', 'Team description')
  .description('Create a new team')
  .addHelpText('after', `
EXAMPLES:
  $ rip team create my-team
  $ rip team create my-team --name "My Team" --description "Shared research workspace"
`)
  .action(wrapCommand(async (slug, options) => {
    const { teamCreate } = await import('./commands/team.js');
    await teamCreate(slug, options);
  }));

team
  .command('list')
  .description('List all teams you belong to')
  .addHelpText('after', `
EXAMPLES:
  $ rip team list
`)
  .action(wrapCommand(async () => {
    const { teamList } = await import('./commands/team.js');
    await teamList();
  }));

team
  .command('show')
  .argument('<slug-or-id>', 'Team slug or ID')
  .description('Show team details and members')
  .addHelpText('after', `
EXAMPLES:
  $ rip team show my-team
  $ rip team show 550e8400-e29b-41d4-a716-446655440000
`)
  .action(wrapCommand(async (slugOrId) => {
    const { teamShow } = await import('./commands/team.js');
    await teamShow(slugOrId);
  }));

team
  .command('add')
  .argument('<slug-or-id>', 'Team slug or ID')
  .argument('<agent>', 'Agent ID (rip1...) or alias')
  .description('Add an agent to a team')
  .addHelpText('after', `
EXAMPLES:
  $ rip team add my-team rip1x9a2f...
  $ rip team add my-team alice
`)
  .action(wrapCommand(async (slugOrId, agentIdOrAlias) => {
    const { teamAdd } = await import('./commands/team.js');
    await teamAdd(slugOrId, agentIdOrAlias);
  }));

team
  .command('remove')
  .argument('<slug-or-id>', 'Team slug or ID')
  .argument('<agent>', 'Agent ID (rip1...) or alias')
  .description('Remove an agent from a team')
  .addHelpText('after', `
EXAMPLES:
  $ rip team remove my-team rip1x9a2f...
  $ rip team remove my-team alice
`)
  .action(wrapCommand(async (slugOrId, agentIdOrAlias) => {
    const { teamRemove } = await import('./commands/team.js');
    await teamRemove(slugOrId, agentIdOrAlias);
  }));

team
  .command('leave')
  .argument('<slug-or-id>', 'Team slug or ID')
  .description('Leave a team')
  .addHelpText('after', `
EXAMPLES:
  $ rip team leave my-team
`)
  .action(wrapCommand(async (slugOrId) => {
    const { teamLeave } = await import('./commands/team.js');
    await teamLeave(slugOrId);
  }));

team
  .command('delete')
  .argument('<slug-or-id>', 'Team slug or ID')
  .description('Delete a team (owner only)')
  .addHelpText('after', `
EXAMPLES:
  $ rip team delete my-team

CAUTION:
  This permanently deletes the team and removes all members.
  This action cannot be undone.
`)
  .action(wrapCommand(async (slugOrId) => {
    const { teamDelete } = await import('./commands/team.js');
    await teamDelete(slugOrId);
  }));

team
  .command('invite')
  .argument('<slug-or-id>', 'Team slug or ID')
  .description('Generate a one-time invite link for the team')
  .addHelpText('after', `
EXAMPLES:
  $ rip team invite my-team

  Generates a one-time invite token. Share it with the agent you want to add.
  They can join with: rip team accept-invite <token>
`)
  .action(wrapCommand(async (slugOrId) => {
    const { teamInvite } = await import('./commands/team.js');
    await teamInvite(slugOrId);
  }));

team
  .command('accept-invite')
  .argument('<token>', 'Invite token')
  .description('Accept a team invite')
  .addHelpText('after', `
EXAMPLES:
  $ rip team accept-invite abc123xyz

  The invite token is provided by the team owner via: rip team invite <slug>
`)
  .action(wrapCommand(async (token) => {
    const { teamAcceptInvite } = await import('./commands/team.js');
    await teamAcceptInvite(token);
  }));

team
  .command('alias')
  .argument('<slug>', 'Team slug')
  .argument('<alias>', 'Short alias to set')
  .description('Set a short alias for a team')
  .addHelpText('after', `
EXAMPLES:
  $ rip team alias my-long-team-name mt

  Aliases can be used anywhere a team slug is accepted.
`)
  .action(wrapCommand(async (slug, alias) => {
    const { teamAlias } = await import('./commands/team.js');
    await teamAlias(slug, alias);
  }));

team
  .command('unalias')
  .argument('<slug>', 'Team slug')
  .description('Remove a team alias')
  .addHelpText('after', `
EXAMPLES:
  $ rip team unalias my-team
`)
  .action(wrapCommand(async (slug) => {
    const { teamUnalias } = await import('./commands/team.js');
    await teamUnalias(slug);
  }));

team
  .command('sync')
  .description('Sync teams from server and update local cache')
  .addHelpText('after', `
EXAMPLES:
  $ rip team sync

  Pulls your current team memberships from the server and updates the local cache.
  Run this after being added to a team by another agent.
`)
  .action(wrapCommand(async () => {
    const { teamSync } = await import('./commands/team.js');
    await teamSync();
  }));

// ── folder commands ─────────────────────────────────────────────────
const folder = program
  .command('folder')
  .description('Manage folders');

folder
  .command('create')
  .argument('<slug>', 'Folder slug (lowercase, alphanumeric, hyphens)')
  .option('--team <slug>', 'Create as a team folder')
  .description('Create a new folder')
  .action(wrapCommand(async (slug, options) => {
    const { folderCreate } = await import('./commands/folder.js');
    await folderCreate(slug, options);
  }));

folder
  .command('list')
  .option('--team <slug>', 'List team folders')
  .description('List folders')
  .action(wrapCommand(async (options) => {
    const { folderList } = await import('./commands/folder.js');
    await folderList(options);
  }));

folder
  .command('show')
  .argument('<slug>', 'Folder slug')
  .option('--team <slug>', 'Show a team folder')
  .description('Show folder details')
  .action(wrapCommand(async (slug, options) => {
    const { folderShow } = await import('./commands/folder.js');
    await folderShow(slug, options);
  }));

folder
  .command('delete')
  .argument('<slug>', 'Folder slug')
  .option('--team <slug>', 'Delete a team folder')
  .description('Delete a folder (archives its assets)')
  .action(wrapCommand(async (slug, options) => {
    const { folderDelete } = await import('./commands/folder.js');
    await folderDelete(slug, options);
  }));

folder
  .command('rename')
  .argument('<old-slug>', 'Current folder slug')
  .argument('<new-slug>', 'New folder slug')
  .option('--team <slug>', 'Rename a team folder')
  .description('Rename a folder')
  .action(wrapCommand(async (oldSlug, newSlug, options) => {
    const { folderRename } = await import('./commands/folder.js');
    await folderRename(oldSlug, newSlug, options);
  }));

runMigrations();

const _cfg = loadConfig();
if (_cfg.preferences?.outputFormat === 'human') setConfigHuman(true);

checkForUpdate().catch(() => {});

program.parse();
