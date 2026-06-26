/**
 * Segment 类型
 */
interface Segment {
  type: string
  value: string
  ref_key?: string
}

/**
 * 解析 segments 数组为字符串
 * @param segments Segment 数组
 * @returns 解析后的字符串
 */
export function parseSegments(segments: Segment[]): string {
  if (!segments || segments.length === 0) {
    return ''
  }

  return segments
    .map((seg) => {
      // 只取 value，忽略其他类型标记
      return seg.value
    })
    .join('')
    .trim()
}

/**
 * 格式化日期
 * @param date 日期字符串
 * @returns 格式化后的日期
 */
export function formatDate(date: string): string {
  if (!date || date === '-') {
    return '-'
  }
  return date
}

/**
 * 格式化持股比例
 * @param percent 持股比例
 * @returns 格式化后的持股比例
 */
export function formatPercent(percent: string | number): string {
  if (!percent || percent === '-') {
    return '-'
  }
  if (typeof percent === 'number') {
    return `${percent}%`
  }
  return percent
}
