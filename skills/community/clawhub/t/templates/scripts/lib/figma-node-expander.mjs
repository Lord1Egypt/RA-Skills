import { createStableError } from './redact.mjs';

const LEAF_TYPES = new Set(['TEXT', 'VECTOR', 'BOOLEAN_OPERATION', 'LINE', 'ELLIPSE', 'POLYGON', 'STAR', 'IMAGE']);
const BROAD_TYPES = new Set(['DOCUMENT', 'CANVAS', 'SECTION']);

function childrenOf(node) {
  return Array.isArray(node?.children) ? node.children : [];
}

function summarizeNode(node, extra = {}) {
  return {
    id: node?.id ?? null,
    name: node?.name ?? null,
    type: node?.type ?? null,
    visible: node?.visible ?? true,
    absoluteBoundingBox: node?.absoluteBoundingBox ?? null,
    layoutMode: node?.layoutMode ?? null,
    componentId: node?.componentId ?? null,
    componentKey: node?.componentKey ?? null,
    componentProperties: node?.componentProperties ?? null,
    variantProperties: node?.variantProperties ?? null,
    ...extra,
  };
}

function traverse(node, visitor, depth = 0, parent = null, parentChain = []) {
  visitor(node, depth, parent, parentChain);
  for (const child of childrenOf(node)) {
    traverse(child, visitor, depth + 1, node, [parent, ...parentChain].filter(Boolean));
  }
}

function findTarget(rootNode, targetNodeId) {
  let result = null;
  traverse(rootNode, (node, depth, parent, parentChain) => {
    if (node?.id === targetNodeId) {
      result = { node, depth, parent, parentChain };
    }
  });
  return result;
}

function collectChildren(node, maxDepth, remainingBudget) {
  const output = [];
  function walk(current, depth) {
    if (depth > maxDepth || output.length >= remainingBudget) {
      return;
    }
    for (const child of childrenOf(current)) {
      if (output.length >= remainingBudget) {
        return;
      }
      output.push(summarizeNode(child, { depth, source: 'child' }));
      walk(child, depth + 1);
    }
  }
  walk(node, 1);
  return output;
}

function isLeafTarget(node) {
  return LEAF_TYPES.has(node?.type) || childrenOf(node).length === 0;
}

function isBroadTarget(node, budgets) {
  if (BROAD_TYPES.has(node?.type)) {
    return true;
  }
  const box = node?.absoluteBoundingBox;
  if (box && (box.width >= 1800 || box.height >= 1400)) {
    return true;
  }
  let count = 0;
  traverse(node, () => {
    count += 1;
  });
  return count > budgets.maxNodesPerUrl;
}

function nearestLayoutContainer(targetInfo) {
  const chain = [targetInfo.parent, ...targetInfo.parentChain].filter(Boolean);
  return chain.find((node) => Boolean(node.layoutMode)) ?? chain[0] ?? null;
}

function pushCandidate(candidates, seen, node, source, extra = {}) {
  if (!node?.id || seen.has(`${node.id}:${source}`)) {
    return;
  }
  seen.add(`${node.id}:${source}`);
  candidates.push(summarizeNode(node, { source, ...extra }));
}

export function expandFigmaNodeContext({ targetNodeId, rootNode, budgets }) {
  const resolvedBudgets = {
    maxParentDepth: 6,
    maxChildDepth: 4,
    maxSiblings: 16,
    maxNodesPerUrl: 600,
    ...budgets,
  };
  const targetInfo = findTarget(rootNode, targetNodeId);
  if (!targetInfo) {
    throw createStableError('figma_target_not_found_in_context', 'Target node was not found in the Figma context tree');
  }

  const warnings = [];
  const parents = [targetInfo.parent, ...targetInfo.parentChain]
    .filter(Boolean)
    .slice(0, resolvedBudgets.maxParentDepth)
    .map((node, index) => summarizeNode(node, { depth: index + 1, source: 'parent' }));

  const siblings = targetInfo.parent
    ? childrenOf(targetInfo.parent)
        .filter((node) => node.id !== targetNodeId)
        .slice(0, resolvedBudgets.maxSiblings)
        .map((node) => summarizeNode(node, { source: 'sibling' }))
    : [];

  const remainingChildBudget = Math.max(0, resolvedBudgets.maxNodesPerUrl - 1 - parents.length - siblings.length);
  const children = collectChildren(targetInfo.node, resolvedBudgets.maxChildDepth, remainingChildBudget);

  const broad = isBroadTarget(targetInfo.node, resolvedBudgets);
  const leaf = isLeafTarget(targetInfo.node);
  if (broad) {
    warnings.push('target_too_broad');
  }
  if (leaf && targetInfo.parent) {
    warnings.push('target_may_be_child_node');
  }

  const expandedCount = 1 + parents.length + siblings.length + children.length;
  if (expandedCount >= resolvedBudgets.maxNodesPerUrl || broad) {
    warnings.push('expansion_budget_exceeded');
  }

  const candidates = [];
  const candidateSeen = new Set();
  pushCandidate(candidates, candidateSeen, targetInfo.node, 'target');

  const layoutContainer = nearestLayoutContainer(targetInfo);
  if (layoutContainer && layoutContainer.id !== targetInfo.node.id) {
    pushCandidate(candidates, candidateSeen, layoutContainer, 'layout-container');
  }

  if (broad) {
    for (const child of childrenOf(targetInfo.node).slice(0, resolvedBudgets.maxNodesPerUrl - 1)) {
      pushCandidate(candidates, candidateSeen, child, 'child');
    }
  }

  for (const sibling of siblings) {
    pushCandidate(candidates, candidateSeen, sibling, 'sibling');
  }

  if (targetInfo.node.componentId || targetInfo.node.componentKey || targetInfo.node.type === 'INSTANCE') {
    pushCandidate(candidates, candidateSeen, targetInfo.node, 'component-instance');
  }

  const bestTargetInterpretation =
    leaf && layoutContainer
      ? {
          id: layoutContainer.id,
          name: layoutContainer.name ?? null,
          type: layoutContainer.type ?? null,
          reason: 'nearest_layout_container_for_leaf_target',
        }
      : {
          id: targetInfo.node.id,
          name: targetInfo.node.name ?? null,
          type: targetInfo.node.type ?? null,
          reason: broad ? 'target_is_broad_context_node' : 'target_node',
        };

  return {
    schemaVersion: 'figma-context-tree/v1',
    target: summarizeNode(targetInfo.node, { source: 'target' }),
    parents,
    children,
    siblings,
    candidates,
    warnings: [...new Set(warnings)],
    budgets: resolvedBudgets,
    bestTargetInterpretation,
  };
}
