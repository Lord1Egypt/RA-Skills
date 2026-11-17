import fs from 'node:fs/promises';
// Preserve the last complete state if the process stops during a write.
export async function saveState(file, state) {
  const temporary = `${file}.${process.pid}.tmp`;
  await fs.writeFile(temporary, JSON.stringify(state, null, 2), { mode: 0o600 });
  await fs.rename(temporary, file);
}
