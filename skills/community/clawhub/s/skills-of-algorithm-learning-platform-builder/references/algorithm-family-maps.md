# Algorithm Family Maps

This file defines reusable family-level patterns for algorithm teaching pages and algorithm learning platforms.

Its purpose is to help the skill quickly determine:
- what kind of algorithm the user is asking about
- what page structure fits that family
- which formulas must be explained
- which interactions are most useful
- which charts are most educational
- how to scale from a single page to a family comparison page

---

# Table of Contents

1. Purpose
2. General family classification rules
3. Multi-criteria decision-making algorithms
4. Classical machine learning algorithms
5. Optimization algorithms
6. Statistical and dimensionality-reduction algorithms
7. Clustering and unsupervised learning algorithms
8. Tree and ensemble algorithms
9. Time-series and forecasting algorithms
10. Graph and network algorithms
11. Numerical methods algorithms
12. Deep learning related algorithms
13. How to use this file

---

# 1. Purpose

When the user asks for an algorithm page, first map the request into an algorithm family.

This family mapping helps determine:
- what the page should emphasize
- what formulas are central
- what numerical substitution is necessary
- what visual interaction is most useful
- whether the request should become:
  - a single algorithm page
  - a comparison page
  - a reusable platform page

This file is not an exhaustive taxonomy of all algorithms.
It is a practical design map for teaching-page generation.

---

# 2. General Family Classification Rules

## 2.1 First decide whether the algorithm is mainly about:
- scoring or evaluation
- prediction
- classification
- optimization
- decomposition
- clustering
- iteration
- search
- approximation
- graph structure
- representation learning

## 2.2 Then identify the family

### Common family types
- multi-criteria decision-making
- classical supervised learning
- optimization
- statistical / dimensionality reduction
- clustering / unsupervised learning
- tree ensembles
- time-series / forecasting
- graph algorithms
- numerical methods
- deep learning

## 2.3 Then decide the page type

### Use a single algorithm page when:
- the user wants one algorithm explained deeply
- the workflow is already rich enough by itself
- the educational goal is understanding one method clearly

### Use a comparison page when:
- the user names two or more algorithms
- the user asks for advantages, differences, or “which is better”
- the family naturally contains closely related methods

### Use a reusable platform page when:
- the user wants a general tool for many algorithms
- the request mentions “platform”, “switch”, “toggle”, “generalize”, “for any algorithm”
- the user wants modular extension

---

# 3. Multi-Criteria Decision-Making Algorithms

Examples:
- AHP
- entropy weight method
- TOPSIS
- CRITIC
- fuzzy comprehensive evaluation
- grey relational analysis
- combination weighting
- VIKOR

## 3.1 Core teaching goal
Help the learner understand:
- how indicators are weighted
- how scores are computed
- how ranking is generated
- why one weighting or scoring formula is chosen over another

## 3.2 Best page type
- single algorithm page for one method
- comparison page for weighting-method comparisons
- platform page for “evaluation-method toolkit” requests

## 3.3 Must-explain formulas
Usually include:
- normalization formula
- weight calculation formula
- score / closeness / distance formula
- ranking formula
- consistency formula if relevant
- objective function if relevant

## 3.4 Must-show numerical substitution
Usually show:
- original matrix
- normalized matrix
- weight derivation
- score derivation
- ranking result

## 3.5 Useful interactions
- matrix editing
- indicator direction switching
- parameter sliders
- weighting method toggles
- ranking recomputation
- step navigation

## 3.6 Useful charts
- weight bar chart
- score bar chart
- radar chart
- sensitivity analysis chart
- rank comparison chart

## 3.7 Good comparison dimensions
- subjective vs objective weighting
- interpretability
- sensitivity to data
- suitability for small samples
- ranking stability

---

# 4. Classical Machine Learning Algorithms

Examples:
- linear regression
- logistic regression
- k-nearest neighbors
- naive bayes
- support vector machine
- decision tree

## 4.1 Core teaching goal
Help the learner understand:
- what prediction target is being learned
- what function or rule maps input to output
- how the model parameters or decision logic are obtained
- how predictions are made

## 4.2 Best page type
- single algorithm page for one learner-facing explanation
- comparison page for model comparison
- platform page for “classical ML study tool” requests

## 4.3 Must-explain formulas
Usually include:
- hypothesis / prediction function
- loss function or decision rule
- parameter update or fitting rule
- classification boundary or probability formula

## 4.4 Must-show numerical substitution
Usually show:
- one sample prediction
- one loss or score computation
- one update step if iterative
- one boundary or decision example

## 4.5 Useful interactions
- sample editing
- parameter sliders
- feature toggles
- task switching between regression and classification
- prediction buttons

## 4.6 Useful charts
- regression fit plot
- decision boundary plot
- probability curve
- confusion-style summary
- parameter sensitivity curve

## 4.7 Good comparison dimensions
- interpretability
- training cost
- nonlinear capability
- probability output
- robustness

---

# 5. Optimization Algorithms

Examples:
- gradient descent
- stochastic gradient descent
- Newton method
- simulated annealing
- genetic algorithm
- particle swarm optimization
- Lagrange multiplier methods

## 5.1 Core teaching goal
Help the learner understand:
- what objective is being minimized or maximized
- how the update rule moves the solution
- why convergence behavior changes with parameters
- how iteration affects results

## 5.2 Best page type
- single algorithm page for one optimization method
- comparison page for multiple optimizers
- platform page for “optimization visualizer” requests

## 5.3 Must-explain formulas
Usually include:
- objective function
- gradient or search direction
- update rule
- convergence criterion
- step-size rule if relevant

## 5.4 Must-show numerical substitution
Usually show:
- initial point
- first gradient
- first update
- later update comparison
- objective value change

## 5.5 Useful interactions
- learning rate slider
- iteration count
- initialization control
- optimizer switch
- convergence threshold control

## 5.6 Useful charts
- objective curve
- parameter trajectory
- contour path
- convergence comparison chart

## 5.7 Good comparison dimensions
- convergence speed
- stability
- sensitivity to initialization
- computational cost
- local vs global search

---

# 6. Statistical and Dimensionality-Reduction Algorithms

Examples:
- PCA
- factor analysis
- LDA
- ICA
- SVD-based methods

## 6.1 Core teaching goal
Help the learner understand:
- how high-dimensional information is transformed
- what variance, covariance, or projection means
- how components are extracted
- how much information is preserved

## 6.2 Best page type
- single algorithm page for PCA or FA
- comparison page for PCA vs FA vs LDA
- platform page for dimensionality reduction modules

## 6.3 Must-explain formulas
Usually include:
- covariance matrix
- eigenvalue / eigenvector relationship
- projection formula
- explained variance ratio
- loading matrix if relevant

## 6.4 Must-show numerical substitution
Usually show:
- input matrix
- covariance matrix
- eigenvalues
- selected components
- projected coordinates

## 6.5 Useful interactions
- number of components selector
- sample matrix editing
- standardized vs non-standardized toggle
- variance threshold slider

## 6.6 Useful charts
- scree plot
- explained variance bar chart
- projected scatter plot
- loading heatmap
- component contribution chart

## 6.7 Good comparison dimensions
- interpretability
- supervision or unsupervision
- dimensionality reduction quality
- variance explanation
- factor meaning

---

# 7. Clustering and Unsupervised Learning Algorithms

Examples:
- KMeans
- hierarchical clustering
- DBSCAN
- Gaussian mixture model
- spectral clustering

## 7.1 Core teaching goal
Help the learner understand:
- how samples are grouped
- how cluster centers or cluster rules are formed
- how the algorithm updates cluster assignments
- what parameters affect cluster quality

## 7.2 Best page type
- single algorithm page for one clustering method
- comparison page for clustering methods
- platform page for clustering visualizer requests

## 7.3 Must-explain formulas
Usually include:
- distance function
- objective function
- assignment rule
- update rule
- density condition if relevant

## 7.4 Must-show numerical substitution
Usually show:
- sample coordinates
- initial cluster state
- one reassignment step
- one centroid update
- final cluster grouping

## 7.5 Useful interactions
- cluster count slider
- epsilon / minPts controls
- initialization switch
- dataset selector

## 7.6 Useful charts
- scatter plot
- centroid movement plot
- cluster comparison chart
- silhouette or compactness summary

## 7.7 Good comparison dimensions
- need for predefined cluster count
- sensitivity to noise
- shape flexibility
- scalability
- interpretability

---

# 8. Tree and Ensemble Algorithms

Examples:
- decision tree
- random forest
- GBDT
- XGBoost
- LightGBM
- AdaBoost

## 8.1 Core teaching goal
Help the learner understand:
- how tree structure is built
- how split criteria are chosen
- how ensemble methods combine weak learners
- how different boosting or bagging methods differ

## 8.2 Best page type
- single algorithm page for one tree algorithm
- comparison page for tree-family comparison
- platform page for tree-learning platform requests

## 8.3 Must-explain formulas
Usually include:
- split criterion
- impurity or gain formula
- update rule for boosting
- weighting rule
- regularization terms for advanced boosting

## 8.4 Must-show numerical substitution
Usually show:
- first split
- leaf value calculation
- one iteration update
- final prediction calculation

## 8.5 Useful interactions
- depth control
- tree count control
- learning rate slider
- algorithm switch
- task switch
- iteration stepper

## 8.6 Useful charts
- loss curve
- prediction comparison chart
- residual chart
- feature importance chart
- split gain chart
- multi-model comparison chart

## 8.7 Good comparison dimensions
- one-stage vs iterative learning
- first-order vs second-order optimization
- regularization
- engineering speed
- interpretability

---

# 9. Time-Series and Forecasting Algorithms

Examples:
- moving average
- exponential smoothing
- ARIMA
- Holt-Winters
- simple forecasting baselines

## 9.1 Core teaching goal
Help the learner understand:
- what the algorithm assumes about temporal dependence
- how the forecast is updated over time
- how trend and seasonality are handled
- how future values are generated

## 9.2 Best page type
- single algorithm page for a forecasting method
- comparison page for forecasting methods
- platform page for time-series learning tools

## 9.3 Must-explain formulas
Usually include:
- forecast update formula
- smoothing formula
- trend or seasonal update if relevant
- error measure

## 9.4 Must-show numerical substitution
Usually show:
- a short time series
- one forecast step
- one update step
- error calculation

## 9.5 Useful interactions
- smoothing parameter slider
- forecast horizon control
- seasonality toggle
- model switch

## 9.6 Useful charts
- time-series line chart
- forecast vs actual chart
- residual chart
- rolling error chart

## 9.7 Good comparison dimensions
- interpretability
- trend handling
- seasonality handling
- data requirement
- forecasting horizon suitability

---

# 10. Graph and Network Algorithms

Examples:
- shortest path
- PageRank
- minimum spanning tree
- max flow
- graph traversal
- community detection basics

## 10.1 Core teaching goal
Help the learner understand:
- what structure the algorithm operates on
- how updates travel through the graph
- how node or edge values are computed
- how the final graph-level or node-level result is determined

## 10.2 Best page type
- single algorithm page for one graph method
- comparison page for related graph methods
- platform page for graph algorithm visualizer requests

## 10.3 Must-explain formulas
Usually include:
- update or propagation rule
- path cost formula
- centrality or score update formula
- stopping condition

## 10.4 Must-show numerical substitution
Usually show:
- a small graph
- one iteration or traversal step
- one cost or score update
- final result

## 10.5 Useful interactions
- edge editing
- node weight editing
- source/target selection
- step traversal buttons

## 10.6 Useful charts
- graph visualization
- cost evolution chart
- node score chart
- path summary table

## 10.7 Good comparison dimensions
- exactness
- efficiency
- static vs dynamic graph suitability
- weighted vs unweighted applicability

---

# 11. Numerical Methods Algorithms

Examples:
- Newton interpolation
- Lagrange interpolation
- least squares approximation
- best approximation
- numerical integration
- root-finding methods

## 11.1 Core teaching goal
Help the learner understand:
- what numerical problem is being solved
- how approximations are constructed
- how formulas are built from known points
- how error behaves

## 11.2 Best page type
- single algorithm page for one numerical method
- comparison page for related numerical methods
- platform page for numerical methods teaching toolkit

## 11.3 Must-explain formulas
Usually include:
- interpolation or approximation formula
- basis function definition
- update or recursive form
- error term if appropriate

## 11.4 Must-show numerical substitution
Usually show:
- sample points
- basis construction
- one interpolated value
- one error comparison

## 11.5 Useful interactions
- point editing
- polynomial degree selector
- function selector
- error chart toggle

## 11.6 Useful charts
- curve plot
- interpolation vs true function chart
- error curve
- node distribution chart

## 11.7 Good comparison dimensions
- stability
- approximation quality
- error sensitivity
- computational complexity
- interpretability

---

# 12. Deep Learning Related Algorithms

Examples:
- perceptron
- backpropagation demo
- simple neural network
- attention basics
- convolution basics

## 12.1 Core teaching goal
Help the learner understand:
- layered transformation
- forward computation
- loss computation
- gradient-based update
- role of parameters

## 12.2 Best page type
- single algorithm page for one concept
- comparison page for architecture comparison
- platform page for neural network teaching tool requests

## 12.3 Must-explain formulas
Usually include:
- forward pass
- activation function
- loss function
- gradient or update rule

## 12.4 Must-show numerical substitution
Usually show:
- one forward pass
- one loss value
- one gradient example
- one parameter update

## 12.5 Useful interactions
- weight editing
- learning rate slider
- epoch slider
- architecture toggle
- activation selector

## 12.6 Useful charts
- loss curve
- activation curve
- parameter update chart
- prediction comparison chart

## 12.7 Good comparison dimensions
- expressiveness
- interpretability
- training cost
- data requirement
- optimization difficulty

---

# 13. How to Use This File

When a new user request arrives:

1. identify the algorithm family
2. choose the corresponding teaching pattern
3. choose the page type
4. determine the formulas that must be explained
5. determine the numerical substitutions that must appear
6. determine the interactions that are actually useful
7. determine the charts that best fit that family

This file should guide structure and emphasis.
It should not force every page into the same exact visual output.

The main goal is:
- preserve educational clarity
- preserve family-specific teaching logic
- make the generated page feel natural for that algorithm family