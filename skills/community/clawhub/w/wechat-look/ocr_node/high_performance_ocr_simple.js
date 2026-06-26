const Tesseract = require('tesseract.js');

class HighPerformanceOCR {
  constructor(options = {}) {
    this.options = {
      language: options.language || 'eng+chi_sim',
      verbose: options.verbose || false
    };
    this.worker = null;
  }

  async initialize() {
    if (!this.worker) {
      this.worker = await Tesseract.createWorker();
      await this.worker.loadLanguage(this.options.language);
      await this.worker.initialize(this.options.language);
    }
    return this.worker;
  }

  async recognize(imageBuffer) {
    await this.initialize();
    const result = await this.worker.recognize(imageBuffer, {
      logger: this.options.verbose ? m => console.log(m) : () => {}
    });
    return { text: result.data.text || '' };
  }

  async terminate() {
    if (this.worker) {
      await this.worker.terminate();
      this.worker = null;
    }
  }
}

module.exports = { HighPerformanceOCR };
