# Appendix

Idiomatic Materialize appendix, containing example data and cheatsheets

---

## Example data: items and orders

The following sample data is used in the various Idiomatic Materialize SQL
pages:

```mzsql
CREATE TABLE orders (
    order_id int NOT NULL,
    order_date timestamp NOT NULL,
    item text NOT NULL,
    quantity int NOT NULL,
    status text NOT NULL
);

INSERT INTO orders VALUES
(1,current_timestamp - (1 * interval '3 day') - (35 * interval '1 minute'),'brownies',12, 'Complete'),
(1,current_timestamp - (1 * interval '3 day') - (35 * interval '1 minute'),'cupcake',12, 'Complete'),
(1,current_timestamp - (1 * interval '3 day') - (35 * interval '1 minute'),'chocolate cake',1, 'Complete'),
(2,current_timestamp - (1 * interval '3 day') - (15 * interval '1 minute'),'cheesecake',1, 'Complete'),
(3,current_timestamp - (1 * interval '3 day'),'chiffon cake',1, 'Complete'),
(3,current_timestamp - (1 * interval '3 day'),'egg tart',6, 'Complete'),
(3,current_timestamp - (1 * interval '3 day'),'fruit tart',6, 'Complete'),
(4,current_timestamp - (1 * interval '2 day')- (30 * interval '1 minute'),'cupcake',6, 'Shipped'),
(4,current_timestamp - (1 * interval '2 day')- (30 * interval '1 minute'),'cupcake',6, 'Shipped'),
(5,current_timestamp - (1 * interval '2 day'),'chocolate cake',1, 'Processing'),
(6,current_timestamp,'brownie',10, 'Pending'),
(6,current_timestamp,'chocolate cake',1, 'Pending'),
(7,current_timestamp,'chocolate chip cookie',20, 'Processing'),
(8,current_timestamp,'coffee cake',1, 'Complete'),
(8,current_timestamp,'fruit tart',4, 'Complete'),
(9,current_timestamp + (15 * interval '1 minute'),'chocolate chip cookie',20, 'Pending'),
(9,current_timestamp + (15 * interval '1 minute'),'brownie',20, 'Processing'),
(10,current_timestamp + (30 * interval '1 minute'),'sugar cookie',10, 'Pending'),
(10,current_timestamp + (30 * interval '1 minute'),'donut',36, 'Pending'),
(11,current_timestamp + (30 * interval '1 minute'),'chiffon cake',2, 'Pending'),
(11,current_timestamp + (30 * interval '1 minute'),'egg tart',6, 'Pending'),
(12,current_timestamp + (1 * interval '1 day') + (35 * interval '1 minute'),'cheesecake',1, 'Pending'),
(13,current_timestamp + (1 * interval '1 day')+ (35 * interval '1 minute'),'chocolate chip cookie',20, 'Pending'),
(14,current_timestamp + (1 * interval '1 day')+ (35 * interval '1 minute'),'brownie',20, 'Pending'),
(14,current_timestamp + (1 * interval '1 day')+ (35 * interval '1 minute'),'cheesecake',1, 'Pending'),
(14,current_timestamp + (1 * interval '1 day')+ (35 * interval '1 minute'),'cupcake',6, 'Pending'),
(15,current_timestamp + (1 * interval '1 day')+ (35 * interval '1 minute'),'chocolate cake',1, 'Pending'),
(16,current_timestamp + (1 * interval '2 day'),'chocolate cake',1, 'Pending'),
(17,current_timestamp + (1 * interval '2 day')+ (10 * interval '1 minute'),'coffee cake',1, 'Pending'),
(17,current_timestamp + (1 * interval '2 day')+ (10 * interval '1 minute'),'egg tart',12, 'Pending'),
(18,current_timestamp + (1 * interval '2 day')+ (15 * interval '1 minute'),'chocolate chip cookie',12, 'Pending'),
(18,current_timestamp + (1 * interval '2 day')+ (15 * interval '1 minute'),'brownie',12, 'Pending'),
(18,current_timestamp + (1 * interval '2 day')+ (15 * interval '1 minute'),'sugar cookie',12, 'Pending'),
(18,current_timestamp + (1 * interval '2 day')+ (15 * interval '1 minute'),'donut',12, 'Pending'),
(19,current_timestamp + (1 * interval '2 day')+ (30 * interval '1 minute'),'cupcake',6, 'Pending'),
(20,current_timestamp + (1 * interval '3 day'),'chiffon cake',1, 'Pending'),
(20,current_timestamp + (1 * interval '3 day'),'egg tart',6, 'Pending'),
(20,current_timestamp + (1 * interval '3 day'),'fruit tart',6, 'Pending'),
(21,current_timestamp + (1 * interval '3 day') + (15 * interval '1 minute'),'cheesecake',1, 'Pending'),
(22,current_timestamp + (1 * interval '3 day') + (35 * interval '1 minute'),'brownies',12, 'Pending'),
(22,current_timestamp + (1 * interval '3 day') + (35 * interval '1 minute'),'cupcake',12, 'Pending'),
(22,current_timestamp + (1 * interval '3 day') + (35 * interval '1 minute'),'chocolate cake',1, 'Pending')
;

CREATE TABLE items(
    item text NOT NULL,
    price numeric(8,4) NOT NULL,
    currency text NOT NULL DEFAULT 'USD'
);

INSERT INTO items VALUES
('brownie',2.25,'USD'),
('cheesecake',40,'USD'),
('chiffon cake',30,'USD'),
('chocolate cake',30,'USD'),
('chocolate chip cookie',2.5,'USD'),
('coffee cake',25,'USD'),
('cupcake',3,'USD'),
('donut',1.25,'USD'),
('egg tart',2.5,'USD'),
('fruit tart',4.5,'USD'),
('sugar cookie',2.5,'USD');

CREATE VIEW orders_view AS
SELECT o.*,i.price,o.quantity * i.price as subtotal
FROM orders as o
JOIN items as i
ON o.item = i.item;

CREATE VIEW orders_daily_totals AS
SELECT date_trunc('day',order_date) AS order_date,
       sum(subtotal) AS daily_total
FROM orders_view
GROUP BY date_trunc('day',order_date);

CREATE TABLE sales_items (
  week_of date NOT NULL,
  items text[]
);

INSERT INTO sales_items VALUES
(date_trunc('week', current_timestamp),ARRAY['brownie','chocolate chip cookie','chocolate cake']),
(date_trunc('week', current_timestamp + (1* interval '7 day')),ARRAY['chocolate chip cookie','donut','cupcake']);
```

---

## Idiomatic Materialize SQL chart

Materialize follows the SQL standard (SQL-92) implementation and strives for
compatibility with the PostgreSQL dialect. However, for some use cases,
Materialize provides its own idiomatic query patterns that can provide better
performance.

## General

### Query Patterns

|   | Idiomatic Materialize SQL Pattern |
| --- | --- |
| <a href="/transform-data/idiomatic-materialize-sql/any/" ><code>ANY()</code> Equi-join condition</a> | <p><strong>If no duplicates exist in the unnested field:</strong> Use a Common Table Expression (CTE) to <a href="/sql/functions/#unnest" ><code>UNNEST()</code></a> the array of values and perform the equi-join on the unnested values.</p> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="c1">-- array_field contains no duplicates.-- </span></span></span><span class="line"><span class="cl"><span class="c1"></span> </span></span><span class="line"><span class="cl"><span class="k">WITH</span> <span class="n">my_expanded_values</span> <span class="k">AS</span> </span></span><span class="line"><span class="cl"><span class="p">(</span><span class="k">SELECT</span> <span class="k">UNNEST</span><span class="p">(</span><span class="n">array_field</span><span class="p">)</span> <span class="k">AS</span> <span class="n">fieldZ</span> <span class="k">FROM</span> <span class="n">tableB</span><span class="p">)</span> </span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">a</span><span class="mf">.</span><span class="n">fieldA</span><span class="p">,</span> <span class="mf">...</span> </span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">tableA</span> <span class="n">a</span> </span></span><span class="line"><span class="cl"><span class="k">JOIN</span> <span class="n">my_expanded_values</span> <span class="n">t</span> <span class="k">ON</span> <span class="n">a</span><span class="mf">.</span><span class="n">fieldZ</span> <span class="o">=</span> <span class="n">t</span><span class="mf">.</span><span class="n">fieldZ</span> </span></span><span class="line"><span class="cl"><span class="p">;</span> </span></span></code></pre></div><p><strong>Duplicates may exist in the unnested field:</strong> Use a Common Table Expression (CTE) to <a href="/sql/select/#select-distinct" ><code>DISTINCT</code></a> <a href="/sql/functions/#unnest" ><code>UNNEST()</code></a> the array of values and perform the equi-join on the unnested values.</p> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="c1">-- array_field may contain duplicates.-- </span></span></span><span class="line"><span class="cl"><span class="c1"></span> </span></span><span class="line"><span class="cl"><span class="k">WITH</span> <span class="n">my_expanded_values</span> <span class="k">AS</span> </span></span><span class="line"><span class="cl"><span class="p">(</span><span class="k">SELECT</span> <span class="k">DISTINCT</span> <span class="k">UNNEST</span><span class="p">(</span><span class="n">array_field</span><span class="p">)</span> <span class="k">AS</span> <span class="n">fieldZ</span> <span class="k">FROM</span> <span class="n">tableB</span><span class="p">)</span> </span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">a</span><span class="mf">.</span><span class="n">fieldA</span><span class="p">,</span> <span class="mf">...</span> </span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">tableA</span> <span class="n">a</span> </span></span><span class="line"><span class="cl"><span class="k">JOIN</span> <span class="n">my_expanded_values</span> <span class="n">t</span> <span class="k">ON</span> <span class="n">a</span><span class="mf">.</span><span class="n">fieldZ</span> <span class="o">=</span> <span class="n">t</span><span class="mf">.</span><span class="n">fieldZ</span> </span></span><span class="line"><span class="cl"><span class="p">;</span> </span></span></code></pre></div> |
| <a href="/transform-data/idiomatic-materialize-sql/not-in/" ><code>NOT IN (&lt;subquery&gt;)</code> predicate</a> | <p><strong>Rewrite to <code>NOT EXISTS</code> with a correlated subquery.</strong></p> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">t1</span><span class="mf">.</span><span class="o">*</span> </span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">t1</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="k">NOT</span> <span class="k">EXISTS</span> <span class="p">(</span><span class="k">SELECT</span> <span class="mf">1</span> <span class="k">FROM</span> <span class="n">t2</span> <span class="k">WHERE</span> <span class="n">t2</span><span class="mf">.</span><span class="n">a</span> <span class="o">=</span> <span class="n">t1</span><span class="mf">.</span><span class="n">a</span><span class="p">)</span> </span></span><span class="line"><span class="cl"><span class="p">;</span> </span></span></code></pre></div><p><strong>Filter out <code>NULL</code>s on both sides of the <code>NOT IN</code>.</strong></p> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">t1</span><span class="mf">.</span><span class="o">*</span> </span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">t1</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">t1</span><span class="mf">.</span><span class="n">a</span> <span class="k">IS</span> <span class="k">NOT</span> <span class="k">NULL</span> </span></span><span class="line"><span class="cl">  <span class="k">AND</span> <span class="n">t1</span><span class="mf">.</span><span class="n">a</span> <span class="k">NOT</span> <span class="k">IN</span> <span class="p">(</span><span class="k">SELECT</span> <span class="n">t2</span><span class="mf">.</span><span class="n">a</span> <span class="k">FROM</span> <span class="n">t2</span> <span class="k">WHERE</span> <span class="n">t2</span><span class="mf">.</span><span class="n">a</span> <span class="k">IS</span> <span class="k">NOT</span> <span class="k">NULL</span><span class="p">)</span> </span></span><span class="line"><span class="cl"><span class="p">;</span> </span></span></code></pre></div> |
| <a href="/transform-data/idiomatic-materialize-sql/mz_now/#mz_now-expressions-to-calculate-past-or-future-timestamp" ><code>mz_now()</code> with date/time operators</a> | Rewrite the query expression; specifically, move the operation to the other side of the comparison. |
| <a href="/transform-data/idiomatic-materialize-sql/mz_now/#disjunctions-or" ><code>mz_now()</code> with disjunctions (<code>OR</code>) in materialized/indexed view definitions and <code>SUBSCRIBE</code> statements</a> | <p>Rewrite as <code>UNION ALL</code> or <code>UNION</code>, deduplicating as necessary:</p> <ul> <li> <p>In some cases, you may need to modify the conditions to deduplicate results when using <code>UNION ALL</code>. For example, you might add the negation of one input&rsquo;s condition to the other as a conjunction.</p> </li> <li> <p>In some cases, using <code>UNION</code> instead of <code>UNION ALL</code> may suffice if the inputs do not contain other duplicates that need to be retained.</p> </li> </ul>  |

### Examples

|   | Example |
| --- | --- |
| <a href="/transform-data/idiomatic-materialize-sql/any/" ><code>ANY()</code> Equi-join condition</a> | <p><em><strong>If no duplicates in the unnested field</strong></em></p> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="c1">-- sales_items.items contains no duplicates. -- </span></span></span><span class="line"><span class="cl"><span class="c1"></span> </span></span><span class="line"><span class="cl"><span class="k">WITH</span> <span class="n">individual_sales_items</span> <span class="k">AS</span> </span></span><span class="line"><span class="cl"><span class="p">(</span><span class="k">SELECT</span> <span class="k">unnest</span><span class="p">(</span><span class="n">items</span><span class="p">)</span> <span class="k">as</span> <span class="n">item</span><span class="p">,</span> <span class="n">week_of</span> <span class="k">FROM</span> <span class="n">sales_items</span><span class="p">)</span> </span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">s</span><span class="mf">.</span><span class="n">week_of</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">quantity</span> </span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">orders</span> <span class="n">o</span> </span></span><span class="line"><span class="cl"><span class="k">JOIN</span> <span class="n">individual_sales_items</span> <span class="n">s</span> <span class="k">ON</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span> <span class="o">=</span> <span class="n">s</span><span class="mf">.</span><span class="n">item</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">date_trunc</span><span class="p">(</span><span class="s1">&#39;week&#39;</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_date</span><span class="p">)</span> <span class="o">=</span> <span class="n">s</span><span class="mf">.</span><span class="n">week_of</span> </span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">s</span><span class="mf">.</span><span class="n">week_of</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">quantity</span> </span></span><span class="line"><span class="cl"><span class="p">;</span> </span></span></code></pre></div><p><em><strong>To omit duplicates that may exist in the unnested field</strong></em></p> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="c1">-- sales_items.items may contains duplicates -- </span></span></span><span class="line"><span class="cl"><span class="c1"></span> </span></span><span class="line"><span class="cl"><span class="k">WITH</span> <span class="n">individual_sales_items</span> <span class="k">AS</span> </span></span><span class="line"><span class="cl"><span class="p">(</span><span class="k">SELECT</span> <span class="k">DISTINCT</span> <span class="k">unnest</span><span class="p">(</span><span class="n">items</span><span class="p">)</span> <span class="k">as</span> <span class="n">item</span><span class="p">,</span> <span class="n">week_of</span> <span class="k">FROM</span> <span class="n">sales_items</span><span class="p">)</span> </span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">s</span><span class="mf">.</span><span class="n">week_of</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">quantity</span> </span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">orders</span> <span class="n">o</span> </span></span><span class="line"><span class="cl"><span class="k">JOIN</span> <span class="n">individual_sales_items</span> <span class="n">s</span> <span class="k">ON</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span> <span class="o">=</span> <span class="n">s</span><span class="mf">.</span><span class="n">item</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">date_trunc</span><span class="p">(</span><span class="s1">&#39;week&#39;</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_date</span><span class="p">)</span> <span class="o">=</span> <span class="n">s</span><span class="mf">.</span><span class="n">week_of</span> </span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">s</span><span class="mf">.</span><span class="n">week_of</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">quantity</span> </span></span><span class="line"><span class="cl"><span class="p">;</span> </span></span></code></pre></div> |
| <a href="/transform-data/idiomatic-materialize-sql/not-in/" ><code>NOT IN (&lt;subquery&gt;)</code> predicate</a> | <p>Because the subquery uses <a href="/sql/functions/#unnest" ><code>UNNEST()</code></a> on a column of the outer-correlated row, factor the <code>UNNEST()</code> into an uncorrelated <a href="/sql/select/#common-table-expressions-ctes" >Common Table Expression (CTE)</a> first.</p> <p><em><strong>Rewrite to <code>NOT EXISTS</code> with a CTE for the <code>UNNEST()</code></strong></em></p> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">WITH</span> <span class="n">this_weeks_sales</span> <span class="k">AS</span> <span class="p">(</span> </span></span><span class="line"><span class="cl">  <span class="k">SELECT</span> <span class="k">unnest</span><span class="p">(</span><span class="n">items</span><span class="p">)</span> <span class="k">AS</span> <span class="n">sale_item</span> </span></span><span class="line"><span class="cl">  <span class="k">FROM</span> <span class="n">sales_items</span> </span></span><span class="line"><span class="cl">  <span class="k">WHERE</span> <span class="n">week_of</span> <span class="o">=</span> <span class="n">date_trunc</span><span class="p">(</span><span class="s1">&#39;week&#39;</span><span class="p">,</span> <span class="n">current_timestamp</span><span class="p">)</span> </span></span><span class="line"><span class="cl"><span class="p">)</span> </span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">i</span><span class="mf">.</span><span class="n">item</span><span class="p">,</span> <span class="n">i</span><span class="mf">.</span><span class="n">price</span> </span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">items</span> <span class="n">i</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="k">NOT</span> <span class="k">EXISTS</span> <span class="p">(</span> </span></span><span class="line"><span class="cl">  <span class="k">SELECT</span> <span class="mf">1</span> <span class="k">FROM</span> <span class="n">this_weeks_sales</span> <span class="n">s</span> <span class="k">WHERE</span> <span class="n">s</span><span class="mf">.</span><span class="n">sale_item</span> <span class="o">=</span> <span class="n">i</span><span class="mf">.</span><span class="n">item</span> </span></span><span class="line"><span class="cl"><span class="p">)</span> </span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">i</span><span class="mf">.</span><span class="n">item</span> </span></span><span class="line"><span class="cl"><span class="p">;</span> </span></span></code></pre></div><p><em><strong>Filter out <code>NULL</code>s with a CTE for the <code>UNNEST()</code></strong></em></p> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">WITH</span> <span class="n">this_weeks_sales</span> <span class="k">AS</span> <span class="p">(</span> </span></span><span class="line"><span class="cl">  <span class="k">SELECT</span> <span class="k">unnest</span><span class="p">(</span><span class="n">items</span><span class="p">)</span> <span class="k">AS</span> <span class="n">sale_item</span> </span></span><span class="line"><span class="cl">  <span class="k">FROM</span> <span class="n">sales_items</span> </span></span><span class="line"><span class="cl">  <span class="k">WHERE</span> <span class="n">week_of</span> <span class="o">=</span> <span class="n">date_trunc</span><span class="p">(</span><span class="s1">&#39;week&#39;</span><span class="p">,</span> <span class="n">current_timestamp</span><span class="p">)</span> </span></span><span class="line"><span class="cl"><span class="p">)</span> </span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">i</span><span class="mf">.</span><span class="n">item</span><span class="p">,</span> <span class="n">i</span><span class="mf">.</span><span class="n">price</span> </span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">items</span> <span class="n">i</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">i</span><span class="mf">.</span><span class="n">item</span> <span class="k">IS</span> <span class="k">NOT</span> <span class="k">NULL</span> </span></span><span class="line"><span class="cl">  <span class="k">AND</span> <span class="n">i</span><span class="mf">.</span><span class="n">item</span> <span class="k">NOT</span> <span class="k">IN</span> <span class="p">(</span> </span></span><span class="line"><span class="cl">    <span class="k">SELECT</span> <span class="n">sale_item</span> <span class="k">FROM</span> <span class="n">this_weeks_sales</span> <span class="k">WHERE</span> <span class="n">sale_item</span> <span class="k">IS</span> <span class="k">NOT</span> <span class="k">NULL</span> </span></span><span class="line"><span class="cl">  <span class="p">)</span> </span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">i</span><span class="mf">.</span><span class="n">item</span> </span></span><span class="line"><span class="cl"><span class="p">;</span> </span></span></code></pre></div> |
| <a href="/transform-data/idiomatic-materialize-sql/mz_now/#mz_now-expressions-to-calculate-past-or-future-timestamp" ><code>mz_now()</code> with date/time operators</a> | <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="o">*</span> <span class="k">from</span> <span class="n">orders</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">mz_now</span><span class="p">()</span> <span class="o">&gt;</span> <span class="n">order_date</span> <span class="o">+</span> <span class="nb">INTERVAL</span> <span class="s1">&#39;5min&#39;</span> </span></span><span class="line"><span class="cl"><span class="p">;</span> </span></span></code></pre></div> |
| <a href="/transform-data/idiomatic-materialize-sql/mz_now/#disjunctions-or" ><code>mz_now()</code> with disjunctions (<code>OR</code>) in materialized/indexed view definitions and <code>SUBSCRIBE</code> statements</a> | <p><strong>Rewrite as <code>UNION ALL</code> with possible duplicates</strong></p> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">CREATE</span> <span class="k">MATERIALIZED</span> <span class="k">VIEW</span> <span class="n">forecast_completed_orders_duplicates_possible</span> <span class="k">AS</span> </span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">item</span><span class="p">,</span> <span class="n">quantity</span><span class="p">,</span> <span class="n">status</span> <span class="k">from</span> <span class="n">orders</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">status</span> <span class="o">=</span> <span class="s1">&#39;Shipped&#39;</span> </span></span><span class="line"><span class="cl"><span class="k">UNION</span> <span class="k">ALL</span> </span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">item</span><span class="p">,</span> <span class="n">quantity</span><span class="p">,</span> <span class="n">status</span> <span class="k">from</span> <span class="n">orders</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">order_date</span> <span class="o">+</span> <span class="nb">interval</span> <span class="s1">&#39;30&#39;</span> <span class="k">minutes</span> <span class="o">&gt;=</span> <span class="n">mz_now</span><span class="p">()</span> </span></span><span class="line"><span class="cl"><span class="p">;</span> </span></span></code></pre></div><p><strong>Rewrite as <code>UNION ALL</code> that avoids duplicates across queries</strong></p> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">CREATE</span> <span class="k">MATERIALIZED</span> <span class="k">VIEW</span> <span class="n">forecast_completed_orders_deduplicated_union_all</span> <span class="k">AS</span> </span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">item</span><span class="p">,</span> <span class="n">quantity</span><span class="p">,</span> <span class="n">status</span> <span class="k">from</span> <span class="n">orders</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">status</span> <span class="o">=</span> <span class="s1">&#39;Shipped&#39;</span> </span></span><span class="line"><span class="cl"><span class="k">UNION</span> <span class="k">ALL</span> </span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">item</span><span class="p">,</span> <span class="n">quantity</span><span class="p">,</span> <span class="n">status</span> <span class="k">from</span> <span class="n">orders</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">order_date</span> <span class="o">+</span> <span class="nb">interval</span> <span class="s1">&#39;30&#39;</span> <span class="k">minutes</span> <span class="o">&gt;=</span> <span class="n">mz_now</span><span class="p">()</span> </span></span><span class="line"><span class="cl"><span class="k">AND</span> <span class="n">status</span> <span class="o">!=</span> <span class="s1">&#39;Shipped&#39;</span> <span class="c1">-- Deduplicate by excluding those with status &#39;Shipped&#39; </span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="p">;</span> </span></span></code></pre></div><p><strong>Rewrite as <code>UNION</code> to deduplicate any and all duplicated results</strong></p> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">CREATE</span> <span class="k">MATERIALIZED</span> <span class="k">VIEW</span> <span class="n">forecast_completed_orders_deduplicated_results</span> <span class="k">AS</span> </span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">item</span><span class="p">,</span> <span class="n">quantity</span><span class="p">,</span> <span class="n">status</span> <span class="k">from</span> <span class="n">orders</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">status</span> <span class="o">=</span> <span class="s1">&#39;Shipped&#39;</span> </span></span><span class="line"><span class="cl"><span class="k">UNION</span> </span></span><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">item</span><span class="p">,</span> <span class="n">quantity</span><span class="p">,</span> <span class="n">status</span> <span class="k">from</span> <span class="n">orders</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">order_date</span> <span class="o">+</span> <span class="nb">interval</span> <span class="s1">&#39;30&#39;</span> <span class="k">minutes</span> <span class="o">&gt;=</span> <span class="n">mz_now</span><span class="p">()</span> </span></span><span class="line"><span class="cl"><span class="p">;</span> </span></span></code></pre></div> |

## Window Functions
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

### Query Patterns

|   | Idiomatic Materialize SQL Pattern |
| --- | --- |
| <a href="/transform-data/idiomatic-materialize-sql/top-k/#for-k--1" >Top-K over partition<br>(K &gt;= 1)</a> | <p>Use a subquery to <a href="/sql/select/#select-distinct" >SELECT DISTINCT</a> on the grouping key (e.g., <code>fieldA</code>), and perform a <a href="/sql/select/join/#lateral-subqueries" >LATERAL</a> join (by the grouping key <code>fieldA</code>) with another subquery that specifies the ordering (e.g., <code>fieldZ [ASC\|DESC]</code>) and the limit K.</p> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">fieldA</span><span class="p">,</span> <span class="n">fieldB</span><span class="p">,</span> <span class="mf">...</span> </span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="p">(</span><span class="k">SELECT</span> <span class="k">DISTINCT</span> <span class="n">fieldA</span> <span class="k">FROM</span> <span class="n">tableA</span><span class="p">)</span> <span class="n">grp</span><span class="p">,</span> </span></span><span class="line"><span class="cl">     <span class="k">LATERAL</span> <span class="p">(</span><span class="k">SELECT</span> <span class="n">fieldB</span><span class="p">,</span> <span class="mf">...</span> <span class="p">,</span> <span class="n">fieldZ</span> <span class="k">FROM</span> <span class="n">tableA</span> </span></span><span class="line"><span class="cl">        <span class="k">WHERE</span> <span class="n">fieldA</span> <span class="o">=</span> <span class="n">grp</span><span class="mf">.</span><span class="n">fieldA</span> </span></span><span class="line"><span class="cl">        <span class="k">ORDER</span> <span class="k">BY</span> <span class="n">fieldZ</span> <span class="mf">...</span> <span class="k">LIMIT</span> <span class="n">K</span><span class="p">)</span>   <span class="c1">-- K is a number &gt;= 1 </span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">fieldA</span><span class="p">,</span> <span class="n">fieldZ</span> <span class="mf">...</span> <span class="p">;</span> </span></span></code></pre></div> |
| <a href="/transform-data/idiomatic-materialize-sql/top-k/#for-k--1-1" >Top-K over partition<br>(K = 1)</a> | <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="k">DISTINCT</span> <span class="k">ON</span><span class="p">(</span><span class="n">fieldA</span><span class="p">)</span> <span class="n">fieldA</span><span class="p">,</span> <span class="n">fieldB</span><span class="p">,</span> <span class="mf">...</span> </span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">tableA</span> </span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">fieldA</span><span class="p">,</span> <span class="n">fieldZ</span> <span class="mf">...</span> <span class="p">;</span> </span></span></code></pre></div> |
| <a href="/transform-data/idiomatic-materialize-sql/first-value/" >First value over partition<br>order by &hellip;</a> | <p>Use a subquery that uses the <a href="/sql/functions/#min" >MIN()</a> or <a href="/sql/functions/#max" >MAX()</a> aggregate function.</p> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">tableA</span><span class="mf">.</span><span class="n">fieldA</span><span class="p">,</span> <span class="n">tableA</span><span class="mf">.</span><span class="n">fieldB</span><span class="p">,</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">Z</span> </span></span><span class="line"><span class="cl"> <span class="k">FROM</span> <span class="n">tableA</span><span class="p">,</span> </span></span><span class="line"><span class="cl"> <span class="p">(</span><span class="k">SELECT</span> <span class="n">fieldA</span><span class="p">,</span> </span></span><span class="line"><span class="cl">    <span class="n">MIN</span><span class="p">(</span><span class="n">fieldZ</span><span class="p">),</span> </span></span><span class="line"><span class="cl">    <span class="k">MAX</span><span class="p">(</span><span class="n">fieldZ</span><span class="p">)</span> </span></span><span class="line"><span class="cl"> <span class="k">FROM</span> <span class="n">tableA</span> </span></span><span class="line"><span class="cl"> <span class="k">GROUP</span> <span class="k">BY</span> <span class="n">fieldA</span><span class="p">)</span> <span class="n">minmax</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">tableA</span><span class="mf">.</span><span class="n">fieldA</span> <span class="o">=</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">fieldA</span> </span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">fieldA</span> <span class="mf">...</span> <span class="p">;</span> </span></span></code></pre></div> |
| <a href="/transform-data/idiomatic-materialize-sql/last-value/" >Last value over partition<br>order by &hellip;<br>range between unbounded preceding<br>and unbounded following</a> | <p>Use a subquery that uses the <a href="/sql/functions/#min" >MIN()</a> or <a href="/sql/functions/#max" >MAX()</a> aggregate function.</p> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">tableA</span><span class="mf">.</span><span class="n">fieldA</span><span class="p">,</span> <span class="n">tableA</span><span class="mf">.</span><span class="n">fieldB</span><span class="p">,</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">Z</span> </span></span><span class="line"><span class="cl"> <span class="k">FROM</span> <span class="n">tableA</span><span class="p">,</span> </span></span><span class="line"><span class="cl"> <span class="p">(</span><span class="k">SELECT</span> <span class="n">fieldA</span><span class="p">,</span> </span></span><span class="line"><span class="cl">    <span class="k">MAX</span><span class="p">(</span><span class="n">fieldZ</span><span class="p">),</span> </span></span><span class="line"><span class="cl">    <span class="n">MIN</span><span class="p">(</span><span class="n">fieldZ</span><span class="p">)</span> </span></span><span class="line"><span class="cl"> <span class="k">FROM</span> <span class="n">tableA</span> </span></span><span class="line"><span class="cl"> <span class="k">GROUP</span> <span class="k">BY</span> <span class="n">fieldA</span><span class="p">)</span> <span class="n">minmax</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">tableA</span><span class="mf">.</span><span class="n">fieldA</span> <span class="o">=</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">fieldA</span> </span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">fieldA</span> <span class="mf">...</span> <span class="p">;</span> </span></span></code></pre></div> |
| <a href="/transform-data/idiomatic-materialize-sql/lag/" >Lag over (order by) whose ordering can be represented by some equality condition.</a> | <p><em><strong>To exclude the first row since it has no previous row</strong></em></p> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="c1">-- Excludes the first row in the results -- </span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="k">SELECT</span> <span class="n">t1</span><span class="mf">.</span><span class="n">fieldA</span><span class="p">,</span> <span class="n">t2</span><span class="mf">.</span><span class="n">fieldB</span> <span class="k">as</span> <span class="n">previous_row_value</span> </span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">tableA</span> <span class="n">t1</span><span class="p">,</span> <span class="n">tableA</span> <span class="n">t2</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">t1</span><span class="mf">.</span><span class="n">fieldA</span> <span class="o">=</span> <span class="n">t2</span><span class="mf">.</span><span class="n">fieldA</span> <span class="o">+</span> <span class="mf">...</span> <span class="c1">-- or some other operand </span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">fieldA</span><span class="p">;</span> </span></span></code></pre></div><p><em><strong>To include the first row</strong></em></p> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="c1">-- Includes the first row in the results -- </span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="k">SELECT</span> <span class="n">t1</span><span class="mf">.</span><span class="n">fieldA</span><span class="p">,</span> <span class="n">t2</span><span class="mf">.</span><span class="n">fieldB</span> <span class="k">as</span> <span class="n">previous_row_value</span> </span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">tableA</span> <span class="n">t1</span> </span></span><span class="line"><span class="cl"><span class="k">LEFT</span> <span class="k">JOIN</span> <span class="n">tableA</span> <span class="n">t2</span> </span></span><span class="line"><span class="cl"><span class="k">ON</span> <span class="n">t1</span><span class="mf">.</span><span class="n">fieldA</span> <span class="o">=</span> <span class="n">t2</span><span class="mf">.</span><span class="n">fieldA</span> <span class="o">+</span> <span class="mf">...</span> <span class="c1">-- or some other operand </span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">fieldA</span><span class="p">;</span> </span></span></code></pre></div> |
| <a href="/transform-data/idiomatic-materialize-sql/lead/" >Lead over (order by) whose ordering can be represented by some equality condition.</a> | <p><em><strong>To exclude the last row since it has no next row</strong></em></p> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="c1">-- Excludes the last row in the results -- </span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="k">SELECT</span> <span class="n">t1</span><span class="mf">.</span><span class="n">fieldA</span><span class="p">,</span> <span class="n">t2</span><span class="mf">.</span><span class="n">fieldB</span> <span class="k">as</span> <span class="n">next_row_value</span> </span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">tableA</span> <span class="n">t1</span><span class="p">,</span> <span class="n">tableA</span> <span class="n">t2</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">t1</span><span class="mf">.</span><span class="n">fieldA</span> <span class="o">=</span> <span class="n">t2</span><span class="mf">.</span><span class="n">fieldA</span> <span class="o">-</span> <span class="mf">...</span> <span class="c1">-- or some other operand </span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">fieldA</span><span class="p">;</span> </span></span></code></pre></div><p><em><strong>To include the last row</strong></em></p> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="c1">-- Includes the last row in the results -- </span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="k">SELECT</span> <span class="n">t1</span><span class="mf">.</span><span class="n">fieldA</span><span class="p">,</span> <span class="n">t2</span><span class="mf">.</span><span class="n">fieldB</span> <span class="k">as</span> <span class="n">next_row_value</span> </span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">tableA</span> <span class="n">t1</span> </span></span><span class="line"><span class="cl"><span class="k">LEFT</span> <span class="k">JOIN</span> <span class="n">tableA</span> <span class="n">t2</span> </span></span><span class="line"><span class="cl"><span class="k">ON</span> <span class="n">t1</span><span class="mf">.</span><span class="n">fieldA</span> <span class="o">=</span> <span class="n">t2</span><span class="mf">.</span><span class="n">fieldA</span> <span class="o">-</span> <span class="mf">...</span> <span class="c1">-- or some other operand </span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">fieldA</span><span class="p">;</span> </span></span></code></pre></div> |

### Examples

|   | Example |
| --- | --- |
| <a href="/transform-data/idiomatic-materialize-sql/top-k/#for-k--1" >Top-K over partition<br>(K &gt;= 1)</a> | <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">order_id</span><span class="p">,</span> <span class="n">item</span><span class="p">,</span> <span class="n">subtotal</span> </span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="p">(</span><span class="k">SELECT</span> <span class="k">DISTINCT</span> <span class="n">order_id</span> <span class="k">FROM</span> <span class="n">orders_view</span><span class="p">)</span> <span class="n">grp</span><span class="p">,</span> </span></span><span class="line"><span class="cl">     <span class="k">LATERAL</span> <span class="p">(</span><span class="k">SELECT</span> <span class="n">item</span><span class="p">,</span> <span class="n">subtotal</span> <span class="k">FROM</span> <span class="n">orders_view</span> </span></span><span class="line"><span class="cl">        <span class="k">WHERE</span> <span class="n">order_id</span> <span class="o">=</span> <span class="n">grp</span><span class="mf">.</span><span class="n">order_id</span> </span></span><span class="line"><span class="cl">        <span class="k">ORDER</span> <span class="k">BY</span> <span class="n">subtotal</span> <span class="k">DESC</span> <span class="k">LIMIT</span> <span class="mf">3</span><span class="p">)</span> </span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">order_id</span><span class="p">,</span> <span class="n">subtotal</span> <span class="k">DESC</span><span class="p">;</span> </span></span></code></pre></div> |
| <a href="/transform-data/idiomatic-materialize-sql/top-k/#for-k--1-1" >Top-K over partition<br>(K = 1)</a> | <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="k">DISTINCT</span> <span class="k">ON</span><span class="p">(</span><span class="n">order_id</span><span class="p">)</span> <span class="n">order_id</span><span class="p">,</span> <span class="n">item</span><span class="p">,</span> <span class="n">subtotal</span> </span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">orders_view</span> </span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">order_id</span><span class="p">,</span> <span class="n">subtotal</span> <span class="k">DESC</span><span class="p">;</span> </span></span></code></pre></div> |
| <a href="/transform-data/idiomatic-materialize-sql/first-value/" >First value over partition<br>order by &hellip;</a> | <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span><span class="p">,</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">lowest_price</span><span class="p">,</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">highest_price</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">price</span><span class="p">,</span> </span></span><span class="line"><span class="cl">  <span class="n">o</span><span class="mf">.</span><span class="n">price</span> <span class="o">-</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">lowest_price</span> <span class="k">AS</span> <span class="n">diff_lowest_price</span><span class="p">,</span> </span></span><span class="line"><span class="cl">  <span class="n">o</span><span class="mf">.</span><span class="n">price</span> <span class="o">-</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">highest_price</span> <span class="k">AS</span> <span class="n">diff_highest_price</span> </span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">orders_view</span> <span class="n">o</span><span class="p">,</span> </span></span><span class="line"><span class="cl">      <span class="p">(</span><span class="k">SELECT</span> <span class="n">order_id</span><span class="p">,</span> </span></span><span class="line"><span class="cl">         <span class="n">MIN</span><span class="p">(</span><span class="n">price</span><span class="p">)</span> <span class="k">AS</span> <span class="n">lowest_price</span><span class="p">,</span> </span></span><span class="line"><span class="cl">         <span class="k">MAX</span><span class="p">(</span><span class="n">price</span><span class="p">)</span> <span class="k">AS</span> <span class="n">highest_price</span> </span></span><span class="line"><span class="cl">      <span class="k">FROM</span> <span class="n">orders_view</span> </span></span><span class="line"><span class="cl">      <span class="k">GROUP</span> <span class="k">BY</span> <span class="n">order_id</span><span class="p">)</span> <span class="n">minmax</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span> <span class="o">=</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">order_id</span> </span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span><span class="p">;</span> </span></span></code></pre></div> |
| <a href="/transform-data/idiomatic-materialize-sql/last-value/" >Last value over partition<br>order by &hellip;<br>range between unbounded preceding<br>and unbounded following</a> | <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span><span class="p">,</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">lowest_price</span><span class="p">,</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">highest_price</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">price</span><span class="p">,</span> </span></span><span class="line"><span class="cl">  <span class="n">o</span><span class="mf">.</span><span class="n">price</span> <span class="o">-</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">lowest_price</span> <span class="k">AS</span> <span class="n">diff_lowest_price</span><span class="p">,</span> </span></span><span class="line"><span class="cl">  <span class="n">o</span><span class="mf">.</span><span class="n">price</span> <span class="o">-</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">highest_price</span> <span class="k">AS</span> <span class="n">diff_highest_price</span> </span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">orders_view</span> <span class="n">o</span><span class="p">,</span> </span></span><span class="line"><span class="cl">      <span class="p">(</span><span class="k">SELECT</span> <span class="n">order_id</span><span class="p">,</span> </span></span><span class="line"><span class="cl">         <span class="n">MIN</span><span class="p">(</span><span class="n">price</span><span class="p">)</span> <span class="k">AS</span> <span class="n">lowest_price</span><span class="p">,</span> </span></span><span class="line"><span class="cl">         <span class="k">MAX</span><span class="p">(</span><span class="n">price</span><span class="p">)</span> <span class="k">AS</span> <span class="n">highest_price</span> </span></span><span class="line"><span class="cl">      <span class="k">FROM</span> <span class="n">orders_view</span> </span></span><span class="line"><span class="cl">      <span class="k">GROUP</span> <span class="k">BY</span> <span class="n">order_id</span><span class="p">)</span> <span class="n">minmax</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span> <span class="o">=</span> <span class="n">minmax</span><span class="mf">.</span><span class="n">order_id</span> </span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">o</span><span class="mf">.</span><span class="n">order_id</span><span class="p">,</span> <span class="n">o</span><span class="mf">.</span><span class="n">item</span><span class="p">;</span> </span></span></code></pre></div> |
| <a href="/transform-data/idiomatic-materialize-sql/lag/" >Lag over (order by) whose ordering can be represented by some equality condition.</a> | <p><em><strong>To exclude the first row since it has no previous row</strong></em></p> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">o1</span><span class="mf">.</span><span class="n">order_date</span><span class="p">,</span> <span class="n">o1</span><span class="mf">.</span><span class="n">daily_total</span><span class="p">,</span> </span></span><span class="line"><span class="cl">    <span class="n">o2</span><span class="mf">.</span><span class="n">daily_total</span> <span class="k">as</span> <span class="n">previous_daily_total</span> </span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">orders_daily_totals</span> <span class="n">o1</span><span class="p">,</span> <span class="n">orders_daily_totals</span> <span class="n">o2</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">o1</span><span class="mf">.</span><span class="n">order_date</span> <span class="o">=</span> <span class="n">o2</span><span class="mf">.</span><span class="n">order_date</span> <span class="o">+</span> <span class="nb">INTERVAL</span> <span class="s1">&#39;1&#39;</span> <span class="k">DAY</span> </span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">order_date</span><span class="p">;</span> </span></span></code></pre></div><p><em><strong>To include the first row</strong></em></p> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">o1</span><span class="mf">.</span><span class="n">order_date</span><span class="p">,</span> <span class="n">o1</span><span class="mf">.</span><span class="n">daily_total</span><span class="p">,</span> </span></span><span class="line"><span class="cl">    <span class="n">o2</span><span class="mf">.</span><span class="n">daily_total</span> <span class="k">as</span> <span class="n">previous_daily_total</span> </span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">orders_daily_totals</span> <span class="n">o1</span> </span></span><span class="line"><span class="cl"><span class="k">LEFT</span> <span class="k">JOIN</span> <span class="n">orders_daily_totals</span> <span class="n">o2</span> </span></span><span class="line"><span class="cl"><span class="k">ON</span> <span class="n">o1</span><span class="mf">.</span><span class="n">order_date</span> <span class="o">=</span> <span class="n">o2</span><span class="mf">.</span><span class="n">order_date</span> <span class="o">+</span> <span class="nb">INTERVAL</span> <span class="s1">&#39;1&#39;</span> <span class="k">DAY</span> </span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">order_date</span><span class="p">;</span> </span></span></code></pre></div> |
| <a href="/transform-data/idiomatic-materialize-sql/lead/" >Lead over (order by) whose ordering can be represented by some equality condition.</a> | <p><em><strong>To exclude the last row since it has no next row</strong></em></p> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">o1</span><span class="mf">.</span><span class="n">order_date</span><span class="p">,</span> <span class="n">o1</span><span class="mf">.</span><span class="n">daily_total</span><span class="p">,</span> </span></span><span class="line"><span class="cl">    <span class="n">o2</span><span class="mf">.</span><span class="n">daily_total</span> <span class="k">as</span> <span class="n">next_daily_total</span> </span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">orders_daily_totals</span> <span class="n">o1</span><span class="p">,</span> <span class="n">orders_daily_totals</span> <span class="n">o2</span> </span></span><span class="line"><span class="cl"><span class="k">WHERE</span> <span class="n">o1</span><span class="mf">.</span><span class="n">order_date</span> <span class="o">=</span> <span class="n">o2</span><span class="mf">.</span><span class="n">order_date</span> <span class="o">-</span> <span class="nb">INTERVAL</span> <span class="s1">&#39;1&#39;</span> <span class="k">DAY</span> </span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">order_date</span><span class="p">;</span> </span></span></code></pre></div><p><em><strong>To include the last row</strong></em></p> <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">SELECT</span> <span class="n">o1</span><span class="mf">.</span><span class="n">order_date</span><span class="p">,</span> <span class="n">o1</span><span class="mf">.</span><span class="n">daily_total</span><span class="p">,</span> </span></span><span class="line"><span class="cl">    <span class="n">o2</span><span class="mf">.</span><span class="n">daily_total</span> <span class="k">as</span> <span class="n">next_daily_total</span> </span></span><span class="line"><span class="cl"><span class="k">FROM</span> <span class="n">orders_daily_totals</span> <span class="n">o1</span> </span></span><span class="line"><span class="cl"><span class="k">LEFT</span> <span class="k">JOIN</span> <span class="n">orders_daily_totals</span> <span class="n">o2</span> </span></span><span class="line"><span class="cl"><span class="k">ON</span> <span class="n">o1</span><span class="mf">.</span><span class="n">order_date</span> <span class="o">=</span> <span class="n">o2</span><span class="mf">.</span><span class="n">order_date</span> <span class="o">-</span> <span class="nb">INTERVAL</span> <span class="s1">&#39;1&#39;</span> <span class="k">DAY</span> </span></span><span class="line"><span class="cl"><span class="k">ORDER</span> <span class="k">BY</span> <span class="n">order_date</span><span class="p">;</span> </span></span></code></pre></div> |

## See also

- [SQL Functions](/sql/functions/)
- [SQL Types](/sql/types/)
- [SELECT](/sql/select/)
- [DISTINCT](/sql/select/#select-distinct)
- [DISTINCT ON](/sql/select/#select-distinct-on)

---

## Window function to idiomatic Materialize

Materialize offers a wide range of [window
functions](/sql/functions/#window-functions). However, for some
[`LAG()`](/sql/functions/#lag), [`LEAD()`](/sql/functions/#lead),
[`ROW_NUMBER()`](/sql/functions/#row_number),
[`FIRST_VALUE()`](/sql/functions/#first_value), and
[`LAST_VALUE()`](/sql/functions/#last_value) use cases, Materialize provides its
own idiomatic query patterns that do <red>not</red> use the window functions and
can provide better performance.

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

<table>
<thead>
<tr>
<th>
Windows function anti-pattern
</th>
<th>
Materialize idiomatic SQL
</th>
</tr>
</thead>
<tbody>

<tr>
<td colspan=2>

**First value within groups.** For more information and examples, see [Idiomatic Materialize SQL: First
value](/transform-data/idiomatic-materialize-sql/first-value/).

</td>
</tr>
<tr>
<td>
<div style="background-color: var(--code-block)">

```nofmt
-- Anti-pattern. Avoid. --
SELECT fieldA, fieldB,
 FIRST_VALUE(fieldZ)
   OVER (PARTITION BY fieldA ORDER BY ...)
FROM tableA
ORDER BY fieldA, ...;
```

</div>
</td>
<td class="copyableCode">

```mzsql
SELECT tableA.fieldA, tableA.fieldB, minmax.Z
FROM tableA,
     (SELECT fieldA,
        MIN(fieldZ)
      FROM tableA
      GROUP BY fieldA) minmax
WHERE tableA.fieldA = minmax.fieldA
ORDER BY fieldA ... ;
```

</td>
</tr>

<tr>
<td colspan=2>

**Lag over whose order by field advances in a regular pattern.**
For more information and examples, see [Idiomatic Materialize SQL: Lag
over](/transform-data/idiomatic-materialize-sql/lag/).

</td>
</tr>
<tr>
<td>
<div style="background-color: var(--code-block)">

```nofmt
-- Anti-pattern. Avoid --
SELECT fieldA, ...
  LAG(fieldZ)
    OVER (ORDER BY fieldA) as previous_row_value
FROM tableA;
```

</div>
</td>
<td class="copyableCode">

```mzsql
-- Excludes the first row in the results --
SELECT t1.fieldA, t2.fieldB as previous_row_value
FROM tableA t1, tableA t2
WHERE t1.fieldA = t2.fieldA + ...
ORDER BY fieldA;
```

</td>
</tr>

<tr>
<td colspan=2>

**Last value within groups.** For more information and examples, see [Idiomatic Materialize SQL: Last value in
group](/transform-data/idiomatic-materialize-sql/last-value/).

</td>
</tr>
<tr>
<td>
<div style="background-color: var(--code-block)">

```nofmt
-- Anti-pattern. Unsupported range. --
SELECT fieldA, fieldB,
  LAST_VALUE(fieldZ)
    OVER (PARTITION BY fieldA ORDER BY fieldZ
          RANGE BETWEEN
            UNBOUNDED PRECEDING AND
            UNBOUNDED FOLLOWING)
FROM tableA
ORDER BY fieldA, ...;
```

</div>
</td>
<td class="copyableCode">

```mzsql
SELECT tableA.fieldA, tableA.fieldB, minmax.Z
 FROM tableA,
      (SELECT fieldA,
         MAX(fieldZ)
       FROM tableA
       GROUP BY fieldA) minmax
WHERE tableA.fieldA = minmax.fieldA
ORDER BY fieldA ... ;
```

</td>
</tr>

<tr>
<td colspan=2>

**Lead over whose order by field advances in a regular pattern.** For more
information and examples, see [Idiomatic Materialize SQL: Lead
over](/transform-data/idiomatic-materialize-sql/lead/).

</td>
</tr>
<tr>
<td>
<div style="background-color: var(--code-block)">

```nofmt
-- Anti-pattern. Avoid. --
SELECT fieldA, ...
    LEAD(fieldZ)
      OVER (ORDER BY fieldA) as next_row_value
FROM tableA;
```

</div>
</td>
<td class="copyableCode">

```mzsql
-- Excludes the last row in the results --
SELECT t1.fieldA, t2.fieldB as next_row_value
FROM tableA t1, tableA t2
WHERE t1.fieldA = t2.fieldA - ...
ORDER BY fieldA;
```

</td>
</tr>

<tr>
<td colspan=2>

**Top-K queries.** For more information and examples, see [Idiomatic Materialize SQL: Top-K in
group](/transform-data/idiomatic-materialize-sql/top-k/).

</td>
</tr>
<tr>
<td>
<div style="background-color: var(--code-block)">

```nofmt
-- Anti-pattern. Avoid. --
SELECT fieldA, fieldB, ...
FROM (
  SELECT fieldA, fieldB, ... , fieldZ,
     ROW_NUMBER() OVER (PARTITION BY fieldA
     ORDER BY fieldZ ... ) as rn
  FROM tableA)
WHERE rn <= K
ORDER BY fieldA, fieldZ ...;
```

</div>
</td>
<td class="copyableCode">

```mzsql
SELECT fieldA, fieldB, ...
FROM (SELECT DISTINCT fieldA FROM tableA) grp,
  LATERAL (SELECT fieldB, ... , fieldZ FROM tableA
           WHERE fieldA = grp.fieldA
           ORDER BY fieldZ ... LIMIT K)
ORDER BY fieldA, fieldZ ... ;
```

</td>
</tr>
</tbody>
</table>

