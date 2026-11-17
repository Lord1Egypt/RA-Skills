# Literature — the basis for each phase

**Verify every citation (authors, year, venue) before quoting it in a deck.** These lists were
assembled from memory, not from a library search; a wrong citation in a pricing
deck costs more than a missing one.

## Market (phase 2)

| Reference | Use |
|---|---|
| Rosen, S. (1974). *Hedonic prices and implicit markets.* Journal of Political Economy 82(1). | The model: price as a function of a product's characteristics; coefficients are implicit prices of features. |
| Griliches, Z. (1961). *Hedonic price indexes for automobiles.* NBER. | Log-price specification; quality adjustment. |
| Triplett, J. (2006). *Handbook on Hedonic Indexes and Quality Adjustments in Price Indexes.* OECD. | Practical specification choices: functional form, dummies, fixed effects, diagnostics. |
| Tibshirani, R. (1996). *Regression shrinkage and selection via the lasso.* JRSS-B. · Zou, H. & Hastie, T. (2005). *Elastic net.* JRSS-B. | Feature selection when features ≫ well-identified effects and are correlated. |
| Belloni, A., Chernozhukov, V. & Hansen, C. (2014). *Inference on treatment effects after selection among high-dimensional controls.* REStud. | Post-double-selection: honest confidence intervals for OUR feature coefficients after lasso. |
| Ghose, A. & Han, S. P. (2014). *Estimating demand for mobile applications in the new economy.* Management Science. | Empirical precedent: app characteristics → price/demand in an app marketplace. |
| Heckman, J. (1979). *Sample selection bias as a specification error.* Econometrica 47(1). | Most standalone vendors publish no price; a priced sample is selected. Model the selection, or at least report the visibility share per tier and cluster. |
| Cragg, J. (1971). *Some statistical models for limited dependent variables.* Econometrica. | Two-part / hurdle models: free-only and quote-only states before the price equation. |
| Nagle, Müller & Gruyaert (2018), ch. on price structure. | Why SaaS plans scale on a value metric (connectors, seats, spend), which fixes the reference-price rule at segment reference volumes. |

**The assumption phase 2 rests on, stated in every output:** listed prices reflect delivered value.
They don't fully: prices are set strategically, markets are out of equilibrium, only surviving listed
products are observed, and published prices skew to the self-serve end (quote-only vendors are a sales
motion, not a missing value). Treat the result as a market reference, not as value.

## Cost (phase 5)

| Reference | Use |
|---|---|
| Kaplan, R. & Anderson, S. (2004). *Time-driven activity-based costing.* HBR. | Allocating shared/fixed platform cost to clients by driver, not evenly. |
| Nagle, T., Müller, G. & Gruyaert, E. (2018). *The Strategy and Tactics of Pricing*, 6th ed. | Why cost is a **floor**, never the price; incremental vs average cost. |

## Value (phase 3)

| Reference | Use |
|---|---|
| Forbis, J. & Mehta, N. (1981). *Value-based strategies for industrial products.* Business Horizons. | Economic Value to the Customer (EVC) = reference alternative + differentiation value. |
| Nagle, Müller & Gruyaert (2018), chs. on value creation/communication. | Value-capture share; price fences; segment by value driver. |
| Breidert, C., Hahsler, M. & Reutterer, T. (2006). *A review of methods for measuring willingness-to-pay.* Innovative Marketing. | Where simulated value sits among WTP methods; what it can't replace. |
| Saltelli, A. et al. (2008). *Global Sensitivity Analysis: The Primer.* Wiley. | Which assumptions (action rate, capture share) drive the value ceiling. |
| Shapley, L. (1953). *A value for n-person games.* · Castro, J., Gómez, D. & Tejada, J. (2009). *Polynomial calculation of the Shapley value based on sampling.* Computers & OR. | Fair split of total delivered value across interacting features; permutation sampling. |

## Panel (phase 4b): the academic setup

| Reference | Use |
|---|---|
| Green, P. & Srinivasan, V. (1978, 1990). *Conjoint analysis in consumer research / in marketing.* JCR; J. Marketing. | Why conjoint, and the design choices (attributes, levels, tasks). |
| Louviere, J. & Woodworth, G. (1983). *Design and analysis of simulated consumer choice or allocation experiments.* JMR. | Choice-based conjoint as the primary instrument. |
| Huber, J. & Zwerina, K. (1996). *The importance of utility balance in efficient choice designs.* JMR. · Kuhfeld, W. (2010). *Marketing Research Methods in SAS.* | D-efficient designs; report D-error; balanced overlap. |
| Allenby, G. & Rossi, P. (1998); Rossi, Allenby & McCulloch (2005). *Bayesian Statistics and Marketing.* | Hierarchical Bayes multinomial logit for individual part-worths from few tasks. |
| Train, K. (2009). *Discrete Choice Methods with Simulation.* | Mixed logit; WTP as the ratio of part-worth to price coefficient; simulation. |
| Sonnier, G., Ainslie, A. & Otter, T. (2007). *Heterogeneity distributions of willingness-to-pay in choice models.* QME. | WTP-space vs preference-space; report both. |
| Miller, K., Hofstetter, R., Krohmer, H. & Zhang, Z. J. (2011). *How should consumers' willingness to pay be measured?* JMR. | Hypothetical vs incentive-aligned methods; why stated maxima overstate. |
| Ding, M. (2007). *An incentive-aligned mechanism for conjoint analysis.* JMR. · Becker, DeGroot & Marschak (1964). · Wertenbroch, K. & Skiera, B. (2002). *Measuring consumers' WTP at the point of purchase.* JMR. | Incentive-compatible framing; the real-buyer validation after synthesis. |
| Van Westendorp (1976); Gabor & Granger (1966). | Secondary instruments on the configured product; PSM points and the demand curve. |
| Tversky & Kahneman (1974). | The anchor arms: report the gap, never average it away. |
| Saltelli et al. (2008). | Sobol indices on action rate, realisation, capture share, archetype weights. |

## Silicon samples: validity

| Reference | Use |
|---|---|
| Argyle et al. (2023). *Out of one, many.* Political Analysis. | Conditioning synthetic respondents on real population attributes (sampled rows of the buyer frame, never invented personas). |
| Horton (2023). NBER WP 31122. | Homo silicus: what simulated agents can and cannot tell you. |
| Brand, Israeli & Ngwe (2023). HBS WP 23-062. | Direction right, level biased; the benchmark to replicate for level-bias calibration. |
| Aher, G., Arriaga, R. & Kalai, A. (2023). *Using large language models to simulate multiple humans and replicate human subject studies.* ICML. | Turing-experiment framing; one respondent per call. |
| Gui, G. & Toubia, O. (2023). *The challenge of using LLMs to simulate human behavior: a causal inference perspective.* | Confounding when a prompt changes more than the manipulated attribute; vary one thing per arm. |
| Goli, A. & Singh, A. (2024). *Frontiers: Can LLMs capture human preferences?* Marketing Science. | Known failure modes of simulated preferences; the reason for paraphrase arms and holdouts. |
| Santurkar et al. (2023). *Whose opinions do language models reflect?* ICML. | Representativeness of a default LLM persona; why conditioning on strata matters. |
| Li, P., Castelo, N., Katona, Z. & Sarvary, M. (2024). *Frontiers: Determining the validity of LLMs for automated perceptual analysis.* Marketing Science. | Validation procedure shape: compare against a human benchmark before use. |

## Council (phase 4a)

| Reference | Use |
|---|---|
| Dalkey, N. & Helmer, O. (1963). *An experimental application of the Delphi method to the use of experts.* Management Science. | Blind first round, collated feedback, a revision round; why two rounds and stop. |
| Ramanujam, M. & Tacke, G. (2016). *Monetizing Innovation.* Wiley. | Willingness-to-pay conversations early; segment by needs; leaders, fillers, killers. |

## Packaging and synthesis (phase 6)

| Reference | Use |
|---|---|
| Shapiro, C. & Varian, H. (1998). *Versioning: the smart way to sell information.* HBR; *Information Rules* (1999). | Tiering information goods by a dimension high-value users care about. |
| Adams, W. & Yellen, J. (1976). *Commodity bundling and the burden of monopoly.* QJE. · Bakos, Y. & Brynjolfsson, E. (1999). *Bundling information goods.* Management Science. | Bundle vs unbundle; why bundling zero-marginal-cost features raises capture. |
| Simonson, I. (1989). *Choice based on reasons: the case of attraction and compromise effects.* JCR. · Huber, J., Payne, J. & Puto, C. (1982). *Adding asymmetrically dominated alternatives.* JCR. | Middle-tier anchoring; decoy tiers. Also why the market phase reads the recommended tier. |
| Mohammed, R. (2018). *The good-better-best approach to pricing.* HBR. | Three-tier structure in practice. |
| Shampanier, K., Mazar, N. & Ariely, D. (2007). *Zero as a special price.* Marketing Science. | Free tier / trial effects (the app has `trial_days`). |
| Van Westendorp, P. (1976). Price Sensitivity Meter. · Gabor, A. & Granger, C. (1966). | Secondary panel instruments; the real-buyer validation (phase 7). |
