from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.config import settings
from src.agent_core.graph import run_travel_agent

# 1. Initialize application and validate system keys
settings.validate_keys()
app = FastAPI(title="Autonomous Travel & Camping Planner API", version="1.0.0")

# 2. Configure CORS middleware so Streamlit (port 8501) can safely communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development ease
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Define the data structure for incoming browser requests
class TripRequest(BaseModel):
    destination: str
    duration_days: int = 3
    additional_notes: str = ""

@app.get("/")
def read_root():
    return {"status": "active", "message": "Travel Planner Backend Engine is running."}

@app.post("/api/plan-trip")
def plan_trip(request: TripRequest):
    try:
        # Construct a natural language query for the agent execution layer
        constructed_query = (
            f"Build a comprehensive {request.duration_days}-day itinerary for {request.destination}. "
            f"Additional user requests: {request.additional_notes}"
        )
        
        # Dispatch to the LangChain v1.x runtime core
        agent_response = run_travel_agent(constructed_query)
        return {"success": True, "itinerary": agent_response}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
