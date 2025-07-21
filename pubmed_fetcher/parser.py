from typing import List, Dict, Optional
import xml.etree.ElementTree as ET
import re

NON_ACADEMIC_KEYWORDS = ["pharma", "biotech", "inc", "ltd", "llc", "corporation", "company", "gmbh", "pvt"]
ACADEMIC_KEYWORDS = ["university", "institute", "college", "hospital", "school", "center", "centre"]

def extract_email(text: str) -> Optional[str]:
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None

def is_non_academic_affiliation(affiliation: str) -> bool:
    aff_lower = affiliation.lower()
    return any(k in aff_lower for k in NON_ACADEMIC_KEYWORDS)


def parse_pubmed_xml(xml_data: str) -> List[Dict[str, str]]:
    root = ET.fromstring(xml_data)
    articles = []

    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID") or "Unknown"
        title = article.findtext(".//ArticleTitle") or "No Title"
        pub_date = article.findtext(".//PubDate/Year") or "Unknown"

        non_academic_authors = []
        company_affiliations = []
        corresponding_email = ""

        for author in article.findall(".//Author"):
            fore_name = author.findtext("ForeName") or ""
            last_name = author.findtext("LastName") or ""
            full_name = f"{fore_name} {last_name}".strip()

            aff_info = author.find(".//AffiliationInfo")
            if aff_info is None:
                continue

            affiliation = aff_info.findtext("Affiliation") or ""

            if is_non_academic_affiliation(affiliation):
                non_academic_authors.append(full_name)
                company_affiliations.append(affiliation)

            if not corresponding_email:
                email = extract_email(affiliation)
                if email:
                    corresponding_email = email

        if non_academic_authors:
            articles.append({
                "PubmedID": pmid,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": "; ".join(non_academic_authors),
                "Company Affiliation(s)": "; ".join(company_affiliations),
                "Corresponding Author Email": corresponding_email
            })

    return articles
