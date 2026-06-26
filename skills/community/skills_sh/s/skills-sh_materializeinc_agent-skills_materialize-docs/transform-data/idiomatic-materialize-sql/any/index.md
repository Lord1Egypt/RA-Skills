# `ANY()` equi-join condition
Use idiomatic Materialize SQL for equi-join whose `ON` expression includes the `ANY()` operator.
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
