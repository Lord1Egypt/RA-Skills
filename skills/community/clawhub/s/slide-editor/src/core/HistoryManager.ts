import type { EditorState, HistoryAction } from '../types';

export class HistoryManager {
  private state: EditorState;
  private maxHistory = 100;

  constructor(state: EditorState) {
    this.state = state;
  }

  push(action: HistoryAction): void {
    // If we're not at the end of history, truncate forward items
    if (this.state.historyIndex < this.state.historyStack.length) {
      this.state.historyStack = this.state.historyStack.slice(0, this.state.historyIndex);
    }

    this.state.historyStack.push(action);

    // Limit history size
    if (this.state.historyStack.length > this.maxHistory) {
      this.state.historyStack.shift();
    } else {
      this.state.historyIndex++;
    }
  }

  canUndo(): boolean {
    return this.state.historyIndex > 0;
  }

  canRedo(): boolean {
    return this.state.historyIndex < this.state.historyStack.length;
  }

  undo(): HistoryAction | null {
    if (!this.canUndo()) return null;

    this.state.historyIndex--;
    return this.state.historyStack[this.state.historyIndex];
  }

  redo(): HistoryAction | null {
    if (!this.canRedo()) return null;

    const action = this.state.historyStack[this.state.historyIndex];
    this.state.historyIndex++;
    return action;
  }

  getHistoryLength(): number {
    return this.state.historyStack.length;
  }
}
