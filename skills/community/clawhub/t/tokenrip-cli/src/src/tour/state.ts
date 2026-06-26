import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

export interface TourState {
  step: number;
  assetId: string | null;
  threadId: string | null;
  startedAt: string; // ISO 8601
}

export function TOUR_FILE(): string {
  const dir = process.env.TOKENRIP_CONFIG_DIR ?? path.join(os.homedir(), '.config', 'tokenrip');
  return path.join(dir, 'tour.json');
}

export function loadTourState(): TourState | null {
  try {
    const raw = fs.readFileSync(TOUR_FILE(), 'utf-8');
    return JSON.parse(raw) as TourState;
  } catch {
    return null;
  }
}

export function saveTourState(state: TourState): void {
  const file = TOUR_FILE();
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(state, null, 2), 'utf-8');
}

export function clearTourState(): void {
  try {
    fs.unlinkSync(TOUR_FILE());
  } catch {
    // already gone, not our problem
  }
}
