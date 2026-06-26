import fs from 'node:fs/promises';
import path from 'node:path';

export async function loadState(outputDir) {
  const statePath = path.join(outputDir, '.weread-import-state.json');
  try {
    const raw = await fs.readFile(statePath, 'utf8');
    const data = JSON.parse(raw);
    return { path: statePath, data: data && typeof data === 'object' ? data : { books: {} } };
  } catch {
    return { path: statePath, data: { books: {} } };
  }
}

export async function saveState(state) {
  await fs.mkdir(path.dirname(state.path), { recursive: true });
  await fs.writeFile(state.path, `${JSON.stringify(state.data, null, 2)}\n`, 'utf8');
}
