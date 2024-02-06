# CS-Options
Code Samples of Option Pricing Models, Greeks computations, Monte Carlo simulations, etc

### Descriptions of the files:

BMS.py - This is a file that contains analytical computations for option prices and Greeks based  under the Black Merton Scholes model.

Asian Option Variance Reduction - This is a notebook that explores pricing an asian option using several variance reduction techniques. It is priced using standard Monte Carlo simulation, Antithetic Variates, Terminal stratification (proportional), post stratification, and latin hypercube sampling. Explanations of each variance reduction technique is provided and a comparison of results follows.

Barrier Options with Control Variates: This notebook shows how to simulate the price of barrier options, and uses control variates as a variance reduction technique. Three separate variates are used, and I analyze which variate performs best.

Conditional MC example: This is a short notebook showing how to use conditional monte carlo simulation. Conditional MC involves partially simulating and then using analytical formulae to compute results. It is a technique that cannot always be used.

Correlated Underlyings Options: This notebook simulates brownian motions with correlations, and showcases how different correlations result in different payoffs for spread options, basket options, and outperformance options.

Finite Differences: This notebook shows how to use finite difference method to price American style options.

Greeks Sensitivites CRN: This notebook computes option greeks (delta, gamma, vega) using standard monte carlo, common random numbers, pathwise estimation, and likelihood ratio method.

Importance Sampling: This notebook shows how importance sampling can lead to more accurate results for extreme events, and can provide a general decrease in variance when estimating values.
