import type { EditorState, HistoryAction } from '../types';

export class DragManager {
  private state: EditorState;
  private isDragging = false;
  private dragStartX = 0;
  private dragStartY = 0;
  private elementStartPositions: Map<string, { x: number; y: number }> = new Map();
  private historyPush: (action: HistoryAction) => void;
  private onDragEnd: (() => void) | null = null;

  constructor(state: EditorState, historyPush: (action: HistoryAction) => void) {
    this.state = state;
    this.historyPush = historyPush;
  }

  setOnDragEnd(callback: () => void): void {
    this.onDragEnd = callback;
  }

  startDrag(e: PointerEvent, elementId: string): void {
    if (!this.state.selectedIds.has(elementId)) return;

    this.isDragging = true;
    this.dragStartX = e.clientX;
    this.dragStartY = e.clientY;
    this.elementStartPositions.clear();

    // Store starting positions of all selected elements
    this.state.selectedIds.forEach((id) => {
      const el = document.querySelector(`[data-editor-id="${id}"]`) as HTMLElement;
      if (el) {
        this.elementStartPositions.set(id, {
          x: parseFloat(el.style.left) || el.offsetLeft,
          y: parseFloat(el.style.top) || el.offsetTop,
        });
      }
    });

    // Capture pointer
    const target = e.target as HTMLElement;
    target.setPointerCapture(e.pointerId);

    e.preventDefault();
    e.stopPropagation();
  }

  handleMove(e: PointerEvent): void {
    if (!this.isDragging) return;

    const deltaX = e.clientX - this.dragStartX;
    const deltaY = e.clientY - this.dragStartY;

    // Move all selected elements
    this.elementStartPositions.forEach((startPos, id) => {
      const el = document.querySelector(`[data-editor-id="${id}"]`) as HTMLElement;
      if (el) {
        const newX = startPos.x + deltaX;
        const newY = startPos.y + deltaY;
        el.style.left = `${newX}px`;
        el.style.top = `${newY}px`;
      }
    });
  }

  endDrag(e: PointerEvent): void {
    if (!this.isDragging) return;

    const deltaX = e.clientX - this.dragStartX;
    const deltaY = e.clientY - this.dragStartY;

    // Only record history if there was actual movement
    if (Math.abs(deltaX) > 2 || Math.abs(deltaY) > 2) {
      // Record history for each moved element
      this.elementStartPositions.forEach((startPos, id) => {
        const el = document.querySelector(`[data-editor-id="${id}"]`) as HTMLElement;
        if (el) {
          this.historyPush({
            type: 'move',
            elementId: id,
            from: { x: startPos.x, y: startPos.y },
            to: { x: startPos.x + deltaX, y: startPos.y + deltaY },
          });
        }
      });
    }

    this.isDragging = false;
    this.elementStartPositions.clear();

    if (this.onDragEnd) {
      this.onDragEnd();
    }
  }

  isActive(): boolean {
    return this.isDragging;
  }
}
