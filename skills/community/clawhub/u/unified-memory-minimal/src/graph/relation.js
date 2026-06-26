/**
 * Relationship Extraction - 抽取实体间关系
 * 关系类型：WORKED_WITH, BELONGS_TO, USES_TOOL, PARTICIPATED_IN, DECIDED, CREATED, RELATED_TO
 *
 * @module graph/relation
 */

// 关系类型定义
export const RELATION_TYPES = {
  WORKED_WITH: 'worked_with',
  BELONGS_TO: 'belongs_to',
  USES_TOOL: 'uses_tool',
  PARTICIPATED_IN: 'participated_in',
  DECIDED: 'decided',
  CREATED: 'created',
  RELATED_TO: 'related_to',
};

// 关系 ID 格式：rel_${Date.now()}_${random}
export function generateRelationId() {
  return `rel_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
}

/**
 * 关键词模式 → 关系类型映射
 * @type {Array<{ patterns: RegExp[], relation: string, direction: 'forward' | 'backward' }>}
 */
const RELATION_PATTERNS = [
  // worked_with: 和...一起、跟...合作、与...协作
  {
    patterns: [/(?:和|跟|与|同)[^，。！？、\n]{0,20}(?:一起|合作|协作|讨论|开会|工作)/g],
    relation: RELATION_TYPES.WORKED_WITH,
    direction: 'bidirectional',
  },
  // uses_tool: 使用、采用、用、借助
  {
    patterns: [
      /(?:使用|采用|借助|用|依赖|基于|通过)(?:了)?(?:工具|框架|平台|软件|语言|系统)?\s*([^\s，。！？、\n]{1,30})/g,
    ],
    relation: RELATION_TYPES.USES_TOOL,
    direction: 'forward',
  },
  // participated_in: 参加、参与、出席、加入了
  {
    patterns: [
      /(?:参加|参与|出席|加入|参加了|参与了)\s*([^\s，。！？、\n]{1,30})(?:会议|讨论|评审|活动|项目|培训|周会|例会)?/g,
    ],
    relation: RELATION_TYPES.PARTICIPATED_IN,
    direction: 'forward',
  },
  // decided: 决定、选定、拍板、敲定
  {
    patterns: [
      /(?:我|我们|刘总|老板|领导|他|她)(?:决定|选定|拍板|敲定|选择)(?:了)?\s*([^\s，。！？、\n]{1,30})/g,
    ],
    relation: RELATION_TYPES.DECIDED,
    direction: 'forward',
  },
  // created: 创建、开发、建立、搭建了
  {
    patterns: [
      /(?:创建|开发|建立|搭建|实现|构建)(?:了)?\s*([^\s，。！？、\n]{1,30})(?:项目|系统|平台|应用|工具|网站|服务)?/g,
    ],
    relation: RELATION_TYPES.CREATED,
    direction: 'forward',
  },
  // belongs_to: 属于、旗下、是...的、...的团队
  {
    patterns: [
      /([^\s，、。！？]{1,20})(?:是|属于|旗下)(?:的)?([^\s，。！？]{1,20})(?:团队|部门|公司|组织|机构|项目)/g,
      /([^\s，。！？]{1,20})(?:团队|部门|公司|组织)(?:的)?([^\s，。！？]{1,20})/g,
    ],
    relation: RELATION_TYPES.BELONGS_TO,
    direction: 'backward',
  },
];

/**
 * 从文本中抽取实体对之间的关系
 * @param {string} text
 * @param {Array<{ id: string, name: string, type: string }>} entities
 * @param {object} options
 * @returns {Promise<Array<{ id: string, from: string, to: string, relation: string, confidence: number, source: string }>>}
 */
export async function extractRelations(text, entities, options = {}) {
  if (!entities || entities.length === 0) return [];

  /** @type {Array<{ id: string, from: string, to: string, relation: string, confidence: number, source: string }>} */
  const relations = [];

  // Build entity name lookup for faster matching
  const entityNames = entities.map(e => e.name);

  // Pattern-based relation extraction
  for (const { patterns, relation, direction } of RELATION_PATTERNS) {
    for (const pattern of patterns) {
      pattern.lastIndex = 0;
      let match;

      while ((match = pattern.exec(text)) !== null) {
        let fromName = null;
        let toName = null;

        if (direction === 'forward' || direction === 'bidirectional') {
          // Find which entity appears before or as the match
          const beforeText = text.slice(0, match.index);
          const afterText = text.slice(match.index + match[0].length);

          // Try to find entities in context
          for (const name of entityNames) {
            // Check if entity appears right before the pattern
            const beforeIdx = beforeText.lastIndexOf(name);
            if (beforeIdx !== -1 && beforeIdx > beforeText.lastIndexOf(/[。！？\n]/)) {
              fromName = name;
            }
            // Check if entity appears right after the pattern
            if (afterText.startsWith(name)) {
              toName = name;
            }
          }

          // If forward and we captured a group
          if (!toName && match[1]) {
            // Try to match captured group to an entity
            const captured = match[1].trim();
            for (const name of entityNames) {
              if (captured.includes(name) || name.includes(captured)) {
                toName = name;
                break;
              }
            }
            if (!toName && captured.length > 0) {
              toName = captured;
            }
          }
        }

        if (direction === 'backward') {
          // Backward: subject after pattern
          if (match[1]) {
            for (const name of entityNames) {
              if (match[1].includes(name)) {
                fromName = name;
                break;
              }
            }
            if (!fromName) fromName = match[1].trim();
          }
          if (match[2]) {
            for (const name of entityNames) {
              if (match[2].includes(name)) {
                toName = name;
                break;
              }
            }
            if (!toName) toName = match[2].trim();
          }
        }

        if (direction === 'bidirectional') {
          // Try to find two entities in the surrounding context
          const context = text.slice(Math.max(0, match.index - 50), match.index + match[0].length + 50);
          const found = entityNames.filter(n => context.includes(n));
          if (found.length >= 2) {
            fromName = found[0];
            toName = found[1];
          }
        }

        if (fromName && toName && fromName !== toName) {
          // Map entity names to IDs
          const fromEntity = entities.find(e => e.name === fromName);
          const toEntity = entities.find(e => e.name === toName);

          if (fromEntity && toEntity) {
            relations.push({
              id: generateRelationId(),
              from: fromEntity.id,
              to: toEntity.id,
              relation,
              confidence: 0.7,
              source: match[0].slice(0, 50),
            });
          }
        }
      }
    }
  }

  // Co-occurrence based relations: entities appearing in same sentence
  const sentences = text.split(/[。！？\n]/);
  for (const sentence of sentences) {
    const foundInSentence = entities.filter(e => sentence.includes(e.name));
    if (foundInSentence.length >= 2) {
      // Add co-occurrence relations with lower confidence
      for (let i = 0; i < foundInSentence.length; i++) {
        for (let j = i + 1; j < foundInSentence.length; j++) {
          const fromEntity = foundInSentence[i];
          const toEntity = foundInSentence[j];

          // Check not already added
          const exists = relations.some(
            r => (r.from === fromEntity.id && r.to === toEntity.id) ||
                 (r.from === toEntity.id && r.to === fromEntity.id)
          );

          if (!exists) {
            relations.push({
              id: generateRelationId(),
              from: fromEntity.id,
              to: toEntity.id,
              relation: RELATION_TYPES.RELATED_TO,
              confidence: 0.4,
              source: sentence.slice(0, 50),
            });
          }
        }
      }
    }
  }

  // Deduplicate by from+to+relation
  const seen = new Set();
  const deduped = relations.filter(r => {
    const key = `${r.from}::${r.to}::${r.relation}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });

  return deduped;
}

/**
 * 构建邻接表
 * @param {Array<{ from: string, to: string, relation: string, confidence: number }>} relations
 * @returns {Map<string, Array<{ neighbor: string, relation: string, weight: number }>>}
 */
export function buildAdjacencyList(relations) {
  /** @type {Map<string, Array<{ neighbor: string, relation: string, weight: number }>>} */
  const adj = new Map();

  for (const r of relations) {
    if (!adj.has(r.from)) {
      adj.set(r.from, []);
    }
    adj.get(r.from).push({
      neighbor: r.to,
      relation: r.relation,
      weight: r.confidence || 1.0,
    });

    // For bidirectional-like relations (worked_with, related_to), add reverse edge
    if (r.relation === RELATION_TYPES.WORKED_WITH || r.relation === RELATION_TYPES.RELATED_TO) {
      if (!adj.has(r.to)) {
        adj.set(r.to, []);
      }
      adj.get(r.to).push({
        neighbor: r.from,
        relation: r.relation,
        weight: r.confidence || 1.0,
      });
    }
  }

  return adj;
}

/**
 * 获取某实体的所有邻居
 * @param {string} entityId
 * @param {Array<{ from: string, to: string, relation: string, confidence: number }>} relations
 * @returns {Array<{ entityId: string, relation: string, weight: number }>}
 */
export function getNeighbors(entityId, relations) {
  const neighbors = [];

  for (const r of relations) {
    if (r.from === entityId) {
      neighbors.push({ entityId: r.to, relation: r.relation, weight: r.confidence || 1.0 });
    }
    // Include reverse for symmetric relations
    if (r.to === entityId && (r.relation === RELATION_TYPES.WORKED_WITH || r.relation === RELATION_TYPES.RELATED_TO)) {
      neighbors.push({ entityId: r.from, relation: r.relation, weight: r.confidence || 1.0 });
    }
  }

  return neighbors;
}

/**
 * BFS 图查询
 * @param {string} startEntityId
 * @param {Array<{ from: string, to: string, relation: string, confidence: number }>} relations
 * @param {number} depth
 * @param {string|null} relationType
 * @returns {Array<{ path: string[], relations: string[], totalWeight: number }>}
 */
export function queryGraphPaths(startEntityId, relations, depth = 1, relationType = null) {
  /** @type {Array<{ path: string[], relations: string[], totalWeight: number }>} */
  const results = [];

  /** @type {Map<string, boolean>} */
  const visited = new Map();
  visited.set(startEntityId, true);

  /** @type {Array<{ current: string, path: string[], relations: string[], weight: number }>} */
  const queue = [{ current: startEntityId, path: [startEntityId], relations: [], weight: 1.0 }];

  while (queue.length > 0) {
    const { current, path, relations: pathRels, weight } = queue.shift();

    if (path.length > depth + 1) continue;

    const neighbors = getNeighbors(current, relations);

    for (const n of neighbors) {
      if (visited.has(n.entityId) && path.length > 1) continue;

      const newPath = [...path, n.entityId];
      const newRels = [...pathRels, n.relation];
      const newWeight = weight * n.weight;

      if (relationType && n.relation !== relationType) continue;

      if (newPath.length >= 2) {
        results.push({
          path: newPath,
          relations: newRels,
          totalWeight: newWeight,
        });
      }

      visited.set(n.entityId, true);
      queue.push({ current: n.entityId, path: newPath, relations: newRels, weight: newWeight });
    }
  }

  return results;
}
