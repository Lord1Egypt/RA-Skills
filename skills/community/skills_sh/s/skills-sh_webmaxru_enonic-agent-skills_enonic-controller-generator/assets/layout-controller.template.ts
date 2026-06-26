// Layout controller template for Enonic XP
// Replace <LAYOUT_NAME> with the actual layout name (e.g., "two-column")
// Pair with descriptor: src/main/resources/site/layouts/<LAYOUT_NAME>/<LAYOUT_NAME>.xml

import { getComponent } from '/lib/xp/portal';
import thymeleafLib from '/lib/thymeleaf';

const view = resolve('<LAYOUT_NAME>.html');

export function get(req) {
  const component = getComponent();

  const model = {
    leftRegion: component.regions.left,
    rightRegion: component.regions.right
    // Add or rename regions to match the descriptor
  };

  return {
    body: thymeleafLib.render(view, model),
    contentType: 'text/html'
  };
}

/*
--- Paired XML Descriptor ---
File: src/main/resources/site/layouts/<LAYOUT_NAME>/<LAYOUT_NAME>.xml

<layout>
  <display-name>LAYOUT_DISPLAY_NAME</display-name>
  <description>LAYOUT_DESCRIPTION</description>
  <form/>
  <regions>
    <region name="left"/>
    <region name="right"/>
  </regions>
</layout>

--- Paired Thymeleaf View ---
File: src/main/resources/site/layouts/<LAYOUT_NAME>/<LAYOUT_NAME>.html

<div class="row">
  <div class="col-left" data-portal-region="left">
    <div data-th-each="component : ${leftRegion.components}"
         data-th-remove="tag"
         data-portal-component="${component.path}">
    </div>
  </div>
  <div class="col-right" data-portal-region="right">
    <div data-th-each="component : ${rightRegion.components}"
         data-th-remove="tag"
         data-portal-component="${component.path}">
    </div>
  </div>
</div>
*/
