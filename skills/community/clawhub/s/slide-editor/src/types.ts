// Core types for the slide editor

export interface SlideInfo {
  index: number;
  id: string;
  elements: ElementInfo[];
}

export interface ElementInfo {
  id: string;
  type: 'text' | 'image' | 'shape' | 'unknown';
  x: number;
  y: number;
  width: number;
  height: number;
  content?: string;
  src?: string;
  styles: Record<string, string>;
}

export interface TextOptions {
  x?: number;
  y?: number;
  width?: number;
  height?: number;
  content?: string;
  fontSize?: string;
  color?: string;
  fontWeight?: string;
  textAlign?: 'left' | 'center' | 'right';
}

export interface ImageOptions {
  x?: number;
  y?: number;
  width?: number;
  height?: number;
  src: string;
  alt?: string;
}

export interface CropRect {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface HistoryAction {
  type: 'move' | 'resize' | 'text' | 'style' | 'add' | 'delete' | 'crop' | 'slide';
  elementId?: string;
  slideIndex?: number;
  from?: unknown;
  to?: unknown;
}

export interface EditorState {
  enabled: boolean;
  selectedIds: Set<string>;
  currentSlideIndex: number;
  historyStack: HistoryAction[];
  historyIndex: number;
}

// Editor API interface - exposed as window.__openclawEditor
export interface EditorAPI {
  // Mode control
  enable(): void;
  disable(): void;
  isEnabled(): boolean;

  // Query
  getSlides(): SlideInfo[];
  getSelectedElement(): ElementInfo | null;
  getSelectedElements(): ElementInfo[];
  getElementAt(x: number, y: number): ElementInfo | null;
  getElementById(id: string): ElementInfo | null;

  // Slide operations
  addSlide(index?: number): SlideInfo;
  deleteSlide(index: number): void;
  moveSlide(from: number, to: number): void;
  duplicateSlide(index: number): SlideInfo;
  getCurrentSlide(): SlideInfo | null;
  setCurrentSlide(index: number): void;

  // Element operations
  addText(options: TextOptions): ElementInfo;
  addImage(options: ImageOptions): ElementInfo;
  deleteElement(id: string): void;
  deleteSelected(): void;
  moveElement(id: string, x: number, y: number): void;
  resizeElement(id: string, width: number, height: number): void;
  setTextContent(id: string, content: string): void;
  setStyle(id: string, styles: Record<string, string>): void;
  cropImage(id: string, rect: CropRect): void;
  startCropImage(id: string): void;
  bringToFront(id: string): void;
  sendToBack(id: string): void;

  // Selection
  selectElement(id: string, addToSelection?: boolean): void;
  deselectAll(): void;

  // History
  undo(): void;
  redo(): void;
  canUndo(): boolean;
  canRedo(): boolean;

  // Export
  export(): string;
  exportWithEditor(): string;
}

// Resize handle positions
export type HandlePosition = 'nw' | 'n' | 'ne' | 'e' | 'se' | 's' | 'sw' | 'w';

export interface ResizeHandle {
  position: HandlePosition;
  element: HTMLDivElement;
  cursor?: string;
}
