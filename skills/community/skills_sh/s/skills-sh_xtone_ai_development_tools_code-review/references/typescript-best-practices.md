# TypeScript ベストプラクティス

コードレビュー時にTypeScriptコードを評価するためのチェックリストです。

> 出典: [AWS 規範ガイダンス - TypeScript のベストプラクティス](https://docs.aws.amazon.com/ja_jp/prescriptive-guidance/latest/best-practices-cdk-typescript-iac/typescript-best-practices.html)

## 目次

- [型安全性](#型安全性)
- [列挙型の使用](#列挙型の使用)
- [インターフェイス設計](#インターフェイス設計)
- [デストラクチャリング](#デストラクチャリング)
- [命名規則](#命名規則)
- [変数宣言](#変数宣言)
- [アクセス修飾子](#アクセス修飾子)
- [ユーティリティ型](#ユーティリティ型)
- [設計パターン](#設計パターン)
- [リンター・フォーマッター](#リンターフォーマッター)

---

## 型安全性

### `any`型の使用を避ける（Major）

`any`型はTypeScriptの型チェックを無効化するため、バグの温床となる。
オブジェクトと関数の型を明示的に指定する。

```typescript
// ❌ any型の使用
function processData(data: any) {
    return data.value; // 型チェックが効かない
}

// ✅ 型を明示的に指定
type Result = "success" | "failure";

function verifyResult(result: Result) {
    if (result === "success") {
        console.log("Passed");
    } else {
        console.log("Failed");
    }
}
```

**レビュー観点：**
- [ ] `any`型が使用されていないか
- [ ] 関数の引数と戻り値に型が指定されているか
- [ ] ユニオン型やリテラル型で値の範囲を制限しているか

---

## 列挙型の使用

### 名前付き定数にはenumを使う（Minor）

関連する定数のグループにはenumを使用し、コードの可読性と保守性を高める。

```typescript
// ❌ マジックナンバーや文字列リテラルの直接使用
if (event === 0) {
    console.log("Created");
}

// ✅ enumで意味のある名前を付ける
enum EventType {
    Create,
    Delete,
    Update,
}

class InfraEvent {
    constructor(event: EventType) {
        if (event === EventType.Create) {
            console.log(`Event Captured: ${event}`);
        }
    }
}
```

**レビュー観点：**
- [ ] 関連する定数群がenumまたはユニオン型でグループ化されているか
- [ ] マジックナンバーや意味不明な文字列リテラルが散在していないか

---

## インターフェイス設計

### インターフェイスで契約を定義する（Major）

クラスやオブジェクトの形状をインターフェイスで定義し、型の一貫性を強制する。

```typescript
interface BucketProps {
    name: string;
    region: string;
    encryption: boolean;
}

class S3Bucket {
    constructor(props: BucketProps) {
        console.log(props.name);
    }
}
```

### readonlyプロパティを活用する（Minor）

変更されるべきでないプロパティには`readonly`を指定し、不変性を保証する。

```typescript
interface Position {
    readonly latitude: number;
    readonly longitude: number;
}
```

### インターフェイスの拡張でプロパティの重複を減らす（Minor）

共通プロパティを基底インターフェイスにまとめ、拡張で派生させる。

```typescript
// ❌ プロパティの重複
interface EncryptedVolume {
    name: string;
    keyName: string;
}

interface UnencryptedVolume {
    name: string;
    tags: string[];
}

// ✅ 共通プロパティを基底に抽出
interface BaseVolume {
    name: string;
}

interface EncryptedVolume extends BaseVolume {
    keyName: string;
}

interface UnencryptedVolume extends BaseVolume {
    tags: string[];
}
```

### 空のインターフェイスを避ける（Major）

空のインターフェイスは型の契約を強制せず、型安全性の恩恵を受けられない。

```typescript
// ❌ 空のインターフェイス - 任意のオブジェクトを受け入れてしまう
interface BucketProps {}

class S3Bucket implements BucketProps {
    constructor(props: BucketProps) {
        console.log(props);
    }
}

// 異なる構造のオブジェクトが両方とも受け入れられてしまう
const bucket1 = new S3Bucket({ name: "bucket", region: "us-east-1", encryption: false });
const bucket2 = new S3Bucket({ name: "bucket" });
```

**レビュー観点：**
- [ ] 空のインターフェイスが定義されていないか
- [ ] 共通プロパティが基底インターフェイスにまとめられているか
- [ ] 変更されないプロパティに`readonly`が付与されているか

---

## デストラクチャリング

### プロパティアクセスにデストラクチャリングを使う（Suggestion）

ES6のデストラクチャリングで冗長なプロパティアクセスを減らす。

```typescript
const config = {
    name: "myApp",
    scope: "global",
};

// ❌ 冗長なプロパティアクセス
const appName = config.name;
const appScope = config.scope;

// ✅ デストラクチャリング
const { name, scope } = config;
```

**レビュー観点：**
- [ ] 同一オブジェクトから複数プロパティを取得する際にデストラクチャリングが使われているか

---

## 命名規則

### 標準の命名規則に従う（Minor）

| 対象 | 規則 | 例 |
|------|------|-----|
| 変数・関数 | camelCase | `userName`, `getUserData()` |
| グローバル定数 | UPPER_CASE | `MAX_RETRY_ATTEMPTS`, `API_BASE_URL` |
| クラス・インターフェイス | PascalCase | `DatabaseConnection`, `UserProfile` |
| 型・列挙型 | PascalCase | `ResponseStatus`, `HttpStatusCode` |
| インターフェイスメンバー | camelCase | `firstName`, `isActive` |

```typescript
// ✅ 命名規則に従った例
const userName = "john";
function getUserData() {}

const MAX_RETRY_ATTEMPTS = 3;
const API_BASE_URL = "https://api.example.com";

class DatabaseConnection {}
interface UserProfile {}

type ResponseStatus = "success" | "error";
enum HttpStatusCode {}
```

**レビュー観点：**
- [ ] 変数・関数がcamelCaseで命名されているか
- [ ] クラス・インターフェイス・型がPascalCaseで命名されているか
- [ ] グローバル定数がUPPER_CASEで命名されているか
- [ ] プロジェクト全体で命名規則が一貫しているか

---

## 変数宣言

### `var`キーワードを使わない（Major）

`var`は関数スコープで動作し、意図しない変数の上書きを引き起こす。`let`と`const`を使用する。

| キーワード | スコープ | 再宣言 | 再割り当て |
|-----------|---------|--------|-----------|
| `var` | 関数スコープ | 可 | 可 |
| `let` | ブロックスコープ | 不可 | 可 |
| `const` | ブロックスコープ | 不可 | 不可 |

```typescript
// ❌ varの使用
var count = 0;
if (true) {
    var count = 1; // 外側のcountを上書き
}
console.log(count); // 1（意図しない挙動）

// ✅ letの使用
let count = 0;
if (true) {
    let count = 1; // ブロックスコープ内のみ
}
console.log(count); // 0（期待通り）
```

**レビュー観点：**
- [ ] `var`が使用されていないか
- [ ] 再割り当てしない変数には`const`が使われているか
- [ ] 再割り当てが必要な場合のみ`let`が使われているか

---

## アクセス修飾子

### 適切なアクセス修飾子を使用する（Minor）

クラスメンバーの可視性を制御し、カプセル化を実現する。

| 修飾子 | 可視範囲 | 用途 |
|--------|--------|------|
| `private` | 同一クラスのみ | 内部実装の隠蔽 |
| `public` | すべての場所 | 外部に公開するAPI（省略時のデフォルト） |
| `protected` | 同一クラス + サブクラス | 継承時にサブクラスからアクセス可能にする |

**レビュー観点：**
- [ ] 内部実装のメンバーに`private`が付与されているか
- [ ] `public`がデフォルトで良い場合、明示的に省略されているか（プロジェクト規約に従う）
- [ ] 継承を考慮して`protected`が適切に使われているか

---

## ユーティリティ型

### ユーティリティ型を活用する（Suggestion）

TypeScript組み込みのユーティリティ型で、既存の型を効率的に変換する。

### Partial\<Type\>

すべてのプロパティをオプションにする。部分更新に有用。

```typescript
interface Dog {
    name: string;
    age: number;
    breed: string;
    weight: number;
}

// すべてのプロパティがオプション
let partialDog: Partial<Dog> = {};
```

### Required\<Type\>

すべてのプロパティを必須にする。Partialの逆。

```typescript
interface Dog {
    name: string;
    age: number;
    breed: string;
    weight?: number;
}

// weightも必須になる
let dog: Required<Dog> = {
    name: "scruffy",
    age: 5,
    breed: "labrador",
    weight: 55,
};
```

### その他の主要ユーティリティ型

| 型 | 説明 |
|----|------|
| `Pick<T, K>` | 指定したプロパティのみを抽出 |
| `Omit<T, K>` | 指定したプロパティを除外 |
| `Record<K, V>` | キーと値の型を指定したオブジェクト型を作成 |
| `Readonly<T>` | すべてのプロパティをreadonlyにする |

**レビュー観点：**
- [ ] 手動で型を再定義する代わりにユーティリティ型が活用されているか
- [ ] 部分更新には`Partial`が使われているか

---

## 設計パターン

### ファクトリーパターンを活用する（Suggestion）

オブジェクト作成ロジックが複雑な場合、ファクトリーパターンに委任して責務を分離する。

```typescript
// ❌ コンストラクト内で直接作成
class MyStack {
    constructor() {
        // 複雑な作成ロジックが散在
        const lambda1 = new Lambda(/* 多数のパラメータ */);
        const lambda2 = new Lambda(/* 多数のパラメータ */);
    }
}

// ✅ ファクトリーに委任
class LambdaFactory {
    static create(name: string, config: LambdaConfig): Lambda {
        // 作成ロジックを集約
        return new Lambda(/* ... */);
    }
}
```

**レビュー観点：**
- [ ] 類似オブジェクトの作成が複数箇所に散在していないか
- [ ] 複雑な初期化ロジックが適切に抽象化されているか

---

## リンター・フォーマッター

### ESLintとPrettierを導入する（Suggestion）

| ツール | 役割 |
|--------|------|
| **ESLint** | 静的解析によるコード品質チェック。問題の検出と自動修正 |
| **Prettier** | コードフォーマット。スタイルの自動統一 |

```json
{
    "scripts": {
        "lint": "eslint --ext .js,.ts .",
        "format": "prettier --ignore-path .gitignore --write '**/*.+(js|ts|json)'"
    }
}
```

**レビュー観点：**
- [ ] ESLintの警告やエラーが未解決のまま残っていないか
- [ ] コードフォーマットがプロジェクトの規約に従っているか
