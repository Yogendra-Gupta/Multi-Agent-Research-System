import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url

load_dotenv()

# -----------------------------------------------------------------------------
# LLM configuration
# OpenAI is intentionally not used. Mistral is the primary provider.
# You can change GROQ_MODEL in .env without changing the code.
# -----------------------------------------------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is missing. Add it to your .env file. "
        "Example: GROQ_API_KEY=GROQ_API_KEY"
    )

llm = ChatGroq(
    model=GROQ_MODEL,
    temperature=0,
    api_key=GROQ_API_KEY,
)


# -----------------------------------------------------------------------------
# Agents
# -----------------------------------------------------------------------------
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt=(
            "You are a web research agent. Search the web using the provided tool. "
            "Return useful, recent and reliable sources with their titles, URLs and "
            "key facts. Do not invent URLs or facts."
        ),
    )


def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt=(
            "You are a research reading agent. From the supplied search results, "
            "select the most relevant URL and use the scrape_url tool to extract "
            "deeper information. Return the URL used and the extracted facts. "
            "Do not invent content."
        ),
    )


# -----------------------------------------------------------------------------
# Writer chain
# -----------------------------------------------------------------------------
writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research writer. Write clear, structured, factual and "
        "professional reports. Distinguish source-backed facts from uncertainty.",
    ),
    (
        "human",
        """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
# Introduction
# Key Findings
Provide at least 3 well-explained findings.
# Conclusion
# Sources
List every URL that appears in the research gathered.

Rules:
- Do not invent sources, URLs, statistics or quotations.
- Prefer information supported by the supplied research.
- If the supplied research is insufficient, clearly say so.
- Keep the report readable and professional.""",
    ),
])

writer_chain = writer_prompt | llm | StrOutputParser()


# -----------------------------------------------------------------------------
# Critic chain
# -----------------------------------------------------------------------------
critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a sharp and constructive research critic. Evaluate factual support, "
        "clarity, completeness and source quality. Be honest and specific.",
    ),
    (
        "human",
        """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
...""",
    ),
])

critic_chain = critic_prompt | llm | StrOutputParser()
