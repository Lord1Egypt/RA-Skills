# References

---

## Explain plan operators

Materialize offers several output formats for [`EXPLAIN
PLAN`](/sql/explain-plan/) and debugging. LIR plans as rendered in
[`mz_introspection.mz_lir_mapping`](../../reference/system-catalog/mz_introspection/#mz_lir_mapping)
are deliberately succinct, while the plans in other formats give more detail.

The decorrelated and optimized plans from `EXPLAIN DECORRELATED PLAN
FOR ...`, `EXPLAIN LOCALLY OPTIMIZED PLAN FOR ...`, and `EXPLAIN
OPTIMIZED PLAN FOR ...` are in a mid-level representation that is
closer to LIR than SQL. The raw plans from `EXPLAIN RAW PLAN FOR ...`
are closer to SQL (and therefore less indicative of how the query will
actually run).

**In fully optimized physical (LIR) plans (Default):**
The following table lists the operators that are available in the LIR plan.

- For those operators that require memory to maintain intermediate state, **Uses memory** is marked with **Yes**.
- For those operators that expand the data size (either rows or columns), **Can increase data size** is marked with **Yes**.| Operator | Description | Example |
| --- | --- | --- |
| **Constant** | Always produces the same collection of rows.  **Can increase data size:** No **Uses memory:** No | <code>→Constant (2 rows)</code> |
| **Stream, Arranged, Index Lookup, Read** | <p>Produces rows from either an existing relation (source/view/materialized view/table) or from a previous CTE in the same plan. A parent <code>Fused Map/Filter/Project</code> operator can combine with this operator.</p> <p>There are four types of <code>Get</code>.</p> <ol> <li> <p><code>Stream</code> indicates that the results are not <a href="/get-started/arrangements/#arrangements" >arranged</a> in memory and will be streamed directly.</p> </li> <li> <p><code>Arranged</code> indicates that the results are <a href="/get-started/arrangements/#arrangements" >arranged</a> in memory.</p> </li> <li> <p><code>Index Lookup</code> indicates the results will be <em>looked up</em> in an existing [arrangement]((/get-started/arrangements/#arrangements).</p> </li> <li> <p><code>Read</code> indicates that the results are unarranged, and will be processed as they arrive.</p> </li> </ol>   **Can increase data size:** No **Uses memory:** No | <code>Arranged materialize.public.t</code> |
| **Map/Filter/Project** | <p>Computes new columns (maps), filters columns, and projects away columns. Works row-by-row. Maps and filters will be printed, but projects will not.</p> <p>These may be marked as <strong><code>Fused</code></strong> <code>Map/Filter/Project</code>, which means they will combine with the operator beneath them to run more efficiently.</p>   **Can increase data size:** Each row may have more data, from the <code>Map</code>. Each row may also have less data, from the <code>Project</code>. There may be fewer rows, from the <code>Filter</code>. **Uses memory:** No | <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="err">→</span><span class="k">Map</span><span class="o">/</span><span class="k">Filter</span><span class="o">/</span><span class="n">Project</span> </span></span><span class="line"><span class="cl">  <span class="k">Filter</span><span class="p">:</span> <span class="p">(</span><span class="o">#</span><span class="mf">0</span><span class="p">{</span><span class="n">a</span><span class="p">}</span> <span class="o">&lt;</span> <span class="mf">7</span><span class="p">)</span> </span></span><span class="line"><span class="cl">  <span class="k">Map</span><span class="p">:</span> <span class="p">(</span><span class="o">#</span><span class="mf">0</span><span class="p">{</span><span class="n">a</span><span class="p">}</span> <span class="o">+</span> <span class="o">#</span><span class="mf">1</span><span class="p">{</span><span class="n">b</span><span class="p">})</span> </span></span></code></pre></div> |
| **Table Function** | <p>Appends the result of some (one-to-many) <a href="/sql/functions/#table-functions" >table function</a> to each row in the input.</p> <p>A parent <code>Fused Table Function unnest_list</code> operator will fuse with its child <code>GroupAggregate</code> operator. Fusing these operator is part of how we efficiently compile window functions from SQL to dataflows.</p> <p>A parent <code>Fused Map/Filter/Project</code> can combine with this operator.</p>   **Can increase data size:** Depends on the <a href="/sql/functions/#table-functions" >table function</a> used. **Uses memory:** No | <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="err">→</span><span class="k">Table</span> <span class="k">Function</span> <span class="n">generate_series</span><span class="p">(</span><span class="o">#</span><span class="mf">0</span><span class="p">{</span><span class="n">a</span><span class="p">},</span> <span class="o">#</span><span class="mf">1</span><span class="p">{</span><span class="n">b</span><span class="p">},</span> <span class="mf">1</span><span class="p">)</span> </span></span><span class="line"><span class="cl">  <span class="k">Input</span> <span class="k">key</span><span class="p">:</span> <span class="p">(</span><span class="o">#</span><span class="mf">0</span><span class="p">{</span><span class="n">a</span><span class="p">})</span> </span></span></code></pre></div> |
| **Differential Join, Delta Join** | <p>Both join operators indicate the join ordering selected.</p> <p>Returns combinations of rows from each input whenever some equality predicates are <code>true</code>.</p> <p>Joins will indicate the join order of their children, starting from 0. For example, <code>Differential Join %1 » %0</code> will join its second child into its first.</p> <p>The <a href="/transform-data/optimization/#join" >two joins differ in performance characteristics</a>.</p>   **Can increase data size:** Depends on the join order and facts about the joined collections. **Uses memory:** ✅ Uses memory for 3-way or more differential joins. | <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="err">→</span><span class="n">Differential</span> <span class="k">Join</span> <span class="o">%</span><span class="mf">1</span> <span class="err">»</span> <span class="o">%</span><span class="mf">0</span> </span></span><span class="line"><span class="cl">  <span class="k">Join</span> <span class="n">stage</span> <span class="o">%</span><span class="mf">0</span><span class="p">:</span> <span class="n">Lookup</span> <span class="k">key</span> <span class="o">#</span><span class="mf">0</span><span class="p">{</span><span class="n">a</span><span class="p">}</span> <span class="k">in</span> <span class="o">%</span><span class="mf">0</span> </span></span></code></pre></div> |
| **GroupAggregate** | <p>Groups the input rows by some scalar expressions, reduces each group using some aggregate functions, and produces rows containing the group key and aggregate outputs.</p> <p>There are five types of <code>GroupAggregate</code>, ordered by increasing complexity:</p> <ol> <li> <p><code>Distinct GroupAggregate</code> corresponds to the SQL <code>DISTINCT</code> operator.</p> </li> <li> <p><code>Accumulable GroupAggregate</code> (e.g., <code>SUM</code>, <code>COUNT</code>) corresponds to several easy to implement aggregations that can be executed efficiently.</p> </li> <li> <p><code>Hierarchical GroupAggregate</code> (e.g., <code>MIN</code>, <code>MAX</code>) corresponds to an aggregation requiring a tower of arrangements. These can be either monotonic (more efficient) or bucketed. These may benefit from a hint; <a href="/reference/system-catalog/mz_introspection/#mz_expected_group_size_advice" >see <code>mz_introspection.mz_expected_group_size_advice</code></a>. These may either be bucketed or monotonic (more efficient). These may consolidate their output, which will increase memory usage.</p> </li> <li> <p><code>Collated Multi-GroupAggregate</code> corresponds to an arbitrary mix of reductions of different types, which will be performed separately and then joined together.</p> </li> <li> <p><code>Non-incremental GroupAggregate</code> (e.g., window functions, <code>list_agg</code>) corresponds to a single non-incremental aggregation. These are the most computationally intensive reductions.</p> </li> </ol> <p>A parent <code>Fused Map/Filter/Project</code> can combine with this operator.</p>   **Can increase data size:** No **Uses memory:** ✅ <code>Distinct</code> and <code>Accumulable</code> aggregates use a moderate amount of memory (proportional to twice the output size). <code>MIN</code> and <code>MAX</code> aggregates can use significantly more memory. This can be improved by including group size hints in the query, see <a href="/reference/system-catalog/mz_introspection/#mz_expected_group_size_advice" ><code>mz_introspection.mz_expected_group_size_advice</code></a>. <code>Non-incremental</code> aggregates use memory proportional to the input + output size. <code>Collated</code> aggregates use memory that is the sum of their constituents, plus some memory for the join at the end. | <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="err">→</span><span class="n">Accumulable</span> <span class="n">GroupAggregate</span> </span></span><span class="line"><span class="cl">  <span class="n">Simple</span> <span class="n">aggregates</span><span class="p">:</span> <span class="k">count</span><span class="p">(</span><span class="o">*</span><span class="p">)</span> </span></span><span class="line"><span class="cl">  <span class="n">Post</span><span class="o">-</span><span class="n">process</span> <span class="k">Map</span><span class="o">/</span><span class="k">Filter</span><span class="o">/</span><span class="n">Project</span> </span></span><span class="line"><span class="cl">    <span class="k">Filter</span><span class="p">:</span> <span class="p">(</span><span class="o">#</span><span class="mf">0</span> <span class="o">&gt;</span> <span class="mf">1</span><span class="p">)</span> </span></span></code></pre></div> |
| **TopK** | <p>Groups the input rows, sorts them according to some ordering, and returns at most <code>K</code> rows at some offset from the top of the list, where <code>K</code> is some (possibly computed) limit.</p> <p>There are three types of <code>TopK</code>. Two are special cased for monotonic inputs (i.e., inputs which never retract data).</p> <ol> <li><code>Monotonic Top1</code>.</li> <li><code>Monotonic TopK</code>, which may give an expression indicating the limit.</li> <li><code>Non-monotonic TopK</code>, a generic <code>TopK</code> plan.</li> </ol> <p>Each version of the <code>TopK</code> operator may include grouping, ordering, and limit directives.</p>   **Can increase data size:** No **Uses memory:** ✅ <code>Monotonic Top1</code> and <code>Monotonic TopK</code> use a moderate amount of memory. <code>Non-monotonic TopK</code> uses significantly more memory as the operator can significantly overestimate the group sizes. Consult <a href="/reference/system-catalog/mz_introspection/#mz_expected_group_size_advice" ><code>mz_introspection.mz_expected_group_size_advice</code></a>. | <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="err">→</span><span class="n">Consolidating</span> <span class="n">Monotonic</span> <span class="n">TopK</span> </span></span><span class="line"><span class="cl">  <span class="k">Order</span> <span class="k">By</span> <span class="o">#</span><span class="mf">1</span> <span class="k">asc</span> <span class="n">nulls_last</span><span class="p">,</span> <span class="o">#</span><span class="mf">0</span> <span class="k">desc</span> <span class="n">nulls_first</span> </span></span><span class="line"><span class="cl">  <span class="k">Limit</span> <span class="mf">5</span> </span></span></code></pre></div> |
| **Negate Diffs** | Negates the row counts of the input. This is usually used in combination with union to remove rows from the other union input.  **Can increase data size:** No **Uses memory:** No | <code>→Negate Diffs</code> |
| **Threshold Diffs** | Removes any rows with negative counts.  **Can increase data size:** No **Uses memory:** ✅ Uses memory proportional to the input and output size, twice. | <code>→Threshold Diffs</code> |
| **Union** | Combines its inputs into a unified output, emitting one row for each row on any input. (Corresponds to <code>UNION ALL</code> rather than <code>UNION</code>/<code>UNION DISTINCT</code>.)  **Can increase data size:** No **Uses memory:** ✅ A <code>Consolidating Union</code> will make moderate use of memory, particularly at hydration time. A <code>Union</code> that is not <code>Consolidating</code> will not consume memory. | <code>→Consolidating Union</code> |
| **Arrange** | Indicates a point that will become an <a href="/get-started/arrangements/#arrangements" >arrangement</a> in the dataflow engine, i.e., it will consume memory to cache results.  **Can increase data size:** No **Uses memory:** ✅ Uses memory proportional to the input size. Note that in the LIR / physical plan, <code>Arrange</code>/<code>ArrangeBy</code> almost always means that an arrangement will actually be created. (This is in contrast to the &ldquo;optimized&rdquo; plan, where an <code>ArrangeBy</code> being present in the plan often does not mean that an arrangement will actually be created.) | <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="err">→</span><span class="n">Arrange</span> </span></span><span class="line"><span class="cl">    <span class="k">Keys</span><span class="p">:</span> <span class="mf">1</span> <span class="k">arrangement</span> <span class="n">available</span><span class="p">,</span> <span class="n">plus</span> <span class="k">raw</span> <span class="n">stream</span> </span></span><span class="line"><span class="cl">      <span class="k">Arrangement</span> <span class="mf">0</span><span class="p">:</span> <span class="o">#</span><span class="mf">0</span> </span></span></code></pre></div> |
| **Unarranged Raw Stream** | Indicates a point where data will be streamed (even if it is somehow already arranged).  **Can increase data size:** No **Uses memory:** No | <code>→Unarranged Raw Stream</code> |
| **With ... Return ...** | Introduces CTEs, i.e., makes it possible for sub-plans to be consumed multiple times by downstream operators.  **Can increase data size:** No **Uses memory:** No | <a href="/sql/explain-plan/#reading-plans" >See Reading plans</a> |
**Notes:**
- **Can increase data size:** Specifies whether the operator can increase the data size (can be the number of rows or the number of columns).
- **Uses memory:** Specifies whether the operator use memory to maintain state for its inputs.

**In decorrelated and optimized plans:**
The following table lists the operators that are available in the optimized plan.

- For those operators that require memory to maintain intermediate state, **Uses memory** is marked with **Yes**.
- For those operators that expand the data size (either rows or columns), **Can increase data size** is marked with **Yes**.| Operator | Description | Example |
| --- | --- | --- |
| **Constant** | Always produces the same collection of rows.  **Can increase data size:** No **Uses memory:** No | <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="n">Constant</span> </span></span><span class="line"><span class="cl"><span class="o">-</span> <span class="p">((</span><span class="mf">1</span><span class="p">,</span> <span class="mf">2</span><span class="p">)</span> <span class="n">x</span> <span class="mf">2</span><span class="p">)</span> </span></span><span class="line"><span class="cl"><span class="o">-</span> <span class="p">(</span><span class="mf">3</span><span class="p">,</span> <span class="mf">4</span><span class="p">)</span> </span></span></code></pre></div> |
| **Get** | Produces rows from either an existing relation (source/view/materialized view/table) or from a previous CTE in the same plan.  **Can increase data size:** No **Uses memory:** No | <code>Get materialize.public.ordered</code> |
| **Project** | Produces a subset of the <a href="/sql/explain-plan/#explain-plan-columns" >columns</a> in the input rows. See also <a href="/sql/explain-plan/#explain-plan-columns" >column numbering</a>.  **Can increase data size:** No **Uses memory:** No | <code>Project (#2, #3)</code> |
| **Map** | Appends the results of some scalar expressions to each row in the input.  **Can increase data size:** Each row has more data (i.e., longer rows but same number of rows). **Uses memory:** No | <code>Map (((#1 * 10000000dec) / #2) * 1000dec)</code> |
| **FlatMap** | Appends the result of some (one-to-many) <a href="/sql/functions/#table-functions" >table function</a> to each row in the input.  **Can increase data size:** Depends on the <a href="/sql/functions/#table-functions" >table function</a> used. **Uses memory:** No | <code>FlatMap jsonb_foreach(#3)</code> |
| **Filter** | Removes rows of the input for which some scalar predicates return <code>false</code>.  **Can increase data size:** No **Uses memory:** No | <code>Filter (#20 &lt; #21)</code> |
| **Join** | Returns combinations of rows from each input whenever some equality predicates are <code>true</code>.  **Can increase data size:** Depends on the join order and facts about the joined collections. **Uses memory:** ✅ The <code>Join</code> operator itself uses memory only for <code>type=differential</code> with more than 2 inputs. However, <code>Join</code> operators need <a href="/get-started/arrangements/#arrangements" >arrangements</a> on their inputs (shown by the <code>ArrangeBy</code> operator). These arrangements use memory proportional to the input sizes. If an input has an <a href="/transform-data/optimization/#join" >appropriate index</a>, then the arrangement of the index will be reused. | <code>Join on=(#1 = #2) type=delta</code> |
| **CrossJoin** | An alias for a <code>Join</code> with an empty predicate (emits all combinations). Note that not all cross joins are marked as <code>CrossJoin</code>: In a join with more than 2 inputs, it can happen that there is a cross join between some of the inputs. You can recognize this case by <code>ArrangeBy</code> operators having empty keys, i.e., <code>ArrangeBy keys=[[]]</code>.  **Can increase data size:** Cartesian product of the inputs (\|N\| x \|M\|). **Uses memory:** ✅ Uses memory for 3-way or more differential joins. | <code>CrossJoin type=differential</code> |
| **Reduce** | Groups the input rows by some scalar expressions, reduces each group using some aggregate functions, and produces rows containing the group key and aggregate outputs.  **Can increase data size:** No **Uses memory:** ✅ <code>SUM</code>, <code>COUNT</code>, and most other aggregations use a moderate amount of memory (proportional either to twice the output size or to input size + output size). <code>MIN</code> and <code>MAX</code> aggregates can use significantly more memory. This can be improved by including group size hints in the query, see <a href="/reference/system-catalog/mz_introspection/#mz_expected_group_size_advice" ><code>mz_introspection.mz_expected_group_size_advice</code></a>. | <code>Reduce group_by=[#0] aggregates=[max((#0 * #1))]</code> |
| **Distinct** | Alias for a <code>Reduce</code> with an empty aggregate list.  **Can increase data size:** No **Uses memory:** ✅ Uses memory proportional to twice the output size. | <code>Distinct</code> |
| **TopK** | Groups the input rows by some scalar expressions, sorts each group using the group key, removes the top <code>offset</code> rows in each group, and returns the next <code>limit</code> rows.  **Can increase data size:** No **Uses memory:** ✅ Can use significant amount as the operator can significantly overestimate the group sizes. Consult <a href="/reference/system-catalog/mz_introspection/#mz_expected_group_size_advice" ><code>mz_introspection.mz_expected_group_size_advice</code></a>. | <code>TopK order_by=[#1 asc nulls_last, #0 desc nulls_first] limit=5</code> |
| **Negate** | Negates the row counts of the input. This is usually used in combination with union to remove rows from the other union input.  **Can increase data size:** No **Uses memory:** No | <code>Negate</code> |
| **Threshold** | Removes any rows with negative counts.  **Can increase data size:** No **Uses memory:** ✅ Uses memory proportional to the input and output size, twice. | <code>Threshold</code> |
| **Union** | Sums the counts of each row of all inputs. (Corresponds to <code>UNION ALL</code> rather than <code>UNION</code>/<code>UNION DISTINCT</code>.)  **Can increase data size:** No **Uses memory:** ✅ Moderate use of memory. Some union operators force consolidation, which results in a memory spike, largely at hydration time. | <code>Union</code> |
| **ArrangeBy** | Indicates a point that will become an <a href="/get-started/arrangements/#arrangements" >arrangement</a> in the dataflow engine (each <code>keys</code> element will be a different arrangement). Note that if an appropriate index already exists on the input or the output of the previous operator is already arranged with a key that is also requested here, then this operator will just pass on that existing arrangement instead of creating a new one.  **Can increase data size:** No **Uses memory:** ✅ Depends. If arrangements need to be created, they use memory proportional to the input size. | <code>ArrangeBy keys=[[#0]]</code> |
| **With ... Return ...** | Introduces CTEs, i.e., makes it possible for sub-plans to be consumed multiple times by downstream operators.  **Can increase data size:** No **Uses memory:** No | <a href="/sql/explain-plan/#reading-plans" >See Reading plans</a> |
**Notes:**
- **Can increase data size:** Specifies whether the operator can increase the data size (can be the number of rows or the number of columns).
- **Uses memory:** Specifies whether the operator use memory to maintain state for its inputs.

**In raw plans:**
The following table lists the operators that are available in the raw plan.

- For those operators that require memory to maintain intermediate state, **Uses memory** is marked with **Yes**.
- For those operators that expand the data size (either rows or columns), **Can increase data size** is marked with **Yes**.| Operator | Description | Example |
| --- | --- | --- |
| **Constant** | Always produces the same collection of rows.  **Can increase data size:** No **Uses memory:** No | <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="n">Constant</span> </span></span><span class="line"><span class="cl"><span class="o">-</span> <span class="p">((</span><span class="mf">1</span><span class="p">,</span> <span class="mf">2</span><span class="p">)</span> <span class="n">x</span> <span class="mf">2</span><span class="p">)</span> </span></span><span class="line"><span class="cl"><span class="o">-</span> <span class="p">(</span><span class="mf">3</span><span class="p">,</span> <span class="mf">4</span><span class="p">)</span> </span></span></code></pre></div> |
| **Get** | Produces rows from either an existing relation (source/view/materialized view/table) or from a previous CTE in the same plan.  **Can increase data size:** No **Uses memory:** No | <code>Get materialize.public.ordered</code> |
| **Project** | Produces a subset of the <a href="/sql/explain-plan/#explain-plan-columns" >columns</a> in the input rows. See also <a href="/sql/explain-plan/#explain-plan-columns" >column numbering</a>.  **Can increase data size:** No **Uses memory:** No | <code>Project (#2, #3)</code> |
| **Map** | Appends the results of some scalar expressions to each row in the input.  **Can increase data size:** Each row has more data (i.e., longer rows but same number of rows). **Uses memory:** No | <code>Map (((#1 * 10000000dec) / #2) * 1000dec)</code> |
| **CallTable** | Appends the result of some (one-to-many) <a href="/sql/functions/#table-functions" >table function</a> to each row in the input.  **Can increase data size:** Depends on the <a href="/sql/functions/#table-functions" >table function</a> used. **Uses memory:** No | <code>CallTable generate_series(1, 7, 1)</code> |
| **Filter** | Removes rows of the input for which some scalar predicates return <code>false</code>.  **Can increase data size:** No **Uses memory:** No | <code>Filter (#20 &lt; #21)</code> |
| **~Join** | Performs one of <code>INNER</code> / <code>LEFT</code> / <code>RIGHT</code> / <code>FULL OUTER</code> / <code>CROSS</code> join on the two inputs, using the given predicate.  **Can increase data size:** For <code>CrossJoin</code>s, Cartesian product of the inputs (\|N\| x \|M\|). Note that, in many cases, a join that shows up as a cross join in the RAW PLAN will actually be turned into an inner join in the OPTIMIZED PLAN, by making use of an equality WHERE condition. For other join types, depends on the join order and facts about the joined collections. **Uses memory:** ✅ Uses memory proportional to the input sizes, unless <a href="/transform-data/optimization/#join" >the inputs have appropriate indexes</a>. Certain joins with more than 2 inputs use additional memory, see details in the optimized plan. | <code>InnerJoin (#0 = #2)</code> |
| **Reduce** | Groups the input rows by some scalar expressions, reduces each group using some aggregate functions, and produces rows containing the group key and aggregate outputs.  In the case where the group key is empty and the input is empty, returns a single row with the aggregate functions applied to the empty input collection.  **Can increase data size:** No **Uses memory:** ✅ <code>SUM</code>, <code>COUNT</code>, and most other aggregations use a moderate amount of memory (proportional either to twice the output size or to input size + output size). <code>MIN</code> and <code>MAX</code> aggregates can use significantly more memory. This can be improved by including group size hints in the query, see <a href="/reference/system-catalog/mz_introspection/#mz_expected_group_size_advice" ><code>mz_introspection.mz_expected_group_size_advice</code></a>. | <code>Reduce group_by=[#0] aggregates=[max((#0 * #1))]</code> |
| **Distinct** | Removes duplicate copies of input rows.  **Can increase data size:** No **Uses memory:** ✅ Uses memory proportional to twice the output size. | <code>Distinct</code> |
| **TopK** | Groups the input rows by some scalar expressions, sorts each group using the group key, removes the top <code>offset</code> rows in each group, and returns the next <code>limit</code> rows.  **Can increase data size:** No **Uses memory:** ✅ Can use significant amount as the operator can significantly overestimate the group sizes. Consult <a href="/reference/system-catalog/mz_introspection/#mz_expected_group_size_advice" ><code>mz_introspection.mz_expected_group_size_advice</code></a>. | <code>TopK order_by=[#1 asc nulls_last, #0 desc nulls_first] limit=5</code> |
| **Negate** | Negates the row counts of the input. This is usually used in combination with union to remove rows from the other union input.  **Can increase data size:** No **Uses memory:** No | <code>Negate</code> |
| **Threshold** | Removes any rows with negative counts.  **Can increase data size:** No **Uses memory:** ✅ Uses memory proportional to the input and output size, twice. | <code>Threshold</code> |
| **Union** | Sums the counts of each row of all inputs. (Corresponds to <code>UNION ALL</code> rather than <code>UNION</code>/<code>UNION DISTINCT</code>.)  **Can increase data size:** No **Uses memory:** ✅ Moderate use of memory. Some union operators force consolidation, which results in a memory spike, largely at hydration time. | <code>Union</code> |
| **With ... Return ...** | Introduces CTEs, i.e., makes it possible for sub-plans to be consumed multiple times by downstream operators.  **Can increase data size:** No **Uses memory:** No | <a href="/sql/explain-plan/#reading-plans" >See Reading plans</a> |
**Notes:**
- **Can increase data size:** Specifies whether the operator can increase the data size (can be the number of rows or the number of columns).
- **Uses memory:** Specifies whether the operator use memory to maintain state for its inputs.

Operators are sometimes marked as `Fused ...`. This indicates that the operator is fused with its input, i.e., the operator below it. That is, if you see a `Fused X` operator above a `Y` operator:

```
→Fused X
  →Y
```

Then the `X` and `Y` operators will be combined into a single, more efficient operator.

See also:

- [`EXPLAIN PLAn`](/sql/explain-plan/)

---

## Isolation levels

An *isolation level* determines which effects of concurrent transactions are
visible to a transaction during its execution.

## Supported isolation levels

Materialize accepts the following isolation levels:

<table>
  <thead>
      <tr>
          <th>Isolation level</th>
          <th>Behavior in Materialize</th>
      </tr>
  </thead>
  <tbody>
      <tr>
          <td><a href="#strict-serializable" ><strong>Strict Serializable</strong></a></td>
          <td><strong>Default.</strong> Provides serializability and linearizability.</td>
      </tr>
      <tr>
          <td><a href="#serializable" ><strong>Serializable</strong></a></td>
          <td>Provides serializability but not linearizability.</td>
      </tr>
      <tr>
          <td>Read Uncommitted, Read Committed, Repeatable Read</td>
          <td>Accepted for compatibility; treated as Serializable.</td>
      </tr>
  </tbody>
</table>

## Serializable

Serializable prevents the following three phenomena[^1]:

| Phenomenon | Description |
| --- | --- |
| **P1 (Dirty read)** | A transaction **T1** modifies a row; another transaction **T2** reads the row before **T1** commits. If **T1** rolls back, **T2** has read a row that was never committed. |
| **P2 (Non-repeatable read)** | A transaction **T1** reads a row; another transaction **T2** modifies or deletes that row and commits. If **T1** attempts to reread the row, it may see the modified value or discover that the row no longer exists.|
| **P3 (Phantom)** | A transaction **T1** reads a set of rows that match a specific search condition; another transaction **T2** inserts rows that also match the condition and commits. If **T1** repeats the read with the same search condition, it gets a different set of rows. |

[^1]: Phenomenon descriptions adapted from ISO/IEC 9075-2:1999 (E), §4.32
    "SQL-transactions."

Serializable also guarantees that the result of concurrently executing
transactions is equivalent to some serial execution of those transactions. A
serial execution is one in which each transaction completes before the next one
begins. However, Serializable does not guarantee
[linearizability](https://jepsen.io/consistency/models/linearizable); that is,
it does not guarantee that the serial order matches the real-time order of the
transactions. For example, if transaction **T1** completes before transaction
**T2** begins in real time, the result may be equivalent to a serial execution
in which **T2** executes before **T1**.

Non-linearizable orderings are more likely to occur when querying indexes and
materialized views with large propagation delays. For example, suppose
transaction **T1** queries table `t` and is followed in real time by transaction
**T2**, which queries a computationally expensive materialized view `mv` defined
over `t`. If the two transactions execute sufficiently close together, `mv` may
not yet reflect the latest updates to `t` that **T1** observed, so **T2** may
not observe all rows visible to **T1**.

### Logical timestamp selection {#serializable-logical-timestamp-selection}

When using the [serializable](/reference/isolation-level#serializable)
isolation level, the logical timestamp may be arbitrarily ahead of or behind the
system clock. For example, at a wall clock time of 9pm, Materialize may choose
to execute a serializable query as of logical time 8:30pm, perhaps because data
for 8:30–9pm has not yet arrived. In this scenario, `now()` would return 9pm,
while `mz_now()` would return 8:30pm.

## Strict Serializable

Strict Serializable provides all the guarantees of Serializable isolation and
additionally guarantees
[linearizability](https://jepsen.io/consistency/models/linearizable). With
linearizability, the serial order matches the real-time order of the
transactions. For example, if transaction **T1** completes before transaction
**T2** begins in real time, the result is equivalent to a serial execution in
which **T1** executes before **T2**.

More concretely, suppose transaction **T1** queries table `t` and is followed in
real time by transaction **T2**, which queries a computationally expensive
materialized view `mv` defined over `t`. Under Strict Serializable, **T2** is
guaranteed to observe all rows visible to **T1**.

The linearizable guarantee applies only to transactions (including single-statement SQL queries, which are implicitly single-statement transactions), not to data written while ingesting from upstream sources.

- If a piece of data has been fully ingested from an upstream source, it is not
  guaranteed to appear in the next read transaction. See [real-time
  recency](#real-time-recency) for more details.

- However, once that data is included in the results of a read transaction, all
  subsequent read transactions are guaranteed to see it.

### Logical timestamp selection {#strict-serializable-logical-timestamp-selection}

When using the [strict
serializable](/reference/isolation-level#strict-serializable) isolation level,
Materialize attempts to keep the logical timestamp reasonably close to wall
clock time. In most cases, the logical timestamp of a query will be within a few
seconds of the wall clock time. For example, when executing a strict
serializable query at a wall clock time of 9pm, Materialize will choose a
logical timestamp within a few seconds of 9pm, even if data for 8:30–9pm has not
yet arrived and the query will need to block until the data for 9pm arrives. In
this scenario, both `now()` and `mz_now()` would return 9pm.

### Real-time recency

Materialize offers a form of "end-to-end linearizability" known as real-time
recency. When using real-time recency, all client-issued `SELECT` statements
include at least all data visible to Materialize in any external source (i.e.,
sources created with `CREATE SOURCE` that use `CONNECTION`s, such as Kafka,
MySQL, and PostgreSQL sources) after Materialize receives the query. This is
what we mean by linearizable––the results are guaranteed to contain all visible
data according to physical time.

For example, real-time recency ensures that if you have just performed an
`INSERT` into a PostgreSQL database that Materialize ingests as a source, all of
your real-time recency queries will include the just-written data in their
results.

Note that real-time recency only guarantees that the results will contain _at
least_ the data visible to Materialize when we receive the query. We cannot
guarantee that the results will contain _only_ the data visible when Materialize
receives the query. For instance, the rate at which Materialize ingests data
might include additional data made visible after the timestamp we determined to
be "real-time recent." Another example is that, due to network latency, the
timestamp from the external system that we determine to be "real-time recent"
might be later (i.e. include more data) than you expected.

Because Materialize waits until it ingests the data from the external system,
real-time recency queries can have additional latency. This latency is
introduced by both the time it takes us to ingest and commit data from the
source and the time spent communicating with it to determine what data it has
made available to us (e.g., querying PostgreSQL for the replication slot's LSN).

**Details**

-   Real-time recency is only available with sessions running at the [strict
    serializable isolation level](#strict-serializable).
-   Enable this feature per session using `SET real_time_recency = true`.
-   Control the timeout for connecting to the external source to determine the
    timestamp with the `real_time_recency_timeout` session variable.
-   Real-time recency queries only guarantee visibility of data from external
    systems (e.g., sources like Kafka, MySQL, and PostgreSQL). Real-time recency
    queries do not offer any form of guarantee when querying Materialize-local
    objects, such as [`LOAD GENERATOR`](/sql/create-source/load-generator/)
    sources or system tables.
-   Each real-time recency query connects to each external source transitively
    referenced in the query. The more external sources that are referenced, the
    greater the likelihood of latency caused by the network or ingestion rates.
-   Materialize doesn't currently offer a mechanism to provide a "lower bound"
    on the data we consider to be "real-time recent" in an external source.
    Real-time recency queries return at least all data visible to Materialize
    when our client connection communicates with the external system.

## Isolation levels and query latency

Strict Serializable provides stronger consistency guarantees but may have slower
reads than Serializable.

- **Strict Serializable** (the default) may need to wait for recent writes to
  propagate through materialized views and indexes before serving a read, so
  that the read reflects the real-time order of transactions.

  - [Real-time recency](#real-time-recency) (available only with Strict
    Serializable) introduces additional latency, since Materialize waits to
    determine and ingest the latest data available in upstream sources before
    serving the query.

- **Serializable** does not wait for writes to propagate. It reads a consistent
  (but possibly slightly stale) snapshot, which avoids that latency at the cost
  of linearizability. However, if a consistent snapshot is not available, the
  query blocks until one becomes available.

## Setting isolation level

> **Tip:** Materialize recommends starting with the default Strict Serializable isolation
> level.

You can set the isolation level using the session-level [configuration parameter
`TRANSACTION_ISOLATION`](/sql/set/); for example:

```mzsql
SET TRANSACTION_ISOLATION TO 'STRICT SERIALIZABLE';
```

You can also set the isolation level for an explicit transaction block as part
of the [`BEGIN` statement](/sql/begin); for example:

```mzsql
BEGIN ISOLATION LEVEL STRICT SERIALIZABLE;
--- ...
--- ...
--- ...
COMMIT;
```

## Learn more

Check out:

-   [PostgreSQL documentation](https://www.postgresql.org/docs/current/transaction-iso.html) for more information on
    isolation levels.
-   [Jepsen Consistency Models documentation](https://jepsen.io/consistency) for more information on consistency models.

---

## M.1 to cc size mapping

The following table provides a general mapping between cc and M.1 cluster sizes:

**cc to M.1:**

| cc Size | M.1 Size |
| --- | --- |
| <strong>25cc</strong> | M.1-nano |
| <strong>50cc</strong> | M.1-nano |
| <strong>100cc</strong> | M.1-micro |
| <strong>200cc</strong> | M.1-xsmall |
| <strong>300cc</strong> | M.1-small |
| <strong>400cc</strong> | M.1-small |
| <strong>600cc</strong> | M.1-medium |
| <strong>800cc</strong> | M.1-large or M.1-medium |
| <strong>1200cc</strong> | M.1-1.5xlarge |
| <strong>1600cc</strong> | M.1-2xlarge or M.1-1.5xlarge |
| <strong>3200cc</strong> | M.1-8xlarge or M.1-4xlarge or M.1-3xlarge |
| <strong>6400cc</strong> | M.1-16xlarge |
| <strong>128C</strong> | M.1-32xlarge |
| <strong>256C</strong> | M.1-64xlarge |
| <strong>512C</strong> | M.1-128xlarge |

**M.1 to cc:**

| M.1 Size | cc Size |
| --- | --- |
| M.1-nano | <strong>25cc</strong> |
| M.1-nano | <strong>50cc</strong> |
| M.1-micro | <strong>100cc</strong> |
| M.1-xsmall | <strong>200cc</strong> |
| M.1-small | <strong>300cc or 400cc</strong> |
| M.1-medium | <strong>600cc or 800cc</strong> |
| M.1-large | <strong>800cc</strong> |
| M.1-1.5xlarge | <strong>1200cc or 1600cc</strong> |
| M.1-2xlarge | <strong>1600cc</strong> |
| M.1-3xlarge | <strong>3200cc</strong> |
| M.1-4xlarge | <strong>3200cc</strong> |
| M.1-8xlarge | <strong>3200cc</strong> |
| M.1-16xlarge | <strong>6400cc</strong> |
| M.1-32xlarge | <strong>128C</strong> |
| M.1-64xlarge | <strong>256C</strong> |
| M.1-128xlarge | <strong>512C</strong> |

Some sizes have multiple mappings. When converting between cc and M.1 sizing, we
recommend choosing the larger mapping size first.

---

## System catalog

Materialize exposes a system catalog that contains metadata about the running
Materialize instance.

The system catalog consists of several schemas that are implicitly available in
all databases. These schemas contain sources, tables, and views that expose
different types of metadata.

  * [`mz_catalog`](mz_catalog), which exposes metadata in Materialize's
    native format.

  * [`pg_catalog`](pg_catalog), which presents the data in `mz_catalog` in
    the format used by PostgreSQL.

  * [`information_schema`](information_schema), which presents the data in
    `mz_catalog` in the format used by the SQL standard's information_schema.

  * [`mz_internal`](mz_internal), which exposes internal metadata about
    Materialize in an unstable format that is likely to change.

  * [`mz_introspection`](mz_introspection), which contains replica
    introspection relations.

These schemas contain sources, tables, and views that expose metadata like:

  * Descriptions of each database, schema, source, table, view, sink, and
    index in the system.

  * Descriptions of all running dataflows.

  * Metrics about dataflow execution.

Whenever possible, applications should prefer to query `mz_catalog` over
`pg_catalog`. The mapping between Materialize concepts and PostgreSQL concepts
is not one-to-one, and so the data in `pg_catalog` cannot accurately represent
the particulars of Materialize.

---

## System clusters

## Overview

When you enable a Materialize region, various [system
clusters](/sql/system-clusters/) are pre-installed to improve the user
experience as well as support system administration tasks.

### `quickstart` cluster

A cluster named `quickstart` with a size of `25cc` and a replication factor of
`1` will be pre-installed in every environment. You can modify or drop this
cluster at any time.

> **Note:** The default value for the `cluster` session parameter is `quickstart`.
> This cluster functions as a default option, pre-created for your convenience.
> It allows you to quickly start running queries without needing to configure a cluster first.
> If the `quickstart` cluster is dropped, you must run [`SET cluster`](/sql/select/#ad-hoc-queries)
> to choose a valid cluster in order to run `SELECT` queries. A _superuser_ (i.e. `Organization Admin`)
> can also run [`ALTER SYSTEM SET cluster`](/sql/alter-system-set) to change the
> default value.

### `mz_catalog_server` system cluster

A system cluster named `mz_catalog_server` will be pre-installed in every
environment. This cluster has several indexes installed to speed up `SHOW`
commands and queries using the system catalog.

To take advantage of these indexes, Materialize will automatically re-route
`SHOW` commands and queries using system catalog objects to the
`mz_catalog_server` system cluster. You can disable this behavior in
your session via the `auto_route_catalog_queries`
[configuration parameter](/sql/show/#other-configuration-parameters).

The following characteristics apply to the `mz_catalog_server` cluster:

  * You are **not billed** for this cluster.
  * You cannot create objects in this cluster.
  * You cannot drop this cluster.
  * You can run `SELECT` or `SUBSCRIBE` queries in this cluster as long
    as you only reference objects in the [system catalog](/reference/system-catalog/).

### `mz_probe` system cluster

A system cluster named `mz_probe` will be pre-installed in every environment.
This cluster is used for internal uptime monitoring.

The following characteristics apply to the `mz_probe` cluster:

  * You are **not billed** for this cluster.
  * You cannot create objects in this cluster.
  * You cannot drop this cluster.
  * You cannot run `SELECT` or `SUBSCRIBE` queries in this cluster.

### `mz_support` system cluster

A system cluster named `mz_support` will be pre-installed in every environment.
This cluster is used for internal support tasks.

The following characteristics apply to the `mz_support` cluster:

  * You are **not billed** for this cluster.
  * You cannot create objects in this cluster.
  * You cannot drop this cluster.
  * You cannot run `SELECT` or `SUBSCRIBE` queries in this cluster.

### `mz_system` system cluster

A system cluster named `mz_system` will be pre-installed in every environment.
This cluster is used for internal system jobs.

The following characteristics apply to the `mz_system` cluster:

  * You are **not billed** for this cluster.
  * You cannot create objects in this cluster.
  * You cannot drop this cluster.
  * You cannot run `SELECT` or `SUBSCRIBE` queries in this cluster.

## Related pages

- [`CREATE CLUSTER`](/sql/create-cluster)
- [`SHOW CLUSTER`](/sql/show-clusters)
- [`DROP CLUSTER`](/sql/drop-cluster)

