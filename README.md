# Fincheck

### Utilities to work with financial security identifiers, accounts, and checkdigit algorithms

Provides the following:
1. Check digit algorithms for CUSIPs, ISINs, SEDOLs, and ABA numbers, as well as Luhn's algorithm
2. Extraction methods for finding cusips, isins, sedols, and aba numbers within text
3. Validation methods to check whether a string is a cusip, isin, sedol, or aba number
4. Descriptive object classes for CUSIPs

To install, simply use pip:
```
pip install fincheck
```

Validation Example Usage:
```
>>> from fincheck.validate import *
>>> is_isin("BD0716DELI01")
True
>>> is_cusip("30303M102")
True
>>> is_cusip("30303M103") #change last digit -- should be False
False
```

Extraction Example Usage:
```
>>> from fincheck.extract import *
>>> s = 'This is a test string that contains a cusip, incorrect cusip, isin, aba number, and a\
        sedol M0392N101 M0392N100 US9129091081 122235821 2007849 so we can demo\
        the extraction methods of fincheck.'
>>> get_cusips(s)
['M0392N101']
>>> get_isins(s)
['US9129091081']
>>> get_abas(s)
['122235821']
>>> get_sedols(s)
['2007849']
```

Check Digit Calculation Example:
```
>>> from fincheck.checksum import *
>>> true_isin = "US0231351067"
>>> incomplete_isin = true_isin[:-1] #US023135106
>>> isin_check_digit(incomplete_isin)
7

>>> true_cusip = "931142103"
>>> incomplete_cusip = true_cusip[:-1] #93114210
>>> cusip_check_digit(incomplete_cusip)
3

>>> true_sedol = "B7TL820"
>>> incomplete_sedol = true_sedol[:-1] #B7TL82
>>> sedol_check_digit(incomplete_sedol)
0
```

CUSIP Object Example Usage:
```
>>> from fincheck.data import Cusip
>>> x = Cusip("98986X109")
>>> x.is_valid
True
>>> x.id_
'98986X109'
>>> x.name_
'ZYNERBA PHARMACEUTICALS INC'
>>> x.type_
'COM'
>>> x.issue_
'10'
>>> x.issue_type_
'equity'
>>> x.issuer_
'98986X'
>>> x.to_isin(country="US")
'US98986X1090'

>>> from fincheck.validate import is_isin
>>> is_isin(x.to_isin(country="US"))
True
```
