import type { EditorAPI } from '../types';
import { t, getLocale, setLocale, type Locale } from '../i18n';

export class Toolbar {
  private container: HTMLDivElement;
  private editor: EditorAPI;
  private onExport: () => void;
  private onAddText: () => void;
  private onAddImage: () => void;
  private onTogglePanel: () => void;
  private onToggleTheme: () => void;
  private onLocaleChange: ((locale: Locale) => void) | null = null;
  private isDarkMode = true;

  constructor(editor: EditorAPI, callbacks: {
    onExport: () => void;
    onAddText: () => void;
    onAddImage: () => void;
    onTogglePanel: () => void;
    onToggleTheme: () => void;
  }) {
    this.editor = editor;
    this.onExport = callbacks.onExport;
    this.onAddText = callbacks.onAddText;
    this.onAddImage = callbacks.onAddImage;
    this.onTogglePanel = callbacks.onTogglePanel;
    this.onToggleTheme = callbacks.onToggleTheme;
    this.container = this.createToolbar();
  }

  setOnLocaleChange(callback: (locale: Locale) => void): void {
    this.onLocaleChange = callback;
  }

  private createToolbar(): HTMLDivElement {
    const toolbar = document.createElement('div');
    toolbar.id = 'slide-editor-toolbar';
    toolbar.innerHTML = `
      <div class="slide-editor-toolbar-group">
        <button class="slide-editor-btn" data-action="add-text" title="Add Text">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 7V4h16v3M9 20h6M12 4v16"/>
          </svg>
        </button>
        <button class="slide-editor-btn" data-action="add-image" title="Add Image">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="18" height="18" rx="2"/>
            <circle cx="8.5" cy="8.5" r="1.5"/>
            <path d="M21 15l-5-5L5 21"/>
          </svg>
        </button>
      </div>
      <div class="slide-editor-toolbar-group">
        <button class="slide-editor-btn" data-action="delete" title="Delete">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/>
          </svg>
        </button>
      </div>
      <div class="slide-editor-toolbar-group">
        <button class="slide-editor-btn" data-action="undo" title="Undo (Ctrl+Z)">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 7v6h6M3 13c0-4.97 4.03-9 9-9a9 9 0 019 9 9 9 0 01-9 9c-2.5 0-4.74-1-6.4-2.6"/>
          </svg>
        </button>
        <button class="slide-editor-btn" data-action="redo" title="Redo (Ctrl+Shift+Z)">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 7v6h-6M21 13c0-4.97-4.03-9-9-9a9 9 0 00-9 9 9 9 0 009 9c2.5 0 4.74-1 6.4-2.6"/>
          </svg>
        </button>
      </div>
      <div class="slide-editor-toolbar-spacer"></div>
      <div class="slide-editor-toolbar-group">
        <button class="slide-editor-btn" data-action="toggle-theme" title="Toggle Dark/Light Mode (T)">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="theme-icon-dark">
            <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/>
          </svg>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="theme-icon-light" style="display:none;">
            <circle cx="12" cy="12" r="5"/>
            <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
          </svg>
        </button>
        <button class="slide-editor-btn" data-action="toggle-panel" title="Toggle Properties Panel (P)">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="18" height="18" rx="2"/>
            <path d="M9 3v18"/>
          </svg>
        </button>
        <button class="slide-editor-btn slide-editor-lang-btn" data-action="toggle-lang" title="${t('toolbar.switchLang')}">
          <span class="lang-label">${getLocale() === 'zh' ? '中' : 'EN'}</span>
        </button>
      </div>
      <div class="slide-editor-toolbar-group">
        <button class="slide-editor-btn slide-editor-btn-primary" data-action="export" title="${t('toolbar.export')}">
          ${t('toolbar.export')}
        </button>
      </div>
    `;

    toolbar.addEventListener('click', (e) => {
      const target = (e.target as HTMLElement).closest('[data-action]') as HTMLElement;
      if (!target) return;

      const action = target.dataset.action;
      switch (action) {
        case 'add-text':
          this.onAddText();
          break;
        case 'add-image':
          this.onAddImage();
          break;
        case 'delete':
          this.editor.deleteSelected();
          break;
        case 'undo':
          this.editor.undo();
          break;
        case 'redo':
          this.editor.redo();
          break;
        case 'toggle-panel':
          this.onTogglePanel();
          break;
        case 'toggle-theme':
          this.toggleThemeIcon();
          this.onToggleTheme();
          break;
        case 'toggle-lang':
          this.toggleLanguage();
          break;
        case 'export':
          this.onExport();
          break;
      }
    });

    return toolbar;
  }

  private toggleThemeIcon(): void {
    this.isDarkMode = !this.isDarkMode;
    const darkIcon = this.container.querySelector('.theme-icon-dark');
    const lightIcon = this.container.querySelector('.theme-icon-light');
    if (darkIcon && lightIcon) {
      (darkIcon as HTMLElement).style.display = this.isDarkMode ? 'block' : 'none';
      (lightIcon as HTMLElement).style.display = this.isDarkMode ? 'none' : 'block';
    }
  }

  private toggleLanguage(): void {
    const newLocale: Locale = getLocale() === 'zh' ? 'en' : 'zh';
    setLocale(newLocale);

    // Update button label
    const langLabel = this.container.querySelector('.lang-label');
    if (langLabel) {
      langLabel.textContent = newLocale === 'zh' ? '中' : 'EN';
    }

    // Update export button text
    const exportBtn = this.container.querySelector('[data-action="export"]');
    if (exportBtn) {
      exportBtn.textContent = t('toolbar.export');
    }

    // Notify callback to refresh other components
    if (this.onLocaleChange) {
      this.onLocaleChange(newLocale);
    }
  }

  mount(parent: HTMLElement): void {
    parent.appendChild(this.container);
    // Update export button text with current locale
    const exportBtn = this.container.querySelector('[data-action="export"]');
    if (exportBtn) {
      exportBtn.textContent = t('toolbar.export');
    }
  }

  unmount(): void {
    this.container.remove();
  }

  updateUndoRedoState(): void {
    const undoBtn = this.container.querySelector('[data-action="undo"]');
    const redoBtn = this.container.querySelector('[data-action="redo"]');

    if (undoBtn) {
      (undoBtn as HTMLButtonElement).disabled = !this.editor.canUndo();
      undoBtn.classList.toggle('slide-editor-btn-disabled', !this.editor.canUndo());
    }
    if (redoBtn) {
      (redoBtn as HTMLButtonElement).disabled = !this.editor.canRedo();
      redoBtn.classList.toggle('slide-editor-btn-disabled', !this.editor.canRedo());
    }
  }
}
