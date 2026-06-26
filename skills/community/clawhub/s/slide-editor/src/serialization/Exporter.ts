import type { SlideInfo, ElementInfo, CropRect } from '../types';

export class Exporter {
  exportClean(): string {
    const clone = document.documentElement.cloneNode(true) as HTMLElement;

    // Remove editor UI elements
    clone.querySelectorAll('#slide-editor-toolbar').forEach((el) => el.remove());
    clone.querySelectorAll('#slide-editor-properties').forEach((el) => el.remove());
    clone.querySelectorAll('#slide-editor-navigator').forEach((el) => el.remove());
    clone.querySelectorAll('#slide-editor-styles').forEach((el) => el.remove());
    clone.querySelectorAll('.slide-editor-resize-handle').forEach((el) => el.remove());
    clone.querySelectorAll('.slide-editor-crop-overlay').forEach((el) => el.remove());

    // Remove editor classes
    clone.querySelectorAll('.slide-editor-selected').forEach((el) => {
      el.classList.remove('slide-editor-selected');
    });
    clone.querySelectorAll('.slide-editor-editing').forEach((el) => {
      el.classList.remove('slide-editor-editing');
    });

    // Remove body classes added by editor
    const body = clone.querySelector('body');
    if (body) {
      body.classList.remove('slide-editor-active');
      body.classList.remove('slide-editor-light');
      body.classList.remove('slide-editor-dark');
      body.classList.remove('panel-hidden');
      body.style.paddingTop = '';
      body.style.paddingBottom = '';
      body.style.paddingRight = '';
    }

    // Remove data-editor-id attributes
    clone.querySelectorAll('[data-editor-id]').forEach((el) => {
      el.removeAttribute('data-editor-id');
    });

    // Remove contenteditable
    clone.querySelectorAll('[contenteditable]').forEach((el) => {
      el.removeAttribute('contenteditable');
    });

    // Remove editor script tags (including auto-enable scripts)
    clone.querySelectorAll('script').forEach((script) => {
      const content = script.textContent || '';
      if (content.includes('__openclawEditor') ||
          content.includes('SlideEditor') ||
          content.includes('SLIDE_EDITOR_START') ||
          content.includes('SLIDE_EDITOR_BUNDLE') ||
          (content.includes('Auto-enable editor') && content.includes('window.__openclawEditor'))) {
        script.remove();
      }
    });

    // Make all slides visible - reset inline display style
    // This allows the original CSS to control slide visibility
    clone.querySelectorAll('.slide').forEach((el) => {
      (el as HTMLElement).style.display = '';
    });

    // Always add navigation script for multi-slide presentations
    // This ensures keyboard navigation works even if original script was missing
    const slides = clone.querySelectorAll('.slide');
    if (slides.length > 1) {
      // Remove any existing showSlide scripts that might conflict
      clone.querySelectorAll('script').forEach((script) => {
        const content = script.textContent || '';
        if (content.includes('function showSlide') || content.includes('showSlide(0)')) {
          // Keep the script but it will be supplemented
        }
      });

      // Add comprehensive navigation script
      const navScript = document.createElement('script');
      navScript.textContent = `
(function() {
  let currentSlide = 0;
  const slides = document.querySelectorAll('.slide');

  function showSlide(i) {
    slides.forEach((s, idx) => s.style.display = idx === i ? 'flex' : 'none');
  }

  // Initialize first slide
  showSlide(0);

  // Keyboard navigation
  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === ' ') {
      e.preventDefault();
      currentSlide = (currentSlide + 1) % slides.length;
      showSlide(currentSlide);
    } else if (e.key === 'ArrowLeft') {
      e.preventDefault();
      currentSlide = (currentSlide - 1 + slides.length) % slides.length;
      showSlide(currentSlide);
    }
  });

  // Make showSlide available globally for any existing code
  window.showSlide = showSlide;
})();
`;
      if (body) {
        body.appendChild(navScript);
      }
    }

    return '<!DOCTYPE html>\n' + clone.outerHTML;
  }

  exportWithEditor(editorScript: string): string {
    const html = document.documentElement.outerHTML;

    // Ensure editor script is included
    if (!html.includes('__openclawEditor')) {
      const bodyClose = html.lastIndexOf('</body>');
      if (bodyClose > -1) {
        const scriptTag = `<script>${editorScript}</script>`;
        return '<!DOCTYPE html>\n' +
          html.slice(0, bodyClose) +
          scriptTag +
          '\n<script>window.__openclawEditor.enable();</script>\n' +
          html.slice(bodyClose);
      }
    }

    return '<!DOCTYPE html>\n' + html;
  }

  getSlides(): SlideInfo[] {
    const slides: SlideInfo[] = [];
    const slideElements = document.querySelectorAll('.slide');

    slideElements.forEach((slideEl, index) => {
      const elements = this.getSlideElements(slideEl as HTMLElement);
      slides.push({
        index,
        id: slideEl.id || `slide-${index}`,
        elements,
      });
    });

    return slides;
  }

  private getSlideElements(slideEl: HTMLElement): ElementInfo[] {
    const elements: ElementInfo[] = [];
    const editableElements = slideEl.querySelectorAll('[data-editor-id]');

    editableElements.forEach((el) => {
      const info = this.getElementInfo(el as HTMLElement, slideEl);
      if (info) elements.push(info);
    });

    return elements;
  }

  private getElementInfo(el: HTMLElement, slideEl: HTMLElement): ElementInfo | null {
    const id = el.getAttribute('data-editor-id');
    if (!id) return null;

    const rect = el.getBoundingClientRect();
    const slideRect = slideEl.getBoundingClientRect();

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
    if (['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'div', 'a', 'label'].includes(tagName)) {
      if (el.querySelector('img')) return 'unknown';
      return 'text';
    }
    if (tagName === 'svg' || el.closest('svg')) return 'shape';
    return 'unknown';
  }

  private extractStyles(el: HTMLElement): Record<string, string> {
    const computed = window.getComputedStyle(el);
    const styles: Record<string, string> = {};
    const relevantProps = [
      'fontSize', 'fontFamily', 'fontWeight', 'color', 'backgroundColor',
      'textAlign', 'lineHeight', 'opacity', 'borderRadius', 'padding', 'margin'
    ];

    relevantProps.forEach((prop) => {
      const value = computed.getPropertyValue(this.camelToKebab(prop));
      if (value && value !== 'none' && value !== 'normal') {
        styles[prop] = value;
      }
    });

    return styles;
  }

  private camelToKebab(str: string): string {
    return str.replace(/([a-z0-9])([A-Z])/g, '$1-$2').toLowerCase();
  }
}

export class ImageCropper {
  private overlay: HTMLDivElement | null = null;
  private cropArea: HTMLDivElement | null = null;
  private targetElement: HTMLElement | null = null;
  private targetElementId: string | null = null;
  private onStart: ((rect: CropRect) => void) | null = null;
  private onCancel: (() => void) | null = null;
  private handles: Map<string, HTMLDivElement> = new Map();
  private containerRect: DOMRect | null = null;

  startCrop(elementId: string, onApply: (rect: CropRect) => void, onCancel: () => void): void {
    this.targetElement = document.querySelector(`[data-editor-id="${elementId}"]`) as HTMLElement;
    if (!this.targetElement || this.targetElement.tagName.toLowerCase() !== 'img') {
      return;
    }

    this.targetElementId = elementId;
    this.onStart = onApply;
    this.onCancel = onCancel;

    this.createCropOverlay();
  }

  private createCropOverlay(): void {
    if (!this.targetElement) return;

    // Create overlay
    this.overlay = document.createElement('div');
    this.overlay.className = 'slide-editor-crop-overlay';
    this.overlay.innerHTML = `
      <div class="slide-editor-crop-controls">
        <button class="slide-editor-btn slide-editor-btn-primary" id="crop-apply">Apply Crop</button>
        <button class="slide-editor-btn" id="crop-cancel">Cancel</button>
      </div>
    `;

    // Create crop area
    this.cropArea = document.createElement('div');
    this.cropArea.className = 'slide-editor-crop-area';

    // Position overlay
    const rect = this.targetElement.getBoundingClientRect();
    this.containerRect = rect;
    this.overlay.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.7);
      z-index: 100000;
      display: flex;
      align-items: center;
      justify-content: center;
    `;

    // Create container for the image
    const container = document.createElement('div');
    container.style.cssText = `
      position: relative;
      width: ${rect.width}px;
      height: ${rect.height}px;
    `;

    // Clone the image
    const imgClone = this.targetElement.cloneNode(true) as HTMLImageElement;
    imgClone.style.cssText = `
      width: 100%;
      height: 100%;
      object-fit: contain;
    `;

    // Set up crop area
    this.cropArea.style.cssText = `
      position: absolute;
      top: 10%;
      left: 10%;
      width: 80%;
      height: 80%;
      border: 2px dashed var(--editor-accent, #00ffcc);
      background: transparent;
      cursor: move;
    `;

    container.appendChild(imgClone);
    container.appendChild(this.cropArea);

    // Create resize handles
    this.createCropHandles();

    this.overlay.appendChild(container);
    document.body.appendChild(this.overlay);

    // Add event listeners
    this.overlay.querySelector('#crop-apply')?.addEventListener('click', () => this.applyCrop());
    this.overlay.querySelector('#crop-cancel')?.addEventListener('click', () => this.cancelCrop());

    // Make crop area draggable
    this.setupCropDrag();
  }

  private createCropHandles(): void {
    if (!this.cropArea) return;

    const cropArea = this.cropArea;
    const positions = ['nw', 'n', 'ne', 'e', 'se', 's', 'sw', 'w'];
    const cursors: Record<string, string> = {
      'nw': 'nwse-resize', 'n': 'ns-resize', 'ne': 'nesw-resize', 'e': 'ew-resize',
      'se': 'nwse-resize', 's': 'ns-resize', 'sw': 'nesw-resize', 'w': 'ew-resize'
    };

    positions.forEach((pos) => {
      const handle = document.createElement('div');
      handle.className = 'slide-editor-crop-handle';
      handle.dataset.handlePosition = pos;
      handle.style.cssText = `
        position: absolute;
        width: 12px;
        height: 12px;
        background: white;
        border: 2px solid var(--editor-accent, #00ffcc);
        border-radius: 2px;
        cursor: ${cursors[pos] || 'pointer'};
        z-index: 100002;
      `;
      this.positionHandle(handle, pos);
      cropArea.appendChild(handle);
      this.handles.set(pos, handle);

      // Setup resize drag for each handle
      this.setupHandleDrag(handle, pos);
    });
  }

  private positionHandle(handle: HTMLDivElement, position: string): void {
    const offset = -6; // Half of handle size to center it on the border

    switch (position) {
      case 'nw':
        handle.style.top = `${offset}px`;
        handle.style.left = `${offset}px`;
        break;
      case 'n':
        handle.style.top = `${offset}px`;
        handle.style.left = '50%';
        handle.style.transform = 'translateX(-50%)';
        break;
      case 'ne':
        handle.style.top = `${offset}px`;
        handle.style.right = `${offset}px`;
        break;
      case 'e':
        handle.style.top = '50%';
        handle.style.right = `${offset}px`;
        handle.style.transform = 'translateY(-50%)';
        break;
      case 'se':
        handle.style.bottom = `${offset}px`;
        handle.style.right = `${offset}px`;
        break;
      case 's':
        handle.style.bottom = `${offset}px`;
        handle.style.left = '50%';
        handle.style.transform = 'translateX(-50%)';
        break;
      case 'sw':
        handle.style.bottom = `${offset}px`;
        handle.style.left = `${offset}px`;
        break;
      case 'w':
        handle.style.top = '50%';
        handle.style.left = `${offset}px`;
        handle.style.transform = 'translateY(-50%)';
        break;
    }
  }

  private setupHandleDrag(handle: HTMLDivElement, position: string): void {
    let isResizing = false;
    let startX = 0;
    let startY = 0;
    let startLeft = 0;
    let startTop = 0;
    let startWidth = 0;
    let startHeight = 0;

    handle.addEventListener('pointerdown', (e) => {
      e.stopPropagation();
      isResizing = true;
      startX = e.clientX;
      startY = e.clientY;

      if (this.cropArea) {
        startLeft = this.cropArea.offsetLeft;
        startTop = this.cropArea.offsetTop;
        startWidth = this.cropArea.offsetWidth;
        startHeight = this.cropArea.offsetHeight;
      }

      handle.setPointerCapture(e.pointerId);
    });

    document.addEventListener('pointermove', (e) => {
      if (!isResizing || !this.cropArea || !this.containerRect) return;

      const deltaX = e.clientX - startX;
      const deltaY = e.clientY - startY;

      const minSize = 20;
      const maxWidth = this.containerRect.width;
      const maxHeight = this.containerRect.height;

      let newLeft = startLeft;
      let newTop = startTop;
      let newWidth = startWidth;
      let newHeight = startHeight;

      // Handle resize based on which handle is being dragged
      if (position.includes('w')) {
        newWidth = Math.max(minSize, startWidth - deltaX);
        newLeft = Math.min(startLeft + startWidth - minSize, startLeft + deltaX);
        if (newLeft < 0) {
          newWidth += newLeft;
          newLeft = 0;
        }
      }
      if (position.includes('e')) {
        newWidth = Math.max(minSize, startWidth + deltaX);
        if (newLeft + newWidth > maxWidth) {
          newWidth = maxWidth - newLeft;
        }
      }
      if (position.includes('n')) {
        newHeight = Math.max(minSize, startHeight - deltaY);
        newTop = Math.min(startTop + startHeight - minSize, startTop + deltaY);
        if (newTop < 0) {
          newHeight += newTop;
          newTop = 0;
        }
      }
      if (position.includes('s')) {
        newHeight = Math.max(minSize, startHeight + deltaY);
        if (newTop + newHeight > maxHeight) {
          newHeight = maxHeight - newTop;
        }
      }

      this.cropArea.style.left = `${newLeft}px`;
      this.cropArea.style.top = `${newTop}px`;
      this.cropArea.style.width = `${newWidth}px`;
      this.cropArea.style.height = `${newHeight}px`;
    });

    document.addEventListener('pointerup', () => {
      isResizing = false;
    });
  }

  private setupCropDrag(): void {
    if (!this.cropArea) return;

    let isDragging = false;
    let startX = 0;
    let startY = 0;
    let startLeft = 0;
    let startTop = 0;

    this.cropArea.addEventListener('pointerdown', (e) => {
      // Don't start drag if clicking on a handle
      if ((e.target as HTMLElement).classList.contains('slide-editor-crop-handle')) return;

      isDragging = true;
      startX = e.clientX;
      startY = e.clientY;
      startLeft = this.cropArea!.offsetLeft;
      startTop = this.cropArea!.offsetTop;
      (e.target as HTMLElement).setPointerCapture(e.pointerId);
    });

    document.addEventListener('pointermove', (e) => {
      if (!isDragging || !this.cropArea || !this.containerRect) return;

      const deltaX = e.clientX - startX;
      const deltaY = e.clientY - startY;

      const maxWidth = this.containerRect.width - this.cropArea.offsetWidth;
      const maxHeight = this.containerRect.height - this.cropArea.offsetHeight;

      let newLeft = startLeft + deltaX;
      let newTop = startTop + deltaY;

      // Constrain to container bounds
      newLeft = Math.max(0, Math.min(maxWidth, newLeft));
      newTop = Math.max(0, Math.min(maxHeight, newTop));

      this.cropArea.style.left = `${newLeft}px`;
      this.cropArea.style.top = `${newTop}px`;
    });

    document.addEventListener('pointerup', () => {
      isDragging = false;
    });
  }

  private applyCrop(): void {
    if (!this.cropArea || !this.targetElement || !this.onStart || !this.containerRect) return;

    // The containerRect is the size of the cloned image container
    // cropArea offsets are relative to this container
    const containerWidth = this.containerRect.width;
    const containerHeight = this.containerRect.height;

    // Get crop area position relative to container
    const cropLeft = this.cropArea.offsetLeft;
    const cropTop = this.cropArea.offsetTop;
    const cropWidth = this.cropArea.offsetWidth;
    const cropHeight = this.cropArea.offsetHeight;

    // Calculate relative crop coordinates (percentage)
    const rect: CropRect = {
      x: (cropLeft / containerWidth) * 100,
      y: (cropTop / containerHeight) * 100,
      width: (cropWidth / containerWidth) * 100,
      height: (cropHeight / containerHeight) * 100,
    };

    // Apply CSS clip-path for non-destructive crop
    // inset(top right bottom left)
    const top = rect.y;
    const right = 100 - rect.x - rect.width;
    const bottom = 100 - rect.y - rect.height;
    const left = rect.x;

    this.targetElement.style.clipPath = `inset(${top}% ${right}% ${bottom}% ${left}%)`;

    // Store references before cleanup
    const callback = this.onStart;

    this.cleanup();

    // Call callback after cleanup
    if (callback) {
      callback(rect);
    }
  }

  private cancelCrop(): void {
    if (this.onCancel) {
      this.onCancel();
    }
    this.cleanup();
  }

  private cleanup(): void {
    this.handles.forEach((handle) => handle.remove());
    this.handles.clear();
    this.overlay?.remove();
    this.overlay = null;
    this.cropArea = null;
    this.containerRect = null;
    this.onStart = null;
    this.onCancel = null;
    // Don't clear targetElement or targetElementId immediately - let applyCrop use them
  }
}
