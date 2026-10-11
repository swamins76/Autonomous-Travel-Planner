from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from src.agent_core.tools import travel_tools

def run_travel_agent(user_query: str) -> str:
    model = ChatOpenAI(model="gpt-4o", temperature=0.2)
    
        # Build a more authoritative system instruction block
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are an expert Autonomous Travel & Camping Planner Agent.\n\n"
            "CRITICAL INSTRUCTIONS:\n"
            "1. You must ALWAYS use your tools to research the destination before answering. "
            "Call 'fetch_weather_forecast' and 'search_park_amenities' immediately.\n"
            "2. Never answer with a question or ask the user for more preferences. "
            "Take the input provided and generate a complete, detailed day-by-day itinerary right away.\n"
            "3. If the user mentions gear or food notes, explicitly integrate them into the schedule.\n"
            "4. Organize your output clearly using Markdown headers (e.g., # Day 1, ## Weather Outlook, ## Packing List)."
        )),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    
    agent = create_tool_calling_agent(model, travel_tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=travel_tools, verbose=True)
    
    result = agent_executor.invoke({"input": user_query})
    return result["output"]