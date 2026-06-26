// Part controller template for Enonic XP
// Replace <PART_NAME> with the actual part name (e.g., "hero-banner")
// Pair with descriptor: src/main/resources/site/parts/<PART_NAME>/<PART_NAME>.xml

import { getComponent, imageUrl } from '/lib/xp/portal';
import thymeleafLib from '/lib/thymeleaf';

const view = resolve('<PART_NAME>.html');

export function get(req) {
  const component = getComponent();
  const config = component.config;

  const model = {
    // Map config fields to view model properties
    // Example: heading: config.heading || 'Default Heading',
  };

  return {
    body: thymeleafLib.render(view, model),
    contentType: 'text/html'
  };
}

/*
--- Paired XML Descriptor ---
File: src/main/resources/site/parts/<PART_NAME>/<PART_NAME>.xml

<part>
  <display-name>PART_DISPLAY_NAME</display-name>
  <description>PART_DESCRIPTION</description>
  <form>
    <!-- Add input fields here -->
    <!--
    <input name="heading" type="TextLine">
      <label>Heading</label>
      <occurrences minimum="1" maximum="1"/>
    </input>
    -->
  </form>
</part>
*/
