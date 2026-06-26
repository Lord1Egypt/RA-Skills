const Tesseract = require('tesseract.js');
const sharp = require('sharp');

class HighPerformanceOCR {
  constructor(options = {}) {
    this.options = {
      language: options.language || 'eng+chi_sim',
      maxImageSize: options.maxImageSize || 2000000, // 2MP
      enhance: options.enhance !== false,
      verbose: options.verbose || false
    };
    this.worker = null;
  }

  async initialize() {
    if (!this.worker) {
      this.worker = await Tesseract.createWorker(this.options.language);
    }
    return this.worker;
  }

  async recognize(imageBuffer, options = {}) {
    const startTime = Date.now();
    
    try {
      // 确保worker已初始化
      await this.initialize();
      
      // 图像预处理
      const processedBuffer = await this.preprocessImage(imageBuffer, {
        ...this.options,
        ...options
      });
      
      // OCR识别
      const result = await this.worker.recognize(processedBuffer, {
        logger: this.options.verbose ? m => console.log(m.status) : () => {}
      });
      
      const processingTime = Date.now() - startTime;
      
      if (this.options.verbose) {
        console.error(`OCR完成 - 耗时: ${processingTime}ms, 置信度: ${result.data.confidence}%`);
      }
      
      return {
        text: result.data.text || '',
        confidence: result.data.confidence || 0,
        processingTime,
        words: result.data.words || []
      };
      
    } catch (error) {
      console.error('OCR处理失败:', error.message);
      throw error;
    }
  }

  async preprocessImage(imageBuffer, options) {
    try {
      const metadata = await sharp(imageBuffer).metadata();
      const imagePixels = metadata.width * metadata.height;
      
      // 智能尺寸优化
      let resizeOptions = null;
      
      if (imagePixels > options.maxImageSize) {
        const scale = Math.sqrt(options.maxImageSize / imagePixels);
        resizeOptions = {
          width: Math.round(metadata.width * scale),
          height: Math.round(metadata.height * scale)
        };
      }
      
      // 图像处理流水线
      let pipeline = sharp(imageBuffer);
      
      if (resizeOptions) {
        pipeline = pipeline.resize(resizeOptions);
      }
      
      if (options.enhance) {
        pipeline = pipeline
          .modulate({ brightness: 1.05 })
          .normalize()
          .sharpen(0.3);
      }
      
      return pipeline
        .jpeg({ quality: 85, mozjpeg: true })
        .toBuffer();
        
    } catch (error) {
      console.error('图像预处理失败:', error.message);
      // 如果预处理失败，返回原始图像
      return imageBuffer;
    }
  }

  async terminate() {
    if (this.worker) {
      await this.worker.terminate();
      this.worker = null;
    }
  }
}

module.exports = { HighPerformanceOCR };