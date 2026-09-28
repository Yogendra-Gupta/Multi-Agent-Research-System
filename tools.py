import os
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise RuntimeError(
        "TAVILY_API_KEY is missing. Add it to your .env file. "
        "Example: TAVILY_API_KEY=your_key_here"
    )

tavily = TavilyClient(api_key=TAVILY_API_KEY)


@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information. Returns titles, URLs and snippets."""
    query = (query or "").strip()
    if not query:
        return "Search query is empty."

    try:
        response = tavily.search(
            query=query,
            max_results=5,
            search_depth="advanced",
        )
    except Exception as exc:
        return f"Web search failed: {type(exc).__name__}: {exc}"

    results = response.get("results", [])
    if not results:
        return "No search results were returned."

    output = []
    for item in results:
        title = item.get("title", "Untitled")
        url = item.get("url", "")
        content = item.get("content", "")
        output.append(
            f"Title: {title}\n"
            f"URL: {url}\n"
            f"Snippet: {content[:500]}"
        )

    return "\n\n----\n\n".join(output)


@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a URL for deeper reading."""
    url = (url or "").strip()
    parsed = urlparse(url)

    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return f"Invalid URL: {url}"

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 Chrome/131.0 Safari/537.36"
                )
            },
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "svg"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        text = " ".join(text.split())

        if not text:
            return f"No readable text was extracted from: {url}"

        return f"Source URL: {url}\n\n{text[:6000]}"

    except requests.RequestException as exc:
        return f"Could not scrape URL: {exc}"
    except Exception as exc:
        return f"Could not scrape URL: {type(exc).__name__}: {exc}"
