#!/usr/bin/env bun

import * as games from './commands/games.js';
import * as passes from './commands/passes.js';
import * as products from './commands/products.js';
import type { CLIResult } from './lib/types.js';

const HELP_TEXT = `roblox-cli - Manage Roblox games, passes, and products

Usage:
  roblox-cli [command] [subcommand] [args] [options]

Commands:
  games list                              List games owned by API key holder
  passes list <universeId>                List game passes
  passes get <universeId> <passId>        Get game pass details
  passes create <universeId> [options]    Create game pass
  passes update <universeId> <passId>     Update game pass
  products list <universeId>              List developer products
  products get <universeId> <productId>   Get product details
  products create <universeId> [options]  Create product
  products update <universeId> <productId> Update product

Options for create/update:
  --name <name>           Name of the pass/product
  --description <desc>    Description text
  --price <robux>         Price in Robux
  --for-sale <true|false> Whether item is for sale

Environment:
  ROBLOX_API_KEY    Required. Your Roblox Open Cloud API key.

Examples:
  roblox-cli games list
  roblox-cli passes list 12345
  roblox-cli passes create 12345 --name "VIP Pass" --price 100 --for-sale true
  roblox-cli products update 12345 67890 --price 50
`;

const MAX_NAME_LENGTH = 50;
const MAX_DESCRIPTION_LENGTH = 1000;
const MAX_PRICE = 1000000000; // 1 billion Robux

interface ParsedFlags {
  name?: string;
  description?: string;
  price?: number;
  isForSale?: boolean;
}

interface ParseResult {
  data?: ParsedFlags;
  error?: string;
}

function validateNumericId(value: string, fieldName: string): string | null {
  if (!/^\d+$/.test(value)) {
    return `${fieldName} must be a numeric ID, got: ${value}`;
  }
  return null;
}

function parseFlags(args: string[]): ParseResult {
  const data: ParsedFlags = {};
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg?.startsWith('--')) {
      const key = arg.slice(2);
      const value = args[i + 1];

      if (key === 'name') {
        if (!value || value.startsWith('--')) {
          return { error: '--name requires a value' };
        }
        if (value.length > MAX_NAME_LENGTH) {
          return { error: `Name must be ${MAX_NAME_LENGTH} characters or less` };
        }
        data.name = value;
        i++;
      } else if (key === 'description') {
        if (!value || value.startsWith('--')) {
          return { error: '--description requires a value' };
        }
        if (value.length > MAX_DESCRIPTION_LENGTH) {
          return { error: `Description must be ${MAX_DESCRIPTION_LENGTH} characters or less` };
        }
        data.description = value;
        i++;
      } else if (key === 'price') {
        if (!value || value.startsWith('--')) {
          return { error: '--price requires a value' };
        }
        const price = parseInt(value, 10);
        if (isNaN(price)) {
          return { error: `Price must be a valid number, got: ${value}` };
        }
        if (price < 0) {
          return { error: 'Price cannot be negative' };
        }
        if (price > MAX_PRICE) {
          return { error: `Price cannot exceed ${MAX_PRICE.toLocaleString()} Robux` };
        }
        data.price = price;
        i++;
      } else if (key === 'for-sale') {
        if (!value || value.startsWith('--')) {
          return { error: '--for-sale requires a value (true or false)' };
        }
        if (value !== 'true' && value !== 'false') {
          return { error: `--for-sale must be "true" or "false", got: ${value}` };
        }
        data.isForSale = value === 'true';
        i++;
      }
    }
  }
  return { data };
}

function outputResult(result: CLIResult<unknown>): void {
  console.log(JSON.stringify(result));
  process.exit(result.success ? 0 : 1);
}

function outputError(code: string, message: string): void {
  console.log(JSON.stringify({
    success: false,
    error: { code, message }
  }));
  process.exit(1);
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);

  if (args.includes('--help') || args.includes('-h') || args.length === 0) {
    console.log(HELP_TEXT);
    process.exit(0);
  }

  const apiKey = process.env.ROBLOX_API_KEY;
  if (!apiKey) {
    outputError('MISSING_API_KEY', 'ROBLOX_API_KEY environment variable is required');
    return;
  }

  const [command, subcommand, ...rest] = args;

  let result: CLIResult<unknown>;

  if (command === 'games') {
    if (subcommand === 'list') {
      result = await games.list(apiKey);
    } else {
      outputError('INVALID_ARGS', `Unknown games subcommand: ${subcommand}`);
      return;
    }
  } else if (command === 'passes') {
    const universeId = rest[0];
    if (!universeId && subcommand !== undefined) {
      outputError('INVALID_ARGS', 'Missing required argument: universeId');
      return;
    }
    
    const universeIdError = universeId ? validateNumericId(universeId, 'universeId') : null;
    if (universeIdError) {
      outputError('INVALID_ARGS', universeIdError);
      return;
    }

    if (subcommand === 'list') {
      result = await passes.list(apiKey, universeId!);
    } else if (subcommand === 'get') {
      const passId = rest[1];
      if (!passId) {
        outputError('INVALID_ARGS', 'Missing required argument: passId');
        return;
      }
      const passIdError = validateNumericId(passId, 'passId');
      if (passIdError) {
        outputError('INVALID_ARGS', passIdError);
        return;
      }
      result = await passes.get(apiKey, universeId!, passId);
    } else if (subcommand === 'create') {
      const parseResult = parseFlags(rest.slice(1));
      if (parseResult.error) {
        outputError('INVALID_ARGS', parseResult.error);
        return;
      }
      result = await passes.create(apiKey, universeId!, parseResult.data!);
    } else if (subcommand === 'update') {
      const passId = rest[1];
      if (!passId) {
        outputError('INVALID_ARGS', 'Missing required argument: passId');
        return;
      }
      const passIdError = validateNumericId(passId, 'passId');
      if (passIdError) {
        outputError('INVALID_ARGS', passIdError);
        return;
      }
      const parseResult = parseFlags(rest.slice(2));
      if (parseResult.error) {
        outputError('INVALID_ARGS', parseResult.error);
        return;
      }
      result = await passes.update(apiKey, universeId!, passId, parseResult.data!);
    } else {
      outputError('INVALID_ARGS', `Unknown passes subcommand: ${subcommand}`);
      return;
    }
  } else if (command === 'products') {
    const universeId = rest[0];
    if (!universeId && subcommand !== undefined) {
      outputError('INVALID_ARGS', 'Missing required argument: universeId');
      return;
    }
    
    const universeIdError = universeId ? validateNumericId(universeId, 'universeId') : null;
    if (universeIdError) {
      outputError('INVALID_ARGS', universeIdError);
      return;
    }

    if (subcommand === 'list') {
      result = await products.list(apiKey, universeId!);
    } else if (subcommand === 'get') {
      const productId = rest[1];
      if (!productId) {
        outputError('INVALID_ARGS', 'Missing required argument: productId');
        return;
      }
      const productIdError = validateNumericId(productId, 'productId');
      if (productIdError) {
        outputError('INVALID_ARGS', productIdError);
        return;
      }
      result = await products.get(apiKey, universeId!, productId);
    } else if (subcommand === 'create') {
      const parseResult = parseFlags(rest.slice(1));
      if (parseResult.error) {
        outputError('INVALID_ARGS', parseResult.error);
        return;
      }
      result = await products.create(apiKey, universeId!, parseResult.data!);
    } else if (subcommand === 'update') {
      const productId = rest[1];
      if (!productId) {
        outputError('INVALID_ARGS', 'Missing required argument: productId');
        return;
      }
      const productIdError = validateNumericId(productId, 'productId');
      if (productIdError) {
        outputError('INVALID_ARGS', productIdError);
        return;
      }
      const parseResult = parseFlags(rest.slice(2));
      if (parseResult.error) {
        outputError('INVALID_ARGS', parseResult.error);
        return;
      }
      result = await products.update(apiKey, universeId!, productId, parseResult.data!);
    } else {
      outputError('INVALID_ARGS', `Unknown products subcommand: ${subcommand}`);
      return;
    }
  } else {
    outputError('INVALID_ARGS', `Unknown command: ${command}`);
    return;
  }

  outputResult(result);
}

main().catch((err) => {
  outputError('INTERNAL_ERROR', err instanceof Error ? err.message : 'Unknown error');
});
