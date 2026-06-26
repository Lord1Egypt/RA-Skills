import type { ElementInfo, EditorState } from '../types';

export class SelectionManager {
  private state: EditorState;
  private onSelectionChange: ((selected: ElementInfo[]) => void) | null = null;

  constructor(state: EditorState) {
    this.state = state;
  }

  setOnSelectionChange(callback: (selected: ElementInfo[]) => void): void {
    this.onSelectionChange = callback;
  }

  select(id: string, addToSelection = false): void {
    if (!addToSelection) {
      this.state.selectedIds.clear();
    }
    this.state.selectedIds.add(id);
    this.updateVisualSelection();
    this.notifyChange();
  }

  deselect(id: string): void {
    this.state.selectedIds.delete(id);
    this.updateVisualSelection();
    this.notifyChange();
  }

  deselectAll(): void {
    this.state.selectedIds.clear();
    this.updateVisualSelection();
    this.notifyChange();
  }

  isSelected(id: string): boolean {
    return this.state.selectedIds.has(id);
  }

  getSelectedIds(): string[] {
    return Array.from(this.state.selectedIds);
  }

  hasSelection(): boolean {
    return this.state.selectedIds.size > 0;
  }

  private updateVisualSelection(): void {
    // Remove selection class from all elements
    document.querySelectorAll('[data-editor-id]').forEach((el) => {
      el.classList.remove('slide-editor-selected');
    });

    // Add selection class to selected elements
    this.state.selectedIds.forEach((id) => {
      const el = document.querySelector(`[data-editor-id="${id}"]`);
      if (el) {
        el.classList.add('slide-editor-selected');
      }
    });
  }

  private notifyChange(): void {
    if (this.onSelectionChange) {
      const selected = this.getSelectedIds()
        .map((id) => this.getElementInfo(id))
        .filter((el): el is ElementInfo => el !== null);
      this.onSelectionChange(selected);
    }
  }

  private getElementInfo(id: string): ElementInfo | null {
    const el = document.querySelector(`[data-editor-id="${id}"]`) as HTMLElement;
    if (!el) return null;

    const rect = el.getBoundingClientRect();
    const slideContainer = el.closest('.slide') as HTMLElement;
    const slideRect = slideContainer?.getBoundingClientRect() || { left: 0, top: 0 };

    return {
      id,
      type: this.getElementType(el),
      x: rect.left - slideRect.left,
      y: rect.top - slideRect.top,
      width: rect.width,
      height: rect.height,
      content: el.textContent || undefined,
      src: (el as HTMLImageElement).src || undefined,
      styles: this.extractStyles(el),
    };
  }

  private getElementType(el: HTMLElement): ElementInfo['type'] {
    const tagName = el.tagName.toLowerCase();
    if (tagName === 'img') return 'image';
    if (['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'div'].includes(tagName)) {
      if (el.querySelector('img')) return 'unknown';
      return 'text';
    }
    if (['rect', 'circle', 'ellipse', 'path', 'svg'].includes(tagName)) return 'shape';
    return 'unknown';
  }

  private extractStyles(el: HTMLElement): Record<string, string> {
    const computed = window.getComputedStyle(el);
    const styles: Record<string, string> = {};
    const relevantProps = [
      'fontSize', 'fontFamily', 'fontWeight', 'color', 'backgroundColor',
      'textAlign', 'lineHeight', 'opacity', 'borderRadius'
    ];
    relevantProps.forEach((prop) => {
      const value = computed.getPropertyValue(this.camelToKebab(prop));
      if (value) styles[prop] = value;
    });
    return styles;
  }

  private camelToKebab(str: string): string {
    return str.replace(/([a-z0-9])([A-Z])/g, '$1-$2').toLowerCase();
  }
}
