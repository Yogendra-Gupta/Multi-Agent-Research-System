from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain


def _last_message_content(result: dict) -> str:
    """Safely extract the last AI/tool message content from a LangChain agent result."""
    messages = result.get("messages", [])
    if not messages:
        return "No response was returned by the agent."

    content = messages[-1].content
    if isinstance(content, str):
        return content

    return str(content)


def run_research_pipeline(topic: str) -> dict:
    topic = (topic or "").strip()
    if not topic:
        raise ValueError("Research topic cannot be empty.")

    state = {}

    print("\n" + "=" * 60)
    print("STEP 1 - Search Agent")
    print("=" * 60)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [
            (
                "user",
                f"Find recent, reliable and detailed information about: {topic}. "
                "Use the web search tool and return the best sources with URLs.",
            )
        ]
    })
    state["search_results"] = _last_message_content(search_result)
    print(state["search_results"])

    print("\n" + "=" * 60)
    print("STEP 2 - Reader Agent")
    print("=" * 60)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"For the topic '{topic}', choose the most relevant URL from these "
                "search results and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:6000]}",
            )
        ]
    })
    state["scraped_content"] = _last_message_content(reader_result)
    print(state["scraped_content"])

    print("\n" + "=" * 60)
    print("STEP 3 - Writer Chain")
    print("=" * 60)

    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined,
    })
    print(state["report"])

    print("\n" + "=" * 60)
    print("STEP 4 - Critic Chain")
    print("=" * 60)

    state["feedback"] = critic_chain.invoke({"report": state["report"]})
    print(state["feedback"])

    return state


if __name__ == "__main__":
    topic = input("\nEnter a research topic: ").strip()
    try:
        run_research_pipeline(topic)
    except Exception as exc:
        print(f"\nPipeline failed: {type(exc).__name__}: {exc}")
        raise
