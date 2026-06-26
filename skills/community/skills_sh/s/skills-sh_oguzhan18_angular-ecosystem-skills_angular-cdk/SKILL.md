---
name: angular-cdk
description: "ALWAYS use when working with Angular CDK (Component Dev Kit), building custom accessible components, or using drag-drop, overlay, portal, or virtual scrolling."
metadata:
  version: 21.0.3
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# @angular/cdk (Component Dev Kit)

**Version:** 21.0.3 (Feb 2026)
**Tags:** Accessibility, Drag & Drop, Overlay, Virtual Scroll, Portal

**References:** [Docs](https://material.angular.dev/cdk) — official CDK documentation • [GitHub](https://github.com/angular/components) • [API](https://material.angular.io/cdk/categories)

## API Changes

This section documents recent version-specific API changes.

- NEW: CDK overlays now use browser's built-in popovers for improved accessibility [source](https://blog.angular.dev/announcing-angular-v21)

- NEW: Angular 19 signal-based APIs — Modern signal integration for CDK components

- NEW: Improved focus management — Better `cdkTrapFocus` and `cdkFocusRegion` support

- NEW: Drag & Drop improvements — Enhanced item copying between lists

- DEPRECATED: Legacy overlay strategies — Prefer scroll strategy configuration over deprecated approaches

## Best Practices

- Use CDK for custom UI components — Build your own components without Material styling

```ts
import { OverlayModule } from '@angular/cdk/overlay';
import { PortalModule } from '@angular/cdk/portal';

@Component({
  standalone: true,
  imports: [OverlayModule, PortalModule],
  // ...
})
export class CustomDropdownComponent {}
```

- Use Overlay for floating panels — Tooltips, dropdowns, modals

```ts
import { OverlayRef, Overlay } from '@angular/cdk/overlay';

export class TooltipService {
  private overlayRef: OverlayRef;

  constructor(private overlay: Overlay) {
    this.overlayRef = this.overlay.create({
      hasBackdrop: true,
      positionStrategy: this.overlay.position()
        .connectedTo(origin, { originX: 'center', originY: 'bottom' })
        .withOffsetX(0)
        .withOffsetY(8)
    });
  }
}
```

- Use Drag & Drop for sortable lists

```ts
import { CdkDragDrop, moveItemInArray, transferArrayItem } from '@angular/cdk/drag-drop';

drop(event: CdkDragDrop<string[]>) {
  if (event.previousContainer === event.container) {
    moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
  } else {
    transferArrayItem(
      event.previousContainer.data,
      event.container.data,
      event.previousIndex,
      event.currentIndex
    );
  }
}
```

- Use Virtual Scroll for large lists

```ts
import { ScrollingModule } from '@angular/cdk/scrolling';

@Component({
  standalone: true,
  imports: [ScrollingModule],
  template: `
    <cdk-virtual-scroll-viewport itemSize="50" class="viewport">
      <div *cdkVirtualFor="let item of items">{{item.name}}</div>
    </cdk-virtual-scroll-viewport>
  `
})
export class ListComponent {}
```

- Use Portal for dynamic content

```ts
import { DomPortalOutlet, TemplatePortal } from '@angular/cdk/portal';

@Component({ template: `<ng-template #dialogTemplate>Content</ng-template>` })
export class DialogComponent {
  @ViewChild('dialogTemplate') dialogTemplate!: TemplatePortal;

  attach() {
    const portalOutlet = new DomPortalOutlet(this.document.body);
    portalOutlet.attach(this.dialogTemplate);
  }
}
```

- Use A11y utilities for accessibility

```ts
import { A11yModule, CdkTrapFocus, LiveAnnouncer } from '@angular/cdk/a11y';

@Component({
  standalone: true,
  imports: [A11yModule],
  template: `
    <div cdkTrapFocus>
      <button cdkFocusInitial>First</button>
      <button>Second</button>
    </div>
  `
})
export class AccessibleComponent {
  constructor(private liveAnnouncer: LiveAnnouncer) {
    this.liveAnnouncer.announce('Message for screen readers');
  }
}
```

- Use Layout for responsive breakpoints

```ts
import { LayoutModule } from '@angular/cdk/layout';

@Component({
  standalone: true,
  imports: [LayoutModule],
  template: `
    <div *ngIf="isHandset$ | async">
      Mobile content
    </div>
  `
})
export class ResponsiveComponent {
  isHandset$ = this.breakpointObserver.observe('(max-width: 599px)');
}
```
