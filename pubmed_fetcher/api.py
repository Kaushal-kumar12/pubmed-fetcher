import requests
from typing import List

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

def fetch_pubmed_ids(query: str, retmax: int = 20) -> List[str]:
    response = requests.get(
        f"{BASE_URL}/esearch.fcgi",
        params={
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": retmax
        }
    )
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_pubmed_details(pmids: List[str]) -> str:
    if not pmids:
        return ""
    
    response = requests.get(
        f"{BASE_URL}/efetch.fcgi",
        params={
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml"
        }
    )
    response.raise_for_status()
    return response.text
