""" This is the primary API for this package; most users need to access the methods in this file. """
from .validate import is_cusip, is_isin, is_aba, is_sedol
from .utils import find_and_validate
from typing import List, Dict, 


def get_cusips(s: str) -> List[str]:
    """
    ---------------------------------
    Find and Extract CUSIPs from text
    ---------------------------------
    CUSIP Format:
        > Numeric or Alphanumeric
        > First 6 characters identify the issuer and is called Issuer Code or CUSIP-6
            - The last 3 characters of Issuer Code can be letters
        > 7th and 8th characters identify the exact issue
            - General rule: Numbers for equities and Letters for Fixed Income
            - The letters I and O are not used to avoid confusion with 1 and 0
        > 9th digit is a checksum
    Reference:
        https://www.cusip.com/pdf/CUSIP_Intro_03.14.11.pdf
        https://en.wikipedia.org/wiki/CUSIP
    ------
    PARAMS
    ------
        1. 's' -> input string
    """
    #ensure 9th is digit
    pattern = r"((?<=[^\w])|(?<=^))([A-Za-z0-9]{8}[0-9])(?=[^\w]|$)"
    return find_and_validate(s, pattern, validation_fn=is_cusip)


def get_isins(s: str) -> List[str]:
    """
    ---------------------------------
    Find and Extract ISINs from text
    ---------------------------------
    ISIN Format:
        > First two characters are letters and represent country code
            - Country codes are defined in ISO 3166-1 alpha-2 (https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
        > The following 9 characeters are alphanumeric
            - These 9 characters are the NSIN (https://en.wikipedia.org/wiki/National_Securities_Identifying_Number)
            - Zero-padded if NSIN is less than 9 characters
        > The 12th and last digit is a check digit
    Reference:
        https://en.wikipedia.org/wiki/International_Securities_Identification_Number
    ------
    PARAMS
    ------
        1. 's' -> input string
    """
    pattern = r"((?<=[^\w])|(?<=^))([A-Za-z]{2}[A-Za-z0-9]{9}[0-9])(?=[^\w]|$)"
    return find_and_validate(s, pattern, validation_fn=is_isin)


def get_sedols(s: str) -> List[str]:
    """
    ---------------------------------
    Find and Extract SEDOLs from text
    ---------------------------------
    SEDOL Format:
        - 6 alphanumeric characters and 1 checkdigit
        - Vowels are never used
    Reference:
        https://en.wikipedia.org/wiki/SEDOL
    ------
    PARAMS
    ------
        1. 's' -> input string
    """
    pattern = r"((?<=[^\w])|(?<=^))([0-9BCDFGHJKLMNPQRSTVWXYZ]{6}[0-9])(?=[^\w]|$)"
    return find_and_validate(s, pattern, validation_fn=is_sedol)


def find_securities(s: str, include: List = ["CUSIP", "ISIN", "SEDOL"]) -> Dict:
    allowed_types = {
        "CUSIP": get_cusips, 
        "ISIN": get_isins, 
        "SEDOL": get_sedols
        }
    # ensure that the allowed security measures are correct
    include = [x.upper() for x in include if x.upper() in allowed_types]
    assert len(include) > 0, "Must include at least one of the following: CUSIP, ISIN, or SEDOL"
    return {t: allowed_types[t](s) for t in include}


def get_abas(s: str) -> List[str]:
    """
    --------------------------------------
    Find and Extract ABA Numbers from text
    --------------------------------------
    ABA Format:
        > 9 digits 
        > XXXXYYYYC
            - XXXX = Federal Reserve Routing Symbol
            - YYYY = ABA Institution Identifier
            - C = Check Digit
        > The first two digits of the nine digit RTN must be in the ranges:
            - 00 - 12 
            - 21 - 32 
            - 61 - 72
            - 80
    Reference:
        https://en.wikipedia.org/wiki/ABA_routing_transit_number
    ------
    PARAMS
    ------
        1. 's' -> input string
    """
    pattern = r"((?<=[^\w])|(?<=^))(\d{9})(?=[^\w]|$)"
    return find_and_validate(s, pattern, validation_fn=is_aba)


def process_substrings(s: str, include: List[str] = ["CUSIP", "ISIN", "SEDOL"]) -> Dict:
    """
    This method allows users to check that the substrings of the input string match the various
    types of identifiers. 

    Args:
        s (str): The string to process to see if a slice of it is a valid cusip, isin or sedol string.
        include (list): The name of the validation checks. Should be one of CUSIP, ISIN or SEDOL

    Returns:
        dict. The key-value dictionary with each check paired with the set of matches for the check.
    """
    def _range(name: str) -> int:
        """ get the length of the expected strings. """
        return {"CUSIP": 8, "ISIN": 12, "SEDOL": 12}.get(name)
        
    allowed_types = Dict(
        CUSIP=get_cusips,
        ISIN=get_isins,
        SEDOL=get_sedols
    )
    
    # ensure that the allowed security measures are correct
    include = [x.upper() for x in include if x.upper() in allowed_types]
    assert len(include) > 0, "Must include at least one of the following: CUSIP, ISIN, or SEDOL"
    result = dict()
    
    # process each slice of the string
    for id_type, caller in allowed_types.items():
        for idx in _range(id_type):
            result[id_type] = result.get(id_type, []).extend(caller(s[idx:idx+_range(id_type)]))
    return result
    
    
def process_list(l: List[str], include: List[str] = ["CUSIP", "ISIN", "SEDOL"]) -> Dict:
    """
    This method allows users to check that the substrings of the input set of strings match the 
    various types of identifiers. 

    Args:
        l (list): The list of strings to process to see if a slice of it is a valid cusip, isin or sedol string.
        include (list): The name of the validation checks. Should be one of CUSIP, ISIN or SEDOL

    Returns:
        dict. The key-value dictionary with each check paired with the set of matches for the check.
    """
    p = process_substrings(l[0], include)
    for ell in l[1:]:
        p.update(process_substrings(ell, include))
    return p
    
