/**
 * skill-sediment 插件的类型定义。
 */

// ---------------------------------------------------------------------------
// 技能管理
// ---------------------------------------------------------------------------

/** skill_manage 工具支持的动作类型。 */
export type SkillManageAction =
  | "create"
  | "edit"
  | "patch"
  | "delete"
  | "write_file"
  | "remove_file"
  | "view"
  | "list"
  | "promote";

/** skill_manage 调用参数。 */
export interface SkillManageParams {
  action: SkillManageAction;
  name?: string;
  content?: string;
  file_path?: string;
  file_content?: string;
  old_string?: string;
  new_string?: string;
  replace_all?: boolean;
  /**
   * `promote` 动作专用：review subagent 引用的"二次召回证据"
   */
  promote_reason?: string;
}

/** skill_manage 动作执行结果。 */
export interface SkillManageResult {
  success: boolean;
  message?: string;
  error?: string;
  path?: string;
  hint?: string;
  skill_md?: string;
  file_preview?: string;
  available_files?: string[];
  rejectionTag?: string;
  /** list action 返回的技能摘要列表。 */
  skills?: Array<{
    name: string;
    description: string;
    path: string;
    source?: SkillSource | string;
    revisionCount?: number;
    /**
     * 技能位置/可写性标识（与 listSkills 实际产出保持一致）：
     * - "sediment"        ：物理位于 sediment_skills/ 下（未启用，可写）
     * - "sediment-active" ：位于 skills/ 下，但 originSource === "SEDIMENT"（已启用沉淀，可写）
     * - "official"        ：source === "OFFICIAL"（只读）
     * - "native"          ：位于 skills/ 下的其它来源（只读）
     */
    location: SkillLocation;
  }>;
  /** view action 返回的完整 SKILL.md 内容。 */
  skill_content?: string;
  /** 技能来源（view action 返回）。 */
  source?: SkillSource | string;
  /**
   * 技能位置/可写性标识（view action 返回）。
   * 语义与 list 中的 `skills[].location` 一致，方便消费方
   * 不依赖 message 文本即可判断技能可操作性。
   */
  location?: SkillLocation;
}

/**
 * 技能位置/可写性标识。
 * 由 list / view 输出，供消费方判断技能是否可被本插件修改。
 */
export type SkillLocation = "sediment" | "sediment-active" | "official" | "native";

// ---------------------------------------------------------------------------
// 安全扫描（skills guard）
// ---------------------------------------------------------------------------

/** 风险发现严重级别。 */
export type FindingSeverity = "critical" | "high" | "medium" | "low";

/** 威胁分类。 */
export type ThreatCategory =
  | "exfiltration"
  | "injection"
  | "destructive"
  | "persistence"
  | "network"
  | "obfuscation"
  | "execution"
  | "traversal"
  | "mining"
  | "supply_chain"
  | "privilege_escalation"
  | "credential_exposure";

/** 技能来源信任级别。 */
export type TrustLevel = "builtin" | "trusted" | "community" | "agent-created";

/** 扫描结论（整体风险判断）。 */
export type ScanVerdict = "safe" | "caution" | "dangerous";

/** 安装策略判定。 */
export type InstallDecision = "allow" | "block" | "ask";

/** 单条威胁模式定义。 */
export interface ThreatPattern {
  regex: RegExp;
  patternId: string;
  severity: FindingSeverity;
  category: ThreatCategory;
  description: string;
  /** 标记此模式需要跨行匹配（如 [\s\S]*?），逐行扫描无法检测，需额外全文扫描。 */
  multiline?: boolean;
}

/** 单条扫描发现。 */
export interface Finding {
  patternId: string;
  severity: FindingSeverity;
  category: ThreatCategory;
  file: string;
  line: number;
  match: string;
  description: string;
}

/** 完整扫描结果。 */
export interface ScanResult {
  skillName: string;
  source: string;
  trustLevel: TrustLevel;
  verdict: ScanVerdict;
  findings: Finding[];
  scannedAt: string;
  summary: string;
}

// ---------------------------------------------------------------------------
// Frontmatter（扩展字段）
// ---------------------------------------------------------------------------

/**
 * SKILL.md frontmatter 扩展字段（在 name/description 之外）。
 * - platforms：运行平台约束（例如 ["linux", "macos"]）
 * - prerequisites：前置命令或环境变量
 * - compatibility：兼容性说明
 * - version：技能版本号
 * - tags：检索/过滤标签
 */
export interface SkillFrontmatter {
  name: string;
  description: string;
  platforms?: string[];
  prerequisites?: SkillPrerequisites;
  compatibility?: string;
  version?: string;
  tags?: string[];
}

/** 技能前置条件。 */
export interface SkillPrerequisites {
  commands?: string[];
  env_vars?: string[];
}

/** 允许的平台标识。 */
export const VALID_PLATFORMS = new Set([
  "linux",
  "macos",
  "windows",
  "darwin",
  "freebsd",
  "openbsd",
  "android",
  "ios",
]);

// ---------------------------------------------------------------------------
// 技能元数据
// ---------------------------------------------------------------------------

/** 技能来源标识。 */
export type SkillSource = "LOCAL_GENERATED" | "OFFICIAL";

/**
 * 技能"原始来源"标识（启用迁移后由 starter 写入）。
 *
 * 沉淀技能在 sediment_skills/ 阶段没有此字段；
 * 当被 starter 的 enable_seal_skill 接口迁移到 skills/ 后，
 * starter 会重写 meta 并打上 originSource，作为追踪/权限识别的关键字段。
 */
export type SkillOriginSource = "SEAL" | "SEDIMENT";

/**
 * 技能修改动作类型（记录在元数据中）。
 *
 * 注意：故意不包含 "delete"——删除技能后整个目录连同 meta 一起被移除，
 * 没有载体记录这次操作；只对仍存在的技能记录变更历史。
 */
export type SkillMetaAction =
  | "create"
  | "edit"
  | "patch"
  | "write_file"
  | "remove_file"
  | "promote";

/** 单条修改历史记录。 */
export interface SkillEditRecord {
  /** 修改动作。 */
  action: SkillMetaAction;
  /** 修改时间（ISO 8601）。 */
  at: string;
  /** 修改摘要（可选，如 patch 的目标文件、edit 的内容长度等）。 */
  summary?: string;
}

/**
 * 与技能一起存储的元数据（`__skill_meta__.json`）。
 */
export interface SkillMeta {
  source: SkillSource | string;
  /**
   * 启用迁移后由 starter 写入的"原始来源"字段。
   * 沉淀阶段的 meta 没有此字段；
   * 启用后值为 "SEDIMENT" 表示这条技能曾经是沉淀技能，本插件仍然有权管理它。
   */
  originSource?: SkillOriginSource | string;
  /**
   * 安装/最近本地修改时间（ISO 8601）。
   * starter 在 installSkill / moveSealSkillToSkills 中写入；
   * 本插件每次写动作后刷新为当前时间，作为平台 listSkills 的"最近变更"展示来源。
   */
  installedAt?: string;
  /**
   * 透传 starter `SkillMetaFile` 已声明的字段（id / code / name / enname /
   * version / desc / type / agentId / url）。本插件**不得**在此塞自定义扩展
   * 字段——任何新东西都应进 {@link SedimentMeta}。
   */
  [extraField: string]: unknown;
}

/**
 * 沉淀插件私有的修改细节元数据（`__sediment_meta__.json`）。
 *
 * **重要：该文件不会被 starter 透传给外部接口。**
 * 用于隔离本插件维护的修改细节（创建时间、修订次数、修改历史、最近动作等），
 * 避免 `__skill_meta__.json` 被这些字段污染、随平台接口外泄。
 *
 * 字段所有权：
 *  - 全部由本插件 ({@link updateMeta}) 写入和读取；starter 不感知。
 *  - 历史数据迁移：若读取时该文件不存在但旧版 `__skill_meta__.json`
 *    含有这些字段，{@link readSedimentMeta} 会自动迁移并把对应字段从
 *    `__skill_meta__.json` 中清除。
 */
export interface SedimentMeta {
  /** 首次创建时间（ISO 8601）。 */
  createdAt: string;
  /** 最近一次本插件修改时间（ISO 8601）。 */
  updatedAt: string;
  /**最近一次被"访问"的时间（ISO 8601），用于 LRU 回收排序。*/
  lastTouchedAt?: string;
  /** 最近一次修改的动作类型。 */
  lastAction?: SkillMetaAction;
  /** 累计修改次数（create 算第 1 次）。 */
  revisionCount?: number;
  /** 最近 N 条修改历史（最新在前，上限 10 条）。 */
  editHistory?: SkillEditRecord[];
  /**技能从 sediment_skills/ 升级到 skills/ 的时间（ISO 8601）。*/
  promotedAt?: string;
  /**
   *  - "auto" ：review subagent 二次召回后自动 promote
   *  - "user" ：用户在前端手动启用（由 starter 写入，向后兼容保留）
   */
  promotedBy?: "auto" | "user";
  /**promote 时记录的"二次召回证据"，对应 SkillManageParams.promote_reason*/
  promotedReason?: string;
  /**review subagent 二次命中并采用（promote）该 sediment 技能的累计次数。*/
  reviewMatchedCount?: number;
  /**该 sediment 在哪个父会话（parent sessionKey）中被创建。*/
  createdInParentSession?: string;
}

// ---------------------------------------------------------------------------
// 常量
// ---------------------------------------------------------------------------

/** 技能名最大字符数。 */
export const MAX_NAME_LENGTH = 64;

/** frontmatter 中 description 最大字符数。 */
export const MAX_DESCRIPTION_LENGTH = 1024;

/** SKILL.md 最大字符数。 */
export const MAX_SKILL_CONTENT_CHARS = 100_000;

/** 附属文件最大字节数。 */
export const MAX_SKILL_FILE_BYTES = 1_048_576; // 1 MiB

/** 合法技能名正则（小写字母、数字、点、下划线、连字符）。 */
export const VALID_NAME_RE = /^[a-z0-9][a-z0-9._-]*$/;

/** write_file/remove_file 允许写入的子目录。 */
export const ALLOWED_SUBDIRS = new Set(["references", "templates", "scripts", "assets"]);
