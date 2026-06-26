# `NOT IN` subquery
Use idiomatic Materialize SQL for `NOT IN (subquery)` predicates to avoid a cross join in the dataflow plan.
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
