'use strict'

const { publicUrl } = require('./media')
const { long } = require('./translation')
const { VibbitError } = require('./client')

const object = value => value !== null && typeof value === 'object' && !Array.isArray(value)
const assert = (condition, message) => { if (!condition) throw new Error(message) }
const batchFields = ['url', 'name', 'price', 'price_unit', 'image_url', 'image_urls',
  'description', 'selling_points', 'third_product_id', 'third_product_url', 'source', 'platform', 'status']

function productFields(value, prefix) {
  if (value.name !== undefined) assert(typeof value.name === 'string' && value.name.trim(), `${prefix}.name must be nonempty text`)
  if (value.price !== undefined) assert(typeof value.price === 'number' && Number.isFinite(value.price) && value.price >= 0, `${prefix}.price must be a nonnegative number`)
  for (const key of ['price_unit', 'third_product_id', 'source', 'platform']) {
    if (value[key] !== undefined) assert(typeof value[key] === 'string' && value[key].trim(), `${prefix}.${key} must be nonempty text`)
  }
  if (value.description !== undefined) assert(typeof value.description === 'string', `${prefix}.description must be text`)
  for (const key of ['url', 'image_url', 'third_product_url']) {
    if (value[key] !== undefined) publicUrl(value[key], `${prefix}.${key}`)
  }
  if (value.image_urls !== undefined) {
    assert(Array.isArray(value.image_urls) && value.image_urls.length > 0, `${prefix}.image_urls must be a nonempty URL array; omit unknown images`)
    value.image_urls.forEach((url, index) => publicUrl(url, `${prefix}.image_urls[${index}]`))
  }
  if (value.selling_points !== undefined) {
    assert(Array.isArray(value.selling_points) && value.selling_points.every(text => typeof text === 'string' && text.trim()), `${prefix}.selling_points must contain nonempty text`)
  }
}

function validateProducts(name, input) {
  if (input.product_id !== undefined) long(input.product_id, 'product_id')
  if (name === 'list_products') {
    if (input.page !== undefined) assert(input.page >= 0, 'page starts at 0')
    if (input.size !== undefined) assert(input.size > 0, 'size must be positive')
  }
  productFields(input, 'input')
  if (name === 'batch_create_products') {
    assert(input.products.length > 0, 'products must be nonempty')
    input.products.forEach((product, index) => {
      const prefix = `products[${index}]`
      for (const key of Object.keys(product)) assert(batchFields.includes(key), `Undocumented ${prefix}.${key}`)
      assert(typeof product.name === 'string' && product.name.trim(), `${prefix}.name is required`)
      if (product.status !== undefined) assert(product.status === 'SUCCESS', `${prefix}.status must be SUCCESS; do not save failed parse results`)
      productFields(product, prefix)
    })
  }
}

function validId(value) {
  try { long(value, 'product ID'); return true } catch { return false }
}

// Client projections retain the raw result, including business analysis states.
function productOutcome(result, taskType) {
  const protocol = message => { throw new VibbitError('protocol', message) }
  if (taskType === 'ECOM_PRODUCT_LIST') {
    if (!object(result) || !Array.isArray(result.content)) protocol('Product list is missing content')
    if (result.content.some(row => !object(row) || !validId(row.id))) protocol('Product list contains an invalid product ID')
    for (const key of ['total_elements', 'total_pages', 'number', 'size']) {
      if (result[key] !== undefined && (!Number.isSafeInteger(result[key]) || result[key] < 0)) protocol(`Invalid product pagination: ${key}`)
    }
    return {}
  }
  if (taskType === 'ECOM_PRODUCT_PARSE_LINKS' || taskType === 'ECOM_PRODUCT_BATCH_CREATE') {
    if (!Array.isArray(result)) protocol('Expected a product result array')
    const parsing = taskType === 'ECOM_PRODUCT_PARSE_LINKS'
    const summary = { succeeded: 0, failed: 0, unknown: 0 }
    for (const row of result) {
      if (!object(row)) summary.unknown++
      else if (row.status === 'FAILED' || row.error_code) summary.failed++
      else if (parsing ? row.status === 'SUCCESS' : validId(row.id)) summary.succeeded++
      else summary.unknown++
    }
    const incomplete = summary.failed + summary.unknown > 0
    return { ok: result.length > 0 && summary.succeeded > 0,
      item_summary: summary,
      ...(incomplete && summary.succeeded > 0 ? { partial_failure: true } : {}),
    }
  }
  if (taskType === 'ECOM_PRODUCT_DELETE') {
    if (!object(result) || !validId(result.product_id) || typeof result.deleted !== 'boolean') protocol('Product deletion result is missing product_id or deleted')
    return { ok: result.deleted, product_id: String(result.product_id) }
  }
  if (!object(result) || !validId(result.id)) protocol('Product detail or save result is missing a valid product ID')
  return { product_id: String(result.id) }
}

module.exports = { validateProducts, productOutcome }
