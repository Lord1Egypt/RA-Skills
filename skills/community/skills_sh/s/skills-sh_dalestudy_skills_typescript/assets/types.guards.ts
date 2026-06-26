/**
 * 타입 가드 함수 템플릿
 * 
 * 사용법:
 * 1. 이 파일을 복사하여 프로젝트에 맞게 수정
 * 2. 런타임 타입 체크와 타입 좁히기
 */

// 기본 타입 가드
export function isString(value: unknown): value is string {
  return typeof value === "string";
}

export function isNumber(value: unknown): value is number {
  return typeof value === "number" && !isNaN(value);
}

export function isBoolean(value: unknown): value is boolean {
  return typeof value === "boolean";
}

export function isObject(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

export function isArray<T>(value: unknown): value is T[] {
  return Array.isArray(value);
}

export function isNull(value: unknown): value is null {
  return value === null;
}

export function isUndefined(value: unknown): value is undefined {
  return value === undefined;
}

export function isNotNull<T>(value: T | null): value is T {
  return value !== null;
}

export function isNotUndefined<T>(value: T | undefined): value is T {
  return value !== undefined;
}

// 객체 속성 체크
export function hasProperty<K extends string>(
  obj: unknown,
  key: K
): obj is Record<K, unknown> {
  return typeof obj === "object" && obj !== null && key in obj;
}

// 사용자 정의 타입 가드 예시
export interface User {
  id: string;
  name: string;
  email: string;
}

export function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "name" in value &&
    "email" in value &&
    typeof (value as Record<string, unknown>).id === "string" &&
    typeof (value as Record<string, unknown>).name === "string" &&
    typeof (value as Record<string, unknown>).email === "string"
  );
}

// 배열 요소 타입 가드
export function isUserArray(value: unknown): value is User[] {
  return Array.isArray(value) && value.every(isUser);
}

// 유니온 타입 가드
export type StringOrNumber = string | number;

export function isStringOrNumber(value: unknown): value is StringOrNumber {
  return typeof value === "string" || typeof value === "number";
}

// 옵셔널 체이닝과 함께 사용
export function getPropertySafely<T, K extends keyof T>(
  obj: T | null | undefined,
  key: K
): T[K] | undefined {
  if (obj === null || obj === undefined) {
    return undefined;
  }
  return obj[key];
}
