# Lead over
Use idiomatic Materialize SQL to access the next row's value (lead) when ordered by a field that advances in a regular pattern, such as in regular intervals.
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
