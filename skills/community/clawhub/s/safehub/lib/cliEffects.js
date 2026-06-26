/**
 * CLI effects: typing animation and loading indicator.
 * Uses stdout so output is stream-friendly and can be piped.
 */

const CHAR_DELAY_MS = 8;
const LINE_DELAY_MS = 2;
const LOADING_FRAMES = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];
const LOADING_INTERVAL_MS = 80;

/**
 * Writes text to stdout with a typing effect (character by character).
 * @param {string} text - Full text to type out
 * @param {object} options - { delayMs, chunkSize } (chunkSize > 1 speeds up by typing chunks)
 * @returns {Promise<void>}
 */
function typeOut(text, options = {}) {
  const delayMs = options.delayMs ?? CHAR_DELAY_MS;
  const chunkSize = options.chunkSize ?? 1;

  return new Promise((resolve) => {
    let i = 0;
    const len = text.length;

    function writeChunk() {
      if (i >= len) {
        if (typeof process.stdout.write === 'function') {
          process.stdout.write('\n');
        }
        return resolve();
      }
      const end = Math.min(i + chunkSize, len);
      const chunk = text.slice(i, end);
      process.stdout.write(chunk);
      i = end;
      setTimeout(writeChunk, delayMs);
    }

    writeChunk();
  });
}

/**
 * Writes text to stdout with a line-by-line typing effect (each line appears after a short delay).
 * @param {string} text - Full text (can contain newlines)
 * @param {object} options - { lineDelayMs } delay between lines
 * @returns {Promise<void>}
 */
function typeOutLines(text, options = {}) {
  const lineDelayMs = options.lineDelayMs ?? LINE_DELAY_MS;
  const lines = text.split('\n');

  return new Promise((resolve) => {
    let idx = 0;
    function writeNext() {
      if (idx >= lines.length) {
        return resolve();
      }
      process.stdout.write(lines[idx] + (idx < lines.length - 1 ? '\n' : ''));
      idx += 1;
      if (idx < lines.length) {
        setTimeout(writeNext, lineDelayMs);
      } else {
        process.stdout.write('\n');
        resolve();
      }
    }
    writeNext();
  });
}

/**
 * Shows a loading spinner with optional message until the given promise settles.
 * Resolves with the promise result; the spinner is cleared before resolving.
 * @param {Promise<T>} promise - The async work to run
 * @param {string} message - Base message (e.g. "Scanning target")
 * @returns {Promise<T>}
 */
async function runWithSpinner(promise, message = 'Loading') {
  let stopped = false;
  let frameIndex = 0;

  const tick = () => {
    if (stopped) return;
    const frame = LOADING_FRAMES[frameIndex % LOADING_FRAMES.length];
    process.stdout.write(`\r ${frame} ${message}   `);
    frameIndex += 1;
  };

  const interval = setInterval(tick, LOADING_INTERVAL_MS);
  tick();

  try {
    const result = await promise;
    stopped = true;
    clearInterval(interval);
    process.stdout.write('\r' + ' '.repeat((message.length + 6)) + '\r');
    return result;
  } catch (err) {
    stopped = true;
    clearInterval(interval);
    process.stdout.write('\r' + ' '.repeat((message.length + 6)) + '\r');
    throw err;
  }
}

/**
 * Runs async work while showing a typing-style loading line that updates in place.
 * @param {Promise<T>} promise - The async work to run
 * @param {string} baseMessage - e.g. "Scanning"
 * @param {string} suffix - e.g. the target name or URL (shortened if long)
 * @returns {Promise<T>}
 */
async function runWithLoading(promise, baseMessage = 'Scanning', suffix = '') {
  const displaySuffix = suffix.length > 50 ? suffix.slice(0, 47) + '...' : suffix;
  const message = displaySuffix ? `${baseMessage} ${displaySuffix}` : baseMessage;
  return runWithSpinner(promise, message);
}

module.exports = { typeOut, typeOutLines, runWithSpinner, runWithLoading };
