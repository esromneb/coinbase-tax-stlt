# Coinbase Tax Short Term Long Term calculator
Coinbase gives out a "gain/loss" PDF, and CSV. This CSV is named `Coinbase-2022-CB-GAINLOSSCSV_.csv`

# Purpose
This PDF is lacking the correct summary. It gives net gains (proceeds-cost), but it does NOT give `proceeds` or `costs`.

# Solution
This code parses through and gives:
* `short term cost basis`
* `short term proceeds`
* `long term cost basis`
* `long term proceeds`

# Usage
```bash
mkdir input
# put the input file here named Coinbase-2022-CB-GAINLOSSCSV_.csv
make # run make
# output is written to output.csv
```
