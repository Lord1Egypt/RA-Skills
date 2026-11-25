// Stimulus controller for accessible modal dialogs.
// Handles: focus trap, ESC to close, backdrop click, focus return.

import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["container", "closeButton"]
  static values = { open: Boolean }

  connect() {
    this.previousActiveElement = null

    if (this.openValue) {
      this.open()
    }
  }

  disconnect() {
    this.close()
  }

  open() {
    this.previousActiveElement = document.activeElement
    this.element.classList.remove("hidden")
    document.body.classList.add("overflow-hidden")

    // Focus the close button or first focusable element
    setTimeout(() => {
      const focusTarget = this.closeButtonTarget ||
        this.containerTarget.querySelector(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        )
      focusTarget?.focus()
    }, 100)

    this._bindKeys()
  }

  close() {
    this.element.classList.add("hidden")
    document.body.classList.remove("overflow-hidden")
    this._unbindKeys()

    // Return focus to the element that opened the modal
    this.previousActiveElement?.focus()
    this.previousActiveElement = null
  }

  // Close on backdrop click
  closeOnBackdrop(event) {
    if (event.target === this.element) {
      this.close()
    }
  }

  // Trap focus within the modal
  _handleKeydown(event) {
    if (event.key === "Escape") {
      event.preventDefault()
      this.close()
      return
    }

    if (event.key !== "Tab") return

    const focusable = this.containerTarget.querySelectorAll(
      'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
    )

    if (focusable.length === 0) {
      event.preventDefault()
      return
    }

    const first = focusable[0]
    const last = focusable[focusable.length - 1]

    if (event.shiftKey) {
      if (document.activeElement === first) {
        event.preventDefault()
        last.focus()
      }
    } else {
      if (document.activeElement === last) {
        event.preventDefault()
        first.focus()
      }
    }
  }

  _bindKeys() {
    this._boundKeydown = this._handleKeydown.bind(this)
    document.addEventListener("keydown", this._boundKeydown)
  }

  _unbindKeys() {
    if (this._boundKeydown) {
      document.removeEventListener("keydown", this._boundKeydown)
    }
  }
}
