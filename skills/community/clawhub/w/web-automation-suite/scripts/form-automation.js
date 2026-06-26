/**
 * 表单自动化辅助工具
 * 支持批量填充、自动提交、文件上传
 */

/**
 * 填充表单
 * @param {Page} page - Playwright页面实例
 * @param {object} formData - 表单数据 {selector: value}
 * @param {object} options - 选项
 */
async function fillForm(page, formData, options = {}) {
  const { delay = 50, clearFirst = true } = options;

  for (const [selector, value] of Object.entries(formData)) {
    try {
      const el = await page.waitForSelector(selector, { timeout: 5000 });

      if (clearFirst) {
        await el.clear();
      }

      const tagName = await el.evaluate(e => e.tagName.toLowerCase());
      const type = await el.evaluate(e => e.type || '');

      if (tagName === 'select') {
        await page.selectOption(selector, value);
      } else if (type === 'checkbox') {
        if (value) await el.check();
        else await el.uncheck();
      } else if (type === 'radio') {
        await page.check(selector);
      } else if (tagName === 'input' && type === 'file') {
        await page.setInputFiles(selector, value);
      } else {
        await page.fill(selector, String(value));
      }

      if (delay > 0) {
        await page.waitForTimeout(delay);
      }
    } catch (e) {
      console.warn(`Warning: Could not fill ${selector}: ${e.message}`);
    }
  }
}

/**
 * 提交表单
 * @param {Page} page - Playwright页面实例
 * @param {string} submitSelector - 提交按钮选择器
 * @param {object} options - 选项
 */
async function submitForm(page, submitSelector = 'button[type="submit"]', options = {}) {
  const { waitForNavigation = true, timeout = 30000 } = options;

  if (waitForNavigation) {
    await Promise.all([
      page.waitForNavigation({ timeout }),
      page.click(submitSelector)
    ]);
  } else {
    await page.click(submitSelector);
  }
}

/**
 * 批量发布到多个平台
 * @param {Page} page - Playwright页面实例
 * @param {Array} targets - 发布目标 [{url, titleSelector, contentSelector, submitSelector}]
 * @param {object} data - 要发布的内容
 */
async function batchPost(page, targets, data) {
  const results = [];

  for (const target of targets) {
    try {
      await page.goto(target.url, { waitUntil: 'networkidle' });

      if (target.titleSelector) {
        await page.fill(target.titleSelector, data.title || '');
      }
      if (target.contentSelector) {
        await page.fill(target.contentSelector, data.content || '');
      }

      await page.waitForTimeout(500);
      await page.click(target.submitSelector);

      results.push({ url: target.url, success: true });
    } catch (e) {
      results.push({ url: target.url, success: false, error: e.message });
    }

    await page.waitForTimeout(1000);
  }

  return results;
}

/**
 * 文件上传（支持拖拽）
 * @param {Page} page - Playwright页面实例
 * @param {string} inputSelector - 文件输入选择器
 * @param {string|string[]} files - 文件路径
 */
async function uploadFile(page, inputSelector, files) {
  const fileArray = Array.isArray(files) ? files : [files];
  await page.setInputFiles(inputSelector, fileArray);
}

/**
 * 处理多步骤表单（如向导式）
 * @param {Page} page - Playwright页面实例
 * @param {Array} steps - 步骤配置 [{formData, nextButton, validate?}]
 * @param {Function} finalSubmit - 最终提交函数
 */
async function processMultiStepForm(page, steps, finalSubmit) {
  for (let i = 0; i < steps.length; i++) {
    const step = steps[i];

    // 填充当前步骤表单
    if (step.formData) {
      await fillForm(page, step.formData);
    }

    // 验证（如提供）
    if (step.validate) {
      const isValid = await step.validate(page);
      if (!isValid) {
        throw new Error(`Validation failed at step ${i + 1}`);
      }
    }

    // 点击下一步
    if (i < steps.length - 1 && step.nextButton) {
      await page.click(step.nextButton);
      await page.waitForLoadState('networkidle');
    }
  }

  // 执行最终提交
  if (finalSubmit) {
    await finalSubmit(page);
  }
}

module.exports = {
  fillForm,
  submitForm,
  batchPost,
  uploadFile,
  processMultiStepForm
};
