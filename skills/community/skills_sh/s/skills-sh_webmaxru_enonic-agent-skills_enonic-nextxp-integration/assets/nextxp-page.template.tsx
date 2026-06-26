// Next.XP Page Component Template
// Adapt this template to the framework, state model, and file layout in the workspace.
//
// Usage:
//   1. Copy this file to src/components/pages/<PageName>.tsx
//   2. Update the regions to match the Enonic page XML definition
//   3. Register in src/components/_mappings.ts with ComponentRegistry.addPage()

import type {PageProps} from '@enonic/nextjs-adapter';
import React from 'react';
import RegionsView from '@enonic/nextjs-adapter/views/Region';

// Replace 'main' with the region name defined in your Enonic page XML.
const REGION_NAME = 'main';

interface PageComponentProps extends PageProps {}

const PageTemplate = (props: PageComponentProps) => {
    const page = props.page;

    // Ensure region exists even if no components have been added yet.
    const regions = (!page.regions || !Object.keys(page.regions).length) ? {
        [REGION_NAME]: {
            name: REGION_NAME,
            components: [],
        }
    } : page.regions;

    return (
        <>
            <RegionsView {...props} page={{...page, regions}} name={REGION_NAME}/>
        </>
    );
};

export default PageTemplate;

// --- Registration snippet for _mappings.ts ---
// import PageTemplate from './pages/<PageName>';
// import {APP_NAME} from '@enonic/nextjs-adapter';
//
// ComponentRegistry.addPage(`${APP_NAME}:<page-name>`, {
//     view: PageTemplate
// });
