import assert from 'node:assert/strict';
import { describe, it } from 'node:test';

import { expandFigmaNodeContext } from '../scripts/lib/figma-node-expander.mjs';

const budgets = {
  maxParentDepth: 6,
  maxChildDepth: 4,
  maxSiblings: 16,
  maxNodesPerUrl: 600,
  maxScreenshotsPerUrl: 24,
  maxArtifactMiBPerUrl: 100,
  screenshotScale: 2,
};

function node(id, name, type, children = [], extra = {}) {
  return {
    id,
    name,
    type,
    absoluteBoundingBox: extra.absoluteBoundingBox ?? { x: 0, y: 0, width: 100, height: 40 },
    ...extra,
    children,
  };
}

const textTarget = node('1:4', 'Button label', 'TEXT', [], {
  characters: 'Continue',
  absoluteBoundingBox: { x: 20, y: 20, width: 48, height: 16 },
});
const sibling = node('1:5', 'Secondary action', 'INSTANCE');
const buttonFrame = node('1:3', 'Primary button', 'FRAME', [textTarget, sibling], {
  layoutMode: 'HORIZONTAL',
  itemSpacing: 8,
  paddingLeft: 12,
  paddingRight: 12,
});
const section = node('1:2', 'Age gate modal', 'FRAME', [buttonFrame, node('1:6', 'Cancel', 'TEXT')]);
const page = node('1:1', 'Page 1', 'CANVAS', [section]);

describe('expandFigmaNodeContext', () => {
  it('builds parents, children, siblings, and candidates with stable source tags', () => {
    const context = expandFigmaNodeContext({
      targetNodeId: '1:4',
      rootNode: page,
      budgets,
    });

    assert.equal(context.schemaVersion, 'figma-context-tree/v1');
    assert.equal(context.target.id, '1:4');
    assert.deepEqual(
      context.parents.map((entry) => entry.id),
      ['1:3', '1:2', '1:1'],
    );
    assert.deepEqual(
      context.siblings.map((entry) => entry.id),
      ['1:5'],
    );
    assert.equal(context.children.length, 0);
    assert.deepEqual(
      context.candidates.map((entry) => ({ id: entry.id, source: entry.source })),
      [
        { id: '1:4', source: 'target' },
        { id: '1:3', source: 'layout-container' },
        { id: '1:5', source: 'sibling' },
      ],
    );
  });

  it('marks small leaf targets as maybe child nodes and prefers the nearest layout container', () => {
    const context = expandFigmaNodeContext({
      targetNodeId: '1:4',
      rootNode: page,
      budgets,
    });

    assert.equal(context.warnings.includes('target_may_be_child_node'), true);
    assert.equal(context.bestTargetInterpretation.id, '1:3');
    assert.equal(context.bestTargetInterpretation.reason, 'nearest_layout_container_for_leaf_target');
  });

  it('marks broad targets and limits candidate children by the node budget', () => {
    const children = Array.from({ length: 8 }, (_, index) =>
      node(`2:${index + 1}`, `Child ${index + 1}`, 'FRAME'),
    );
    const broadRoot = node('2:0', 'Huge frame', 'FRAME', children, {
      absoluteBoundingBox: { x: 0, y: 0, width: 3000, height: 2400 },
    });

    const context = expandFigmaNodeContext({
      targetNodeId: '2:0',
      rootNode: broadRoot,
      budgets: { ...budgets, maxNodesPerUrl: 5, maxChildDepth: 1 },
    });

    assert.equal(context.warnings.includes('target_too_broad'), true);
    assert.equal(context.warnings.includes('expansion_budget_exceeded'), true);
    assert.equal(context.children.length <= 4, true);
    assert.equal(context.candidates.some((entry) => entry.source === 'child'), true);
  });

  it('throws a stable error when the target node cannot be found', () => {
    assert.throws(
      () =>
        expandFigmaNodeContext({
          targetNodeId: '9:9',
          rootNode: page,
          budgets,
        }),
      { code: 'figma_target_not_found_in_context' },
    );
  });
});
