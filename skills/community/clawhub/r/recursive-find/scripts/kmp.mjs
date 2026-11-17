// Knuth–Morris–Pratt string search.
//
// KMP finds every occurrence of `pattern` in `text` in O(n + m) time by
// precomputing a "longest proper prefix that is also a suffix" (LPS) table,
// which lets us skip re-comparing characters we already know match.

/**
 * Build the LPS (failure) table for a pattern.
 * lps[i] = length of the longest proper prefix of pattern[0..i]
 * that is also a suffix of pattern[0..i].
 * @param {string} pattern
 * @returns {number[]}
 */
export function computeLPS(pattern) {
  const lps = new Array(pattern.length).fill(0);
  let len = 0; // length of the previous longest prefix-suffix
  let i = 1;
  while (i < pattern.length) {
    if (pattern[i] === pattern[len]) {
      lps[i] = ++len;
      i++;
    } else if (len > 0) {
      // fall back — don't advance i, retry with a shorter prefix
      len = lps[len - 1];
    } else {
      lps[i] = 0;
      i++;
    }
  }
  return lps;
}

/**
 * Return the start index of every (possibly overlapping) match of
 * `pattern` in `text`. Empty pattern yields no matches.
 * @param {string} text
 * @param {string} pattern
 * @returns {number[]} match start indices
 */
export function kmpSearch(text, pattern) {
  const matches = [];
  const n = text.length;
  const m = pattern.length;
  if (m === 0 || m > n) return matches;

  const lps = computeLPS(pattern);
  let i = 0; // index into text
  let j = 0; // index into pattern
  while (i < n) {
    if (text[i] === pattern[j]) {
      i++;
      j++;
      if (j === m) {
        matches.push(i - j);
        j = lps[j - 1]; // continue searching for overlapping matches
      }
    } else if (j > 0) {
      j = lps[j - 1];
    } else {
      i++;
    }
  }
  return matches;
}
