// types.ts — PvPoke rankings + IV 数据与查询结果类型定义

/** PvPoke 单条宝可梦记录 */
export interface PvPokePokemon {
  speciesId: string;
  speciesName: string;
  rating: number;
  score: number;
  scores: number[];
  editorScore: number | null;
  editorNotes: string;
  types: string[];
  cp: number;
  level: number;
  moves: {
    fastMoves: { moveId: string; uses: number }[];
    chargedMoves: { moveId: string; uses: number }[];
  };
  moveset: string[];
  stats: {
    product: number;
    atk: number;
    def: number;
    hp: number;
  };
  matchups: { opponent: string; rating: number }[];
  counters: { opponent: string; rating: number }[];
}

/** 联盟配置 */
export interface LeagueInfo {
  key: number | 'master';
  label: string;
  cpLimit: number;
  fileName: string;
}

/** gamemaster 中的宝可梦基础数据 */
export interface PokemonBase {
  speciesId: string;
  speciesName: string;
  atk: number;
  def: number;
  sta: number;
  types: string[];
}

/** 单条 IV 排名记录（无 product 字段） */
export interface IVRecord {
  iv: [number, number, number]; // atk/def/hp IV
  cp: number;
  level: number;
  rank: number;
}

/** IV 查询结果 */
export interface IVResult {
  best: IVRecord;
  top50: IVRecord[];
  total: number;
}

/** 查询结果（含 IV） */
export interface QueryResult {
  pokemon: string;
  speciesName: string;
  league: string;
  rank: number;
  score: number;
  rating: number;
  editorScore: number | null;
  recommendedMoves: string[];
  fastMoves: string[];
  chargeMoves: string[];
  stats: { atk: number; def: number; hp: number; product: number };
  matchups: { opponent: string; rating: number }[];
  counters: { opponent: string; rating: number }[];
  sixScores: string;
  cp: number;
  level: number;
  types: string[];
  /** 最佳 IV 信息 */
  bestIV: IVRecord | null;
  /** 所有 IV 排名（仅前50） */
  ivTop50: IVRecord[];
  /** 用户输入的 IV（可选） */
  userIV: {
    iv: string;          // "a/d/s"
    record: IVRecord | null;
    inTop50: boolean;
    /** IV 差值：最佳 IV vs 用户 IV，如 { atk: -1, def: 0, hp: -5 } */
    ivDiff: { atk: number; def: number; hp: number } | null;
  } | null;
  source: string;
  fetchedAt: string;
}

/** 命令解析结果 */
export interface CommandParse {
  pokemon: string;
  league: string;
  userIV: string | null;   // "a/d/s" or null
  valid: boolean;
  error?: string;
  suggestions?: string[];
}
