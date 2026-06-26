import type { EditorState, HistoryAction, HandlePosition, ResizeHandle } from '../types';

export class ResizeManager {
  private state: EditorState;
  private historyPush: (action: HistoryAction) => void;
  private handles: Map<string, ResizeHandle[]> = new Map();
  private isResizing = false;
  private activeHandle: HandlePosition | null = null;
  private resizeTarget: string | null = null;
  private startX = 0;
  private startY = 0;
  private startWidth = 0;
  private startHeight = 0;
  private startLeft = 0;
  private startTop = 0;
  private onResizeEnd: (() => void) | null = null;

  private readonly cursors: Record<HandlePosition, string> = {
    nw: 'nwse-resize',
    n: 'ns-resize',
    ne: 'nesw-resize',
    e: 'ew-resize',
    se: 'nwse-resize',
    s: 'ns-resize',
    sw: 'nesw-resize',
    w: 'ew-resize',
  };

  constructor(state: EditorState, historyPush: (action: HistoryAction) => void) {
    this.state = state;
    this.historyPush = historyPush;
  }

  setOnResizeEnd(callback: () => void): void {
    this.onResizeEnd = callback;
  }

  createHandles(elementId: string): void {
    this.removeHandles(elementId);

    const el = document.querySelector(`[data-editor-id="${elementId}"]`) as HTMLElement;
    if (!el) return;

    // Ensure parent has position relative for absolute positioning of handles
    const parent = el.parentElement;
    if (parent && getComputedStyle(parent).position === 'static') {
      parent.style.position = 'relative';
    }

    const positions: HandlePosition[] = ['nw', 'n', 'ne', 'e', 'se', 's', 'sw', 'w'];
    const handles: ResizeHandle[] = [];

    positions.forEach((pos) => {
      const handle = document.createElement('div');
      handle.className = 'slide-editor-resize-handle';
      handle.dataset.handlePosition = pos;
      handle.style.cssText = `
        position: absolute;
        width: 10px;
        height: 10px;
        background: white;
        border: 2px solid var(--editor-accent, #00ffcc);
        border-radius: 2px;
        cursor: ${this.cursors[pos]};
        z-index: 10000;
        pointer-events: auto;
      `;

      this.positionHandle(handle, pos, el);
      handle.addEventListener('pointerdown', (e) => this.startResize(e, elementId, pos));

      el.parentElement?.appendChild(handle);
      handles.push({ position: pos, element: handle, cursor: this.cursors[pos] });
    });

    this.handles.set(elementId, handles);
  }

  removeHandles(elementId: string): void {
    const handles = this.handles.get(elementId);
    if (handles) {
      handles.forEach((h) => h.element.remove());
      this.handles.delete(elementId);
    }
  }

  removeAllHandles(): void {
    this.handles.forEach((handles) => {
      handles.forEach((h) => h.element.remove());
    });
    this.handles.clear();
  }

  updateHandlePositions(elementId: string): void {
    const handles = this.handles.get(elementId);
    const el = document.querySelector(`[data-editor-id="${elementId}"]`) as HTMLElement;
    if (handles && el) {
      handles.forEach((h) => this.positionHandle(h.element, h.position, el));
    }
  }

  private positionHandle(handle: HTMLDivElement, pos: HandlePosition, el: HTMLElement): void {
    const rect = el.getBoundingClientRect();
    const parentRect = el.parentElement?.getBoundingClientRect() || { left: 0, top: 0 };

    const left = rect.left - parentRect.left;
    const top = rect.top - parentRect.top;
    const width = rect.width;
    const height = rect.height;

    const halfHandle = 5;

    switch (pos) {
      case 'nw':
        handle.style.left = `${left - halfHandle}px`;
        handle.style.top = `${top - halfHandle}px`;
        break;
      case 'n':
        handle.style.left = `${left + width / 2 - halfHandle}px`;
        handle.style.top = `${top - halfHandle}px`;
        break;
      case 'ne':
        handle.style.left = `${left + width - halfHandle}px`;
        handle.style.top = `${top - halfHandle}px`;
        break;
      case 'e':
        handle.style.left = `${left + width - halfHandle}px`;
        handle.style.top = `${top + height / 2 - halfHandle}px`;
        break;
      case 'se':
        handle.style.left = `${left + width - halfHandle}px`;
        handle.style.top = `${top + height - halfHandle}px`;
        break;
      case 's':
        handle.style.left = `${left + width / 2 - halfHandle}px`;
        handle.style.top = `${top + height - halfHandle}px`;
        break;
      case 'sw':
        handle.style.left = `${left - halfHandle}px`;
        handle.style.top = `${top + height - halfHandle}px`;
        break;
      case 'w':
        handle.style.left = `${left - halfHandle}px`;
        handle.style.top = `${top + height / 2 - halfHandle}px`;
        break;
    }
  }

  private startResize(e: PointerEvent, elementId: string, pos: HandlePosition): void {
    e.preventDefault();
    e.stopPropagation();

    this.isResizing = true;
    this.activeHandle = pos;
    this.resizeTarget = elementId;

    const el = document.querySelector(`[data-editor-id="${elementId}"]`) as HTMLElement;
    if (!el) return;

    this.startX = e.clientX;
    this.startY = e.clientY;
    this.startWidth = el.offsetWidth;
    this.startHeight = el.offsetHeight;

    // Use parsed style values instead of offsetLeft/offsetTop
    // This ensures we get the actual CSS position, not the offsetParent-relative position
    this.startLeft = parseFloat(el.style.left) || 0;
    this.startTop = parseFloat(el.style.top) || 0;

    (e.target as HTMLElement).setPointerCapture(e.pointerId);
  }

  handleMove(e: PointerEvent): void {
    if (!this.isResizing || !this.resizeTarget || !this.activeHandle) return;

    const el = document.querySelector(`[data-editor-id="${this.resizeTarget}"]`) as HTMLElement;
    if (!el) return;

    const deltaX = e.clientX - this.startX;
    const deltaY = e.clientY - this.startY;

    let newWidth = this.startWidth;
    let newHeight = this.startHeight;
    let newLeft = this.startLeft;
    let newTop = this.startTop;

    // Calculate new dimensions based on handle position
    if (this.activeHandle.includes('e')) {
      newWidth = Math.max(20, this.startWidth + deltaX);
    }
    if (this.activeHandle.includes('w')) {
      newWidth = Math.max(20, this.startWidth - deltaX);
      newLeft = this.startLeft + (this.startWidth - newWidth);
    }
    if (this.activeHandle.includes('s')) {
      newHeight = Math.max(20, this.startHeight + deltaY);
    }
    if (this.activeHandle.includes('n')) {
      newHeight = Math.max(20, this.startHeight - deltaY);
      newTop = this.startTop + (this.startHeight - newHeight);
    }

    el.style.width = `${newWidth}px`;
    // Only set height for images or elements that already have explicit height
    if (el.tagName.toLowerCase() === 'img' || el.style.height) {
      el.style.height = `${newHeight}px`;
    }
    el.style.left = `${newLeft}px`;
    el.style.top = `${newTop}px`;

    // Update handle positions
    this.updateHandlePositions(this.resizeTarget);
  }

  endResize(): void {
    if (!this.isResizing || !this.resizeTarget) return;

    const el = document.querySelector(`[data-editor-id="${this.resizeTarget}"]`) as HTMLElement;
    if (el) {
      this.historyPush({
        type: 'resize',
        elementId: this.resizeTarget,
        from: {
          width: this.startWidth,
          height: this.startHeight,
          x: this.startLeft,
          y: this.startTop,
        },
        to: {
          width: el.offsetWidth,
          height: el.offsetHeight,
          x: el.offsetLeft,
          y: el.offsetTop,
        },
      });
    }

    this.isResizing = false;
    this.activeHandle = null;
    this.resizeTarget = null;

    if (this.onResizeEnd) {
      this.onResizeEnd();
    }
  }

  isActive(): boolean {
    return this.isResizing;
  }
}
