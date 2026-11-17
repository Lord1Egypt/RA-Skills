import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { describe, it } from 'node:test';

import {
  buildCssHints,
  normalizeDesignProperties,
  normalizePaintColor,
} from '../scripts/lib/figma-style-normalizer.mjs';

function frameNode(overrides = {}) {
  return {
    id: '1:3',
    name: 'Primary button',
    type: 'FRAME',
    visible: true,
    absoluteBoundingBox: { x: 20, y: 30, width: 120, height: 40 },
    absoluteRenderBounds: { x: 20, y: 30, width: 120, height: 40 },
    relativeTransform: [
      [1, 0, 20],
      [0, 1, 30],
    ],
    clipsContent: false,
    layoutMode: 'HORIZONTAL',
    primaryAxisSizingMode: 'AUTO',
    counterAxisSizingMode: 'FIXED',
    primaryAxisAlignItems: 'CENTER',
    counterAxisAlignItems: 'CENTER',
    itemSpacing: 8,
    paddingTop: 10,
    paddingRight: 12,
    paddingBottom: 10,
    paddingLeft: 12,
    fills: [
      {
        type: 'SOLID',
        visible: true,
        opacity: 1,
        color: { r: 0.1, g: 0.2, b: 0.3, a: 1 },
      },
    ],
    strokes: [
      {
        type: 'SOLID',
        visible: true,
        color: { r: 1, g: 1, b: 1, a: 1 },
      },
    ],
    strokeWeight: 1,
    cornerRadius: 6,
    effects: [
      {
        type: 'DROP_SHADOW',
        visible: true,
        color: { r: 0, g: 0, b: 0, a: 0.2 },
        offset: { x: 0, y: 2 },
        radius: 8,
        spread: 0,
      },
    ],
    ...overrides,
  };
}

const textNode = {
  id: '1:4',
  name: 'Button label',
  type: 'TEXT',
  visible: true,
  characters: 'Continue now',
  absoluteBoundingBox: { x: 32, y: 40, width: 80, height: 16 },
  style: {
    fontFamily: 'Inter',
    fontPostScriptName: 'Inter-SemiBold',
    fontStyle: 'Semi Bold',
    fontWeight: 600,
    fontSize: 14,
    lineHeightPx: 20,
    letterSpacing: 0,
    textAlignHorizontal: 'CENTER',
    textAlignVertical: 'CENTER',
  },
  characterStyleOverrides: [0, 0, 1],
  styleOverrideTable: {
    1: {
      fontFamily: 'Inter',
      fontSize: 12,
      fontWeight: 400,
      fills: [
        {
          type: 'SOLID',
          color: { r: 1, g: 0, b: 0, a: 1 },
        },
      ],
    },
  },
  fills: [
    {
      type: 'SOLID',
      visible: true,
      color: { r: 1, g: 1, b: 1, a: 1 },
    },
  ],
};

describe('normalizePaintColor', () => {
  it('returns Figma RGBA, CSS rgba, and hex values', () => {
    assert.deepEqual(normalizePaintColor({ r: 0.1, g: 0.2, b: 0.3, a: 0.5 }), {
      figma: { r: 0.1, g: 0.2, b: 0.3, a: 0.5 },
      css: 'rgba(26, 51, 77, 0.5)',
      hex: '#1A334D',
    });
  });
});

describe('normalizeDesignProperties', () => {
  it('normalizes layout, text, color, radius, shadow, component, and CSS hint fields', () => {
    const design = normalizeDesignProperties({
      nodes: [
        frameNode({
          componentId: 'component-id',
          componentKey: 'component-key',
          componentName: 'Button / Primary',
          variantProperties: { Size: 'Medium' },
          componentProperties: { Disabled: { type: 'BOOLEAN', value: false } },
        }),
        textNode,
      ],
      contextTree: {
        siblings: [
          { id: '1:3', absoluteBoundingBox: { x: 20, y: 30, width: 120, height: 40 } },
          { id: '1:7', absoluteBoundingBox: { x: 20, y: 82, width: 120, height: 40 } },
        ],
      },
    });

    assert.equal(design.schemaVersion, 'figma-design-properties/v1');
    const frame = design.nodes.find((entry) => entry.id === '1:3');
    const text = design.nodes.find((entry) => entry.id === '1:4');

    assert.equal(frame.normalized.width, '120px');
    assert.equal(frame.normalized.height, '40px');
    assert.equal(frame.normalized.display, 'flex');
    assert.equal(frame.normalized.flexDirection, 'row');
    assert.equal(frame.normalized.gap, '8px');
    assert.equal(frame.normalized.padding, '10px 12px 10px 12px');
    assert.equal(frame.normalized.backgroundColor.hex, '#1A334D');
    assert.equal(frame.normalized.borderRadius, '6px');
    assert.equal(frame.normalized.border, '1px solid rgba(255, 255, 255, 1)');
    assert.equal(frame.normalized.boxShadowHint, '0px 2px 8px 0px rgba(0, 0, 0, 0.2)');
    assert.equal(frame.normalized.inferredSpacing.afterY, 12);
    assert.equal(frame.raw.componentKey, 'component-key');
    assert.equal(frame.normalized.componentName, 'Button / Primary');

    assert.equal(text.normalized.fontFamily, 'Inter');
    assert.equal(text.normalized.fontSize, '14px');
    assert.equal(text.normalized.fontWeight, 600);
    assert.equal(text.normalized.lineHeight, '20px');
    assert.equal(text.normalized.color.hex, '#FFFFFF');
    assert.equal(text.raw.styleRanges.length, 2);
  });

  it('writes null missing fields and warns instead of guessing uncertain values', () => {
    const design = normalizeDesignProperties({
      nodes: [
        {
          id: '2:1',
          name: 'Auto line height text',
          type: 'TEXT',
          characters: 'Hello',
          style: {
            fontFamily: 'Inter',
            fontSize: 16,
            lineHeightUnit: 'AUTO',
          },
        },
      ],
      contextTree: { siblings: [] },
    });

    const text = design.nodes[0];
    assert.equal(text.normalized.lineHeight, null);
    assert.equal(design.warnings.includes('line_height_auto:2:1'), true);
    assert.equal(text.raw.absoluteBoundingBox, null);
    assert.equal(design.missingFields.includes('2:1.absoluteBoundingBox'), true);
  });

  it('marks nodes without core id, name, or type as malformed', () => {
    const design = normalizeDesignProperties({
      nodes: [{ id: '3:1', type: 'FRAME' }],
      contextTree: { siblings: [] },
    });

    assert.equal(design.nodes[0].warnings.includes('node_malformed'), true);
  });

  it('normalizes a sanitized real Figma smoke fixture shape', async () => {
    const fixturePath = path.join(import.meta.dirname, 'fixtures', 'design-node-sample.json');
    const fixture = JSON.parse(await fs.readFile(fixturePath, 'utf8'));

    const design = normalizeDesignProperties({
      nodes: fixture.nodes,
      contextTree: fixture.contextTree,
    });

    const target = design.nodes.find((entry) => entry.id === '6127:21193');
    const title = design.nodes.find((entry) => entry.id === 'I6127:21193;51559:2731');

    assert.equal(target.normalized.display, 'flex');
    assert.equal(target.normalized.flexDirection, 'column');
    assert.equal(target.normalized.gap, '4px');
    assert.deepEqual(target.normalized.inferredSpacing, { afterY: 8 });
    assert.equal(target.normalized.backgroundColor.css, 'rgba(0, 0, 0, 0)');
    assert.equal(target.normalized.componentName, 'KsTitle');
    assert.equal(target.normalized.componentProperties.size.value, 'small');

    assert.equal(title.normalized.fontFamily, 'TikTok Sans Text');
    assert.equal(title.normalized.fontWeight, 500);
    assert.equal(title.normalized.fontSize, '14px');
    assert.equal(title.normalized.lineHeight, '20px');
    assert.equal(title.normalized.color.hex, '#121415');
    assert.equal(design.warnings.length, 0);
  });
});

describe('buildCssHints', () => {
  it('emits deterministic CSS declarations and warnings for uncertain values', () => {
    const design = normalizeDesignProperties({
      nodes: [
        frameNode(),
        {
          ...textNode,
          id: '1:8',
          name: 'Auto text',
          style: {
            ...textNode.style,
            lineHeightUnit: 'AUTO',
            lineHeightPx: undefined,
          },
        },
      ],
      contextTree: { siblings: [] },
    });

    const css = buildCssHints(design);

    assert.match(css, /font-family: Inter;/);
    assert.match(css, /background-color: rgba\(26, 51, 77, 1\);/);
    assert.match(css, /border-radius: 6px;/);
    assert.match(css, /padding: 10px 12px 10px 12px;/);
    assert.match(css, /\/\* line-height is AUTO in Figma; no deterministic CSS hint emitted \*\//);
  });
});
