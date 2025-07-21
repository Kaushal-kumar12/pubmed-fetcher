# PubMed Fetcher 🧪

This is a Python CLI tool that fetches research papers from PubMed with at least one **non-academic author** affiliated with **pharmaceutical or biotech companies**.

## 🔧 Features

- Accepts flexible PubMed search queries
- Fetches live paper metadata via PubMed API
- Filters authors using affiliation heuristics (e.g., "inc", "biotech", etc.)
- Outputs to CSV or prints to console
- Debug mode for tracing flow

## 📦 Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/pubmed-fetcher.git
cd pubmed-fetcher

## Usage
1. python run.py "your pubmed query here" --file results.csv --debug
2. python run.py "cancer immunotherapy" --file output.csv --debug
