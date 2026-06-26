/**
 * Counter - Simple frequency counter utility
 */

export class Counter {
  constructor() {
    this.counts = {};
  }

  increment(key) {
    this.counts[key] = (this.counts[key] || 0) + 1;
  }

  top(n = 5) {
    return Object.entries(this.counts)
      .sort(([, a], [, b]) => b - a)
      .slice(0, n)
      .map(([key, count]) => [key, count]);
  }

  total() {
    return Object.values(this.counts).reduce((a, b) => a + b, 0);
  }
}
