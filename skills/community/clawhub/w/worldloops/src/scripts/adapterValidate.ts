import * as fs from 'node:fs';
import * as path from 'node:path';

import { validateAdapterSignal } from '../adapter/validateAdapterSignal';

function main(): void {
  const filePath = process.argv[2];

  if (!filePath) {
    console.error(
      JSON.stringify(
        {
          ok: false,
          error: {
            code: 'MISSING_FILE',
            message:
              'Usage: npm run adapter:validate -- <path-to-adapter-signal.json>',
          },
          safety: { externalWrite: false },
        },
        null,
        2
      )
    );
    process.exit(1);
  }

  let raw: unknown;
  try {
    const resolved = path.resolve(filePath);
    raw = JSON.parse(fs.readFileSync(resolved, 'utf8'));
  } catch (err) {
    console.error(
      JSON.stringify(
        {
          ok: false,
          error: {
            code: 'FILE_READ_ERROR',
            message: err instanceof Error ? err.message : String(err),
          },
          safety: { externalWrite: false },
        },
        null,
        2
      )
    );
    process.exit(1);
  }

  const result = validateAdapterSignal(raw);

  if (result.ok) {
    console.log('Valid WorldLoops Adapter Signal');
    console.log(`source: ${result.signal.source}`);
    console.log(`sourceType: ${result.signal.sourceType}`);
    console.log(`externalWrite: ${result.signal.externalWrite}`);
    process.exit(0);
  } else {
    console.error(
      JSON.stringify(
        {
          ok: false,
          errors: result.errors,
          safety: { externalWrite: false },
        },
        null,
        2
      )
    );
    process.exit(1);
  }
}

main();
