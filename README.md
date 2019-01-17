# Monte-Carlo Hypothesis Test
This is a simple Python script that provides an Monte Carlo statistical test for independence in contingency tables. This hypothesis test should not have problems with tables containing zeros or low count cells, unlike most asymptotic tests (e.g. Pearson's chi-squared and standard G-test).
## Algorithm
The algorithm consists of the following steps:
 - Calculate mutual information `MI` for the input table;
 - Assuming fixed margins, sample `n=1E6` tables from null-hypothesis distribution;
 - Count the number `r` of tables with mutual information superior to`MI`;
 - Estimate p-value as `(r+1)/(n+1)` (Monte Carlo).
## Pros and Cons
The main advantages of this script are:
 - The test statistic used is mutual information (similar to G-test), which is optimal in the sense of Neyman–Pearson lemma.
 - The Monte Carlo method avoids the usage of asymptotic assumptions, which causes problems when dealing with small samples.

The main disadvantages are:
 - The script is significantly slower than standard asymptotic tests.
 - The calculated p-value is not exact (unlike Fisher's exact test), but an estimate. [Sampling more tables on the Monte Carlo step can ameliorate this issue.]

## Usage
The program receives a contingency table as a tab-separated file, in this syntax:

    python3 ExactTest.py file.txt

By default, this will output the p-value for the independence hypothesis. If you want to output also the mutual information of your data, add `-kl` to this syntax. For verbose output, you can add `-v` to this syntax.
