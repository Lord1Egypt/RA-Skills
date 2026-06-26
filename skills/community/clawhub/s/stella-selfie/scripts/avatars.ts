import * as fs from "fs";
import * as path from "path";

const SUPPORTED_EXTENSIONS = new Set([".jpg", ".jpeg", ".png", ".webp"]);

interface FileWithTime {
  filePath: string;
  time: number;
}

function toPosixPath(p: string): string {
  // Normalize for consistent downstream handling across platforms (tests, logs, consumers)
  return p.replace(/\\/g, "/");
}

/**
 * Get the best available creation/modification time for a file.
 * Priority: birthtime > mtime > ctime
 */
function getFileTime(stat: fs.Stats): number {
  const birthtime = stat.birthtimeMs;
  const mtime = stat.mtimeMs;
  const ctime = stat.ctimeMs;

  // birthtime is 0 or equal to epoch on some systems (Linux ext4 without birth time support)
  if (birthtime && birthtime > 0) {
    return birthtime;
  }
  if (mtime && mtime > 0) {
    return mtime;
  }
  return ctime;
}

/**
 * Resolve a file path to its real path, returning null on error.
 */
function safeRealpath(filePath: string): string | null {
  try {
    return fs.realpathSync(filePath);
  } catch {
    return null;
  }
}

/**
 * Select reference avatar images based on IDENTITY.md config.
 *
 * Logic:
 * 1. If Avatar exists, add it as first entry
 * 2. If AvatarBlendEnabled, scan AvatarsDir for supported image files
 * 3. Sort by file time descending, take up to AvatarMaxRefs total
 * 4. Deduplicate by realpath, keeping Avatar at position 0
 * 5. Warn (don't throw) if AvatarsDir is missing or unreadable
 */
export function selectAvatars(options: {
  avatar: string | null;
  avatarsDir: string | null;
  avatarMaxRefs: number;
  avatarBlendEnabled: boolean;
}): string[] {
  const { avatar, avatarsDir, avatarMaxRefs, avatarBlendEnabled } = options;

  const seenRealpaths = new Set<string>();
  const result: string[] = [];

  // Add primary Avatar first
  if (avatar) {
    if (fs.existsSync(avatar)) {
      const real = safeRealpath(avatar);
      if (real) {
        seenRealpaths.add(real);
        result.push(toPosixPath(avatar));
      }
    } else {
      console.warn(`[stella] Warning: Avatar not found: ${avatar}`);
    }
  }

  // Scan AvatarsDir if blending is enabled
  if (avatarBlendEnabled && avatarsDir) {
    if (!fs.existsSync(avatarsDir)) {
      console.warn(`[stella] Warning: AvatarsDir not found: ${avatarsDir}`);
    } else {
      let entries: fs.Dirent[];
      try {
        entries = fs.readdirSync(avatarsDir, { withFileTypes: true });
      } catch (err) {
        console.warn(
          `[stella] Warning: Cannot read AvatarsDir: ${avatarsDir} — ${(err as Error).message}`
        );
        entries = [];
      }

      const candidates: FileWithTime[] = [];

      for (const entry of entries) {
        if (!entry.isFile()) continue;
        const ext = path.extname(entry.name).toLowerCase();
        if (!SUPPORTED_EXTENSIONS.has(ext)) continue;

        // Use POSIX-style paths for consistent behavior across platforms.
        // Node on Windows accepts forward slashes in most filesystem APIs.
        const filePath = toPosixPath(path.join(avatarsDir, entry.name));
        try {
          const stat = fs.statSync(filePath);
          candidates.push({ filePath, time: getFileTime(stat) });
        } catch {
          // Skip unreadable files silently
        }
      }

      // Sort newest first
      candidates.sort((a, b) => b.time - a.time);

      for (const candidate of candidates) {
        if (result.length >= avatarMaxRefs) break;

        const real = safeRealpath(candidate.filePath);
        if (!real || seenRealpaths.has(real)) continue;

        seenRealpaths.add(real);
        result.push(toPosixPath(candidate.filePath));
      }
    }
  }

  return result;
}
