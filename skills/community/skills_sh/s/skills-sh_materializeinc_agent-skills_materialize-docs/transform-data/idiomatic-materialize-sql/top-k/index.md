# Top-K in group
Use idiomatic Materialize SQL to find the top-k/top-n elements in each group.
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
