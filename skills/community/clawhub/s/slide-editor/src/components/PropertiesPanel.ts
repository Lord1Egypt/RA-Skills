import type { EditorAPI, ElementInfo } from '../types';
import { t } from '../i18n';

export class PropertiesPanel {
  private container: HTMLDivElement;
  private editor: EditorAPI;
  private currentElement: ElementInfo | null = null;

  constructor(editor: EditorAPI) {
    this.editor = editor;
    this.container = this.createPanel();
  }

  private createPanel(): HTMLDivElement {
    const panel = document.createElement('div');
    panel.id = 'slide-editor-properties';
    panel.innerHTML = `
      <div class="slide-editor-panel-header">${t('properties.title')}</div>
      <div class="slide-editor-panel-content">
        <div class="slide-editor-no-selection">${t('properties.noSelection')}</div>
        <div class="slide-editor-properties-form" style="display: none;">
          <div class="slide-editor-field-group">
            <label>${t('properties.position')}</label>
            <div class="slide-editor-field-row">
              <div class="slide-editor-field">
                <span class="slide-editor-field-label">X</span>
                <input type="number" id="prop-x" step="1">
              </div>
              <div class="slide-editor-field">
                <span class="slide-editor-field-label">Y</span>
                <input type="number" id="prop-y" step="1">
              </div>
            </div>
          </div>
          <div class="slide-editor-field-group">
            <label>${t('properties.size')}</label>
            <div class="slide-editor-field-row">
              <div class="slide-editor-field">
                <span class="slide-editor-field-label">W</span>
                <input type="number" id="prop-w" step="1" min="1">
              </div>
              <div class="slide-editor-field">
                <span class="slide-editor-field-label">H</span>
                <input type="number" id="prop-h" step="1" min="1">
              </div>
            </div>
          </div>
          <div class="slide-editor-field-group" id="text-properties" style="display: none;">
            <label>${t('properties.text')}</label>
            <div class="slide-editor-field">
              <span class="slide-editor-field-label">${t('properties.fontSize')}</span>
              <input type="text" id="prop-font-size" placeholder="${t('placeholder.fontSize')}">
            </div>
            <div class="slide-editor-field">
              <span class="slide-editor-field-label">${t('properties.color')}</span>
              <input type="color" id="prop-color">
            </div>
            <div class="slide-editor-field">
              <span class="slide-editor-field-label">${t('properties.fontWeight')}</span>
              <select id="prop-font-weight">
                <option value="normal">${t('properties.fontWeight.normal')}</option>
                <option value="bold">${t('properties.fontWeight.bold')}</option>
                <option value="300">${t('properties.fontWeight.light')}</option>
                <option value="600">${t('properties.fontWeight.semibold')}</option>
              </select>
            </div>
            <div class="slide-editor-field">
              <span class="slide-editor-field-label">${t('properties.textAlign')}</span>
              <select id="prop-text-align">
                <option value="left">${t('properties.textAlign.left')}</option>
                <option value="center">${t('properties.textAlign.center')}</option>
                <option value="right">${t('properties.textAlign.right')}</option>
              </select>
            </div>
          </div>
          <div class="slide-editor-field-group" id="image-properties" style="display: none;">
            <label>${t('properties.image')}</label>
            <div class="slide-editor-field">
              <button class="slide-editor-btn slide-editor-btn-full" id="prop-crop">${t('properties.cropImage')}</button>
            </div>
            <div class="slide-editor-field">
              <span class="slide-editor-field-label">${t('properties.opacity')}</span>
              <input type="range" id="prop-opacity" min="0" max="100" value="100">
            </div>
          </div>
          <div class="slide-editor-field-group">
            <div class="slide-editor-field-row">
              <button class="slide-editor-btn" id="prop-bring-front">${t('properties.bringToFront')}</button>
              <button class="slide-editor-btn" id="prop-send-back">${t('properties.sendToBack')}</button>
            </div>
          </div>
        </div>
      </div>
    `;

    this.setupEventListeners(panel);
    return panel;
  }

  private setupEventListeners(panel: HTMLElement): void {
    // Position inputs
    const xInput = panel.querySelector('#prop-x') as HTMLInputElement;
    const yInput = panel.querySelector('#prop-y') as HTMLInputElement;
    const wInput = panel.querySelector('#prop-w') as HTMLInputElement;
    const hInput = panel.querySelector('#prop-h') as HTMLInputElement;

    [xInput, yInput].forEach((input) => {
      input?.addEventListener('change', () => {
        if (this.currentElement) {
          this.editor.moveElement(
            this.currentElement.id,
            parseFloat(xInput.value) || 0,
            parseFloat(yInput.value) || 0
          );
        }
      });
    });

    [wInput, hInput].forEach((input) => {
      input?.addEventListener('change', () => {
        if (this.currentElement) {
          this.editor.resizeElement(
            this.currentElement.id,
            parseFloat(wInput.value) || 100,
            parseFloat(hInput.value) || 100
          );
        }
      });
    });

    // Text properties
    const fontSizeInput = panel.querySelector('#prop-font-size') as HTMLInputElement;
    const colorInput = panel.querySelector('#prop-color') as HTMLInputElement;
    const fontWeightSelect = panel.querySelector('#prop-font-weight') as HTMLSelectElement;
    const textAlignSelect = panel.querySelector('#prop-text-align') as HTMLSelectElement;

    fontSizeInput?.addEventListener('change', () => {
      if (this.currentElement && fontSizeInput.value.trim()) {
        // Validate font size format (e.g., "24px", "1.5em", "100%")
        const value = fontSizeInput.value.trim();
        if (/^\d+(\.\d+)?(px|em|rem|%|pt|vw|vh)?$/.test(value)) {
          this.editor.setStyle(this.currentElement.id, { fontSize: value });
        } else {
          // Restore previous value if invalid
          fontSizeInput.value = this.currentElement.styles.fontSize || '';
        }
      }
    });

    // Prevent clearing the input completely
    fontSizeInput?.addEventListener('keydown', (e) => {
      // Allow navigation keys, backspace, delete but warn if trying to clear
      if (e.key === 'Enter') {
        e.preventDefault();
        fontSizeInput.blur();
      }
    });

    colorInput?.addEventListener('input', () => {
      if (this.currentElement && colorInput.value) {
        this.editor.setStyle(this.currentElement.id, { color: colorInput.value });
      }
    });

    fontWeightSelect?.addEventListener('change', () => {
      if (this.currentElement) {
        this.editor.setStyle(this.currentElement.id, { fontWeight: fontWeightSelect.value });
      }
    });

    textAlignSelect?.addEventListener('change', () => {
      if (this.currentElement) {
        this.editor.setStyle(this.currentElement.id, { textAlign: textAlignSelect.value });
      }
    });

    // Image properties
    const opacityInput = panel.querySelector('#prop-opacity') as HTMLInputElement;
    opacityInput?.addEventListener('input', () => {
      if (this.currentElement) {
        const opacity = parseFloat(opacityInput.value) / 100;
        this.editor.setStyle(this.currentElement.id, { opacity: opacity.toString() });
      }
    });

    // Crop button
    panel.querySelector('#prop-crop')?.addEventListener('click', () => {
      if (this.currentElement && this.currentElement.type === 'image') {
        this.editor.startCropImage(this.currentElement.id);
      }
    });

    // Layer controls
    panel.querySelector('#prop-bring-front')?.addEventListener('click', () => {
      if (this.currentElement) {
        this.editor.bringToFront(this.currentElement.id);
      }
    });

    panel.querySelector('#prop-send-back')?.addEventListener('click', () => {
      if (this.currentElement) {
        this.editor.sendToBack(this.currentElement.id);
      }
    });
  }

  mount(parent: HTMLElement): void {
    parent.appendChild(this.container);
  }

  unmount(): void {
    this.container.remove();
  }

  refreshLocale(): void {
    // Re-render the panel with new locale
    const parent = this.container.parentElement;
    const currentElement = this.currentElement;
    this.container.remove();
    this.container = this.createPanel();
    if (parent) {
      parent.appendChild(this.container);
    }
    // Restore selection state
    this.updateSelection(currentElement);
  }

  updateSelection(element: ElementInfo | null): void {
    this.currentElement = element;
    const noSelection = this.container.querySelector('.slide-editor-no-selection');
    const form = this.container.querySelector('.slide-editor-properties-form') as HTMLElement;
    const textProps = this.container.querySelector('#text-properties') as HTMLElement;
    const imageProps = this.container.querySelector('#image-properties') as HTMLElement;

    if (!element) {
      noSelection?.classList.remove('slide-editor-hidden');
      form.style.display = 'none';
      return;
    }

    noSelection?.classList.add('slide-editor-hidden');
    form.style.display = 'block';

    // Update position
    (this.container.querySelector('#prop-x') as HTMLInputElement).value = Math.round(element.x).toString();
    (this.container.querySelector('#prop-y') as HTMLInputElement).value = Math.round(element.y).toString();
    (this.container.querySelector('#prop-w') as HTMLInputElement).value = Math.round(element.width).toString();
    (this.container.querySelector('#prop-h') as HTMLInputElement).value = Math.round(element.height).toString();

    // Show/hide type-specific properties
    textProps.style.display = element.type === 'text' ? 'block' : 'none';
    imageProps.style.display = element.type === 'image' ? 'block' : 'none';

    // Update text properties
    if (element.type === 'text') {
      const fontSize = element.styles.fontSize || '';
      const fontWeight = element.styles.fontWeight || 'normal';
      const textAlign = element.styles.textAlign || 'left';
      const color = this.normalizeColor(element.styles.color);

      (this.container.querySelector('#prop-font-size') as HTMLInputElement).value = fontSize;
      (this.container.querySelector('#prop-color') as HTMLInputElement).value = color;
      (this.container.querySelector('#prop-font-weight') as HTMLSelectElement).value = fontWeight;
      (this.container.querySelector('#prop-text-align') as HTMLSelectElement).value = textAlign;
    }

    // Update image properties
    if (element.type === 'image') {
      const opacity = parseFloat(element.styles.opacity || '1') * 100;
      (this.container.querySelector('#prop-opacity') as HTMLInputElement).value = opacity.toString();
    }
  }

  private normalizeColor(color: string | undefined): string {
    if (!color) return '#333333';

    // Already hex
    if (color.startsWith('#')) {
      // Ensure 6-digit format
      if (color.length === 4) {
        // Convert #RGB to #RRGGBB
        return `#${color[1]}${color[1]}${color[2]}${color[2]}${color[3]}${color[3]}`;
      }
      return color;
    }

    // RGB format
    const match = color.match(/rgb\((\d+),\s*(\d+),\s*(\d+)\)/);
    if (match) {
      const r = parseInt(match[1]).toString(16).padStart(2, '0');
      const g = parseInt(match[2]).toString(16).padStart(2, '0');
      const b = parseInt(match[3]).toString(16).padStart(2, '0');
      return `#${r}${g}${b}`;
    }

    // RGBA format
    const rgbaMatch = color.match(/rgba\((\d+),\s*(\d+),\s*(\d+),\s*[\d.]+\)/);
    if (rgbaMatch) {
      const r = parseInt(rgbaMatch[1]).toString(16).padStart(2, '0');
      const g = parseInt(rgbaMatch[2]).toString(16).padStart(2, '0');
      const b = parseInt(rgbaMatch[3]).toString(16).padStart(2, '0');
      return `#${r}${g}${b}`;
    }

    // Named colors or CSS variables - return a default
    return '#333333';
  }

  private rgbToHex(color: string): string {
    return this.normalizeColor(color);
  }
}
