#!/usr/bin/env node
/**
 * Unipile Instagram SDK CLI
 * Usage: node instagram.mjs <command> [options]
 * 
 * Environment:
 *   UNIPILE_DSN           - API endpoint (required)
 *   UNIPILE_ACCESS_TOKEN  - Access token (required)
 *   UNIPILE_PERMISSIONS   - Comma-separated: "read" and/or "write" (default: "read,write")
 * 
 * Examples:
 *   UNIPILE_PERMISSIONS=read node instagram.mjs posts <account> nasa
 *   UNIPILE_PERMISSIONS=read,write node instagram.mjs send <chat_id> "Hello"
 */

import { UnipileClient, UnsuccessfulRequestError } from 'unipile-node-sdk';

const DSN = process.env.UNIPILE_DSN;
const TOKEN = process.env.UNIPILE_ACCESS_TOKEN;
const PERMISSIONS = (process.env.UNIPILE_PERMISSIONS || 'read,write').split(',').map(p => p.trim().toLowerCase());

if (!DSN || !TOKEN) {
  console.error('Error: UNIPILE_DSN and UNIPILE_ACCESS_TOKEN must be set');
  console.error('Get credentials from https://dashboard.unipile.com');
  process.exit(1);
}

const hasRead = PERMISSIONS.includes('read');
const hasWrite = PERMISSIONS.includes('write');

// Commands that require write permission
const WRITE_COMMANDS = [
  'send', 'start-chat', 'create-post', 'comment', 'react'
];

// Commands that are read-only
const READ_COMMANDS = [
  'accounts', 'account', 'chats', 'chat', 'messages',
  'profile', 'my-profile', 'relations', 'followers',
  'posts', 'post', 'attendees', 'comments'
];

const client = new UnipileClient(DSN, TOKEN);

function parseArgs(args) {
  const result = { _: [] };
  for (const arg of args) {
    if (arg.startsWith('--')) {
      const [key, value] = arg.slice(2).split('=');
      result[key] = value ?? true;
    } else {
      result._.push(arg);
    }
  }
  return result;
}

function json(obj) {
  console.log(JSON.stringify(obj, null, 2));
}

function checkPermission(cmd) {
  if (WRITE_COMMANDS.includes(cmd) && !hasWrite) {
    console.error(`Error: Command '${cmd}' requires write permission.`);
    console.error(`Current permissions: ${PERMISSIONS.join(', ')}`);
    console.error(`Set UNIPILE_PERMISSIONS=write or UNIPILE_PERMISSIONS=read,write to enable.`);
    process.exit(3);
  }
  
  if (READ_COMMANDS.includes(cmd) && !hasRead) {
    console.error(`Error: Command '${cmd}' requires read permission.`);
    console.error(`Current permissions: ${PERMISSIONS.join(', ')}`);
    console.error(`Set UNIPILE_PERMISSIONS=read to enable.`);
    process.exit(3);
  }
}

function showHelp() {
  console.log(`Unipile Instagram SDK CLI

Environment:
  UNIPILE_DSN           API endpoint (required)
  UNIPILE_ACCESS_TOKEN  Access token (required)
  UNIPILE_PERMISSIONS   Permissions: "read", "write", or "read,write" (default: read,write)

Read Commands (require read permission):
  accounts                             List Instagram accounts
  account <id>                         Get account details
  chats [--account_id=X] [--limit=N]   List DMs/chats
  chat <id>                            Get chat details
  messages <chat_id> [--limit=N]       List messages in a chat
  profile <account_id> <username>      Get user profile
  my-profile <account_id>              Get own profile
  relations <account_id> [--limit=N]   Get followers/following
  followers <account_id> [--limit=N]   Get followers (alias for relations)
  posts <account_id> <username> [--limit=N]
  post <account_id> <post_id>
  comments <account_id> <post_id> [--limit=N]
  attendees [--account_id=X]           List chat contacts

Write Commands (require write permission):
  send <chat_id> "<text>"              Send message/DM
  start-chat <account_id> "<text>" --to=<id>[,id]
  create-post <account_id> "<text>"
  comment <account_id> <post_id> "<text>"
  react <account_id> <post_id> [--type=like|heart|...]

Examples:
  # Read-only mode (safe for viewing data)
  UNIPILE_PERMISSIONS=read node instagram.mjs posts <account> nasa

  # Full access (required for sending messages, creating posts)
  UNIPILE_PERMISSIONS=read,write node instagram.mjs send <chat_id> "Hello!"

  # Default is full access
  node instagram.mjs accounts
`);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const [cmd, ...params] = args._;

  if (!cmd || cmd === 'help') {
    showHelp();
    return;
  }

  checkPermission(cmd);

  try {
    switch (cmd) {
      // Account
      case 'accounts':
        const allAccounts = await client.account.getAll();
        json(allAccounts.items?.filter(a => a.type === 'INSTAGRAM') || allAccounts);
        break;
        
      case 'account':
        json(await client.account.get(params[0]));
        break;

      // Chats
      case 'chats':
        json(await client.messaging.getAllChats({
          account_type: 'INSTAGRAM',
          account_id: args.account_id,
          limit: args.limit ? parseInt(args.limit) : undefined,
          after: args.after,
        }));
        break;

      case 'chat':
        json(await client.messaging.getChat(params[0]));
        break;

      case 'messages':
        json(await client.messaging.getAllMessagesFromChat({
          chat_id: params[0],
          limit: args.limit ? parseInt(args.limit) : undefined,
        }));
        break;

      case 'send':
        await client.messaging.sendMessage({
          chat_id: params[0],
          text: params[1],
        });
        console.log('Message sent');
        break;

      case 'start-chat':
        await client.messaging.startNewChat({
          account_id: params[0],
          attendees_ids: args.to?.split(',') || [],
          text: params[1],
        });
        console.log('Chat started');
        break;

      // Profiles
      case 'profile':
        json(await client.users.getProfile({
          account_id: params[0],
          identifier: params[1],
        }));
        break;

      case 'my-profile':
        json(await client.users.getOwnProfile(params[0]));
        break;

      case 'relations':
      case 'followers':
        json(await client.users.getAllRelations({
          account_id: params[0],
          limit: args.limit ? parseInt(args.limit) : undefined,
        }));
        break;

      // Posts
      case 'posts':
        json(await client.users.getAllPosts({
          account_id: params[0],
          identifier: params[1],
          limit: args.limit ? parseInt(args.limit) : undefined,
        }));
        break;

      case 'post':
        json(await client.users.getPost({
          account_id: params[0],
          post_id: params[1],
        }));
        break;

      case 'create-post':
        await client.users.createPost({
          account_id: params[0],
          text: params[1],
        });
        console.log('Post created');
        break;

      // Comments
      case 'comments':
        json(await client.users.getAllPostComments({
          account_id: params[0],
          post_id: params[1],
          limit: args.limit ? parseInt(args.limit) : undefined,
        }));
        break;

      case 'comment':
        await client.users.sendPostComment({
          account_id: params[0],
          post_id: params[1],
          text: params[2],
        });
        console.log('Comment added');
        break;

      // Reactions
      case 'react':
        await client.users.sendPostReaction({
          account_id: params[0],
          post_id: params[1],
          reaction_type: args.type || 'like',
        });
        console.log('Reaction added');
        break;

      // Attendees
      case 'attendees':
        json(await client.messaging.getAllAttendees({
          account_id: args.account_id,
          limit: args.limit ? parseInt(args.limit) : undefined,
        }));
        break;

      default:
        console.error(`Unknown command: ${cmd}`);
        console.error('Run with "help" for usage information.');
        process.exit(1);
    }
  } catch (err) {
    if (err instanceof UnsuccessfulRequestError) {
      console.error(`API Error (${err.body?.status}): ${err.message}`);
      console.error('Type:', err.body?.type);
      if (err.body?.detail) console.error('Detail:', err.body.detail);
    } else {
      console.error('Error:', err.message);
    }
    process.exit(1);
  }
}

main();
