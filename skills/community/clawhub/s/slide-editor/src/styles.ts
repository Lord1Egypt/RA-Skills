// Editor styles - injected into the page when editor is enabled

export const editorStyles = `
/* Light theme (default) */
:root {
  --editor-accent: #0891b2;
  --editor-bg: #ffffff;
  --editor-surface: #f8fafc;
  --editor-text: #1e293b;
  --editor-text-muted: #64748b;
  --editor-border: #e2e8f0;
  --editor-hover: #f1f5f9;
  --editor-selected-bg: rgba(8, 145, 178, 0.1);
  --editor-handle-bg: #ffffff;
}

/* Dark theme - matches system preference */
@media (prefers-color-scheme: dark) {
  :root {
    --editor-accent: #22d3ee;
    --editor-bg: #0f172a;
    --editor-surface: #1e293b;
    --editor-text: #f1f5f9;
    --editor-text-muted: #94a3b8;
    --editor-border: #334155;
    --editor-hover: #334155;
    --editor-selected-bg: rgba(34, 211, 238, 0.15);
    --editor-handle-bg: #ffffff;
  }
}

/* Manual theme override classes */
.slide-editor-light {
  --editor-accent: #0891b2;
  --editor-bg: #ffffff;
  --editor-surface: #f8fafc;
  --editor-text: #1e293b;
  --editor-text-muted: #64748b;
  --editor-border: #e2e8f0;
  --editor-hover: #f1f5f9;
  --editor-selected-bg: rgba(8, 145, 178, 0.1);
  --editor-handle-bg: #ffffff;
}

.slide-editor-dark {
  --editor-accent: #22d3ee;
  --editor-bg: #0f172a;
  --editor-surface: #1e293b;
  --editor-text: #f1f5f9;
  --editor-text-muted: #94a3b8;
  --editor-border: #334155;
  --editor-hover: #334155;
  --editor-selected-bg: rgba(34, 211, 238, 0.15);
  --editor-handle-bg: #ffffff;
}

.slide-editor-selected {
  outline: 2px solid var(--editor-accent) !important;
  outline-offset: 2px !important;
}

.slide-editor-editing {
  outline: 2px dashed var(--editor-accent) !important;
  cursor: text !important;
}

.slide-editor-resize-handle {
  position: absolute;
  width: 10px;
  height: 10px;
  background: var(--editor-handle-bg) !important;
  border: 2px solid var(--editor-accent) !important;
  border-radius: 2px !important;
  z-index: 10000 !important;
  pointer-events: auto !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

/* Toolbar */
#slide-editor-toolbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 48px;
  background: var(--editor-bg);
  border-bottom: 1px solid var(--editor-border);
  display: flex;
  align-items: center;
  padding: 0 16px;
  gap: 8px;
  z-index: 99999;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.slide-editor-toolbar-group {
  display: flex;
  align-items: center;
  gap: 4px;
}

.slide-editor-toolbar-spacer {
  flex: 1;
}

.slide-editor-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 12px;
  background: var(--editor-surface);
  color: var(--editor-text);
  border: 1px solid var(--editor-border);
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.15s ease;
}

.slide-editor-btn:hover {
  background: var(--editor-hover);
  border-color: var(--editor-accent);
}

.slide-editor-btn:active {
  transform: scale(0.98);
}

.slide-editor-btn-primary {
  background: var(--editor-accent);
  color: #000;
  border-color: var(--editor-accent);
}

.slide-editor-btn-primary:hover {
  filter: brightness(1.1);
}

.slide-editor-btn-disabled,
.slide-editor-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.slide-editor-btn-full {
  width: 100%;
}

/* Properties Panel */
#slide-editor-properties {
  position: fixed;
  top: 48px;
  right: 0;
  width: 280px;
  height: calc(100vh - 48px - 80px);
  background: var(--editor-bg);
  border-left: 1px solid var(--editor-border);
  z-index: 99998;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  display: flex;
  flex-direction: column;
  transition: transform 0.25s ease, opacity 0.25s ease;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.05);
}

#slide-editor-properties.slide-editor-panel-hidden {
  transform: translateX(100%);
  opacity: 0;
  pointer-events: none;
}

.slide-editor-panel-header {
  padding: 12px 16px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--editor-accent);
  border-bottom: 1px solid var(--editor-border);
  background: var(--editor-surface);
}

.slide-editor-panel-content {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
}

.slide-editor-no-selection {
  color: var(--editor-text-muted);
  text-align: center;
  padding: 24px;
  font-size: 13px;
}

.slide-editor-hidden {
  display: none !important;
}

.slide-editor-properties-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.slide-editor-field-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.slide-editor-field-group > label {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--editor-text-muted);
}

.slide-editor-field-row {
  display: flex;
  gap: 8px;
}

.slide-editor-field {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.slide-editor-field-label {
  font-size: 10px;
  color: var(--editor-text-muted);
}

.slide-editor-field input,
.slide-editor-field select {
  padding: 8px;
  background: var(--editor-surface);
  border: 1px solid var(--editor-border);
  border-radius: 4px;
  color: var(--editor-text);
  font-size: 13px;
}

.slide-editor-field input:focus,
.slide-editor-field select:focus {
  outline: none;
  border-color: var(--editor-accent);
}

.slide-editor-field input[type="color"] {
  padding: 4px;
  height: 32px;
}

.slide-editor-field input[type="range"] {
  padding: 0;
  -webkit-appearance: none;
  background: var(--editor-border);
  height: 4px;
  border-radius: 2px;
}

.slide-editor-field input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 14px;
  height: 14px;
  background: var(--editor-accent);
  border-radius: 50%;
  cursor: pointer;
}

/* Slide Navigator */
#slide-editor-navigator {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 80px;
  background: var(--editor-bg);
  border-top: 1px solid var(--editor-border);
  z-index: 99998;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  display: flex;
  align-items: center;
  padding: 0 24px 12px 24px;
  gap: 16px;
  box-sizing: border-box;
  box-shadow: 0 -1px 3px rgba(0, 0, 0, 0.05);
}

.slide-editor-nav-controls {
  display: flex;
  flex-direction: row;
  gap: 10px;
  align-items: center;
  padding: 8px 12px;
  background: var(--editor-surface);
  border-radius: 10px;
  border: 1px solid var(--editor-border);
}

.slide-editor-nav-controls .slide-editor-btn {
  min-width: 44px;
  height: 44px;
  padding: 10px;
  border-radius: 8px;
  background: var(--editor-bg);
  border: 1px solid var(--editor-border);
  transition: all 0.2s ease;
}

.slide-editor-nav-controls .slide-editor-btn:hover {
  background: var(--editor-hover);
  border-color: var(--editor-accent);
  transform: translateY(-1px);
}

.slide-editor-nav-controls .slide-editor-btn:active {
  transform: translateY(0) scale(0.96);
}

.slide-editor-nav-controls .slide-editor-btn svg {
  width: 22px;
  height: 22px;
  stroke-width: 2.5;
}

.slide-editor-thumbnails {
  flex: 1;
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding: 8px 0;
  flex-direction: row;
}

.slide-editor-thumbnail {
  flex-shrink: 0;
  width: 100px;
  height: 56px;
  background: var(--editor-surface);
  border: 2px solid transparent;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
}

.slide-editor-thumbnail:hover {
  border-color: var(--editor-border);
}

.slide-editor-thumbnail-active {
  border-color: var(--editor-accent) !important;
  background: var(--editor-selected-bg);
}

.slide-editor-thumbnail-number {
  font-size: 14px;
  font-weight: 600;
  color: var(--editor-text);
}

.slide-editor-thumbnail-preview {
  font-size: 10px;
  color: var(--editor-text-muted);
}

.slide-editor-element-count {
  font-size: 9px;
  color: var(--editor-text-muted);
}

.slide-editor-dragging {
  opacity: 0.5;
}

/* Crop Overlay */
.slide-editor-crop-overlay {
  z-index: 100000 !important;
}

.slide-editor-crop-controls {
  position: fixed;
  bottom: 100px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
  z-index: 100001;
}

.slide-editor-crop-area {
  z-index: 100001 !important;
}

/* Toast notification */
.slide-editor-toast {
  position: fixed;
  bottom: 100px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--editor-accent);
  color: #000;
  padding: 12px 24px;
  border-radius: 8px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 14px;
  font-weight: 500;
  z-index: 100001;
  animation: slide-editor-toast-in 0.3s ease;
}

@keyframes slide-editor-toast-in {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

/* Adjust page content for editor */
body.slide-editor-active {
  padding-top: 48px !important;
  padding-bottom: 80px !important;
}

body.slide-editor-active .slides {
  transition: padding-right 0.25s ease;
}

body.slide-editor-active:not(.panel-hidden) .slides {
  padding-right: 280px !important;
}

body.slide-editor-active.panel-hidden .slides {
  padding-right: 0 !important;
}
`;
