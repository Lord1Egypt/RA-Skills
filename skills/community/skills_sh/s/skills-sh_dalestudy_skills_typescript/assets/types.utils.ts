/**
 * 커스텀 유틸리티 타입 정의 템플릿
 * 
 * 사용법:
 * 1. 이 파일을 복사하여 프로젝트에 맞게 수정
 * 2. TypeScript 내장 유틸리티 타입은 별도 import 없이 사용 가능:
 *    - Partial, Required, Readonly, Pick, Omit, Record
 *    - NonNullable, ReturnType, Parameters, Awaited
 *    - Exclude, Extract, InstanceType 등
 * 3. 이 파일에는 커스텀 유틸리티 타입만 정의
 */

// Nullable: null 또는 undefined 추가
export type Nullable<T> = T | null | undefined;

// DeepPartial: 중첩된 객체도 Partial
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

// DeepReadonly: 중첩된 객체도 Readonly
export type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};

// DeepRequired: 중첩된 객체도 Required
export type DeepRequired<T> = {
  [P in keyof T]-?: T[P] extends object ? DeepRequired<T[P]> : T[P];
};

// Optional: 특정 키만 선택적으로
export type Optional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

// RequiredKeys: 필수 키만 추출
export type RequiredKeys<T> = {
  [K in keyof T]-?: {} extends Pick<T, K> ? never : K;
}[keyof T];

// OptionalKeys: 선택적 키만 추출
export type OptionalKeys<T> = {
  [K in keyof T]-?: {} extends Pick<T, K> ? K : never;
}[keyof T];

// 함수 타입 유틸리티

// 함수의 첫 번째 파라미터 타입 추출
// 참고: ReturnType, Parameters, Awaited는 TypeScript 내장 타입
export type FirstParameter<T extends (...args: any) => any> = Parameters<T>[0];

// 배열 타입 유틸리티

// 배열 요소 타입 추출
export type ArrayElement<T> = T extends (infer U)[] ? U : never;

// 배열의 첫 번째 요소 타입
export type First<T extends readonly unknown[]> = T extends readonly [
  infer F,
  ...unknown[]
]
  ? F
  : never;

// 배열의 마지막 요소 타입
export type Last<T extends readonly unknown[]> = T extends readonly [
  ...unknown[],
  infer L
]
  ? L
  : never;

// 객체 타입 유틸리티

// 값 타입 추출
export type ValueOf<T> = T[keyof T];

// 브랜드 타입 (원시 타입 구분)
export type Brand<T, B> = T & { readonly __brand: B };

// 예시: UserId와 ProductId 구분
export type UserId = Brand<string, "UserId">;
export type ProductId = Brand<string, "ProductId">;
