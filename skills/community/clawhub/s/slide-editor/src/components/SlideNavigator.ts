import type { EditorAPI, SlideInfo } from '../types';
import { t } from '../i18n';

export class SlideNavigator {
  private container: HTMLDivElement;
  private editor: EditorAPI;
  private thumbnails: Map<number, HTMLDivElement> = new Map();
  private onSlideChange: ((index: number) => void) | null = null;

  constructor(editor: EditorAPI) {
    this.editor = editor;
    this.container = this.createNavigator();
  }

  setOnSlideChange(callback: (index: number) => void): void {
    this.onSlideChange = callback;
  }

  private createNavigator(): HTMLDivElement {
    const nav = document.createElement('div');
    nav.id = 'slide-editor-navigator';
    nav.innerHTML = `
      <div class="slide-editor-nav-controls">
        <button class="slide-editor-btn slide-editor-nav-btn" id="nav-add-slide" title="${t('navigator.addSlide')}">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
        </button>
        <button class="slide-editor-btn slide-editor-nav-btn" id="nav-duplicate-slide" title="${t('navigator.duplicateSlide')}">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <rect x="9" y="9" width="13" height="13" rx="2"/>
            <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/>
          </svg>
        </button>
        <button class="slide-editor-btn slide-editor-nav-btn" id="nav-delete-slide" title="${t('navigator.deleteSlide')}">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/>
          </svg>
        </button>
      </div>
      <div class="slide-editor-thumbnails" id="slide-thumbnails"></div>
    `;

    this.setupEventListeners(nav);
    return nav;
  }

  private setupEventListeners(nav: HTMLElement): void {
    nav.querySelector('#nav-add-slide')?.addEventListener('click', () => {
      this.editor.addSlide();
      this.refresh();
    });

    nav.querySelector('#nav-duplicate-slide')?.addEventListener('click', () => {
      const current = this.editor.getCurrentSlide();
      if (current) {
        this.editor.duplicateSlide(current.index);
        this.refresh();
      }
    });

    nav.querySelector('#nav-delete-slide')?.addEventListener('click', () => {
      const current = this.editor.getCurrentSlide();
      if (current) {
        this.editor.deleteSlide(current.index);
        this.refresh();
      }
    });
  }

  mount(parent: HTMLElement): void {
    parent.appendChild(this.container);
    this.refresh();
  }

  unmount(): void {
    this.container.remove();
    this.thumbnails.clear();
  }

  refreshLocale(): void {
    // Re-render the navigator with new locale
    this.refresh();
  }

  refresh(): void {
    const container = this.container.querySelector('#slide-thumbnails');
    if (!container) return;

    container.innerHTML = '';
    this.thumbnails.clear();

    const slides = this.editor.getSlides();
    const currentSlide = this.editor.getCurrentSlide();
    const currentIndex = currentSlide?.index ?? 0;

    slides.forEach((slide, index) => {
      const thumbnail = this.createThumbnail(slide, index);
      if (index === currentIndex) {
        thumbnail.classList.add('slide-editor-thumbnail-active');
      }
      container.appendChild(thumbnail);
      this.thumbnails.set(index, thumbnail);
    });

    this.setupDragAndDrop();
  }

  private createThumbnail(slide: SlideInfo, index: number): HTMLDivElement {
    const thumb = document.createElement('div');
    thumb.className = 'slide-editor-thumbnail';
    thumb.dataset.slideIndex = index.toString();

    // Get all slide elements directly from DOM
    const allSlides = document.querySelectorAll('.slide');
    const slideEl = allSlides[index] as HTMLElement;

    const slideNumber = document.createElement('div');
    slideNumber.className = 'slide-editor-thumbnail-number';
    slideNumber.textContent = `${index + 1}`;

    // Create a mini preview
    const preview = document.createElement('div');
    preview.className = 'slide-editor-thumbnail-preview';

    if (slideEl) {
      // Count elements with data-editor-id attribute
      const elementCount = slideEl.querySelectorAll('[data-editor-id]').length;
      const elementText = elementCount === 1 ? t('navigator.element') : t('navigator.elements');
      preview.innerHTML = `<span class="slide-editor-element-count">${elementCount} ${elementText}</span>`;
    }

    thumb.appendChild(slideNumber);
    thumb.appendChild(preview);

    thumb.addEventListener('click', () => {
      this.selectSlide(index);
    });

    return thumb;
  }

  private selectSlide(index: number): void {
    // Update UI
    this.thumbnails.forEach((thumb, i) => {
      thumb.classList.toggle('slide-editor-thumbnail-active', i === index);
    });

    // Notify editor (which will handle showSlide)
    this.editor.setCurrentSlide(index);

    // Trigger callback
    if (this.onSlideChange) {
      this.onSlideChange(index);
    }
  }

  private setupDragAndDrop(): void {
    const container = this.container.querySelector('#slide-thumbnails');
    if (!container) return;

    let draggedIndex: number | null = null;

    container.addEventListener('dragstart', (e) => {
      const target = (e.target as HTMLElement).closest('.slide-editor-thumbnail') as HTMLElement;
      if (!target) return;

      draggedIndex = parseInt(target.dataset.slideIndex || '0');
      target.classList.add('slide-editor-dragging');
      (e as DragEvent).dataTransfer!.effectAllowed = 'move';
    });

    container.addEventListener('dragend', (e) => {
      const target = (e.target as HTMLElement).closest('.slide-editor-thumbnail');
      target?.classList.remove('slide-editor-dragging');
      draggedIndex = null;
    });

    container.addEventListener('dragover', (e) => {
      e.preventDefault();
      (e as DragEvent).dataTransfer!.effectAllowed = 'move';
    });

    container.addEventListener('drop', (e) => {
      e.preventDefault();

      const target = (e.target as HTMLElement).closest('.slide-editor-thumbnail') as HTMLElement;
      if (!target || draggedIndex === null) return;

      const targetIndex = parseInt(target.dataset.slideIndex || '0');
      if (draggedIndex !== targetIndex) {
        this.editor.moveSlide(draggedIndex, targetIndex);
        this.refresh();
      }
    });

    // Make thumbnails draggable
    this.thumbnails.forEach((thumb) => {
      thumb.draggable = true;
    });
  }

  setActiveSlide(index: number): void {
    this.thumbnails.forEach((thumb, i) => {
      thumb.classList.toggle('slide-editor-thumbnail-active', i === index);
    });
  }
}
