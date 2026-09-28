# ResearchMind - Repaired Multi-Agent Research System

This version uses **Mistral instead of OpenAI** and is designed for the LangChain 1.x agent API.

## Architecture

1. Search Agent -> Tavily web search
2. Reader Agent -> selects and scrapes a useful source
3. Writer Chain -> creates the research report
4. Critic Chain -> scores and reviews the report
5. Streamlit -> web UI

## Setup on Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create a `.env` file by copying `.env.example`, then add your API keys:

```env
MISTRAL_API_KEY=your_key
TAVILY_API_KEY=your_key
MISTRAL_MODEL=mistral-small-latest
```

## Test Mistral first

```powershell
python test_mistral.py
```

You should see a model name and a one-sentence response.

## Run from terminal

```powershell
python pipeline.py
```

## Run Streamlit

```powershell
streamlit run app.py
```

## Important

OpenAI packages are intentionally removed from this project. If Mistral reports that the configured model is unavailable for your account, change `MISTRAL_MODEL` in `.env` to a currently available Mistral model shown by your Mistral account.
