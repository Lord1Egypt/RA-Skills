// Internationalization support
export type Locale = 'en' | 'zh';

// Auto-detect locale on module load
function initLocale(): Locale {
  if (typeof navigator !== 'undefined') {
    const lang = navigator.language.toLowerCase();
    if (lang.startsWith('zh')) {
      return 'zh';
    }
  }
  return 'en';
}

let currentLocale: Locale = initLocale();

const translations: Record<Locale, Record<string, string>> = {
  en: {
    // Properties Panel
    'properties.title': 'Properties',
    'properties.noSelection': 'Select an element to edit',
    'properties.position': 'Position',
    'properties.size': 'Size',
    'properties.text': 'Text',
    'properties.fontSize': 'Font Size',
    'properties.color': 'Color',
    'properties.fontWeight': 'Weight',
    'properties.fontWeight.normal': 'Normal',
    'properties.fontWeight.bold': 'Bold',
    'properties.fontWeight.light': 'Light',
    'properties.fontWeight.semibold': 'Semi-Bold',
    'properties.textAlign': 'Align',
    'properties.textAlign.left': 'Left',
    'properties.textAlign.center': 'Center',
    'properties.textAlign.right': 'Right',
    'properties.image': 'Image',
    'properties.cropImage': 'Crop Image',
    'properties.opacity': 'Opacity',
    'properties.bringToFront': 'Bring to Front',
    'properties.sendToBack': 'Send to Back',

    // Toolbar
    'toolbar.addText': 'Add Text',
    'toolbar.addImage': 'Add Image',
    'toolbar.delete': 'Delete',
    'toolbar.undo': 'Undo (Ctrl+Z)',
    'toolbar.redo': 'Redo (Ctrl+Shift+Z)',
    'toolbar.toggleTheme': 'Toggle Dark/Light Mode (T)',
    'toolbar.togglePanel': 'Toggle Properties Panel (P)',
    'toolbar.export': 'Export',
    'toolbar.switchLang': 'Switch Language',

    // Slide Navigator
    'navigator.addSlide': 'Add Slide',
    'navigator.duplicateSlide': 'Duplicate Slide',
    'navigator.deleteSlide': 'Delete Slide',
    'navigator.elements': 'elements',
    'navigator.element': 'element',

    // Placeholder
    'placeholder.fontSize': 'e.g. 24px',
  },
  zh: {
    // Properties Panel
    'properties.title': '属性',
    'properties.noSelection': '选择一个元素进行编辑',
    'properties.position': '位置',
    'properties.size': '大小',
    'properties.text': '文字',
    'properties.fontSize': '字体大小',
    'properties.color': '颜色',
    'properties.fontWeight': '粗细',
    'properties.fontWeight.normal': '正常',
    'properties.fontWeight.bold': '粗体',
    'properties.fontWeight.light': '细体',
    'properties.fontWeight.semibold': '半粗',
    'properties.textAlign': '对齐',
    'properties.textAlign.left': '左对齐',
    'properties.textAlign.center': '居中',
    'properties.textAlign.right': '右对齐',
    'properties.image': '图片',
    'properties.cropImage': '裁剪图片',
    'properties.opacity': '不透明度',
    'properties.bringToFront': '移到最前',
    'properties.sendToBack': '移到最后',

    // Toolbar
    'toolbar.addText': '添加文字',
    'toolbar.addImage': '添加图片',
    'toolbar.delete': '删除',
    'toolbar.undo': '撤销 (Ctrl+Z)',
    'toolbar.redo': '重做 (Ctrl+Shift+Z)',
    'toolbar.toggleTheme': '切换深色/浅色模式',
    'toolbar.togglePanel': '切换属性面板',
    'toolbar.export': '导出',
    'toolbar.switchLang': '切换语言',

    // Slide Navigator
    'navigator.addSlide': '添加幻灯片',
    'navigator.duplicateSlide': '复制幻灯片',
    'navigator.deleteSlide': '删除幻灯片',
    'navigator.elements': '个元素',
    'navigator.element': '个元素',

    // Placeholder
    'placeholder.fontSize': '如 24px',
  }
};

export function setLocale(locale: Locale): void {
  currentLocale = locale;
}

export function getLocale(): Locale {
  return currentLocale;
}

export function t(key: string, params?: Record<string, string>): string {
  let text = translations[currentLocale][key] || translations['en'][key] || key;

  if (params) {
    Object.entries(params).forEach(([k, v]) => {
      text = text.replace(`{${k}}`, v);
    });
  }

  return text;
}

// Detect browser locale
export function detectLocale(): Locale {
  return initLocale();
}
