# Multi-Agent Research System

A Streamlit-based AI research assistant that turns a natural-language
topic into a structured research report. It uses a sequential,
multi-stage workflow for web search, source extraction, report
generation, and critique.

## Overview

The system combines web search, webpage extraction, LLM-based report
generation, and an AI critique step to help users explore a topic and
produce an organized research summary.

## Features

-   **Web research:** Searches the web with Tavily and returns up to
    five results.
-   **Source extraction:** Selects a relevant URL and extracts page text
    using Requests and BeautifulSoup.
-   **AI-generated reports:** Produces a Markdown report with an
    introduction, key findings, conclusion, and sources.
-   **Report critique:** Generates a score, strengths, improvement
    areas, and a brief verdict.
-   **Interactive UI:** Displays pipeline outputs and critique in
    Streamlit.
-   **Markdown export:** Download the generated report for later use.
-   **CLI pipeline:** Run the research workflow from the command line.


## How It Works

``` text
Research Topic
     ↓
Search Agent (Tavily)
     ↓
Reader Agent (selects and scrapes a URL)
     ↓
Writer Chain (generates a structured report)
     ↓
Critic Chain (reviews the draft)
     ↓
Report + Feedback
```

1.  **Search:** Uses Tavily to find relevant web results.
2.  **Read:** Selects a URL from the search output and extracts page
    text.
3.  **Write:** Generates a report with an introduction, key findings,
    conclusion, and sources.
4.  **Critique:** Returns a score, strengths, areas to improve, and a
    short verdict.
5.  **Export:** Displays the report in Streamlit and lets users download
    it as Markdown.

## Tech Stack

-   **Python**
-   **LangChain** --- agent and chain orchestration
-   **OpenAI GPT-4o-mini** --- language model
-   **Tavily** --- web search
-   **Requests + BeautifulSoup** --- webpage retrieval and text
    extraction
-   **Streamlit** --- interactive user interface

## Project Structure

``` text
.
├── agents.py          # LLM setup, search/reader agents, writer and critic chains
├── tools.py           # Tavily search and webpage scraping tools
├── pipeline.py        # Sequential pipeline and command-line entry point
├── app.py             # Streamlit application
├── requirements.txt   # Python dependencies

```

## Getting Started

### 1. Clone the repository

``` bash
git clone https://github.com/AkarshVyas/Multi-agent-research-system.git
cd Multi-agent-research-system
```

### 2. Create and activate a virtual environment

``` bash
python -m venv .venv
```

**Windows**

``` bash
.venv\Scripts\activate
```

**macOS / Linux**

``` bash
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the project root and add your API keys:

``` env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Keep `.env` out of version control. Never commit API keys.

### 5. Run the app

``` bash
streamlit run app.py
```
Enter a topic and run the research pipeline. Review the search and
extraction outputs, generated report, and critique; then download the
report as Markdown.

To run the command-line pipeline, use:

``` bash
python pipeline.py
```

## Current Scope

-   Sequential workflow: search → read → write → critique
-   Up to five search results returned by the search tool
-   One selected webpage is deeply scraped per run
-   Scraped text is limited to 3,000 characters
-   Final report can be downloaded as a Markdown file
-   Critic feedback is displayed but does not automatically trigger a
    rewrite

## Limitations and Future Improvements

This is a **research prototype**, not a production-ready research
platform. Current improvement areas include:

-   Retrieve and compare multiple independent sources
-   Preserve source metadata and connect claims to evidence
-   Verify citations and factual claims
-   Add a critic-driven revision loop
-   Validate URLs and protect against SSRF
-   Add structured logging, retries, rate limits, and cost controls
-   Persist research history and add automated tests
-   Consolidate orchestration so the UI and pipeline share one
    implementation

## Security Note

The application fetches webpages selected during the research process.
Before deploying it publicly, add strict URL and IP validation, block
localhost/private/link-local and cloud-metadata addresses, limit
redirects and response sizes, and review authentication and
rate-limiting requirements. Store API keys in environment variables or a
secrets manager.

`LICENSE` file before presenting the repository as open source.

