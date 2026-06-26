import type { EditorState, HistoryAction } from '../types';

export class TextEditor {
  private state: EditorState;
  private historyPush: (action: HistoryAction) => void;
  private activeElement: string | null = null;
  private originalContent = '';
  private onEditEnd: (() => void) | null = null;

  constructor(state: EditorState, historyPush: (action: HistoryAction) => void) {
    this.state = state;
    this.historyPush = historyPush;
  }

  setOnEditEnd(callback: () => void): void {
    this.onEditEnd = callback;
  }

  startEditing(elementId: string): void {
    const el = document.querySelector(`[data-editor-id="${elementId}"]`) as HTMLElement;
    if (!el) return;

    // Don't edit non-text elements
    if (el.tagName.toLowerCase() === 'img') return;

    this.activeElement = elementId;
    this.originalContent = el.innerHTML;

    // Make editable
    el.contentEditable = 'true';
    el.classList.add('slide-editor-editing');
    el.focus();

    // Select all text
    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(el);
    selection?.removeAllRanges();
    selection?.addRange(range);

    // Listen for blur to save
    el.addEventListener('blur', this.handleBlur);
    el.addEventListener('keydown', this.handleKeydown);
  }

  endEditing(save = true): void {
    if (!this.activeElement) return;

    const activeId = this.activeElement; // Store before clearing
    const el = document.querySelector(`[data-editor-id="${activeId}"]`) as HTMLElement;
    if (!el) {
      this.activeElement = null;
      return;
    }

    el.removeEventListener('blur', this.handleBlur);
    el.removeEventListener('keydown', this.handleKeydown);

    const newContent = el.innerHTML;
    el.contentEditable = 'false';
    el.classList.remove('slide-editor-editing');

    if (save && newContent !== this.originalContent) {
      this.historyPush({
        type: 'text',
        elementId: activeId,
        from: this.originalContent,
        to: newContent,
      });
    } else if (!save) {
      el.innerHTML = this.originalContent;
    }

    this.activeElement = null;
    this.originalContent = '';

    if (this.onEditEnd) {
      this.onEditEnd();
    }
  }

  isEditing(): boolean {
    return this.activeElement !== null;
  }

  getActiveElement(): string | null {
    return this.activeElement;
  }

  private handleBlur = (): void => {
    this.endEditing(true);
  };

  private handleKeydown = (e: KeyboardEvent): void => {
    if (e.key === 'Escape') {
      this.endEditing(false);
    } else if (e.key === 'Enter' && !e.shiftKey) {
      // For single-line elements, blur on Enter
      const el = document.querySelector(`[data-editor-id="${this.activeElement}"]`) as HTMLElement;
      if (el && !this.isMultiline(el)) {
        e.preventDefault();
        el.blur();
      }
    }
  };

  private isMultiline(el: HTMLElement): boolean {
    const tag = el.tagName.toLowerCase();
    return ['p', 'div', 'li', 'td', 'th'].includes(tag) || el.style.whiteSpace === 'pre-wrap';
  }
}
