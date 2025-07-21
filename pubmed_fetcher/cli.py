import typer
import pandas as pd
from pubmed_fetcher.api import fetch_pubmed_ids, fetch_pubmed_details
from pubmed_fetcher.parser import parse_pubmed_xml

app = typer.Typer(help="Fetch PubMed research papers with non-academic authors.")

@app.command()
def main(
    query: str,
    file: str = typer.Option(None, "-f", "--file", help="Filename to save CSV output."),
    debug: bool = typer.Option(False, "-d", "--debug", help="Enable debug mode."),
):
    try:
        if debug:
            typer.echo(f"[DEBUG] Fetching PubMed IDs for query: {query}")

        pmids = fetch_pubmed_ids(query)
        if not pmids:
            typer.echo("No papers found.")
            raise typer.Exit()

        if debug:
            typer.echo(f"[DEBUG] Found {len(pmids)} PMIDs: {pmids}")

        xml_data = fetch_pubmed_details(pmids)
        articles = parse_pubmed_xml(xml_data)

        if not articles:
            typer.echo("No non-academic authors found.")
            raise typer.Exit()

        df = pd.DataFrame(articles)
        if file:
            df.to_csv(file, index=False)
            typer.echo(f"✅ Results saved to {file}")
        else:
            typer.echo(df.to_string(index=False))

    except Exception as e:
        typer.echo(f"❌ Error: {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
