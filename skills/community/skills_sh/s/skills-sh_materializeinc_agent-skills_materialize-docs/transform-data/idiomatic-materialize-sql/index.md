# Idiomatic Materialize SQL

Learn about idiomatic Materialize SQL. Materialize offers various idiomatic query patterns, such as for top-k query pattern, first value/last value query paterrns, etc.

Materialize follows the SQL standard (SQL-92) implementation and strives for
compatibility with the PostgreSQL dialect. However, for some use cases,
Materialize provides its own idiomatic query patterns that can provide better
performance.

## Window functions

| Window Function | Idiomatic Materialize |
| --- | --- |
| <a href="/transform-data/idiomatic-materialize-sql/first-value/" >First value within groups</a> | <a href="/transform-data/idiomatic-materialize-sql/first-value/" >Use <code>MIN/MAX ... GROUP BY</code> subquery</a>. |
| <a href="/transform-data/idiomatic-materialize-sql/lag/" >Lag over a regularly increasing field</a> | <a href="/transform-data/idiomatic-materialize-sql/lag/" >Use self join or a self <code>LEFT JOIN/LEFT OUTER JOIN</code> by an <strong>equality match</strong> on the regularly increasing field</a>. |
| <a href="/transform-data/idiomatic-materialize-sql/last-value/" >Last value within groups</a> | <a href="/transform-data/idiomatic-materialize-sql/last-value/" >Use <code>MIN/MAX ... GROUP BY</code> subquery</a> |
| <a href="/transform-data/idiomatic-materialize-sql/lead/" >Lead over a regularly increasing field</a> | <a href="/transform-data/idiomatic-materialize-sql/lead/" >Use self join or a self <code>LEFT JOIN/LEFT OUTER JOIN</code> by an <strong>equality match</strong> on the regularly increasing field</a>. |
| <a href="/transform-data/idiomatic-materialize-sql/top-k/" >Top-K</a> | <a href="/transform-data/idiomatic-materialize-sql/top-k/" >Use an <code>ORDER BY ... LIMIT</code> subquery with a <code>LATERAL JOIN</code> on a <code>DISTINCT</code> subquery (or, for K=1,  a <code>SELECT DISTINCT ON ... ORDER BY ... LIMIT</code> query)</a> |

## General query patterns

| Query Pattern | Idiomatic Materialize |
| --- | --- |
| <a href="/transform-data/idiomatic-materialize-sql/any/" >ANY() Equi-join condition</a> | <a href="/transform-data/idiomatic-materialize-sql/any/" >Use <code>UNNEST()</code> or <code>DISTINCT UNNEST()</code> to expand the values and join</a>. |
| <a href="/transform-data/idiomatic-materialize-sql/not-in/" ><code>NOT IN (&lt;subquery&gt;)</code> predicate</a> | <a href="/transform-data/idiomatic-materialize-sql/not-in/" >Rewrite to <code>NOT EXISTS</code>, or filter out <code>NULL</code>s on both sides of the <code>NOT IN</code></a>. |
| <a href="/transform-data/idiomatic-materialize-sql/mz_now/#mz_now-expressions-to-calculate-past-or-future-timestamp" ><code>mz_now()</code> with date/time operators</a> | <a href="/transform-data/idiomatic-materialize-sql/mz_now/#mz_now-expressions-to-calculate-past-or-future-timestamp" >Move the operation to the other side of the comparison</a>: |
| <a href="/transform-data/idiomatic-materialize-sql/mz_now/#disjunctions-or" ><code>mz_now()</code> with disjunctions (<code>OR</code>) in materialized/indexed view definitions and <code>SUBSCRIBE</code> statements</a>: | <a href="/transform-data/idiomatic-materialize-sql/mz_now/#disjunctions-or" >Rewrite using <code>UNION ALL</code> or <code>UNION</code> (deduplicating as necessary) expression</a> |

---

## `ANY()` equi-join condition

## Overview

The "`field = ANY(...)`" equality condition returns true if the equality
comparison is true for any of the values in the `ANY()` expression.

For equi-join whose `ON` expression includes an [`ANY` operator
expression](/sql/functions/#expression-bool_op-any),
Materialize provides an idiomatic SQL as an alternative to the `ANY()`
expression.

> ### Materialize and equi-join `ON fieldX = ANY(<array|list|map>)`
> When evaluating an equi-join whose `ON` expression includes the [`ANY` operator
> expression](/sql/functions/#expression-bool_op-any)
> (i.e., `ON fieldX = ANY(<array|list|map>)`), Materialize performs a cross join,
> which can lead to a significant increase in memory usage. If possible, rewrite
> the query to perform an equi-join on the unnested values.

## Idiomatic Materialize SQL

**Idiomatic Materialize SQL:**  For equi-join whose `ON` expression includes
the [`ANY` operator expression](/sql/functions/#expression-bool_op-any) (`ON
fieldX = ANY(<array|list|map>)`), use [UNNEST()](/sql/functions/#unnest) in a
[Common Table Expression (CTE)](/sql/select/#common-table-expressions-ctes) to
unnest the values and perform the equi-join on the unnested values. If the
array/list/map contains duplicates, include [`DISTINCT`](/sql/select/#select-distinct) to remove duplicates.

<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><blue>Materialize SQL</blue></td>
<td class="copyableCode">

<p><strong>If no duplicates exist in the unnested field:</strong> Use a Common Table
Expression (CTE) to <a href="/sql/functions/#unnest" ><code>UNNEST()</code></a> the array of
values and perform the equi-join on the unnested values.</p>
<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="c1">-- array_field contains no duplicates.--
</span></span></span><span class="line"><span class="cl"><span class="c1"></span>
</span></span><span class="line"><span class="cl"><span class="k">WITH</span> <span class="n">my_expanded_values</span> <span class="k">AS</span>
</span></span><span class="line"><span class="cl"><span class="p">(</span><span class="k">SELECT</span> <span class="k">UNNEST</span><span class="p">(</span><span class="n">array_field</span><span class="p">)</span> <span class="k">AS</span> <span class="n">fieldZ</span> <span class="k">FROM</span> <span class="n">tableB</span><span class="p">)</span>
</span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">a</span><span class="mf">.</span><span class="n">fieldA</span><span class="p">,</span> <span class="mf">...</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">tableA</span> <span class="n">a</span>
</span></span><span class="line"><span class="cl"><span class="k">JOIN</span> <span class="n">my_expanded_values</span> <span class="n">t</span> <span class="k">ON</span> <span class="n">a</span><span class="mf">.</span><span class="n">fieldZ</span> <span class="o">=</span> <span class="n">t</span><span class="mf">.</span><span class="n">fieldZ</span>
</span></span><span class="line"><span class="cl"><span class="p">;</span>
</span></span></code></pre></div><p><strong>Duplicates may exist in the unnested field:</strong> Use a Common Table
Expression (CTE) to <a href="/sql/select/#select-distinct" ><code>DISTINCT</code></a>
<a href="/sql/functions/#unnest" ><code>UNNEST()</code></a> the array of values and perform the
equi-join on the unnested values.</p>
<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="c1">-- array_field may contain duplicates.--
</span></span></span><span class="line"><span class="cl"><span class="c1"></span>
</span></span><span class="line"><span class="cl"><span class="k">WITH</span> <span class="n">my_expanded_values</span> <span class="k">AS</span>
</span></span><span class="line"><span class="cl"><span class="p">(</span><span class="k">SELECT</span> <span class="k">DISTINCT</span> <span class="k">UNNEST</span><span class="p">(</span><span class="n">array_field</span><span class="p">)</span> <span class="k">AS</span> <span class="n">fieldZ</span> <span class="k">FROM</span> <span class="n">tableB</span><span class="p">)</span>
</span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">a</span><span class="mf">.</span><span class="n">fieldA</span><span class="p">,</span> <span class="mf">...</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">tableA</span> <span class="n">a</span>
</span></span><span class="line"><span class="cl"><span class="k">JOIN</span> <span class="n">my_expanded_values</span> <span class="n">t</span> <span class="k">ON</span> <span class="n">a</span><span class="mf">.</span><span class="n">fieldZ</span> <span class="o">=</span> <span class="n">t</span><span class="mf">.</span><span class="n">fieldZ</span>
</span></span><span class="line"><span class="cl"><span class="p">;</span>
</span></span></code></pre></div>

</td>
</tr>
<tr>
<td><red>Anti-pattern</red> ❌</td>
<td>

<p><red>Avoid the use of <a href="/sql/functions/#expression-bool_op-any" ><code>ANY(...)</code> function</a> for equi-join
conditions.</red></p>
<pre tabindex="0"><code class="language-nofmt" data-lang="nofmt">-- Anti-pattern. Avoid. --
SELECT a.fieldA, ...
FROM tableA a, tableB b
WHERE a.fieldZ = ANY(b.array_field) -- Anti-pattern. Avoid.
;
</code></pre>

</td>
</tr>

</tbody>
</table>

## Examples

> **Note:** The example data can be found in the
> [Appendix](/transform-data/idiomatic-materialize-sql/appendix/example-orders).

### Find orders with any sales items

Using idiomatic Materialize SQL, the following example finds orders that contain
any of the sales items for the week of the order. That is, the example uses a
CTE to [`UNNEST()`](/sql/functions/#unnest) (or
[`DISTINCT`](/sql/select/#select-distinct)[`UNNEST()`](/sql/functions/#unnest))
the `items` field from the `sales_items` table, and then performs an equi-join
with the `orders` table on the unnested values.

<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>

<tr>
<td><blue>Materialize SQL</blue> ✅</td>
<td class="copyableCode">

<p><em><strong>If no duplicates in the unnested field</strong></em></p>
<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="c1">-- sales_items.items contains no duplicates. --
</span></span></span><span class="line"><span class="cl"><span class="c1"></span>
</span></span><span class="line"><span class="cl"><span class="k">WITH</span> <span class="n">individual_sales_items</span> <span class="k">AS</span>
</span></span><span class="line"><span class="cl"><span class="p">(</span><span class="k">SELECT</span> <span class="k">unnest</span><span class="p">(</span><span class="n">items</span><span class="p">)</span> <span class="k">as</span> <span class="n">item</span><span class="p">,</span> <span class="n">week_of</span> <span class="k">FROM</span> <span class="n">sales_items</span><span class="p">)</span>
</span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">s</span><span class="mf">.</span><span class="n">week_of</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">quantity</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">orders</span> <span class="n">o</span>
</span></span><span class="line"><span class="cl"><span class="k">JOIN</span> <span class="n">individual_sales_items</span> <span class="n">s</span> <span class="k">ON</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span> <span class="o">=</span> <span class="n">s</span><span class="mf">.</span><span class="n">item</span>
</span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">date_trunc</span><span class="p">(</span><span class="s1">&#39;week&#39;</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_date</span><span class="p">)</span> <span class="o">=</span> <span class="n">s</span><span class="mf">.</span><span class="n">week_of</span>
</span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">s</span><span class="mf">.</span><span class="n">week_of</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">quantity</span>
</span></span><span class="line"><span class="cl"><span class="p">;</span>
</span></span></code></pre></div><p><em><strong>To omit duplicates that may exist in the unnested field</strong></em></p>
<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="c1">-- sales_items.items may contains duplicates --
</span></span></span><span class="line"><span class="cl"><span class="c1"></span>
</span></span><span class="line"><span class="cl"><span class="k">WITH</span> <span class="n">individual_sales_items</span> <span class="k">AS</span>
</span></span><span class="line"><span class="cl"><span class="p">(</span><span class="k">SELECT</span> <span class="k">DISTINCT</span> <span class="k">unnest</span><span class="p">(</span><span class="n">items</span><span class="p">)</span> <span class="k">as</span> <span class="n">item</span><span class="p">,</span> <span class="n">week_of</span> <span class="k">FROM</span> <span class="n">sales_items</span><span class="p">)</span>
</span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">s</span><span class="mf">.</span><span class="n">week_of</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">quantity</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">orders</span> <span class="n">o</span>
</span></span><span class="line"><span class="cl"><span class="k">JOIN</span> <span class="n">individual_sales_items</span> <span class="n">s</span> <span class="k">ON</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span> <span class="o">=</span> <span class="n">s</span><span class="mf">.</span><span class="n">item</span>
</span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">date_trunc</span><span class="p">(</span><span class="s1">&#39;week&#39;</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_date</span><span class="p">)</span> <span class="o">=</span> <span class="n">s</span><span class="mf">.</span><span class="n">week_of</span>
</span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">s</span><span class="mf">.</span><span class="n">week_of</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">quantity</span>
</span></span><span class="line"><span class="cl"><span class="p">;</span>
</span></span></code></pre></div>

</td>
</tr>

<tr>
<td><red>Anti-pattern</red> ❌</td>
<td>

<p><red>Avoid the use of <a href="/sql/functions/#expression-bool_op-any" ><code>ANY()</code></a> for the equi-join condition.</red></p>
<pre tabindex="0"><code class="language-nofmt" data-lang="nofmt">-- Anti-pattern. Avoid. --
SELECT s.week_of, o.order_id, o.item, o.quantity
FROM orders o
JOIN sales_items s ON o.item = ANY(s.items)
WHERE date_trunc(&#39;week&#39;, o.order_date) = s.week_of
ORDER BY s.week_of, o.order_id, o.item, o.quantity
;
</code></pre>

</td>
</tr>

</tbody>
</table>

## See also

- [`ANY()`](/sql/functions/#expression-bool_op-any)

- [Common Table Expression (CTE)](/sql/select/#common-table-expressions-ctes)

- [Idiomatic Materialize SQL
  Chart](/transform-data/idiomatic-materialize-sql/appendix/idiomatic-sql-chart/)

- [`UNNEST()`](/sql/functions/#unnest)

---

## `NOT IN` subquery

## Overview

The `fieldX NOT IN (<subquery>)` predicate returns `true` if `fieldX` does not
equal any value returned by the subquery. For predicates where `fieldX` or the
`<subquery>` can contain `NULL` values, Materialize provides idiomatic SQL
alternatives.

### Materialize and `NOT IN (<subquery>)`

When evaluating a `WHERE fieldX NOT IN (<subquery>)` predicate involving
possible `NULL` values for `fieldX` or `<subquery>`, Materialize performs a
cross join between the outer relation and the subquery to preserve SQL `NULL`
semantics, which can significantly increase memory usage. If possible, rewrite
the query to avoid the cross join.

## Idiomatic Materialize SQL

For `fieldX NOT IN (<subquery>)` predicates involving possible `NULL` values,
the following rewrites are available:

> **Note:** Neither rewrite is strictly equivalent to `NOT IN (<subquery>)`.
> Both rewrites avoid the `NULL` propagation semantics of `NOT IN`; that is, they
> treat subquery `NULL` values as non-matches rather than allowing them to
> invalidate the comparison. In addition, the `NOT EXISTS` rewrite retains outer
> rows whose value is `NULL`, whereas both `NOT IN` and the filter-`NULL`s rewrite
> exclude them.

- Rewrite to [`NOT EXISTS`](/sql/functions/#not-exists) with a correlated
  subquery.
- Retain `NOT IN`, but filter out `NULL` values from both the outer field and
  the subquery.

<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><blue>Materialize SQL</blue></td>
<td class="copyableCode">

<p><strong>Rewrite to <code>NOT EXISTS</code> with a correlated subquery.</strong></p>
<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">t1</span><span class="mf">.</span><span class="o">*</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">t1</span>
</span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="k">NOT</span> <span class="k">EXISTS</span> <span class="p">(</span><span class="k">SELECT</span> <span class="mf">1</span> <span class="k">FROM</span> <span class="n">t2</span> <span class="k">WHERE</span> <span class="n">t2</span><span class="mf">.</span><span class="n">a</span> <span class="o">=</span> <span class="n">t1</span><span class="mf">.</span><span class="n">a</span><span class="p">)</span>
</span></span><span class="line"><span class="cl"><span class="p">;</span>
</span></span></code></pre></div><p><strong>Filter out <code>NULL</code>s on both sides of the <code>NOT IN</code>.</strong></p>
<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">t1</span><span class="mf">.</span><span class="o">*</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">t1</span>
</span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">t1</span><span class="mf">.</span><span class="n">a</span> <span class="k">IS</span> <span class="k">NOT</span> <span class="k">NULL</span>
</span></span><span class="line"><span class="cl">  <span class="k">AND</span> <span class="n">t1</span><span class="mf">.</span><span class="n">a</span> <span class="k">NOT</span> <span class="k">IN</span> <span class="p">(</span><span class="k">SELECT</span> <span class="n">t2</span><span class="mf">.</span><span class="n">a</span> <span class="k">FROM</span> <span class="n">t2</span> <span class="k">WHERE</span> <span class="n">t2</span><span class="mf">.</span><span class="n">a</span> <span class="k">IS</span> <span class="k">NOT</span> <span class="k">NULL</span><span class="p">)</span>
</span></span><span class="line"><span class="cl"><span class="p">;</span>
</span></span></code></pre></div>

</td>
</tr>
<tr>
<td><red>Anti-pattern</red> ❌</td>
<td>

<p><red>Avoid <code>NOT IN (&lt;subquery&gt;)</code> predicates, which force a cross join
between the outer relation and the subquery.</red></p>
<pre tabindex="0"><code class="language-nofmt" data-lang="nofmt">-- Anti-pattern. Avoid. --
SELECT t1.*
FROM t1
WHERE t1.a NOT IN (SELECT t2.a FROM t2) -- Anti-pattern. Avoid.
;
</code></pre>

</td>
</tr>

</tbody>
</table>

If the subquery uses [`UNNEST()`](/sql/functions/#unnest) on a column whose
value depends on the outer row:
- Factor the `UNNEST()` into an uncorrelated [Common Table Expression
  (CTE)](/sql/select/#common-table-expressions-ctes) first.
- Then apply the rewrite against the CTE. See the [example
  below](#find-items-not-currently-on-sale).

## Examples

> **Note:** The example data can be found in the
> [Appendix](/transform-data/idiomatic-materialize-sql/appendix/example-orders).

### Find items not currently on sale

Using idiomatic Materialize SQL, the following examples find items in the
`items` table whose `item` value (declared `NOT NULL`) does not appear in any of
this week's sales arrays in `sales_items`, a nullable `text[]`. The subquery
uses [`UNNEST()`](/sql/functions/#unnest) to expand each week's `items` array
into individual values for comparison.

If the subquery uses [`UNNEST()`](/sql/functions/#unnest) on a column whose
value depends on the outer row:

- First, factor the `UNNEST()` into an uncorrelated [Common Table Expression
  (CTE)](/sql/select/#common-table-expressions-ctes).
- Then, apply the rewrite against the CTE.

<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>

<tr>
<td><blue>Materialize SQL</blue> ✅</td>
<td class="copyableCode">

<p>Because the subquery uses <a href="/sql/functions/#unnest" ><code>UNNEST()</code></a> on a column
of the outer-correlated row, factor the <code>UNNEST()</code> into an uncorrelated
<a href="/sql/select/#common-table-expressions-ctes" >Common Table Expression
(CTE)</a> first.</p>
<p><em><strong>Rewrite to <code>NOT EXISTS</code> with a CTE for the <code>UNNEST()</code></strong></em></p>
<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">WITH</span> <span class="n">this_weeks_sales</span> <span class="k">AS</span> <span class="p">(</span>
</span></span><span class="line"><span class="cl">  <span class="k">SELECT</span> <span class="k">unnest</span><span class="p">(</span><span class="n">items</span><span class="p">)</span> <span class="k">AS</span> <span class="n">sale_item</span>
</span></span><span class="line"><span class="cl">  <span class="k">FROM</span> <span class="n">sales_items</span>
</span></span><span class="line"><span class="cl">  <span class="k">WHERE</span> <span class="n">week_of</span> <span class="o">=</span> <span class="n">date_trunc</span><span class="p">(</span><span class="s1">&#39;week&#39;</span><span class="p">,</span> <span class="n">current_timestamp</span><span class="p">)</span>
</span></span><span class="line"><span class="cl"><span class="p">)</span>
</span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">i</span><span class="mf">.</span><span class="n">item</span><span class="p">,</span> <span class="n">i</span><span class="mf">.</span><span class="n">price</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">items</span> <span class="n">i</span>
</span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="k">NOT</span> <span class="k">EXISTS</span> <span class="p">(</span>
</span></span><span class="line"><span class="cl">  <span class="k">SELECT</span> <span class="mf">1</span> <span class="k">FROM</span> <span class="n">this_weeks_sales</span> <span class="n">s</span> <span class="k">WHERE</span> <span class="n">s</span><span class="mf">.</span><span class="n">sale_item</span> <span class="o">=</span> <span class="n">i</span><span class="mf">.</span><span class="n">item</span>
</span></span><span class="line"><span class="cl"><span class="p">)</span>
</span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">i</span><span class="mf">.</span><span class="n">item</span>
</span></span><span class="line"><span class="cl"><span class="p">;</span>
</span></span></code></pre></div><p><em><strong>Filter out <code>NULL</code>s with a CTE for the <code>UNNEST()</code></strong></em></p>
<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">WITH</span> <span class="n">this_weeks_sales</span> <span class="k">AS</span> <span class="p">(</span>
</span></span><span class="line"><span class="cl">  <span class="k">SELECT</span> <span class="k">unnest</span><span class="p">(</span><span class="n">items</span><span class="p">)</span> <span class="k">AS</span> <span class="n">sale_item</span>
</span></span><span class="line"><span class="cl">  <span class="k">FROM</span> <span class="n">sales_items</span>
</span></span><span class="line"><span class="cl">  <span class="k">WHERE</span> <span class="n">week_of</span> <span class="o">=</span> <span class="n">date_trunc</span><span class="p">(</span><span class="s1">&#39;week&#39;</span><span class="p">,</span> <span class="n">current_timestamp</span><span class="p">)</span>
</span></span><span class="line"><span class="cl"><span class="p">)</span>
</span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">i</span><span class="mf">.</span><span class="n">item</span><span class="p">,</span> <span class="n">i</span><span class="mf">.</span><span class="n">price</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">items</span> <span class="n">i</span>
</span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">i</span><span class="mf">.</span><span class="n">item</span> <span class="k">IS</span> <span class="k">NOT</span> <span class="k">NULL</span>
</span></span><span class="line"><span class="cl">  <span class="k">AND</span> <span class="n">i</span><span class="mf">.</span><span class="n">item</span> <span class="k">NOT</span> <span class="k">IN</span> <span class="p">(</span>
</span></span><span class="line"><span class="cl">    <span class="k">SELECT</span> <span class="n">sale_item</span> <span class="k">FROM</span> <span class="n">this_weeks_sales</span> <span class="k">WHERE</span> <span class="n">sale_item</span> <span class="k">IS</span> <span class="k">NOT</span> <span class="k">NULL</span>
</span></span><span class="line"><span class="cl">  <span class="p">)</span>
</span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">i</span><span class="mf">.</span><span class="n">item</span>
</span></span><span class="line"><span class="cl"><span class="p">;</span>
</span></span></code></pre></div>

</td>
</tr>

<tr>
<td><red>Anti-pattern</red> ❌</td>
<td>

<p><red>Avoid <code>NOT IN (&lt;subquery&gt;)</code>, which forces a cross join.</red></p>
<pre tabindex="0"><code class="language-nofmt" data-lang="nofmt">-- Anti-pattern. Avoid. --
SELECT i.item, i.price
FROM items i
WHERE i.item NOT IN (
  SELECT unnest(items) FROM sales_items
  WHERE week_of = date_trunc(&#39;week&#39;, current_timestamp)
)
ORDER BY i.item
;
</code></pre>

</td>
</tr>

</tbody>
</table>

## See also

- [`NOT EXISTS`](/sql/functions/#not-exists)

- [Idiomatic Materialize SQL
  Chart](/transform-data/idiomatic-materialize-sql/appendix/idiomatic-sql-chart/)

---

## Appendix

---

## First value in group

## Overview

The "first value in each group" query pattern returns the first value, according
to some ordering, in each group.

> ### Materialize and window functions
> For indexed views and materialized views that contain [window
> functions](/sql/functions/#window-functions) (including aggregate functions used
> with an `OVER` clause), when an input record in a partition is
> added/removed/changed, Materialize **recomputes the results from scratch** for
> that partition (instead of using incremental computation).
> The `PARTITION BY` clause of your window function determines your partitions. If
> `PARTITION BY` is omitted, all records belong to a single partition (i.e., any
> record change results in a recomputation from scratch over the whole input).
> To avoid performance issues that may arise as the number of records grows,
> consider rewriting your indexed views and materialized views to use idiomatic
> Materialize SQL instead of window functions. If your view definitions cannot be
> rewritten without the window functions and the performance of window functions
> is insufficient for your use case, please [contact our team](/support/).

## Idiomatic Materialize SQL

**Idiomatic Materialize SQL:** To find the first value in each group, use
[MIN()](/sql/functions/#min) or [MAX()](/sql/functions/#max) aggregate function
in a subquery.

<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><blue>Materialize SQL</blue></td>
<td class="copyableCode">

<p>Use a subquery that uses the <a href="/sql/functions/#min" >MIN()</a> or
<a href="/sql/functions/#max" >MAX()</a> aggregate function.</p>
<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">tableA</span><span class="mf">.</span><span class="n">fieldA</span><span class="p">,</span> <span class="n">tableA</span><span class="mf">.</span><span class="n">fieldB</span><span class="p">,</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">Z</span>
</span></span><span class="line"><span class="cl"> <span class="k">FROM</span> <span class="n">tableA</span><span class="p">,</span>
</span></span><span class="line"><span class="cl"> <span class="p">(</span><span class="k">SELECT</span> <span class="n">fieldA</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="n">MIN</span><span class="p">(</span><span class="n">fieldZ</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">    <span class="k">MAX</span><span class="p">(</span><span class="n">fieldZ</span><span class="p">)</span>
</span></span><span class="line"><span class="cl"> <span class="k">FROM</span> <span class="n">tableA</span>
</span></span><span class="line"><span class="cl"> <span class="k">GROUP</span> <span class="k">BY</span> <span class="n">fieldA</span><span class="p">)</span> <span class="n">minmax</span>
</span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">tableA</span><span class="mf">.</span><span class="n">fieldA</span> <span class="o">=</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">fieldA</span>
</span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">fieldA</span> <span class="mf">...</span> <span class="p">;</span>
</span></span></code></pre></div>

</td>
</tr>

<tr>
<td><red>Anti-pattern</red> ❌</td>
<td>

<p><red>Avoid the use of <a href="/sql/functions/#first_value" ><code>FIRST_VALUE() OVER (PARTITION BY ... ORDER BY ...)</code>
window function</a> for first value within groups
queries.</red></p>
<pre tabindex="0"><code class="language-nofmt" data-lang="nofmt">-- Anti-pattern. Avoid. --
SELECT fieldA, fieldB,
 FIRST_VALUE(fieldZ) OVER (PARTITION BY fieldA ORDER BY ...),
 FIRST_VALUE(fieldZ) OVER (PARTITION BY fieldA ORDER BY ... DESC)
FROM tableA
ORDER BY fieldA, ...;
</code></pre>

</td>
</tr>

</tbody>
</table>

### Query hints

To further improve the memory usage of the idiomatic Materialize SQL, you can
specify a [`AGGREGATE INPUT GROUP SIZE` query hint](/sql/select/#query-hints) in
the idiomatic Materialize SQL.

```mzsql
SELECT tableA.fieldA, tableA.fieldB, minmax.Z
 FROM tableA,
 (SELECT fieldA,
    MIN(fieldZ),
    MAX(fieldZ)
 FROM tableA
 GROUP BY fieldA
 OPTIONS (AGGREGATE INPUT GROUP SIZE = ...)
 ) minmax
WHERE tableA.fieldA = minmax.fieldA
ORDER BY fieldA ... ;
```

For more information on setting `AGGREGATE INPUT GROUP SIZE`, see
[Optimization](/transform-data/optimization/#query-hints).

## Examples

> **Note:** The example data can be found in the
> [Appendix](/transform-data/idiomatic-materialize-sql/appendix/example-orders).

### Use MIN() to find the first value

Using idiomatic Materialize SQL, the following example finds the lowest item
price in each order and calculates the difference between the price of each item
in the order and the lowest price. The example uses a subquery that groups by
the `order_id` and selects `MIN(price)` to find the lowest price (i.e., first
value if ordered by ascending price values).

<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><blue>Materialize SQL</blue> ✅</td>
<td class="copyableCode">

<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span><span class="p">,</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">lowest_price</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">price</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="n">o</span><span class="mf">.</span><span class="n">price</span> <span class="o">-</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">lowest_price</span> <span class="k">AS</span> <span class="n">diff_lowest_price</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">orders_view</span> <span class="n">o</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="p">(</span><span class="k">SELECT</span> <span class="n">order_id</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">         <span class="n">MIN</span><span class="p">(</span><span class="n">price</span><span class="p">)</span> <span class="k">AS</span> <span class="n">lowest_price</span>
</span></span><span class="line"><span class="cl">      <span class="k">FROM</span> <span class="n">orders_view</span>
</span></span><span class="line"><span class="cl">      <span class="k">GROUP</span> <span class="k">BY</span> <span class="n">order_id</span><span class="p">)</span> <span class="n">minmax</span>
</span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span> <span class="o">=</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">order_id</span>
</span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span><span class="p">;</span>
</span></span></code></pre></div>

</td>
</tr>
<tr>
<td><red>Anti-pattern</red> ❌</td>
<td>

<p><red>Avoid the use of <a href="/sql/functions/#first_value" ><code>FIRST_VALUE() OVER (PARTITION BY ... ORDER BY ...)</code>
window function</a> for first value within groups queries.</red></p>
<pre tabindex="0"><code class="language-nofmt" data-lang="nofmt">-- Anti-pattern --
SELECT order_id,
  FIRST_VALUE(price)
    OVER (PARTITION BY order_id ORDER BY price) AS lowest_price,
  item,
  price,
  price - FIRST_VALUE(price)
    OVER (PARTITION BY order_id ORDER BY price) AS diff_lowest_price
FROM orders_view
ORDER BY order_id, item;
</code></pre>

</td>
</tr>
</tbody>
</table>

### Use MAX() to find the first value

Using idiomatic Materialize SQL, the following example finds the highest item
price in each order and calculates the difference between the price of each item
in the order and the highest price. The example uses a subquery that groups by
the `order_id` and selects `MAX(price)` to find the highest price (i.e., first
value if ordered by descending price values).

<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><blue>Materialize SQL</blue> ✅</td>
<td class="copyableCode">

<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span><span class="p">,</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">highest_price</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">price</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="n">o</span><span class="mf">.</span><span class="n">price</span> <span class="o">-</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">highest_price</span> <span class="k">AS</span> <span class="n">diff_highest_price</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">orders_view</span> <span class="n">o</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="p">(</span><span class="k">SELECT</span> <span class="n">order_id</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">         <span class="k">MAX</span><span class="p">(</span><span class="n">price</span><span class="p">)</span> <span class="k">AS</span> <span class="n">highest_price</span>
</span></span><span class="line"><span class="cl">      <span class="k">FROM</span> <span class="n">orders_view</span>
</span></span><span class="line"><span class="cl">      <span class="k">GROUP</span> <span class="k">BY</span> <span class="n">order_id</span><span class="p">)</span> <span class="n">minmax</span>
</span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span> <span class="o">=</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">order_id</span>
</span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span><span class="p">;</span>
</span></span></code></pre></div>

</td>
</tr>
<tr>
<td><red>Anti-pattern</red> ❌</td>
<td>

<p><red>Avoid the use of <a href="/sql/functions/#first_value" ><code>FIRST_VALUE() OVER (PARTITION BY ... ORDER BY ...)</code>
window function</a> for first value within groups
queries.</red></p>
<pre tabindex="0"><code class="language-nofmt" data-lang="nofmt">-- Anti-pattern --
SELECT order_id,
  FIRST_VALUE(price)
    OVER (PARTITION BY order_id ORDER BY price DESC) AS highest_price,
  item,
  price,
  price - FIRST_VALUE(price)
    OVER (PARTITION BY order_id ORDER BY price DESC) AS diff_highest_price
FROM orders_view
ORDER BY order_id, item;
</code></pre>

</td>
</tr>
</tbody>
</table>

### Use MIN() and MAX() to find the first values

Using idiomatic Materialize SQL, the following example finds the lowest and the
highest item price in each order and calculates the difference between each item
in the order and these prices. The example uses a subquery that groups by the
`order_id` and selects `MIN(price)` as the lowest price (i.e., first
value if ordered by price values) and `MAX(price)` as the
highest price (i.e., first
value if ordered by descending price values).

<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><blue>Materialize SQL</blue> ✅</td>
<td class="copyableCode">

<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span><span class="p">,</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">lowest_price</span><span class="p">,</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">highest_price</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">price</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="n">o</span><span class="mf">.</span><span class="n">price</span> <span class="o">-</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">lowest_price</span> <span class="k">AS</span> <span class="n">diff_lowest_price</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="n">o</span><span class="mf">.</span><span class="n">price</span> <span class="o">-</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">highest_price</span> <span class="k">AS</span> <span class="n">diff_highest_price</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">orders_view</span> <span class="n">o</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="p">(</span><span class="k">SELECT</span> <span class="n">order_id</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">         <span class="n">MIN</span><span class="p">(</span><span class="n">price</span><span class="p">)</span> <span class="k">AS</span> <span class="n">lowest_price</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">         <span class="k">MAX</span><span class="p">(</span><span class="n">price</span><span class="p">)</span> <span class="k">AS</span> <span class="n">highest_price</span>
</span></span><span class="line"><span class="cl">      <span class="k">FROM</span> <span class="n">orders_view</span>
</span></span><span class="line"><span class="cl">      <span class="k">GROUP</span> <span class="k">BY</span> <span class="n">order_id</span><span class="p">)</span> <span class="n">minmax</span>
</span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span> <span class="o">=</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">order_id</span>
</span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span><span class="p">;</span>
</span></span></code></pre></div>

</td>
</tr>
<tr>
<td><red>Anti-pattern</red> ❌</td>
<td>

<p><red>Avoid the use of <a href="/sql/functions/#first_value" ><code>FIRST_VALUE() OVER (PARTITION BY ... ORDER BY ...)</code>
window function</a> for first value within groups
queries.</red></p>
<pre tabindex="0"><code class="language-nofmt" data-lang="nofmt">-- Anti-pattern --
SELECT order_id,
  FIRST_VALUE(price)
    OVER (PARTITION BY order_id ORDER BY price) AS lowest_price,
  FIRST_VALUE(price)
    OVER (PARTITION BY order_id ORDER BY price DESC) AS highest_price,
  item,
  price,
  price - FIRST_VALUE(price)
    OVER (PARTITION BY order_id ORDER BY price) AS diff_lowest_price,
  price - FIRST_VALUE(price)
    OVER (PARTITION BY order_id ORDER BY price DESC) AS diff_highest_price
FROM orders_view
ORDER BY order_id, item;
</code></pre>

</td>
</tr>
</tbody>
</table>

## See also

- [Last value in a group](/transform-data/idiomatic-materialize-sql/last-value)
- [`MIN()`](/sql/functions/#min)
- [`MAX()`](/sql/functions/#max)
- [Query hints for MIN/MAX](/transform-data/optimization/#query-hints)
- [Window functions](/sql/functions/#window-functions)

---

## Lag over

## Overview

The "lag over (order by )" query pattern accesses the field value of the
previous row as determined by some ordering.

For "lag over (order by)" queries whose ordering can be represented by some
equality condition (such as when ordering by a field that increases at a regular
interval), Materialize provides an idiomatic SQL as an alternative to the window
function.

> ### Materialize and window functions
> For indexed views and materialized views that contain [window
> functions](/sql/functions/#window-functions) (including aggregate functions used
> with an `OVER` clause), when an input record in a partition is
> added/removed/changed, Materialize **recomputes the results from scratch** for
> that partition (instead of using incremental computation).
> The `PARTITION BY` clause of your window function determines your partitions. If
> `PARTITION BY` is omitted, all records belong to a single partition (i.e., any
> record change results in a recomputation from scratch over the whole input).
> To avoid performance issues that may arise as the number of records grows,
> consider rewriting your indexed views and materialized views to use idiomatic
> Materialize SQL instead of window functions. If your view definitions cannot be
> rewritten without the window functions and the performance of window functions
> is insufficient for your use case, please [contact our team](/support/).

## Idiomatic Materialize SQL

> **Important:** Do not use if the "lag over (order by)" ordering cannot be represented by an
> equality match.

### Exclude the first row in results

**Idiomatic Materialize SQL:** To access the lag (previous row's field value)
ordered by some field that increases in a **regular** pattern, use a self join
that specifies an **equality condition** on the order by field (e.g., `WHERE
t1.order_field = t2.order_field + 1`, `WHERE t1.order_field = t2.order_field *
2`, etc.). The query *excludes* the first row since it does not have a previous
row.

<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><blue>Idiomatic Materialize SQL</blue></td>
<td class="copyableCode">

<p>Use a self join that specifies an <strong>equality match</strong> on the lag&rsquo;s order by field
(e.g., <code>fieldA</code>). The order by field must increment in a regular pattern in
order to be represented by an equality condition (e.g., <code>WHERE t1.fieldA = t2.fieldA + ...</code>). The
query <em>excludes</em> the first row in the results since it does not have a previous
row.</p>
> **Important:** The idiomatic Materialize SQL applies only to those "lag over" queries whose
> ordering can be represented by some **equality condition**.

<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="c1">-- Excludes the first row in the results --
</span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="k">SELECT</span> <span class="n">t1</span><span class="mf">.</span><span class="n">fieldA</span><span class="p">,</span> <span class="n">t2</span><span class="mf">.</span><span class="n">fieldB</span> <span class="k">as</span> <span class="n">previous_row_value</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">tableA</span> <span class="n">t1</span><span class="p">,</span> <span class="n">tableA</span> <span class="n">t2</span>
</span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">t1</span><span class="mf">.</span><span class="n">fieldA</span> <span class="o">=</span> <span class="n">t2</span><span class="mf">.</span><span class="n">fieldA</span> <span class="o">+</span> <span class="mf">...</span> <span class="c1">-- or some other operand
</span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">fieldA</span><span class="p">;</span>
</span></span></code></pre></div>

</td>
</tr>

<tr>
<td><red>Anti-pattern</red> ❌</td>
<td>

<p><red>Avoid the use of <a href="/sql/functions/#lag" ><code>LAG(fieldZ) OVER (ORDER BY ...)</code></a>
window function when the order by field increases in a regular pattern.</red></p>
<pre tabindex="0"><code class="language-nofmt" data-lang="nofmt">-- Anti-pattern. Avoid. --
SELECT fieldA, ...
    LAG(fieldZ) OVER (ORDER BY fieldA) as previous_row_value
FROM tableA;
</code></pre>

</td>
</tr>

</tbody>
</table>

### Include the first row in results

**Idiomatic Materialize SQL:** To access the lag (previous row's field value)
ordered by some field that increases in a **regular** pattern, use a self
[`LEFT JOIN/LEFT OUTER JOIN`](/sql/select/join/#left-outer-join) that specifies
an **equality condition** on the order by field (e.g., `ON t1.order_field =
t2.order_field + 1`, `ON t1.order_field = t2.order_field * 2`, etc.). The `LEFT
JOIN/LEFT OUTER JOIN` query *includes* the first row, returning `null` as its
lag value.

<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><blue>Idiomatic Materialize SQL</blue></td>
<td class="copyableCode">

<p>Use a self <a href="/sql/select/join/#left-outer-join" ><code>LEFT JOIN/LEFT OUTER JOIN</code></a>
(e.g., <code>FROM tableA t1 LEFT JOIN tableA t2</code>) that specifies an <strong>equality
match</strong> on the lag&rsquo;s order by field (e.g., <code>fieldA</code>). The order by field must
increment in a regular pattern in order to be represented by an equality
condition (e.g., <code>ON t1.fieldA = t2.fieldA + ...</code>). The
query <em>includes</em> the first row, returning <code>null</code> as its lag value.</p>
> **Important:** The idiomatic Materialize SQL applies only to those "lag over" queries whose
> ordering can be represented by some **equality condition**.

<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="c1">-- Includes the first row in the results --
</span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="k">SELECT</span> <span class="n">t1</span><span class="mf">.</span><span class="n">fieldA</span><span class="p">,</span> <span class="n">t2</span><span class="mf">.</span><span class="n">fieldB</span> <span class="k">as</span> <span class="n">previous_row_value</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">tableA</span> <span class="n">t1</span>
</span></span><span class="line"><span class="cl"><span class="k">LEFT</span> <span class="k">JOIN</span> <span class="n">tableA</span> <span class="n">t2</span>
</span></span><span class="line"><span class="cl"><span class="k">ON</span> <span class="n">t1</span><span class="mf">.</span><span class="n">fieldA</span> <span class="o">=</span> <span class="n">t2</span><span class="mf">.</span><span class="n">fieldA</span> <span class="o">+</span> <span class="mf">...</span> <span class="c1">-- or some other operand
</span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">fieldA</span><span class="p">;</span>
</span></span></code></pre></div>

</td>
</tr>

<tr>
<td><red>Anti-pattern</red> ❌</td>
<td>

<p><red>Avoid the use of <a href="/sql/functions/#lag" ><code>LAG(fieldZ) OVER (ORDER BY ...)</code></a>
window function when the order by field increases in a regular pattern.</red></p>
<pre tabindex="0"><code class="language-nofmt" data-lang="nofmt">-- Anti-pattern. Avoid. --
SELECT fieldA, ...
    LAG(fieldZ) OVER (ORDER BY fieldA) as previous_row_value
FROM tableA;
</code></pre>

</td>
</tr>

</tbody>
</table>

## Examples

> **Note:** The example data can be found in the
> [Appendix](/transform-data/idiomatic-materialize-sql/appendix/example-orders).

### Find previous row's value (exclude the first row in results)

Using idiomatic Materialize SQL, the following example finds the previous day's
order total. That is, the example uses a self join on `orders_daily_totals`. The
row ordering on the `order_date` field is represented by an **equality
condition** using an [interval of `1
DAY`](/sql/types/interval/#valid-operations). The
query excludes the first row in the results since the first row does not have a
previous row.

<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>

<tr>
<td><blue>Materialize SQL</blue> ✅</td>
<td class="copyableCode">

<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="c1">-- Excludes the first row in results --
</span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="k">SELECT</span> <span class="n">o1</span><span class="mf">.</span><span class="n">order_date</span><span class="p">,</span> <span class="n">o1</span><span class="mf">.</span><span class="n">daily_total</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="n">o2</span><span class="mf">.</span><span class="n">daily_total</span> <span class="k">as</span> <span class="n">previous_daily_total</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">orders_daily_totals</span> <span class="n">o1</span><span class="p">,</span> <span class="n">orders_daily_totals</span> <span class="n">o2</span>
</span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">o1</span><span class="mf">.</span><span class="n">order_date</span> <span class="o">=</span> <span class="n">o2</span><span class="mf">.</span><span class="n">order_date</span> <span class="o">+</span> <span class="nb">INTERVAL</span> <span class="s1">&#39;1&#39;</span> <span class="k">DAY</span>
</span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">order_date</span><span class="p">;</span>
</span></span></code></pre></div>> **Important:** The idiomatic Materialize SQL applies only to those "lag over" queries whose
> ordering can be represented by some **equality condition**.

</td>
</tr>

<tr>
<td><red>Anti-pattern</red> ❌</td>
<td>

<p><red>Avoid the use of <a href="/sql/functions/#lag" ><code>LAG() OVER (ORDER BY ...)</code> window
function</a> to access previous row&rsquo;s value if the order by
field increases in a regular pattern.</red></p>
<pre tabindex="0"><code class="language-nofmt" data-lang="nofmt">-- Anti-pattern. Includes the first row&#39;s value. --
SELECT order_date, daily_total,
    LAG(daily_total) OVER (ORDER BY order_date) as previous_daily_total
FROM orders_daily_totals;
</code></pre>

</td>
</tr>
</tbody>
</table>

### Find previous row's value (include the first row in results)

Using idiomatic Materialize SQL, the following example finds the previous day's
order total. The example uses a self [`LEFT JOIN/LEFT OUTER
JOIN`](/sql/select/join/#left-outer-join) on `orders_daily_totals`. The
row ordering on the `order_date` field is represented by an **equality
condition** using an [interval of `1
DAY`](/sql/types/interval/#valid-operations). The
query includes the first row in the results, using `null` as the previous value.

<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>

<tr>
<td><blue>Materialize SQL</blue> ✅</td>
<td class="copyableCode">

<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="c1">-- Include the first row in results --
</span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="k">SELECT</span> <span class="n">o1</span><span class="mf">.</span><span class="n">order_date</span><span class="p">,</span> <span class="n">o1</span><span class="mf">.</span><span class="n">daily_total</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="n">o2</span><span class="mf">.</span><span class="n">daily_total</span> <span class="k">as</span> <span class="n">previous_daily_total</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">orders_daily_totals</span> <span class="n">o1</span>
</span></span><span class="line"><span class="cl"><span class="k">LEFT</span> <span class="k">JOIN</span> <span class="n">orders_daily_totals</span> <span class="n">o2</span>
</span></span><span class="line"><span class="cl"><span class="k">ON</span> <span class="n">o1</span><span class="mf">.</span><span class="n">order_date</span> <span class="o">=</span> <span class="n">o2</span><span class="mf">.</span><span class="n">order_date</span> <span class="o">+</span> <span class="nb">INTERVAL</span> <span class="s1">&#39;1&#39;</span> <span class="k">DAY</span>
</span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">order_date</span><span class="p">;</span>
</span></span></code></pre></div>> **Important:** The idiomatic Materialize SQL applies only to those "lag over" queries whose
> ordering can be represented by some **equality condition**.

</td>
</tr>

<tr>
<td><red>Anti-pattern</red> ❌</td>
<td>

<p><red>Avoid the use of <a href="/sql/functions/#lag" ><code>LAG() OVER (ORDER BY ...)</code> window
function</a> to access previous row&rsquo;s value if the order by
field increases in a regular pattern.</red></p>
<pre tabindex="0"><code class="language-nofmt" data-lang="nofmt">-- Anti-pattern. Includes the first row&#39;s value. --
SELECT order_date, daily_total,
    LAG(daily_total) OVER (ORDER BY order_date) as previous_daily_total
FROM orders_daily_totals;
</code></pre>

</td>
</tr>

</tbody>
</table>

## See also

- [Lead over](/transform-data/idiomatic-materialize-sql/lead)
- [`INTERVAL`](/sql/types/interval/)
- [`LEFT JOIN/LEFT OUTER JOIN`](/sql/select/join/#left-outer-join)
- [`LAG()`](/sql/functions/#lag)
- [Window functions](/sql/functions/#window-functions)

---

## Last value in group

## Overview

The "last value in each group" query pattern returns the last value, according
to some ordering, in each group.

> ### Materialize and window functions
> For indexed views and materialized views that contain [window
> functions](/sql/functions/#window-functions) (including aggregate functions used
> with an `OVER` clause), when an input record in a partition is
> added/removed/changed, Materialize **recomputes the results from scratch** for
> that partition (instead of using incremental computation).
> The `PARTITION BY` clause of your window function determines your partitions. If
> `PARTITION BY` is omitted, all records belong to a single partition (i.e., any
> record change results in a recomputation from scratch over the whole input).
> To avoid performance issues that may arise as the number of records grows,
> consider rewriting your indexed views and materialized views to use idiomatic
> Materialize SQL instead of window functions. If your view definitions cannot be
> rewritten without the window functions and the performance of window functions
> is insufficient for your use case, please [contact our team](/support/).

## Idiomatic Materialize SQL

**Idiomatic Materialize SQL:** To find the last value in each group, use the
[MIN()](/sql/functions/#min) or [MAX()](/sql/functions/#max) aggregate function
in a subquery.

<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><blue>Idiomatic Materialize SQL</blue></td>
<td class="copyableCode">

<p>Use a subquery that uses the <a href="/sql/functions/#min" >MIN()</a> or
<a href="/sql/functions/#max" >MAX()</a> aggregate function.</p>
<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">tableA</span><span class="mf">.</span><span class="n">fieldA</span><span class="p">,</span> <span class="n">tableA</span><span class="mf">.</span><span class="n">fieldB</span><span class="p">,</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">Z</span>
</span></span><span class="line"><span class="cl"> <span class="k">FROM</span> <span class="n">tableA</span><span class="p">,</span>
</span></span><span class="line"><span class="cl"> <span class="p">(</span><span class="k">SELECT</span> <span class="n">fieldA</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="k">MAX</span><span class="p">(</span><span class="n">fieldZ</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">    <span class="n">MIN</span><span class="p">(</span><span class="n">fieldZ</span><span class="p">)</span>
</span></span><span class="line"><span class="cl"> <span class="k">FROM</span> <span class="n">tableA</span>
</span></span><span class="line"><span class="cl"> <span class="k">GROUP</span> <span class="k">BY</span> <span class="n">fieldA</span><span class="p">)</span> <span class="n">minmax</span>
</span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">tableA</span><span class="mf">.</span><span class="n">fieldA</span> <span class="o">=</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">fieldA</span>
</span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">fieldA</span> <span class="mf">...</span> <span class="p">;</span>
</span></span></code></pre></div>

</td>
</tr>

<tr>
<td><red>Anti-pattern</red> ❌</td>
<td>

<p><red>Do not use <a href="/sql/functions/#last_value" ><code>LAST_VALUE() OVER (PARTITION BY ... ORDER BY ... RANGE ...)</code> window function</a> for last value in each group
queries.</red></p>
> **Note:** Materialize does not support `RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED
> FOLLOWING`.

<pre tabindex="0"><code class="language-nofmt" data-lang="nofmt">-- Unsupported --
SELECT fieldA, fieldB,
  LAST_VALUE(fieldZ)
    OVER (PARTITION BY fieldA ORDER BY fieldZ
          RANGE BETWEEN
            UNBOUNDED PRECEDING AND
            UNBOUNDED FOLLOWING),
  LAST_VALUE(fieldZ)
    OVER (PARTITION BY fieldA ORDER BY fieldZ DESC
          RANGE BETWEEN
            UNBOUNDED PRECEDING AND
            UNBOUNDED FOLLOWING)
FROM tableA
ORDER BY fieldA, ...;
</code></pre>

</td>
</tr>

</tbody>
</table>

### Query hints

To further improve the memory usage of the idiomatic Materialize SQL, you can
specify a [`AGGREGATE INPUT GROUP SIZE` query hint](/sql/select/#query-hints) in
the idiomatic Materialize SQL.

```mzsql
SELECT tableA.fieldA, tableA.fieldB, minmax.Z
 FROM tableA,
 (SELECT fieldA,
    MAX(fieldZ),
    MIN(fieldZ)
 FROM tableA
 GROUP BY fieldA
 OPTIONS (AGGREGATE INPUT GROUP SIZE = ...)
 ) minmax
WHERE tableA.fieldA = minmax.fieldA
ORDER BY fieldA ... ;
```

For more information on setting `AGGREGATE INPUT GROUP SIZE`, see
[Optimization](/transform-data/optimization/#query-hints).

## Examples

> **Note:** The example data can be found in the
> [Appendix](/transform-data/idiomatic-materialize-sql/appendix/example-orders).

### Use MAX() to find the last value

Using idiomatic Materialize SQL, the following example finds the highest item
price in each order and calculates the difference between the price of each item
in the order and the highest price. The example uses a subquery that groups by
the `order_id` and selects [`MAX(price)`](/sql/functions/#max)  to find the
highest price (i.e., the last price if ordered by ascending price values):

<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><blue>Idiomatic Materialize SQL</blue> ✅</td>
<td class="copyableCode">

<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span><span class="p">,</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">highest_price</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">price</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="n">o</span><span class="mf">.</span><span class="n">price</span> <span class="o">-</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">highest_price</span> <span class="k">AS</span> <span class="n">diff_highest_price</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">orders_view</span> <span class="n">o</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">     <span class="p">(</span><span class="k">SELECT</span> <span class="n">order_id</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="k">MAX</span><span class="p">(</span><span class="n">price</span><span class="p">)</span> <span class="k">AS</span> <span class="n">highest_price</span>
</span></span><span class="line"><span class="cl">     <span class="k">FROM</span> <span class="n">orders_view</span>
</span></span><span class="line"><span class="cl">     <span class="k">GROUP</span> <span class="k">BY</span> <span class="n">order_id</span><span class="p">)</span> <span class="n">minmax</span>
</span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span> <span class="o">=</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">order_id</span>
</span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span><span class="p">;</span>
</span></span></code></pre></div>

</td>
</tr>

<tr>
<td><red>Anti-pattern</red> ❌</td>
<td>

<p><red>Do not use of <code>LAST_VALUE() OVER (PARTITION BY ... ORDER BY ... RANGE ...)</code>
for last value in each group queries.</red></p>
> **Note:** Materialize does not support `RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED
> FOLLOWING`.

<pre tabindex="0"><code class="language-nofmt" data-lang="nofmt">-- Unsupported --
SELECT order_id,
  LAST_VALUE(price)
    OVER (PARTITION BY order_id ORDER BY price
          RANGE BETWEEN
            UNBOUNDED PRECEDING AND
            UNBOUNDED FOLLOWING) AS highest_price,
  item,
  price,
  price - LAST_VALUE(price)
    OVER (PARTITION BY order_id ORDER BY price
           RANGE BETWEEN
            UNBOUNDED PRECEDING AND
            UNBOUNDED FOLLOWING) AS diff_highest_price
FROM orders_view
ORDER BY order_id, item;
</code></pre>

</td>
</tr>
</tbody>
</table>

### Use MIN() to find the last values

Using idiomatic Materialize SQL, the following example finds the lowest item
price in each order and calculates the difference between the price of each item
in the order and the lowest price.  That is, use a subquery that groups by the
`order_id` and selects [`MIN(price)`](/sql/functions/#min)  as the lowest price
(i.e.,  last price if ordered by descending price value)

<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><blue>Idiomatic Materialize SQL</blue> ✅</td>
<td class="copyableCode">

<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span><span class="p">,</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">lowest_price</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">price</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="n">o</span><span class="mf">.</span><span class="n">price</span> <span class="o">-</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">lowest_price</span> <span class="k">AS</span> <span class="n">diff_lowest_price</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">orders_view</span> <span class="n">o</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">     <span class="p">(</span><span class="k">SELECT</span> <span class="n">order_id</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">MIN</span><span class="p">(</span><span class="n">price</span><span class="p">)</span> <span class="k">AS</span> <span class="n">lowest_price</span>
</span></span><span class="line"><span class="cl">     <span class="k">FROM</span> <span class="n">orders_view</span>
</span></span><span class="line"><span class="cl">     <span class="k">GROUP</span> <span class="k">BY</span> <span class="n">order_id</span><span class="p">)</span> <span class="n">minmax</span>
</span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span> <span class="o">=</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">order_id</span>
</span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span><span class="p">;</span>
</span></span></code></pre></div>

</td>
</tr>

<tr>
<td><red>Anti-pattern</red> ❌</td>
<td>

<p><red>Do not use <code>LAST_VALUE() OVER (PARTITION BY ... ORDER BY ... RANGE ... )</code>
for last value in each group queries.</red></p>
> **Note:** Materialize does not support `RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED
> FOLLOWING`.

<pre tabindex="0"><code class="language-nofmt" data-lang="nofmt">-- Unsupported --
SELECT order_id,
  LAST_VALUE(price)
    OVER (PARTITION BY order_id ORDER BY price DESC
          RANGE BETWEEN
            UNBOUNDED PRECEDING AND
            UNBOUNDED FOLLOWING) AS lowest_price,
  item,
  price,
  price - LAST_VALUE(price)
    OVER (PARTITION BY order_id ORDER BY price DESC
          RANGE BETWEEN
            UNBOUNDED PRECEDING AND
            UNBOUNDED FOLLOWING) AS diff_lowest_price
FROM orders_view
ORDER BY order_id, item;
</code></pre>

</td>
</tr>
</tbody>
</table>

### Use MIN() and MAX() to find the last values

Using idiomatic Materialize SQL, the following example finds the lowest and
highest item price in each order and calculate the difference for each item in
the order from these prices. That is, use a subquery that groups by the
`order_id` and selects [`MIN(price)`](/sql/functions/#min) as the lowest price
(i.e., last value if ordered by descending price values) and
[`MAX(price)`](/sql/functions/#max) as the highest price (i.e., last value if
ordered by ascending price values).

<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><blue>Idiomatic Materialize SQL</blue> ✅</td>
<td class="copyableCode">

<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span><span class="p">,</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">lowest_price</span><span class="p">,</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">highest_price</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">price</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="n">o</span><span class="mf">.</span><span class="n">price</span> <span class="o">-</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">lowest_price</span> <span class="k">AS</span> <span class="n">diff_lowest_price</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="n">o</span><span class="mf">.</span><span class="n">price</span> <span class="o">-</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">highest_price</span> <span class="k">AS</span> <span class="n">diff_highest_price</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">orders_view</span> <span class="n">o</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="p">(</span><span class="k">SELECT</span> <span class="n">order_id</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">         <span class="n">MIN</span><span class="p">(</span><span class="n">price</span><span class="p">)</span> <span class="k">AS</span> <span class="n">lowest_price</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">         <span class="k">MAX</span><span class="p">(</span><span class="n">price</span><span class="p">)</span> <span class="k">AS</span> <span class="n">highest_price</span>
</span></span><span class="line"><span class="cl">      <span class="k">FROM</span> <span class="n">orders_view</span>
</span></span><span class="line"><span class="cl">      <span class="k">GROUP</span> <span class="k">BY</span> <span class="n">order_id</span><span class="p">)</span> <span class="n">minmax</span>
</span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span> <span class="o">=</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">order_id</span>
</span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span><span class="p">;</span>
</span></span></code></pre></div>

</td>
</tr>
<tr>
<td><red>Anti-pattern</red> ❌</td>
<td>

<p><red>Do not use <code>LAST_VALUE() OVER (PARTITION BY ... ORDER BY ...)</code> for last
value within groups queries.</red></p>
> **Note:** Materialize does not support `RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED
> FOLLOWING`.

<pre tabindex="0"><code class="language-nofmt" data-lang="nofmt">-- Unsupported --
SELECT order_id,
  LAST_VALUE(price)
    OVER (PARTITION BY order_id ORDER BY price DESC
          RANGE BETWEEN
            UNBOUNDED PRECEDING AND
            UNBOUNDED FOLLOWING) AS lowest_price,
  LAST_VALUE(price)
    OVER (PARTITION BY order_id ORDER BY price
          RANGE BETWEEN
            UNBOUNDED PRECEDING AND
            UNBOUNDED FOLLOWING) AS highest_price,
  item,
  price,
  price - LAST_VALUE(price)
    OVER (PARTITION BY order_id ORDER BY price DESC
          RANGE BETWEEN
            UNBOUNDED PRECEDING AND
            UNBOUNDED FOLLOWING) AS diff_lowest_price,
  price - LAST_VALUE(price)
    OVER (PARTITION BY order_id ORDER BY price
           RANGE BETWEEN
            UNBOUNDED PRECEDING AND
            UNBOUNDED FOLLOWING) AS diff_highest_price
FROM orders_view
ORDER BY order_id, item;
</code></pre>

</td>
</tr>

</tbody>
</table>

## See also

- [First value in a
  group](/transform-data/idiomatic-materialize-sql/first-value)
- [`MIN()`](/sql/functions/#min)
- [`MAX()`](/sql/functions/#max)
- [Query hints for MIN/MAX](/transform-data/optimization/#query-hints)
- [Window functions](/sql/functions/#window-functions)

---

## Lead over

## Overview

The "lead over" query pattern accesses the field value of the next row as
determined by some ordering.

For "lead over (order by)" queries whose ordering can be represented by some
equality condition (such as when ordering by a field that increases at a regular
interval), Materialize provides an idiomatic SQL as an alternative to the window
function.

> ### Materialize and window functions
> For indexed views and materialized views that contain [window
> functions](/sql/functions/#window-functions) (including aggregate functions used
> with an `OVER` clause), when an input record in a partition is
> added/removed/changed, Materialize **recomputes the results from scratch** for
> that partition (instead of using incremental computation).
> The `PARTITION BY` clause of your window function determines your partitions. If
> `PARTITION BY` is omitted, all records belong to a single partition (i.e., any
> record change results in a recomputation from scratch over the whole input).
> To avoid performance issues that may arise as the number of records grows,
> consider rewriting your indexed views and materialized views to use idiomatic
> Materialize SQL instead of window functions. If your view definitions cannot be
> rewritten without the window functions and the performance of window functions
> is insufficient for your use case, please [contact our team](/support/).

## Idiomatic Materialize SQL

> **Important:** Do not use if the "lead over (order by)" ordering cannot be represented by an
> equality match.

### Exclude the last row in results

**Idiomatic Materialize SQL:** To access the lead (next row's field value)
ordered by some field that increases in **regular** intervals, use a self join
that specifies an **equality condition** on the order by field (e.g., `WHERE
t1.order_field = t2.order_field - 1`, `WHERE t1.order_field = t2.order_field *
2`, etc.). The query *excludes* the last row in the results since it does not
have a next row.

<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><blue>Idiomatic Materialize SQL</blue></td>
<td class="copyableCode">

<p>Use a self join that specifies an <strong>equality match</strong> on the lead&rsquo;s order by
field (e.g., <code>fieldA</code>). The order by field must increment in a regular pattern
in order to be represented by an equality condition (e.g., <code>WHERE t1.fieldA = t2.fieldA - ...</code>). The query <em>excludes</em> the last row in the results since it
does not have a next row.</p>
> **Important:** The idiomatic Materialize SQL applies only to those "lead over" queries whose
> ordering can be represented by some **equality condition**.

<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="c1">-- Excludes the last row in the results --
</span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="k">SELECT</span> <span class="n">t1</span><span class="mf">.</span><span class="n">fieldA</span><span class="p">,</span> <span class="n">t2</span><span class="mf">.</span><span class="n">fieldB</span> <span class="k">as</span> <span class="n">next_row_value</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">tableA</span> <span class="n">t1</span><span class="p">,</span> <span class="n">tableA</span> <span class="n">t2</span>
</span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">t1</span><span class="mf">.</span><span class="n">fieldA</span> <span class="o">=</span> <span class="n">t2</span><span class="mf">.</span><span class="n">fieldA</span> <span class="o">-</span> <span class="mf">...</span>  <span class="c1">-- or some other operand
</span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">fieldA</span><span class="p">;</span>
</span></span></code></pre></div>

</td>
</tr>

<tr>
<td><red>Anti-pattern</red> ❌</td>
<td>

<p><red>Avoid the use of <a href="/sql/functions/#lead" ><code>LEAD(fieldZ) OVER (ORDER BY ...)</code></a>
window function when the order by field increases in a regular pattern.</red></p>
<pre tabindex="0"><code class="language-nofmt" data-lang="nofmt">-- Anti-pattern. Avoid. --
SELECT fieldA, ...
    LEAD(fieldZ) OVER (ORDER BY fieldA) as next_row_value
FROM tableA;
</code></pre>

</td>
</tr>

</tbody>
</table>

### Include the last row in results

**Idiomatic Materialize SQL:** To access the lead (next row's field value)
ordered by some field that increases in **regular** intervals, use a self [`LEFT
JOIN/LEFT OUTER JOIN`](/sql/select/join/#left-outer-join) that specifies an
**equality condition** on the order by field (e.g., `ON t1.order_field =
t2.order_field - 1`, `ON t1.order_field = t2.order_field * 2`, etc.). The `LEFT
JOIN/LEFT OUTER JOIN` query *includes* the last row, returning `null` as its
lead value.

<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><blue>Idiomatic Materialize SQL</blue></td>
<td class="copyableCode">

<p>Use a self <a href="/sql/select/join/#left-outer-join" ><code>LEFT JOIN/LEFT OUTER JOIN</code></a>
(e.g., <code>FROM tableA t1 LEFT JOIN tableA t2</code>) that specifies an <strong>equality
match</strong> on the lag&rsquo;s order by field (e.g., <code>fieldA</code>).  The order by field must
increment in a regular pattern in order to be represented by an equality
condition (e.g., <code>ON t1.fieldA = t2.fieldA - ...</code>). The query <em>includes</em> the
last row, returning <code>null</code> as its lead value.</p>
> **Important:** The idiomatic Materialize SQL applies only to those "lead over" queries whose
> ordering can be represented by some **equality condition**.

<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="c1">-- Includes the last row in the response --
</span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="k">SELECT</span> <span class="n">t1</span><span class="mf">.</span><span class="n">fieldA</span><span class="p">,</span> <span class="n">t2</span><span class="mf">.</span><span class="n">fieldB</span> <span class="k">as</span> <span class="n">next_row_value</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">tableA</span> <span class="n">t1</span>
</span></span><span class="line"><span class="cl"><span class="k">LEFT</span> <span class="k">JOIN</span> <span class="n">tableA</span> <span class="n">t2</span>
</span></span><span class="line"><span class="cl"><span class="k">ON</span> <span class="n">t1</span><span class="mf">.</span><span class="n">fieldA</span> <span class="o">=</span> <span class="n">t2</span><span class="mf">.</span><span class="n">fieldA</span> <span class="o">-</span> <span class="mf">...</span> <span class="c1">-- or some other operand
</span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">fieldA</span><span class="p">;</span>
</span></span></code></pre></div>

</td>
</tr>

<tr>
<td><red>Anti-pattern</red> ❌</td>
<td>

<p><red>Avoid the use of <a href="/sql/functions/#lead" ><code>LEAD(fieldZ) OVER (ORDER BY ...)</code></a>
window function when the order by field increases in a regular pattern.</red></p>
<pre tabindex="0"><code class="language-nofmt" data-lang="nofmt">-- Anti-pattern. Avoid. --
SELECT fieldA, ...
    LEAD(fieldZ) OVER (ORDER BY fieldA) as next_row_value
FROM tableA;
</code></pre>

</td>
</tr>

</tbody>
</table>

## Examples

> **Note:** The example data can be found in the
> [Appendix](/transform-data/idiomatic-materialize-sql/appendix/example-orders).

### Find next row's value (exclude the last row in results)

Using idiomatic Materialize SQL, the following example finds the next day's
order total. That is, the example uses a self join on `orders_daily_totals`. The
row ordering on the `order_date` field is represented by an **equality
condition** using an [interval of `1
DAY`](/sql/types/interval/#valid-operations). The
query excludes the last row in the results since the last row does not have a
next row.

<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>

<tr>
<td><blue>Materialize SQL</blue> ✅</td>
<td class="copyableCode">

<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="c1">-- Excludes the last row in results --
</span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="k">SELECT</span> <span class="n">o1</span><span class="mf">.</span><span class="n">order_date</span><span class="p">,</span> <span class="n">o1</span><span class="mf">.</span><span class="n">daily_total</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="n">o2</span><span class="mf">.</span><span class="n">daily_total</span> <span class="k">as</span> <span class="n">next_daily_total</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">orders_daily_totals</span> <span class="n">o1</span><span class="p">,</span> <span class="n">orders_daily_totals</span> <span class="n">o2</span>
</span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">o1</span><span class="mf">.</span><span class="n">order_date</span> <span class="o">=</span> <span class="n">o2</span><span class="mf">.</span><span class="n">order_date</span> <span class="o">-</span> <span class="nb">INTERVAL</span> <span class="s1">&#39;1&#39;</span> <span class="k">DAY</span>
</span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">order_date</span><span class="p">;</span>
</span></span></code></pre></div>> **Important:** The idiomatic Materialize SQL applies only to those "lead over" queries whose
> ordering can be represented by some **equality condition**.

</td>
</tr>

<tr>
<td><red>Anti-pattern</red> ❌</td>
<td>

<p><red>Avoid the use of <a href="/sql/functions/#lead" ><code>LEAD() OVER (ORDER BY ...)</code> window
function</a> to access next row&rsquo;s value if the order by
field increases in a regular pattern.</red></p>
<pre tabindex="0"><code class="language-nofmt" data-lang="nofmt">-- Anti-pattern. Includes the last row&#39;s value. --
SELECT order_date, daily_total,
    LEAD(daily_total) OVER (ORDER BY order_date) as next_daily_total
FROM orders_daily_totals;
</code></pre>

</td>
</tr>
</tbody>
</table>

### Find next row's value (include the last row in results)

Using idiomatic Materialize SQL, the following example finds the next day's
order total. The example uses a self [`LEFT JOIN/LEFT OUTER
JOIN`](/sql/select/join/#left-outer-join) on `orders_daily_totals`. The row
ordering on the `order_date` field is represented by an **equality condition**
using an [interval of `1
DAY`](/sql/types/interval/#valid-operations)). The
query includes the last row in the results, using `null` as the next row's
value.

<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>

<tr>
<td><blue>Materialize SQL</blue> ✅</td>
<td class="copyableCode">

<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="c1">-- Include the last row in the results --
</span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="k">SELECT</span> <span class="n">o1</span><span class="mf">.</span><span class="n">order_date</span><span class="p">,</span> <span class="n">o1</span><span class="mf">.</span><span class="n">daily_total</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="n">o2</span><span class="mf">.</span><span class="n">daily_total</span> <span class="k">as</span> <span class="n">next_daily_total</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">orders_daily_totals</span> <span class="n">o1</span>
</span></span><span class="line"><span class="cl"><span class="k">LEFT</span> <span class="k">JOIN</span> <span class="n">orders_daily_totals</span> <span class="n">o2</span>
</span></span><span class="line"><span class="cl"><span class="k">ON</span> <span class="n">o1</span><span class="mf">.</span><span class="n">order_date</span> <span class="o">=</span> <span class="n">o2</span><span class="mf">.</span><span class="n">order_date</span> <span class="o">-</span> <span class="nb">INTERVAL</span> <span class="s1">&#39;1&#39;</span> <span class="k">DAY</span>
</span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">order_date</span><span class="p">;</span>
</span></span></code></pre></div>> **Important:** The idiomatic Materialize SQL applies only to those "lead over" queries whose
> ordering can be represented by some **equality condition**.

</td>
</tr>

<tr>
<td><red>Anti-pattern</red> ❌</td>
<td>

<p><red>Avoid the use of <a href="/sql/functions/#lead" ><code>LEAD() OVER (ORDER BY ...)</code> window
function</a> to access next row&rsquo;s value if the order by
field increases in a regular pattern.</red></p>
<pre tabindex="0"><code class="language-nofmt" data-lang="nofmt">-- Anti-pattern. Includes the last row&#39;s value. --
SELECT order_date, daily_total,
    LEAD(daily_total) OVER (ORDER BY order_date) as next_daily_total
FROM orders_daily_totals;
</code></pre>

</td>
</tr>

</tbody>
</table>

## See also

- [Lag over](/transform-data/idiomatic-materialize-sql/lag)
- [`INTERVAL`](/sql/types/interval/)
- [`LEFT JOIN/LEFT OUTER JOIN`](/sql/select/join/#left-outer-join)
- [`LEAD()`](/sql/functions/#lead)
- [Window functions](/sql/functions/#window-functions)

---

## mz_now() expressions

## Overview

In Materialize, [`mz_now()`](/sql/functions/now_and_mz_now/) function returns
Materialize's current virtual timestamp (i.e., returns
[`mz_timestamp`](/sql/types/mz_timestamp/)). The function can be used in
[temporal filters](/transform-data/patterns/temporal-filters/) to reduce the
working dataset.

`mz_now()` expression has the following form:

```mzsql
mz_now() <comparison_operator> <numeric_expr | timestamp_expr>
```

## Idiomatic Materialize SQL

### `mz_now()` expressions to calculate past or future timestamp

**Idiomatic Materialize SQL**: <code>mz_now()</code> must be used with one of the following comparison operators: <code>=</code>,
<code>&lt;</code>, <code>&lt;=</code>, <code>&gt;</code>, <code>&gt;=</code>, or an operator that desugars to them or to a conjunction
(<code>AND</code>) of them (for example, <code>BETWEEN...AND...</code>). That is, you cannot use
date/time operations directly on  <code>mz_now()</code> to calculate a timestamp in the
past or future. Instead, rewrite the query expression to move the operation to
the other side of the comparison.

#### Examples

| <blue>Materialize SQL</blue> ✅ | <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">mz_now</span><span class="p">()</span> <span class="o">&gt;</span> <span class="n">order_date</span> <span class="o">+</span> <span class="nb">INTERVAL</span> <span class="s1">&#39;5min&#39;</span><span class="p">;</span> </span></span></code></pre></div> |
| <red>Anti-pattern</red> ❌ | <p><red>Not supported</red></p> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">mz_now</span><span class="p">()</span> <span class="o">-</span> <span class="nb">INTERVAL</span> <span class="s1">&#39;5min&#39;</span> <span class="o">&gt;</span> <span class="n">order_date</span><span class="p">;</span> </span></span></code></pre></div> |

### Disjunctions (`OR`)

<p>When used in a materialized view definition, a view definition that is being
indexed (i.e., although you can create the view and perform ad-hoc query on
the view, you cannot create an index on that view), or a <code>SUBSCRIBE</code>
statement:</p>
<ul>
<li>
<p><code>mz_now()</code> clauses can only be combined using an <code>AND</code>, and</p>
</li>
<li>
<p>All top-level <code>WHERE</code> or <code>HAVING</code> conditions must be combined using an <code>AND</code>,
even if the <code>mz_now()</code> clause is nested.</p>
</li>
</ul>

For example:

| mz_now() Compound Clause | Valid/Invalid |
| --- | --- |
| <span class="copyableCode"> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="o">*</span> <span class="k">FROM</span> <span class="n">orders</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">status</span> <span class="o">=</span> <span class="s1">&#39;Shipped&#39;</span> </span></span><span class="line"><span class="cl"><span class="k">OR</span> <span class="n">order_date</span> <span class="o">+</span> <span class="nb">interval</span> <span class="s1">&#39;1&#39;</span> <span class="k">days</span> <span class="o">&lt;=</span> <span class="n">mz_now</span><span class="p">()</span> </span></span><span class="line"><span class="cl"><span class="p">;</span> </span></span></code></pre></div></span>  | <p>✅ <strong>Valid</strong></p> <p>Ad-hoc queries do not have the same restrictions.</p>  |
| <span class="copyableCode"> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">CREATE</span> <span class="k">MATERIALIZED</span> <span class="k">VIEW</span> <span class="n">forecast_completed_orders</span> <span class="k">AS</span> </span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="o">*</span> <span class="k">FROM</span> <span class="n">orders</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">order_date</span> <span class="o">+</span> <span class="nb">interval</span> <span class="s1">&#39;3&#39;</span> <span class="k">days</span> <span class="o">&gt;</span> <span class="n">mz_now</span><span class="p">()</span> </span></span><span class="line"><span class="cl"><span class="k">AND</span> <span class="n">order_date</span> <span class="o">+</span> <span class="nb">interval</span> <span class="s1">&#39;1&#39;</span> <span class="k">days</span> <span class="o">&lt;</span> <span class="n">mz_now</span><span class="p">()</span> </span></span><span class="line"><span class="cl"><span class="p">;</span> </span></span></code></pre></div></span>  | ✅ <strong>Valid</strong> |
| <span class="copyableCode"> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">CREATE</span> <span class="k">MATERIALIZED</span> <span class="k">VIEW</span> <span class="n">forecast_completed_orders</span> <span class="k">AS</span> </span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="o">*</span> <span class="k">FROM</span> <span class="n">orders</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="p">(</span><span class="n">status</span> <span class="o">=</span> <span class="s1">&#39;Complete&#39;</span> <span class="k">OR</span> <span class="n">status</span> <span class="o">=</span> <span class="s1">&#39;Shipped&#39;</span><span class="p">)</span> </span></span><span class="line"><span class="cl"><span class="k">AND</span> <span class="n">order_date</span> <span class="o">+</span> <span class="nb">interval</span> <span class="s1">&#39;1&#39;</span> <span class="k">days</span> <span class="o">&lt;=</span> <span class="n">mz_now</span><span class="p">()</span> </span></span><span class="line"><span class="cl"><span class="p">;</span> </span></span></code></pre></div></span>  | ✅ <strong>Valid</strong> |
| <div style="background-color: var(--code-block)"> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">CREATE</span> <span class="k">MATERIALIZED</span> <span class="k">VIEW</span> <span class="n">forecast_completed_orders</span> <span class="k">AS</span> </span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="o">*</span> <span class="k">FROM</span> <span class="n">orders</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">status</span> <span class="o">=</span> <span class="s1">&#39;Shipped&#39;</span> </span></span><span class="line"><span class="cl"><span class="k">OR</span> <span class="n">order_date</span> <span class="o">+</span> <span class="nb">interval</span> <span class="s1">&#39;1&#39;</span> <span class="k">days</span> <span class="o">&lt;=</span> <span class="n">mz_now</span><span class="p">()</span> </span></span><span class="line"><span class="cl"><span class="p">;</span> </span></span></code></pre></div></div>  | <p>❌ <strong>Invalid</strong></p> <p>In materialized view definitions, <code>mz_now()</code> clause can only be combined using an <code>AND</code>.</p>  |
| <div style="background-color: var(--code-block)"> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">CREATE</span> <span class="k">MATERIALIZED</span> <span class="k">VIEW</span> <span class="n">forecast_completed_orders</span> <span class="k">AS</span> </span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="o">*</span> <span class="k">FROM</span> <span class="n">orders</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">status</span> <span class="o">=</span> <span class="s1">&#39;Complete&#39;</span> </span></span><span class="line"><span class="cl"><span class="k">OR</span> <span class="p">(</span><span class="n">status</span> <span class="o">=</span> <span class="s1">&#39;Shipped&#39;</span> <span class="k">AND</span> <span class="n">order_date</span> <span class="o">+</span> <span class="nb">interval</span> <span class="s1">&#39;1&#39;</span> <span class="k">days</span> <span class="o">&lt;=</span> <span class="n">mz_now</span><span class="p">())</span> </span></span></code></pre></div></div>  | <p>❌ <strong>Invalid</strong></p> <p>In materialized view definitions with <code>mz_now()</code> clauses, top-level conditions must be combined using an <code>AND</code>.</p>  |
| <div style="background-color: var(--code-block)"> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">CREATE</span> <span class="k">VIEW</span> <span class="n">forecast_completed_orders</span> <span class="k">AS</span> </span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="o">*</span> <span class="k">FROM</span> <span class="n">orders</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">status</span> <span class="o">=</span> <span class="s1">&#39;Complete&#39;</span> </span></span><span class="line"><span class="cl"><span class="k">OR</span> <span class="p">(</span><span class="n">status</span> <span class="o">=</span> <span class="s1">&#39;Shipped&#39;</span> <span class="k">AND</span> <span class="n">order_date</span> <span class="o">+</span> <span class="nb">interval</span> <span class="s1">&#39;1&#39;</span> <span class="k">days</span> <span class="o">&lt;=</span> <span class="n">mz_now</span><span class="p">())</span> </span></span><span class="line"><span class="cl"><span class="p">;</span> </span></span><span class="line"><span class="cl"> </span></span><span class="line"><span class="cl"><span class="k">CREATE</span> <span class="k">INDEX</span> <span class="n">idx_forecast_completed_orders</span> <span class="k">ON</span> <span class="n">forecast_completed_orders</span> </span></span><span class="line"><span class="cl"><span class="p">(</span><span class="n">order_date</span><span class="p">);</span> <span class="c1">-- Unsupported because of the `mz_now()` clause </span></span></span></code></pre></div></div>  | <p>❌ <strong>Invalid</strong></p> <p>To index a view whose definitions includes <code>mz_now()</code> clauses, top-level conditions must be combined using an <code>AND</code> in the view definition.</p>  |

**Idiomatic Materialize SQL**: When `mz_now()` is included in a materialized
view definition, a view definition that is being indexed, or a `SUBSCRIBE`
statement, instead of using disjunctions (`OR`) when using `mz_now()`, rewrite
the query to use `UNION ALL` or `UNION` instead, deduplicating as necessary:

- In some cases, you may need to modify the conditions to deduplicate results
  when using `UNION ALL`. For example, you might add the negation of one input's
  condition to the other as a conjunction.

- In some cases, using `UNION` instead of `UNION ALL` may suffice if the inputs
  do not contain other duplicates that need to be retained.

#### Examples

| <blue>Materialize SQL</blue> ✅ | <p><strong>Rewrite as UNION ALL with possible duplicates</strong></p> <span class="copyableCode"> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">CREATE</span> <span class="k">MATERIALIZED</span> <span class="k">VIEW</span> <span class="n">forecast_completed_orders_duplicates_possible</span> <span class="k">AS</span> </span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">item</span><span class="p">,</span> <span class="n">quantity</span><span class="p">,</span> <span class="n">status</span> <span class="k">from</span> <span class="n">orders</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">status</span> <span class="o">=</span> <span class="s1">&#39;Shipped&#39;</span> </span></span><span class="line"><span class="cl"><span class="k">UNION</span> <span class="k">ALL</span> </span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">item</span><span class="p">,</span> <span class="n">quantity</span><span class="p">,</span> <span class="n">status</span> <span class="k">from</span> <span class="n">orders</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">order_date</span> <span class="o">+</span> <span class="nb">interval</span> <span class="s1">&#39;30&#39;</span> <span class="k">minutes</span> <span class="o">&gt;=</span> <span class="n">mz_now</span><span class="p">()</span> </span></span><span class="line"><span class="cl"><span class="p">;</span> </span></span></code></pre></div></span> <p><strong>Rewrite as UNION ALL that avoids duplicates across queries</strong></p> <span class="copyableCode"> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">CREATE</span> <span class="k">MATERIALIZED</span> <span class="k">VIEW</span> <span class="n">forecast_completed_orders_deduplicated_union_all</span> <span class="k">AS</span> </span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">item</span><span class="p">,</span> <span class="n">quantity</span><span class="p">,</span> <span class="n">status</span> <span class="k">from</span> <span class="n">orders</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">status</span> <span class="o">=</span> <span class="s1">&#39;Shipped&#39;</span> </span></span><span class="line"><span class="cl"><span class="k">UNION</span> <span class="k">ALL</span> </span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">item</span><span class="p">,</span> <span class="n">quantity</span><span class="p">,</span> <span class="n">status</span> <span class="k">from</span> <span class="n">orders</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">order_date</span> <span class="o">+</span> <span class="nb">interval</span> <span class="s1">&#39;30&#39;</span> <span class="k">minutes</span> <span class="o">&gt;=</span> <span class="n">mz_now</span><span class="p">()</span> </span></span><span class="line"><span class="cl"><span class="k">AND</span> <span class="n">status</span> <span class="o">!=</span> <span class="s1">&#39;Shipped&#39;</span> <span class="c1">-- Deduplicate by excluding those with status &#39;Shipped&#39; </span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="p">;</span> </span></span></code></pre></div></span> <p><strong>Rewrite as UNION to deduplicate any and all duplicated results</strong></p> <span class="copyableCode"> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">CREATE</span> <span class="k">MATERIALIZED</span> <span class="k">VIEW</span> <span class="n">forecast_completed_orders_deduplicated_results</span> <span class="k">AS</span> </span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">item</span><span class="p">,</span> <span class="n">quantity</span><span class="p">,</span> <span class="n">status</span> <span class="k">from</span> <span class="n">orders</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">status</span> <span class="o">=</span> <span class="s1">&#39;Shipped&#39;</span> </span></span><span class="line"><span class="cl"><span class="k">UNION</span> </span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">item</span><span class="p">,</span> <span class="n">quantity</span><span class="p">,</span> <span class="n">status</span> <span class="k">from</span> <span class="n">orders</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">order_date</span> <span class="o">+</span> <span class="nb">interval</span> <span class="s1">&#39;30&#39;</span> <span class="k">minutes</span> <span class="o">&gt;=</span> <span class="n">mz_now</span><span class="p">()</span> </span></span><span class="line"><span class="cl"><span class="p">;</span> </span></span></code></pre></div></span>  |
| <red>Anti-pattern</red> ❌ | <p><red>Not supported</red></p> <div style="background-color: var(--code-block)"> <pre tabindex="0"><code class="language-none" data-lang="none">-- Unsupported CREATE MATERIALIZED VIEW forecast_completed_orders_unsupported AS SELECT item, quantity, status from orders WHERE status = &#39;Shipped&#39; OR order_date + interval &#39;30&#39; minutes &gt;= mz_now(); </code></pre></div> |

---

## Top-K in group

## Overview

The "Top-K in group" query pattern groups by some key and return the first K
elements within each group according to some ordering.

> ### Materialize and window functions
> For indexed views and materialized views that contain [window
> functions](/sql/functions/#window-functions) (including aggregate functions used
> with an `OVER` clause), when an input record in a partition is
> added/removed/changed, Materialize **recomputes the results from scratch** for
> that partition (instead of using incremental computation).
> The `PARTITION BY` clause of your window function determines your partitions. If
> `PARTITION BY` is omitted, all records belong to a single partition (i.e., any
> record change results in a recomputation from scratch over the whole input).
> To avoid performance issues that may arise as the number of records grows,
> consider rewriting your indexed views and materialized views to use idiomatic
> Materialize SQL instead of window functions. If your view definitions cannot be
> rewritten without the window functions and the performance of window functions
> is insufficient for your use case, please [contact our team](/support/).

## Idiomatic Materialize SQL

### For K >= 1

**Idiomatic Materialize SQL**: For Top-K queries where K >= 1, use a subquery to
[SELECT DISTINCT](/sql/select/#select-distinct) on the grouping key and perform
a [LATERAL](/sql/select/join/#lateral-subqueries) join (by the grouping key)
with another subquery that specifies the ordering and the limit K.

<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><blue>Idiomatic Materialize SQL</blue></td>
<td class="copyableCode">

<p>Use a subquery to
<a href="/sql/select/#select-distinct" >SELECT DISTINCT</a> on the grouping key (e.g.,
<code>fieldA</code>), and perform a <a href="/sql/select/join/#lateral-subqueries" >LATERAL</a> join
(by the grouping key <code>fieldA</code>) with another subquery that specifies the ordering
(e.g., <code>fieldZ [ASC|DESC]</code>) and the limit K.</p>
<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">fieldA</span><span class="p">,</span> <span class="n">fieldB</span><span class="p">,</span> <span class="mf">...</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="p">(</span><span class="k">SELECT</span> <span class="k">DISTINCT</span> <span class="n">fieldA</span> <span class="k">FROM</span> <span class="n">tableA</span><span class="p">)</span> <span class="n">grp</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">     <span class="k">LATERAL</span> <span class="p">(</span><span class="k">SELECT</span> <span class="n">fieldB</span><span class="p">,</span> <span class="mf">...</span> <span class="p">,</span> <span class="n">fieldZ</span> <span class="k">FROM</span> <span class="n">tableA</span>
</span></span><span class="line"><span class="cl">        <span class="k">WHERE</span> <span class="n">fieldA</span> <span class="o">=</span> <span class="n">grp</span><span class="mf">.</span><span class="n">fieldA</span>
</span></span><span class="line"><span class="cl">        <span class="k">ORDER</span> <span class="k">BY</span> <span class="n">fieldZ</span> <span class="mf">...</span> <span class="k">LIMIT</span> <span class="n">K</span><span class="p">)</span>   <span class="c1">-- K is a number &gt;= 1
</span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">fieldA</span><span class="p">,</span> <span class="n">fieldZ</span> <span class="mf">...</span> <span class="p">;</span>
</span></span></code></pre></div>

</td>
</tr>
<tr>
<td><red>Anti-pattern</red></td>
<td>

<p><red>Avoid the use of <code>ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)</code> for Top-K queries.</red></p>
<pre tabindex="0"><code class="language-nofmt" data-lang="nofmt">-- Anti-pattern. Avoid. --
SELECT fieldA, fieldB, ...
FROM (
   SELECT fieldA, fieldB, ... , fieldZ,
      ROW_NUMBER() OVER (PARTITION BY fieldA
      ORDER BY fieldZ ... ) as rn
   FROM tableA)
WHERE rn &lt;= K     -- K is a number &gt;= 1
ORDER BY fieldA, fieldZ ...;
</code></pre>

</td>
</tr>
</tbody>
</table>

#### Query hints

To further improve the memory usage of the idiomatic Materialize SQL, you can
specify a [`LIMIT INPUT GROUP SIZE` query hint](/sql/select/#query-hints) in the
idiomatic Materialize SQL.

```mzsql
SELECT fieldA, fieldB, ...
FROM (SELECT DISTINCT fieldA FROM tableA) grp,
     LATERAL (SELECT fieldB, ... , fieldZ FROM tableA
        WHERE fieldA = grp.fieldA
        OPTIONS (LIMIT INPUT GROUP SIZE = ...)
        ORDER BY fieldZ ... LIMIT K)   -- K is a number >= 1
ORDER BY fieldA, fieldZ ... ;
```

For more information on setting `LIMIT INPUT GROUP SIZE`, see
[Optimization](/transform-data/optimization/#query-hints).

### For K = 1

**Idiomatic Materialize SQL**: For K = 1, use a [SELECT DISTINCT
ON()](/sql/select/#select-distinct-on) on the grouping key (e.g., `fieldA`) and
order the results first by the `DISTINCT ON` key and then the Top-K ordering
key (e.g., `fieldA, fieldZ [ASC|DESC]`).

Alternatively, you can also use the more general [Top-K where K >= 1](#for-k--1)
pattern, specifying 1 as the limit.

<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><blue>Idiomatic Materialize SQL</blue></td>
<td class="copyableCode">

<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="k">DISTINCT</span> <span class="k">ON</span><span class="p">(</span><span class="n">fieldA</span><span class="p">)</span> <span class="n">fieldA</span><span class="p">,</span> <span class="n">fieldB</span><span class="p">,</span> <span class="mf">...</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">tableA</span>
</span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">fieldA</span><span class="p">,</span> <span class="n">fieldZ</span> <span class="mf">...</span> <span class="p">;</span>
</span></span></code></pre></div>

</td>
</tr>

<tr>
<td><red>Anti-pattern</red></td>
<td>

<p><red>Avoid the use of <code>ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)</code> for Top-K queries.</red></p>
<pre tabindex="0"><code class="language-nofmt" data-lang="nofmt">-- Anti-pattern. Avoid. --
SELECT fieldA, fieldB, ...
FROM (
   SELECT fieldA, fieldB, ... , fieldZ,
      ROW_NUMBER() OVER (PARTITION BY fieldA
      ORDER BY fieldZ ... ) as rn
   FROM tableA)
WHERE rn = 1
ORDER BY fieldA, fieldZ ...;
</code></pre>

</td>
</tr>
</tbody>
</table>

### Query hints

To further improve the memory usage of the idiomatic Materialize SQL, you can
specify a [`DISTINCT ON INPUT GROUP SIZE` query hint](/sql/select/#query-hints)
in the idiomatic Materialize SQL.

```mzsql
SELECT DISTINCT ON(fieldA) fieldA, fieldB, ...
FROM tableA
OPTIONS (DISTINCT ON INPUT GROUP SIZE = ...)
ORDER BY fieldA, fieldZ ... ;
```

For more information on setting `DISTINCT ON INPUT GROUP SIZE`, see
[`EXPLAIN ANALYZE HINTS`](/sql/explain-analyze/#explain-analyze-hints).

## Examples

> **Note:** The example data can be found in the
> [Appendix](/transform-data/idiomatic-materialize-sql/appendix/example-orders).

### Select Top-3 items

Using idiomatic Materialize SQL, the following example finds the top 3 items (by
descending subtotal) in each order. The example uses a subquery to [SELECT
DISTINCT](/sql/select/#select-distinct) on the grouping key (`order_id`), and
performs a [LATERAL](/sql/select/join/#lateral-subqueries) join (by the grouping
key) with another subquery that specifies the ordering (`ORDER BY subtotal
DESC`) and limits its results to 3 (`LIMIT 3`).

<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><blue>Idiomatic Materialize SQL</blue></td>
<td class="copyableCode">

<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">order_id</span><span class="p">,</span> <span class="n">item</span><span class="p">,</span> <span class="n">subtotal</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="p">(</span><span class="k">SELECT</span> <span class="k">DISTINCT</span> <span class="n">order_id</span> <span class="k">FROM</span> <span class="n">orders_view</span><span class="p">)</span> <span class="n">grp</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">     <span class="k">LATERAL</span> <span class="p">(</span><span class="k">SELECT</span> <span class="n">item</span><span class="p">,</span> <span class="n">subtotal</span> <span class="k">FROM</span> <span class="n">orders_view</span>
</span></span><span class="line"><span class="cl">        <span class="k">WHERE</span> <span class="n">order_id</span> <span class="o">=</span> <span class="n">grp</span><span class="mf">.</span><span class="n">order_id</span>
</span></span><span class="line"><span class="cl">        <span class="k">ORDER</span> <span class="k">BY</span> <span class="n">subtotal</span> <span class="k">DESC</span> <span class="k">LIMIT</span> <span class="mf">3</span><span class="p">)</span>
</span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">order_id</span><span class="p">,</span> <span class="n">subtotal</span> <span class="k">DESC</span><span class="p">;</span>
</span></span></code></pre></div>

</td>
</tr>

<tr>
<td><red>Anti-pattern</red> ❌</td>
<td>

<p><red>Avoid the use of <code>ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)</code> for Top-K queries.</red></p>
<pre tabindex="0"><code class="language-nofmt" data-lang="nofmt">-- Anti-pattern --
SELECT order_id, item, subtotal
FROM (
   SELECT order_id, item, subtotal,
      ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY subtotal DESC) as rn
   FROM orders_view)
WHERE rn &lt;= 3
ORDER BY order_id, subtotal DESC;
</code></pre>

</td>
</tr>

</tbody>
</table>

### Select Top-1 item

Using idiomatic Materialize SQL, the following example finds the top 1 item (by
descending subtotal) in each order. The example uses a query to [SELECT DISTINCT
ON()](/sql/select/#select-distinct-on) on the grouping key (`order_id`) with an
`ORDER BY order_id, subtotal DESC` (i.e., ordering first by the `DISTINCT
ON`/grouping key, then the descending subtotal). [^1]

<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><blue>Idiomatic Materialize SQL</blue></td>
<td class="copyableCode">

<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="k">DISTINCT</span> <span class="k">ON</span><span class="p">(</span><span class="n">order_id</span><span class="p">)</span> <span class="n">order_id</span><span class="p">,</span> <span class="n">item</span><span class="p">,</span> <span class="n">subtotal</span>
</span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">orders_view</span>
</span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">order_id</span><span class="p">,</span> <span class="n">subtotal</span> <span class="k">DESC</span><span class="p">;</span>
</span></span></code></pre></div>

</td>
</tr>
<tr>
<td><red>Anti-pattern</red> ❌</td>
<td>

<p><red>Avoid the use of <code>ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)</code> for Top-K queries.</red></p>
<pre tabindex="0"><code class="language-nofmt" data-lang="nofmt">-- Anti-pattern --
SELECT order_id, item, subtotal
FROM (
   SELECT order_id, item, subtotal,
      ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY subtotal DESC) as rn
   FROM orders_view)
WHERE rn = 1
ORDER BY order_id, subtotal DESC;
</code></pre>

</td>
</tr>
</tbody>
</table>

[^1]: Alternatively, you can also use the [idiomatic Materialize SQL for the
    more general Top K query](#for-k--1), specifying 1 as the limit.

## See also

- [SELECT DISTINCT](/sql/select/#select-distinct)
- [LATERAL subqueries](/sql/select/join/#lateral-subqueries)
- [Query hints for Top K](/transform-data/optimization/#query-hints)
- [Window functions](/sql/functions/#window-functions)

