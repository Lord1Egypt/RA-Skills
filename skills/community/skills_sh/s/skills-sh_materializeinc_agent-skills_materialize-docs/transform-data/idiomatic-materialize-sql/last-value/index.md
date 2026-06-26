# Last value in group
Use idiomatic Materialize SQL to find the last value in each group.
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
